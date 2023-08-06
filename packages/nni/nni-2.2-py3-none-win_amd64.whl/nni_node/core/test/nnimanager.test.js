'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
const os = require("os");
const chai_1 = require("chai");
const typescript_ioc_1 = require("typescript-ioc");
const component = require("../../common/component");
const datastore_1 = require("../../common/datastore");
const manager_1 = require("../../common/manager");
const experimentManager_1 = require("../../common/experimentManager");
const utils_1 = require("../../common/utils");
const nniExperimentsManager_1 = require("../nniExperimentsManager");
const nnimanager_1 = require("../nnimanager");
const sqlDatabase_1 = require("../sqlDatabase");
const mockedTrainingService_1 = require("./mockedTrainingService");
const mockedDatastore_1 = require("./mockedDatastore");
const tensorboardManager_1 = require("../../common/tensorboardManager");
const nniTensorboardManager_1 = require("../../core/nniTensorboardManager");
const path = require("path");
async function initContainer() {
    utils_1.prepareUnitTest();
    typescript_ioc_1.Container.bind(manager_1.Manager).to(nnimanager_1.NNIManager).scope(typescript_ioc_1.Scope.Singleton);
    typescript_ioc_1.Container.bind(datastore_1.Database).to(sqlDatabase_1.SqlDB).scope(typescript_ioc_1.Scope.Singleton);
    typescript_ioc_1.Container.bind(datastore_1.DataStore).to(mockedDatastore_1.MockedDataStore).scope(typescript_ioc_1.Scope.Singleton);
    typescript_ioc_1.Container.bind(experimentManager_1.ExperimentManager).to(nniExperimentsManager_1.NNIExperimentsManager).scope(typescript_ioc_1.Scope.Singleton);
    typescript_ioc_1.Container.bind(tensorboardManager_1.TensorboardManager).to(nniTensorboardManager_1.NNITensorboardManager).scope(typescript_ioc_1.Scope.Singleton);
    await component.get(datastore_1.DataStore).init();
}
describe('Unit test for nnimanager', function () {
    this.timeout(10000);
    let nniManager;
    let ClusterMetadataKey = 'mockedMetadataKey';
    let experimentParams = {
        experimentName: 'naive_experiment',
        trialConcurrency: 3,
        maxExperimentDuration: '5s',
        maxTrialNumber: 3,
        trainingService: {
            platform: 'local'
        },
        searchSpace: { 'lr': { '_type': 'choice', '_value': [0.01, 0.001] } },
        tuner: {
            name: 'TPE',
            classArgs: {
                optimize_mode: 'maximize'
            }
        },
        assessor: {
            name: 'Medianstop'
        },
        trialCommand: 'sleep 2',
        trialCodeDirectory: '',
        debug: true
    };
    let updateExperimentParams = {
        experimentName: 'another_experiment',
        trialConcurrency: 2,
        maxExperimentDuration: '6s',
        maxTrialNumber: 2,
        trainingService: {
            platform: 'local'
        },
        searchSpace: '{"lr": {"_type": "choice", "_value": [0.01,0.001]}}',
        tuner: {
            name: 'TPE',
            classArgs: {
                optimize_mode: 'maximize'
            }
        },
        assessor: {
            name: 'Medianstop'
        },
        trialCommand: 'sleep 2',
        trialCodeDirectory: '',
        debug: true
    };
    let experimentProfile = {
        params: updateExperimentParams,
        id: 'test',
        execDuration: 0,
        logDir: '',
        startTime: 0,
        nextSequenceId: 0,
        revision: 0
    };
    let mockedInfo = {
        "unittest": {
            "port": 8080,
            "startTime": 1605246730756,
            "endTime": "N/A",
            "status": "INITIALIZED",
            "platform": "local",
            "experimentName": "testExp",
            "tag": [], "pid": 11111,
            "webuiUrl": [],
            "logDir": null
        }
    };
    before(async () => {
        await initContainer();
        fs.writeFileSync('.experiment.test', JSON.stringify(mockedInfo));
        const experimentsManager = component.get(experimentManager_1.ExperimentManager);
        experimentsManager.setExperimentPath('.experiment.test');
        nniManager = component.get(manager_1.Manager);
        const expId = await nniManager.startExperiment(experimentParams);
        chai_1.assert.strictEqual(expId, 'unittest');
        const manager = nniManager;
        manager.trainingService.removeTrialJobMetricListener(manager.trialJobMetricListener);
        manager.trainingService.cleanUp();
        manager.trainingService = new mockedTrainingService_1.MockedTrainingService();
    });
    after(async () => {
        await setTimeout(() => { nniManager.stopExperiment(); }, 15000);
        utils_1.cleanupUnitTest();
    });
    it('test addCustomizedTrialJob', () => {
        return nniManager.addCustomizedTrialJob('"hyperParams"').then(() => {
        }).catch((error) => {
            chai_1.assert.fail(error);
        });
    });
    it('test listTrialJobs', () => {
        return nniManager.listTrialJobs().then(function (trialjobdetails) {
            chai_1.expect(trialjobdetails.length).to.be.equal(2);
        }).catch((error) => {
            chai_1.assert.fail(error);
        });
    });
    it('test getTrialJob valid', () => {
        return nniManager.getTrialJob('1234').then(function (trialJobDetail) {
            chai_1.expect(trialJobDetail.trialJobId).to.be.equal('1234');
        }).catch((error) => {
            chai_1.assert.fail(error);
        });
    });
    it('test getTrialJob with invalid id', () => {
        return nniManager.getTrialJob('4567').then((jobid) => {
            chai_1.assert.fail();
        }).catch((error) => {
            chai_1.assert.isTrue(true);
        });
    });
    it('test cancelTrialJobByUser', () => {
        return nniManager.cancelTrialJobByUser('1234').then(() => {
        }).catch((error) => {
            console.log(error);
            chai_1.assert.fail(error);
        });
    });
    it('test getExperimentProfile', () => {
        return nniManager.getExperimentProfile().then((experimentProfile) => {
            chai_1.expect(experimentProfile.id).to.be.equal('unittest');
            chai_1.expect(experimentProfile.logDir).to.be.equal(path.join(os.homedir(), 'nni-experiments', 'unittest'));
        }).catch((error) => {
            chai_1.assert.fail(error);
        });
    });
    it('test updateExperimentProfile TRIAL_CONCURRENCY', () => {
        return nniManager.updateExperimentProfile(experimentProfile, 'TRIAL_CONCURRENCY').then(() => {
            nniManager.getExperimentProfile().then((updateProfile) => {
                chai_1.expect(updateProfile.params.trialConcurrency).to.be.equal(2);
            });
        }).catch((error) => {
            chai_1.assert.fail(error);
        });
    });
    it('test updateExperimentProfile MAX_EXEC_DURATION', () => {
        return nniManager.updateExperimentProfile(experimentProfile, 'MAX_EXEC_DURATION').then(() => {
            nniManager.getExperimentProfile().then((updateProfile) => {
                chai_1.expect(updateProfile.params.maxExperimentDuration).to.be.equal('6s');
            });
        }).catch((error) => {
            chai_1.assert.fail(error);
        });
    });
    it('test updateExperimentProfile SEARCH_SPACE', () => {
        return nniManager.updateExperimentProfile(experimentProfile, 'SEARCH_SPACE').then(() => {
            nniManager.getExperimentProfile().then((updateProfile) => {
                chai_1.expect(updateProfile.params.searchSpace).to.be.equal('{"lr": {"_type": "choice", "_value": [0.01,0.001]}}');
            });
        }).catch((error) => {
            chai_1.assert.fail(error);
        });
    });
    it('test updateExperimentProfile MAX_TRIAL_NUM', () => {
        return nniManager.updateExperimentProfile(experimentProfile, 'MAX_TRIAL_NUM').then(() => {
            nniManager.getExperimentProfile().then((updateProfile) => {
                chai_1.expect(updateProfile.params.maxTrialNumber).to.be.equal(2);
            });
        }).catch((error) => {
            chai_1.assert.fail(error);
        });
    });
    it('test getStatus', () => {
        chai_1.assert.strictEqual(nniManager.getStatus().status, 'RUNNING');
    });
    it('test getMetricData with trialJobId', () => {
        return nniManager.getMetricData('4321', 'CUSTOM').then((metricData) => {
            chai_1.expect(metricData.length).to.be.equal(1);
            chai_1.expect(metricData[0].trialJobId).to.be.equal('4321');
            chai_1.expect(metricData[0].parameterId).to.be.equal('param1');
        }).catch((error) => {
            chai_1.assert.fail(error);
        });
    });
    it('test getMetricData with invalid trialJobId', () => {
        return nniManager.getMetricData('43210', 'CUSTOM').then((metricData) => {
            chai_1.assert.fail();
        }).catch((error) => {
        });
    });
    it('test getTrialJobStatistics', () => {
        return nniManager.getTrialJobStatistics().then(function (trialJobStatistics) {
            chai_1.expect(trialJobStatistics.length).to.be.equal(2);
            if (trialJobStatistics[0].trialJobStatus === 'WAITING') {
                chai_1.expect(trialJobStatistics[0].trialJobNumber).to.be.equal(2);
                chai_1.expect(trialJobStatistics[1].trialJobNumber).to.be.equal(1);
            }
            else {
                chai_1.expect(trialJobStatistics[1].trialJobNumber).to.be.equal(2);
                chai_1.expect(trialJobStatistics[0].trialJobNumber).to.be.equal(1);
            }
        }).catch((error) => {
            chai_1.assert.fail(error);
        });
    });
    it('test addCustomizedTrialJob reach maxTrialNumber', () => {
        return nniManager.addCustomizedTrialJob('"hyperParam"').then(() => {
            nniManager.getTrialJobStatistics().then(function (trialJobStatistics) {
                if (trialJobStatistics[0].trialJobStatus === 'WAITING')
                    chai_1.expect(trialJobStatistics[0].trialJobNumber).to.be.equal(2);
                else
                    chai_1.expect(trialJobStatistics[1].trialJobNumber).to.be.equal(2);
            });
        }).catch((error) => {
            chai_1.assert.fail(error);
        });
    });
    it('test resumeExperiment', async () => {
    });
});
