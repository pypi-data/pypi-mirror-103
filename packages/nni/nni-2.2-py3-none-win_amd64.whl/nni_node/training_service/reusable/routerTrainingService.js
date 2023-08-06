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
const component = require("../../common/component");
const log_1 = require("../../common/log");
const errors_1 = require("../../common/errors");
const utils_1 = require("../../common/utils");
const paiTrainingService_1 = require("../pai/paiTrainingService");
const remoteMachineTrainingService_1 = require("../remote_machine/remoteMachineTrainingService");
const trialDispatcher_1 = require("./trialDispatcher");
let RouterTrainingService = class RouterTrainingService {
    constructor(config) {
        this.log = log_1.getLogger();
        const platform = Array.isArray(config.trainingService) ? 'hybrid' : config.trainingService.platform;
        if (platform === 'remote' && !config.trainingService.reuseMode) {
            this.internalTrainingService = new remoteMachineTrainingService_1.RemoteMachineTrainingService(config);
        }
        else if (platform === 'openpai' && !config.trainingService.reuseMode) {
            this.internalTrainingService = new paiTrainingService_1.PAITrainingService(config);
        }
        else {
            this.internalTrainingService = new trialDispatcher_1.TrialDispatcher(config);
        }
    }
    async listTrialJobs() {
        if (this.internalTrainingService === undefined) {
            throw new Error("TrainingService is not assigned!");
        }
        return await this.internalTrainingService.listTrialJobs();
    }
    async getTrialJob(trialJobId) {
        if (this.internalTrainingService === undefined) {
            throw new Error("TrainingService is not assigned!");
        }
        return await this.internalTrainingService.getTrialJob(trialJobId);
    }
    async getTrialLog(_trialJobId, _logType) {
        throw new errors_1.MethodNotImplementedError();
    }
    addTrialJobMetricListener(listener) {
        if (this.internalTrainingService === undefined) {
            throw new Error("TrainingService is not assigned!");
        }
        this.internalTrainingService.addTrialJobMetricListener(listener);
    }
    removeTrialJobMetricListener(listener) {
        if (this.internalTrainingService === undefined) {
            throw new Error("TrainingService is not assigned!");
        }
        this.internalTrainingService.removeTrialJobMetricListener(listener);
    }
    async submitTrialJob(form) {
        if (this.internalTrainingService === undefined) {
            throw new Error("TrainingService is not assigned!");
        }
        return await this.internalTrainingService.submitTrialJob(form);
    }
    async updateTrialJob(trialJobId, form) {
        if (this.internalTrainingService === undefined) {
            throw new Error("TrainingService is not assigned!");
        }
        return await this.internalTrainingService.updateTrialJob(trialJobId, form);
    }
    async cancelTrialJob(trialJobId, isEarlyStopped) {
        if (this.internalTrainingService === undefined) {
            throw new Error("TrainingService is not assigned!");
        }
        await this.internalTrainingService.cancelTrialJob(trialJobId, isEarlyStopped);
    }
    async setClusterMetadata(_key, _value) { return; }
    async getClusterMetadata(_key) { return ''; }
    async cleanUp() {
        if (this.internalTrainingService === undefined) {
            throw new Error("TrainingService is not assigned!");
        }
        await this.internalTrainingService.cleanUp();
    }
    async run() {
        while (this.internalTrainingService === undefined) {
            await utils_1.delay(100);
        }
        return await this.internalTrainingService.run();
    }
    async getTrialOutputLocalPath(trialJobId) {
        if (this.internalTrainingService === undefined) {
            throw new Error("TrainingService is not assigned!");
        }
        return this.internalTrainingService.getTrialOutputLocalPath(trialJobId);
    }
    async fetchTrialOutput(trialJobId, subpath) {
        if (this.internalTrainingService === undefined) {
            throw new Error("TrainingService is not assigned!");
        }
        return this.internalTrainingService.fetchTrialOutput(trialJobId, subpath);
    }
};
RouterTrainingService = __decorate([
    component.Singleton,
    __metadata("design:paramtypes", [Object])
], RouterTrainingService);
exports.RouterTrainingService = RouterTrainingService;
