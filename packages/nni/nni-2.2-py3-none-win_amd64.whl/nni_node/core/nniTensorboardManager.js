'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
const cp = require("child_process");
const path = require("path");
const component = require("../common/component");
const log_1 = require("../common/log");
const utils_1 = require("../common/utils");
const manager_1 = require("../common/manager");
class TensorboardTaskDetail {
    constructor(id, status, trialJobIdList, trialLogDirectoryList) {
        this.id = id;
        this.status = status;
        this.trialJobIdList = trialJobIdList;
        this.trialLogDirectoryList = trialLogDirectoryList;
    }
}
exports.TensorboardTaskDetail = TensorboardTaskDetail;
class NNITensorboardManager {
    constructor() {
        this.log = log_1.getLogger();
        this.tensorboardTaskMap = new Map();
        this.setTensorboardVersion();
        this.nniManager = component.get(manager_1.Manager);
    }
    async startTensorboardTask(tensorboardParams) {
        const trialJobIds = tensorboardParams.trials;
        const trialJobIdList = [];
        const trialLogDirectoryList = [];
        await Promise.all(trialJobIds.split(',').map(async (trialJobId) => {
            const trialTensorboardDataPath = path.join(await this.nniManager.getTrialOutputLocalPath(trialJobId), 'tensorboard');
            utils_1.mkDirPSync(trialTensorboardDataPath);
            trialJobIdList.push(trialJobId);
            trialLogDirectoryList.push(trialTensorboardDataPath);
        }));
        this.log.info(`tensorboard: ${trialJobIdList} ${trialLogDirectoryList}`);
        return await this.startTensorboardTaskProcess(trialJobIdList, trialLogDirectoryList);
    }
    async startTensorboardTaskProcess(trialJobIdList, trialLogDirectoryList) {
        const host = 'localhost';
        const port = await utils_1.getFreePort(host, 6006, 65535);
        const command = await this.getTensorboardStartCommand(trialJobIdList, trialLogDirectoryList, port);
        this.log.info(`tensorboard start command: ${command}`);
        const tensorboardTask = new TensorboardTaskDetail(utils_1.uniqueString(5), 'RUNNING', trialJobIdList, trialLogDirectoryList);
        this.tensorboardTaskMap.set(tensorboardTask.id, tensorboardTask);
        const tensorboardProc = utils_1.getTunerProc(command, 'ignore', process.cwd(), process.env, true, true);
        tensorboardProc.on('error', async (error) => {
            this.log.error(error);
            const alive = await utils_1.isAlive(tensorboardProc.pid);
            if (alive) {
                process.kill(-tensorboardProc.pid);
            }
            this.setTensorboardTaskStatus(tensorboardTask, 'ERROR');
        });
        tensorboardTask.pid = tensorboardProc.pid;
        tensorboardTask.port = `${port}`;
        this.log.info(`tensorboard task id: ${tensorboardTask.id}`);
        this.updateTensorboardTask(tensorboardTask.id);
        return tensorboardTask;
    }
    async getTensorboardStartCommand(trialJobIdList, trialLogDirectoryList, port) {
        if (this.tensorboardVersion === undefined) {
            this.setTensorboardVersion();
            if (this.tensorboardVersion === undefined) {
                throw new Error(`Tensorboard may not installed, if you want to use tensorboard, please check if tensorboard installed.`);
            }
        }
        if (trialJobIdList.length !== trialLogDirectoryList.length) {
            throw new Error('trial list length does not match');
        }
        if (trialJobIdList.length === 0) {
            throw new Error('trial list length is 0');
        }
        let logdirCmd = '--logdir';
        if (this.tensorboardVersion >= '2.0') {
            logdirCmd = '--bind_all --logdir_spec';
        }
        try {
            const logRealPaths = [];
            for (const idx in trialJobIdList) {
                const realPath = fs.realpathSync(trialLogDirectoryList[idx]);
                const trialJob = await this.nniManager.getTrialJob(trialJobIdList[idx]);
                logRealPaths.push(`${trialJob.sequenceId}-${trialJobIdList[idx]}:${realPath}`);
            }
            const command = `tensorboard ${logdirCmd}=${logRealPaths.join(',')} --port=${port}`;
            return command;
        }
        catch (error) {
            throw new Error(`${error.message}`);
        }
    }
    setTensorboardVersion() {
        let command = `python3 -c 'import tensorboard ; print(tensorboard.__version__)'`;
        if (process.platform === 'win32') {
            command = `python -c 'import tensorboard ; print(tensorboard.__version__)'`;
        }
        try {
            const tensorboardVersion = cp.execSync(command).toString();
            if (/\d+(.\d+)*/.test(tensorboardVersion)) {
                this.tensorboardVersion = tensorboardVersion;
            }
        }
        catch (error) {
            this.log.warning(`Tensorboard may not installed, if you want to use tensorboard, please check if tensorboard installed.`);
        }
    }
    async getTensorboardTask(tensorboardTaskId) {
        const tensorboardTask = this.tensorboardTaskMap.get(tensorboardTaskId);
        if (tensorboardTask === undefined) {
            throw new Error('Tensorboard task not found');
        }
        else {
            if (tensorboardTask.status !== 'STOPPED') {
                const alive = await utils_1.isAlive(tensorboardTask.pid);
                if (!alive) {
                    this.setTensorboardTaskStatus(tensorboardTask, 'ERROR');
                }
            }
            return tensorboardTask;
        }
    }
    async listTensorboardTasks() {
        const result = [];
        this.tensorboardTaskMap.forEach((value) => {
            result.push(value);
        });
        return result;
    }
    setTensorboardTaskStatus(tensorboardTask, newStatus) {
        if (tensorboardTask.status !== newStatus) {
            const oldStatus = tensorboardTask.status;
            tensorboardTask.status = newStatus;
            this.log.info(`tensorboardTask ${tensorboardTask.id} status update: ${oldStatus} to ${tensorboardTask.status}`);
        }
    }
    downloadDataFinished(tensorboardTask) {
        this.setTensorboardTaskStatus(tensorboardTask, 'RUNNING');
    }
    async updateTensorboardTask(tensorboardTaskId) {
        const tensorboardTask = await this.getTensorboardTask(tensorboardTaskId);
        if (['RUNNING', 'FAIL_DOWNLOAD_DATA'].includes(tensorboardTask.status)) {
            this.setTensorboardTaskStatus(tensorboardTask, 'DOWNLOADING_DATA');
            Promise.all(tensorboardTask.trialJobIdList.map((trialJobId) => {
                this.nniManager.fetchTrialOutput(trialJobId, 'tensorboard');
            })).then(() => {
                this.downloadDataFinished(tensorboardTask);
            }).catch((error) => {
                this.setTensorboardTaskStatus(tensorboardTask, 'FAIL_DOWNLOAD_DATA');
                this.log.error(`${error.message}`);
            });
            return tensorboardTask;
        }
        else {
            throw new Error('only tensorboard task with RUNNING or FAIL_DOWNLOAD_DATA can update data');
        }
    }
    async stopTensorboardTask(tensorboardTaskId) {
        const tensorboardTask = await this.getTensorboardTask(tensorboardTaskId);
        if (['RUNNING', 'FAIL_DOWNLOAD_DATA'].includes(tensorboardTask.status)) {
            this.killTensorboardTaskProc(tensorboardTask);
            return tensorboardTask;
        }
        else {
            throw new Error('Only RUNNING FAIL_DOWNLOAD_DATA task can be stopped');
        }
    }
    async killTensorboardTaskProc(tensorboardTask) {
        if (['ERROR', 'STOPPED'].includes(tensorboardTask.status)) {
            return;
        }
        const alive = await utils_1.isAlive(tensorboardTask.pid);
        if (!alive) {
            this.setTensorboardTaskStatus(tensorboardTask, 'ERROR');
        }
        else {
            this.setTensorboardTaskStatus(tensorboardTask, 'STOPPING');
            if (tensorboardTask.pid) {
                process.kill(-tensorboardTask.pid);
            }
            this.log.debug(`Tensorboard task ${tensorboardTask.id} stopped.`);
            this.setTensorboardTaskStatus(tensorboardTask, 'STOPPED');
            this.tensorboardTaskMap.delete(tensorboardTask.id);
        }
    }
    async stopAllTensorboardTask() {
        this.log.info('Forced stopping all tensorboard task.');
        for (const task of this.tensorboardTaskMap) {
            await this.killTensorboardTaskProc(task[1]);
        }
        this.log.info('All tensorboard task stopped.');
    }
    async stop() {
        await this.stopAllTensorboardTask();
        this.log.info('Tensorboard manager stopped.');
    }
}
exports.NNITensorboardManager = NNITensorboardManager;
