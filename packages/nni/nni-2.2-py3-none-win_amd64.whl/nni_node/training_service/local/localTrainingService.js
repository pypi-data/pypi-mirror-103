'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const events_1 = require("events");
const fs = require("fs");
const path = require("path");
const ts = require("tail-stream");
const tkill = require("tree-kill");
const errors_1 = require("../../common/errors");
const experimentStartupInfo_1 = require("../../common/experimentStartupInfo");
const log_1 = require("../../common/log");
const utils_1 = require("../../common/utils");
const experimentConfig_1 = require("../../common/experimentConfig");
const util_1 = require("../common/util");
const gpuScheduler_1 = require("./gpuScheduler");
function decodeCommand(data) {
    if (data.length < 8) {
        return [false, '', '', data];
    }
    const commandType = data.slice(0, 2).toString();
    const contentLength = parseInt(data.slice(2, 8).toString(), 10);
    if (data.length < contentLength + 8) {
        return [false, '', '', data];
    }
    const content = data.slice(8, contentLength + 8).toString();
    const remain = data.slice(contentLength + 8);
    return [true, commandType, content, remain];
}
class LocalTrialJobDetail {
    constructor(id, status, submitTime, workingDirectory, form) {
        this.id = id;
        this.status = status;
        this.submitTime = submitTime;
        this.workingDirectory = workingDirectory;
        this.form = form;
        this.url = `file://localhost:${workingDirectory}`;
        this.gpuIndices = [];
    }
}
class LocalTrainingService {
    constructor(config) {
        this.config = experimentConfig_1.flattenConfig(config, 'local');
        this.eventEmitter = new events_1.EventEmitter();
        this.jobMap = new Map();
        this.jobQueue = [];
        this.stopping = false;
        this.log = log_1.getLogger();
        this.experimentId = experimentStartupInfo_1.getExperimentId();
        this.jobStreamMap = new Map();
        this.log.info('Construct local machine training service.');
        this.occupiedGpuIndexNumMap = new Map();
        if (this.config.trialGpuNumber !== undefined && this.config.trialGpuNumber > 0) {
            this.gpuScheduler = new gpuScheduler_1.GPUScheduler();
        }
        if (this.config.gpuIndices === []) {
            throw new Error('gpuIndices cannot be empty when specified.');
        }
        this.rootDir = utils_1.getExperimentRootDir();
        if (!fs.existsSync(this.rootDir)) {
            throw new Error('root dir not created');
        }
        this.initialized = true;
    }
    async run() {
        this.log.info('Run local machine training service.');
        const longRunningTasks = [this.runJobLoop()];
        if (this.gpuScheduler !== undefined) {
            longRunningTasks.push(this.gpuScheduler.run());
        }
        await Promise.all(longRunningTasks);
        this.log.info('Local machine training service exit.');
    }
    async listTrialJobs() {
        const jobs = [];
        for (const key of this.jobMap.keys()) {
            const trialJob = await this.getTrialJob(key);
            jobs.push(trialJob);
        }
        return jobs;
    }
    async getTrialJob(trialJobId) {
        const trialJob = this.jobMap.get(trialJobId);
        if (trialJob === undefined) {
            throw new errors_1.NNIError(errors_1.NNIErrorNames.NOT_FOUND, 'Trial job not found');
        }
        if (trialJob.status === 'RUNNING') {
            const alive = await utils_1.isAlive(trialJob.pid);
            if (!alive) {
                trialJob.endTime = Date.now();
                this.setTrialJobStatus(trialJob, 'FAILED');
                try {
                    const state = await fs.promises.readFile(path.join(trialJob.workingDirectory, '.nni', 'state'), 'utf8');
                    const match = state.trim()
                        .match(/^(\d+)\s+(\d+)/);
                    if (match !== null) {
                        const { 1: code, 2: timestamp } = match;
                        if (parseInt(code, 10) === 0) {
                            this.setTrialJobStatus(trialJob, 'SUCCEEDED');
                        }
                        trialJob.endTime = parseInt(timestamp, 10);
                    }
                }
                catch (error) {
                }
                this.log.debug(`trialJob status update: ${trialJobId}, ${trialJob.status}`);
            }
        }
        return trialJob;
    }
    async getTrialLog(trialJobId, logType) {
        let logPath;
        if (logType === 'TRIAL_LOG') {
            logPath = path.join(this.rootDir, 'trials', trialJobId, 'trial.log');
        }
        else if (logType === 'TRIAL_ERROR') {
            logPath = path.join(this.rootDir, 'trials', trialJobId, 'stderr');
        }
        else {
            throw new Error('unexpected log type');
        }
        return fs.promises.readFile(logPath, 'utf8');
    }
    addTrialJobMetricListener(listener) {
        this.eventEmitter.on('metric', listener);
    }
    removeTrialJobMetricListener(listener) {
        this.eventEmitter.off('metric', listener);
    }
    submitTrialJob(form) {
        const trialJobId = utils_1.uniqueString(5);
        const trialJobDetail = new LocalTrialJobDetail(trialJobId, 'WAITING', Date.now(), path.join(this.rootDir, 'trials', trialJobId), form);
        this.jobQueue.push(trialJobId);
        this.jobMap.set(trialJobId, trialJobDetail);
        this.log.debug(`submitTrialJob: return: ${JSON.stringify(trialJobDetail)} `);
        return Promise.resolve(trialJobDetail);
    }
    async updateTrialJob(trialJobId, form) {
        const trialJobDetail = this.jobMap.get(trialJobId);
        if (trialJobDetail === undefined) {
            throw new Error(`updateTrialJob failed: ${trialJobId} not found`);
        }
        await this.writeParameterFile(trialJobDetail.workingDirectory, form.hyperParameters);
        return trialJobDetail;
    }
    async cancelTrialJob(trialJobId, isEarlyStopped = false) {
        const trialJob = this.jobMap.get(trialJobId);
        if (trialJob === undefined) {
            throw new errors_1.NNIError(errors_1.NNIErrorNames.NOT_FOUND, 'Trial job not found');
        }
        if (trialJob.pid === undefined) {
            this.setTrialJobStatus(trialJob, 'USER_CANCELED');
            return Promise.resolve();
        }
        tkill(trialJob.pid, 'SIGTERM');
        const startTime = Date.now();
        while (await utils_1.isAlive(trialJob.pid)) {
            if (Date.now() - startTime > 4999) {
                tkill(trialJob.pid, 'SIGKILL', (err) => {
                    if (err) {
                        this.log.error(`kill trial job error: ${err}`);
                    }
                });
                break;
            }
            await utils_1.delay(500);
        }
        this.setTrialJobStatus(trialJob, utils_1.getJobCancelStatus(isEarlyStopped));
        return Promise.resolve();
    }
    async setClusterMetadata(_key, _value) { return; }
    async getClusterMetadata(_key) { return ''; }
    async cleanUp() {
        this.log.info('Stopping local machine training service...');
        this.stopping = true;
        for (const stream of this.jobStreamMap.values()) {
            stream.end(0);
            stream.emit('end');
        }
        if (this.gpuScheduler !== undefined) {
            await this.gpuScheduler.stop();
        }
        return Promise.resolve();
    }
    onTrialJobStatusChanged(trialJob, oldStatus) {
        if (['SUCCEEDED', 'FAILED', 'USER_CANCELED', 'SYS_CANCELED', 'EARLY_STOPPED'].includes(trialJob.status)) {
            if (this.jobStreamMap.has(trialJob.id)) {
                const stream = this.jobStreamMap.get(trialJob.id);
                if (stream === undefined) {
                    throw new Error(`Could not find stream in trial ${trialJob.id}`);
                }
                setTimeout(() => {
                    stream.end(0);
                    stream.emit('end');
                    this.jobStreamMap.delete(trialJob.id);
                }, 5000);
            }
        }
        if (trialJob.gpuIndices !== undefined && trialJob.gpuIndices.length > 0 && this.gpuScheduler !== undefined) {
            if (oldStatus === 'RUNNING' && trialJob.status !== 'RUNNING') {
                for (const index of trialJob.gpuIndices) {
                    const num = this.occupiedGpuIndexNumMap.get(index);
                    if (num === undefined) {
                        throw new Error(`gpu resource schedule error`);
                    }
                    else if (num === 1) {
                        this.occupiedGpuIndexNumMap.delete(index);
                    }
                    else {
                        this.occupiedGpuIndexNumMap.set(index, num - 1);
                    }
                }
            }
        }
    }
    getEnvironmentVariables(trialJobDetail, resource, gpuNum) {
        const envVariables = [
            { key: 'NNI_PLATFORM', value: 'local' },
            { key: 'NNI_EXP_ID', value: this.experimentId },
            { key: 'NNI_SYS_DIR', value: trialJobDetail.workingDirectory },
            { key: 'NNI_TRIAL_JOB_ID', value: trialJobDetail.id },
            { key: 'NNI_OUTPUT_DIR', value: trialJobDetail.workingDirectory },
            { key: 'NNI_TRIAL_SEQ_ID', value: trialJobDetail.form.sequenceId.toString() },
            { key: 'NNI_CODE_DIR', value: this.config.trialCodeDirectory }
        ];
        if (gpuNum !== undefined) {
            envVariables.push({
                key: 'CUDA_VISIBLE_DEVICES',
                value: this.gpuScheduler === undefined ? '-1' : resource.gpuIndices.join(',')
            });
        }
        return envVariables;
    }
    setExtraProperties(trialJobDetail, resource) {
        trialJobDetail.gpuIndices = resource.gpuIndices;
    }
    tryGetAvailableResource() {
        const resource = { gpuIndices: [] };
        if (this.gpuScheduler === undefined) {
            return [true, resource];
        }
        let selectedGPUIndices = [];
        const availableGpuIndices = this.gpuScheduler.getAvailableGPUIndices(this.config.useActiveGpu, this.occupiedGpuIndexNumMap);
        for (const index of availableGpuIndices) {
            const num = this.occupiedGpuIndexNumMap.get(index);
            if (num === undefined || num < this.config.maxTrialNumberPerGpu) {
                selectedGPUIndices.push(index);
            }
        }
        if (this.config.gpuIndices !== undefined) {
            this.checkSpecifiedGpuIndices();
            selectedGPUIndices = selectedGPUIndices.filter((index) => this.config.gpuIndices.includes(index));
        }
        if (selectedGPUIndices.length < this.config.trialGpuNumber) {
            return [false, resource];
        }
        selectedGPUIndices.splice(this.config.trialGpuNumber);
        Object.assign(resource, { gpuIndices: selectedGPUIndices });
        return [true, resource];
    }
    checkSpecifiedGpuIndices() {
        const gpuCount = this.gpuScheduler.getSystemGpuCount();
        if (this.config.gpuIndices !== undefined && gpuCount !== undefined) {
            for (const index of this.config.gpuIndices) {
                if (index >= gpuCount) {
                    throw new Error(`Specified GPU index not found: ${index}`);
                }
            }
        }
    }
    occupyResource(resource) {
        if (this.gpuScheduler !== undefined) {
            for (const index of resource.gpuIndices) {
                const num = this.occupiedGpuIndexNumMap.get(index);
                if (num === undefined) {
                    this.occupiedGpuIndexNumMap.set(index, 1);
                }
                else {
                    this.occupiedGpuIndexNumMap.set(index, num + 1);
                }
            }
        }
    }
    async runJobLoop() {
        while (!this.stopping) {
            while (!this.stopping && this.jobQueue.length !== 0) {
                const trialJobId = this.jobQueue[0];
                const trialJobDetail = this.jobMap.get(trialJobId);
                if (trialJobDetail !== undefined && trialJobDetail.status === 'WAITING') {
                    const [success, resource] = this.tryGetAvailableResource();
                    if (!success) {
                        break;
                    }
                    this.occupyResource(resource);
                    await this.runTrialJob(trialJobId, resource);
                }
                this.jobQueue.shift();
            }
            await utils_1.delay(5000);
        }
    }
    setTrialJobStatus(trialJob, newStatus) {
        if (trialJob.status !== newStatus) {
            const oldStatus = trialJob.status;
            trialJob.status = newStatus;
            this.onTrialJobStatusChanged(trialJob, oldStatus);
        }
    }
    getScript(workingDirectory) {
        const script = [];
        if (process.platform === 'win32') {
            script.push(`cd $env:NNI_CODE_DIR`);
            script.push(`cmd.exe /c ${this.config.trialCommand} 2>&1 | Out-File "${path.join(workingDirectory, 'stderr')}" -encoding utf8`, `$NOW_DATE = [int64](([datetime]::UtcNow)-(get-date "1/1/1970")).TotalSeconds`, `$NOW_DATE = "$NOW_DATE" + (Get-Date -Format fff).ToString()`, `Write $LASTEXITCODE " " $NOW_DATE  | Out-File "${path.join(workingDirectory, '.nni', 'state')}" -NoNewline -encoding utf8`);
        }
        else {
            script.push(`cd $NNI_CODE_DIR`);
            script.push(`eval ${this.config.trialCommand} 2>"${path.join(workingDirectory, 'stderr')}"`);
            if (process.platform === 'darwin') {
                script.push(`echo $? \`date +%s999\` >'${path.join(workingDirectory, '.nni', 'state')}'`);
            }
            else {
                script.push(`echo $? \`date +%s%3N\` >'${path.join(workingDirectory, '.nni', 'state')}'`);
            }
        }
        return script;
    }
    async runTrialJob(trialJobId, resource) {
        const trialJobDetail = this.jobMap.get(trialJobId);
        const variables = this.getEnvironmentVariables(trialJobDetail, resource, this.config.trialGpuNumber);
        const runScriptContent = [];
        if (process.platform !== 'win32') {
            runScriptContent.push('#!/bin/bash');
        }
        else {
            runScriptContent.push(`$env:PATH="${process.env.path}"`);
        }
        for (const variable of variables) {
            runScriptContent.push(util_1.setEnvironmentVariable(variable));
        }
        const scripts = this.getScript(trialJobDetail.workingDirectory);
        scripts.forEach((script) => {
            runScriptContent.push(script);
        });
        await util_1.execMkdir(trialJobDetail.workingDirectory);
        await util_1.execMkdir(path.join(trialJobDetail.workingDirectory, '.nni'));
        await util_1.execNewFile(path.join(trialJobDetail.workingDirectory, '.nni', 'metrics'));
        const scriptName = util_1.getScriptName('run');
        await fs.promises.writeFile(path.join(trialJobDetail.workingDirectory, scriptName), runScriptContent.join(utils_1.getNewLine()), { encoding: 'utf8', mode: 0o777 });
        await this.writeParameterFile(trialJobDetail.workingDirectory, trialJobDetail.form.hyperParameters);
        const trialJobProcess = util_1.runScript(path.join(trialJobDetail.workingDirectory, scriptName));
        this.setTrialJobStatus(trialJobDetail, 'RUNNING');
        trialJobDetail.startTime = Date.now();
        trialJobDetail.pid = trialJobProcess.pid;
        this.setExtraProperties(trialJobDetail, resource);
        let buffer = Buffer.alloc(0);
        const stream = ts.createReadStream(path.join(trialJobDetail.workingDirectory, '.nni', 'metrics'));
        stream.on('data', (data) => {
            buffer = Buffer.concat([buffer, data]);
            while (buffer.length > 0) {
                const [success, , content, remain] = decodeCommand(buffer);
                if (!success) {
                    break;
                }
                this.eventEmitter.emit('metric', {
                    id: trialJobDetail.id,
                    data: content
                });
                this.log.debug(`Sending metrics, job id: ${trialJobDetail.id}, metrics: ${content}`);
                buffer = remain;
            }
        });
        this.jobStreamMap.set(trialJobDetail.id, stream);
    }
    async writeParameterFile(directory, hyperParameters) {
        const filepath = path.join(directory, utils_1.generateParamFileName(hyperParameters));
        await fs.promises.writeFile(filepath, hyperParameters.value, { encoding: 'utf8' });
    }
    async getTrialOutputLocalPath(trialJobId) {
        return Promise.resolve(path.join(this.rootDir, 'trials', trialJobId));
    }
    async fetchTrialOutput(trialJobId, subpath) {
        let trialLocalPath = await this.getTrialOutputLocalPath(trialJobId);
        if (subpath !== undefined) {
            trialLocalPath = path.join(trialLocalPath, subpath);
        }
        if (fs.existsSync(trialLocalPath)) {
            return Promise.resolve();
        }
        else {
            return Promise.reject(new Error('Trial local path not exist.'));
        }
    }
}
exports.LocalTrainingService = LocalTrainingService;
