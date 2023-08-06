'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const kubernetesConfig_1 = require("../kubernetesConfig");
class FrameworkAttemptCompletionPolicy {
    constructor(minFailedTaskCount, minSucceededTaskCount) {
        this.minFailedTaskCount = minFailedTaskCount;
        this.minSucceededTaskCount = minSucceededTaskCount;
    }
}
exports.FrameworkAttemptCompletionPolicy = FrameworkAttemptCompletionPolicy;
class FrameworkControllerTrialConfigTemplate extends kubernetesConfig_1.KubernetesTrialConfigTemplate {
    constructor(taskNum, command, gpuNum, cpuNum, memoryMB, image, frameworkAttemptCompletionPolicy, privateRegistryFilePath) {
        super(command, gpuNum, cpuNum, memoryMB, image, privateRegistryFilePath);
        this.frameworkAttemptCompletionPolicy = frameworkAttemptCompletionPolicy;
        this.name = name;
        this.taskNum = taskNum;
    }
}
exports.FrameworkControllerTrialConfigTemplate = FrameworkControllerTrialConfigTemplate;
class FrameworkControllerTrialConfig extends kubernetesConfig_1.KubernetesTrialConfig {
    constructor(codeDir, taskRoles) {
        super(codeDir);
        this.taskRoles = taskRoles;
        this.codeDir = codeDir;
    }
}
exports.FrameworkControllerTrialConfig = FrameworkControllerTrialConfig;
class FrameworkControllerClusterConfig extends kubernetesConfig_1.KubernetesClusterConfig {
    constructor(apiVersion, serviceAccountName, configPath, namespace) {
        super(apiVersion, undefined, namespace);
        this.serviceAccountName = serviceAccountName;
    }
}
exports.FrameworkControllerClusterConfig = FrameworkControllerClusterConfig;
class FrameworkControllerClusterConfigPVC extends kubernetesConfig_1.KubernetesClusterConfigPVC {
    constructor(serviceAccountName, apiVersion, pvc, configPath, storage, namespace) {
        super(apiVersion, pvc, storage, namespace);
        this.serviceAccountName = serviceAccountName;
        this.configPath = configPath;
    }
    static getInstance(jsonObject) {
        const kubernetesClusterConfigObjectPVC = jsonObject;
        assert(kubernetesClusterConfigObjectPVC !== undefined);
        return new FrameworkControllerClusterConfigPVC(kubernetesClusterConfigObjectPVC.serviceAccountName, kubernetesClusterConfigObjectPVC.apiVersion, kubernetesClusterConfigObjectPVC.pvc, kubernetesClusterConfigObjectPVC.configPath, kubernetesClusterConfigObjectPVC.storage, kubernetesClusterConfigObjectPVC.namespace);
    }
}
exports.FrameworkControllerClusterConfigPVC = FrameworkControllerClusterConfigPVC;
class FrameworkControllerClusterConfigNFS extends kubernetesConfig_1.KubernetesClusterConfigNFS {
    constructor(serviceAccountName, apiVersion, nfs, storage, namespace, configPath) {
        super(apiVersion, nfs, storage, namespace);
        this.serviceAccountName = serviceAccountName;
        this.configPath = configPath;
    }
    static getInstance(jsonObject) {
        const kubernetesClusterConfigObjectNFS = jsonObject;
        assert(kubernetesClusterConfigObjectNFS !== undefined);
        return new FrameworkControllerClusterConfigNFS(kubernetesClusterConfigObjectNFS.serviceAccountName, kubernetesClusterConfigObjectNFS.apiVersion, kubernetesClusterConfigObjectNFS.nfs, kubernetesClusterConfigObjectNFS.storage, kubernetesClusterConfigObjectNFS.namespace);
    }
}
exports.FrameworkControllerClusterConfigNFS = FrameworkControllerClusterConfigNFS;
class FrameworkControllerClusterConfigAzure extends kubernetesConfig_1.KubernetesClusterConfigAzure {
    constructor(serviceAccountName, apiVersion, keyVault, azureStorage, storage, uploadRetryCount, namespace, configPath) {
        super(apiVersion, keyVault, azureStorage, storage, uploadRetryCount, namespace);
        this.serviceAccountName = serviceAccountName;
        this.configPath = configPath;
    }
    static getInstance(jsonObject) {
        const kubernetesClusterConfigObjectAzure = jsonObject;
        return new FrameworkControllerClusterConfigAzure(kubernetesClusterConfigObjectAzure.serviceAccountName, kubernetesClusterConfigObjectAzure.apiVersion, kubernetesClusterConfigObjectAzure.keyVault, kubernetesClusterConfigObjectAzure.azureStorage, kubernetesClusterConfigObjectAzure.storage, kubernetesClusterConfigObjectAzure.uploadRetryCount, kubernetesClusterConfigObjectAzure.namespace);
    }
}
exports.FrameworkControllerClusterConfigAzure = FrameworkControllerClusterConfigAzure;
class FrameworkControllerClusterConfigFactory {
    static generateFrameworkControllerClusterConfig(jsonObject) {
        const storageConfig = jsonObject;
        if (storageConfig === undefined) {
            throw new Error('Invalid json object as a StorageConfig instance');
        }
        if (storageConfig.storage !== undefined && storageConfig.storage === 'azureStorage') {
            return FrameworkControllerClusterConfigAzure.getInstance(jsonObject);
        }
        else if (storageConfig.storage === undefined || storageConfig.storage === 'nfs') {
            return FrameworkControllerClusterConfigNFS.getInstance(jsonObject);
        }
        else if (storageConfig.storage !== undefined && storageConfig.storage === 'pvc') {
            return FrameworkControllerClusterConfigPVC.getInstance(jsonObject);
        }
        throw new Error(`Invalid json object ${jsonObject}`);
    }
}
exports.FrameworkControllerClusterConfigFactory = FrameworkControllerClusterConfigFactory;
