'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const chai = require("chai");
const chaiAsPromised = require("chai-as-promised");
const fs = require("fs");
const path = require("path");
const tmp = require("tmp");
const utils_1 = require("../../common/utils");
const localTrainingService_1 = require("../local/localTrainingService");
const localCodeDir = tmp.dirSync().name.split('\\').join('\\\\');
const mockedTrialPath = './training_service/test/mockedTrial.py';
fs.copyFileSync(mockedTrialPath, localCodeDir + '/mockedTrial.py');
describe('Unit Test for LocalTrainingService', () => {
    const config = {
        trialCommand: 'sleep 1h && echo hello',
        trialCodeDirectory: `${localCodeDir}`,
        trialGpuNumber: 1,
        trainingService: {
            platform: 'local'
        }
    };
    const config2 = {
        trialCommand: 'python3 mockedTrial.py',
        trialCodeDirectory: `${localCodeDir}`,
        trialGpuNumber: 0,
        trainingService: {
            platform: 'local'
        }
    };
    before(() => {
        chai.should();
        chai.use(chaiAsPromised);
        utils_1.prepareUnitTest();
    });
    after(() => {
        utils_1.cleanupUnitTest();
    });
    it('List empty trial jobs', async () => {
        const localTrainingService = new localTrainingService_1.LocalTrainingService(config);
        localTrainingService.run();
        chai.expect(await localTrainingService.listTrialJobs()).to.be.empty;
        localTrainingService.cleanUp();
    });
    it('Submit job and Cancel job', async () => {
        const localTrainingService = new localTrainingService_1.LocalTrainingService(config);
        localTrainingService.run();
        const form = {
            sequenceId: 0,
            hyperParameters: {
                value: 'mock hyperparameters',
                index: 0
            }
        };
        const jobDetail = await localTrainingService.submitTrialJob(form);
        chai.expect(jobDetail.status).to.be.equals('WAITING');
        await localTrainingService.cancelTrialJob(jobDetail.id);
        chai.expect(jobDetail.status).to.be.equals('USER_CANCELED');
        localTrainingService.cleanUp();
    }).timeout(20000);
    it('Get trial log', async () => {
        const localTrainingService = new localTrainingService_1.LocalTrainingService(config);
        localTrainingService.run();
        const form = {
            sequenceId: 0,
            hyperParameters: {
                value: 'mock hyperparameters',
                index: 0
            }
        };
        const jobDetail = await localTrainingService.submitTrialJob(form);
        const rootDir = utils_1.getExperimentRootDir();
        fs.mkdirSync(path.join(rootDir, 'trials'));
        fs.mkdirSync(jobDetail.workingDirectory);
        fs.writeFileSync(path.join(jobDetail.workingDirectory, 'trial.log'), 'trial log');
        fs.writeFileSync(path.join(jobDetail.workingDirectory, 'stderr'), 'trial stderr');
        chai.expect(await localTrainingService.getTrialLog(jobDetail.id, 'TRIAL_LOG')).to.be.equals('trial log');
        chai.expect(await localTrainingService.getTrialLog(jobDetail.id, 'TRIAL_ERROR')).to.be.equals('trial stderr');
        fs.unlinkSync(path.join(jobDetail.workingDirectory, 'trial.log'));
        fs.unlinkSync(path.join(jobDetail.workingDirectory, 'stderr'));
        fs.rmdirSync(jobDetail.workingDirectory);
        fs.rmdirSync(path.join(rootDir, 'trials'));
        await localTrainingService.cancelTrialJob(jobDetail.id);
        localTrainingService.cleanUp();
    }).timeout(20000);
    it('Read metrics, Add listener, and remove listener', async () => {
        const localTrainingService = new localTrainingService_1.LocalTrainingService(config2);
        localTrainingService.run();
        const form = {
            sequenceId: 0,
            hyperParameters: {
                value: 'mock hyperparameters',
                index: 0
            }
        };
        const jobDetail = await localTrainingService.submitTrialJob(form);
        chai.expect(jobDetail.status).to.be.equals('WAITING');
        localTrainingService.listTrialJobs().then((jobList) => {
            chai.expect(jobList.length).to.be.equals(1);
        });
        const listener1 = function f1(metric) {
            chai.expect(metric.id).to.be.equals(jobDetail.id);
        };
        localTrainingService.addTrialJobMetricListener(listener1);
        await utils_1.delay(1000);
        await localTrainingService.cancelTrialJob(jobDetail.id);
        localTrainingService.removeTrialJobMetricListener(listener1);
        localTrainingService.cleanUp();
    }).timeout(20000);
});
