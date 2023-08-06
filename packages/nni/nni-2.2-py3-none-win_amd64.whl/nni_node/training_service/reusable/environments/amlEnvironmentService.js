'use strict';
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
const path = require("path");
const component = require("../../../common/component");
const experimentStartupInfo_1 = require("../../../common/experimentStartupInfo");
const log_1 = require("../../../common/log");
const utils_1 = require("../../../common/utils");
const experimentConfig_1 = require("../../../common/experimentConfig");
const util_1 = require("../../common/util");
const amlClient_1 = require("../aml/amlClient");
const amlConfig_1 = require("../aml/amlConfig");
const environment_1 = require("../environment");
const amlCommandChannel_1 = require("../channels/amlCommandChannel");
const sharedStorage_1 = require("../sharedStorage");
let AMLEnvironmentService = class AMLEnvironmentService extends environment_1.EnvironmentService {
    constructor(config) {
        super();
        this.log = log_1.getLogger();
        this.experimentId = experimentStartupInfo_1.getExperimentId();
        this.experimentRootDir = utils_1.getExperimentRootDir();
        this.config = experimentConfig_1.flattenConfig(config, 'aml');
        util_1.validateCodeDir(this.config.trialCodeDirectory);
    }
    get hasStorageService() {
        return false;
    }
    initCommandChannel(eventEmitter) {
        this.commandChannel = new amlCommandChannel_1.AMLCommandChannel(eventEmitter);
    }
    createEnvironmentInformation(envId, envName) {
        return new amlConfig_1.AMLEnvironmentInformation(envId, envName);
    }
    get getName() {
        return 'aml';
    }
    async refreshEnvironmentsStatus(environments) {
        environments.forEach(async (environment) => {
            const amlClient = environment.amlClient;
            if (!amlClient) {
                return Promise.reject('AML client not initialized!');
            }
            const newStatus = await amlClient.updateStatus(environment.status);
            switch (newStatus.toUpperCase()) {
                case 'WAITING':
                case 'QUEUED':
                    environment.setStatus('WAITING');
                    break;
                case 'RUNNING':
                    environment.setStatus('RUNNING');
                    break;
                case 'COMPLETED':
                case 'SUCCEEDED':
                    environment.setStatus('SUCCEEDED');
                    break;
                case 'FAILED':
                    environment.setStatus('FAILED');
                    return Promise.reject(`AML: job ${environment.envId} is failed!`);
                case 'STOPPED':
                case 'STOPPING':
                    environment.setStatus('USER_CANCELED');
                    break;
                default:
                    environment.setStatus('UNKNOWN');
            }
        });
    }
    async startEnvironment(environment) {
        const amlEnvironment = environment;
        const environmentLocalTempFolder = path.join(this.experimentRootDir, "environment-temp");
        if (!fs.existsSync(environmentLocalTempFolder)) {
            await fs.promises.mkdir(environmentLocalTempFolder, { recursive: true });
        }
        if (amlEnvironment.useSharedStorage) {
            const environmentRoot = component.get(sharedStorage_1.SharedStorageService).remoteWorkingRoot;
            const remoteMountCommand = component.get(sharedStorage_1.SharedStorageService).remoteMountCommand;
            amlEnvironment.command = `${remoteMountCommand} && cd ${environmentRoot} && ${amlEnvironment.command}`.replace(/"/g, `\\"`);
        }
        else {
            amlEnvironment.command = `mv envs outputs/envs && cd outputs && ${amlEnvironment.command}`;
        }
        amlEnvironment.command = `import os\nos.system('${amlEnvironment.command}')`;
        amlEnvironment.useActiveGpu = !!this.config.deprecated.useActiveGpu;
        amlEnvironment.maxTrialNumberPerGpu = this.config.maxTrialNumberPerGpu;
        await fs.promises.writeFile(path.join(environmentLocalTempFolder, 'nni_script.py'), amlEnvironment.command, { encoding: 'utf8' });
        const amlClient = new amlClient_1.AMLClient(this.config.subscriptionId, this.config.resourceGroup, this.config.workspaceName, this.experimentId, this.config.computeTarget, this.config.dockerImage, 'nni_script.py', environmentLocalTempFolder);
        amlEnvironment.id = await amlClient.submit();
        this.log.debug('aml: before getTrackingUrl');
        amlEnvironment.trackingUrl = await amlClient.getTrackingUrl();
        this.log.debug('aml: after getTrackingUrl');
        amlEnvironment.amlClient = amlClient;
    }
    async stopEnvironment(environment) {
        const amlEnvironment = environment;
        const amlClient = amlEnvironment.amlClient;
        if (!amlClient) {
            throw new Error('AML client not initialized!');
        }
        amlClient.stop();
    }
};
AMLEnvironmentService = __decorate([
    component.Singleton,
    __metadata("design:paramtypes", [Object])
], AMLEnvironmentService);
exports.AMLEnvironmentService = AMLEnvironmentService;
