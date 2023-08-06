'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const timeUnits = { d: 24 * 3600, h: 3600, m: 60, s: 1 };
function toSeconds(time) {
    for (const [unit, factor] of Object.entries(timeUnits)) {
        if (time.toLowerCase().endsWith(unit)) {
            const digits = time.slice(0, -1);
            return Number(digits) * factor;
        }
    }
    throw new Error(`Bad time string "${time}"`);
}
exports.toSeconds = toSeconds;
const sizeUnits = { tb: 1024 * 1024, gb: 1024 * 1024, mb: 1, kb: 1 / 1024 };
function toMegaBytes(size) {
    for (const [unit, factor] of Object.entries(sizeUnits)) {
        if (size.toLowerCase().endsWith(unit)) {
            const digits = size.slice(0, -2);
            return Math.floor(Number(digits) * factor);
        }
    }
    throw new Error(`Bad size string "${size}"`);
}
exports.toMegaBytes = toMegaBytes;
function toCudaVisibleDevices(gpuIndices) {
    return gpuIndices === undefined ? '' : gpuIndices.join(',');
}
exports.toCudaVisibleDevices = toCudaVisibleDevices;
function flattenConfig(config, platform) {
    const flattened = {};
    Object.assign(flattened, config);
    if (Array.isArray(config.trainingService)) {
        for (const trainingService of config.trainingService) {
            if (trainingService.platform === platform) {
                Object.assign(flattened, trainingService);
            }
        }
    }
    else {
        assert(config.trainingService.platform === platform);
        Object.assign(flattened, config.trainingService);
    }
    return flattened;
}
exports.flattenConfig = flattenConfig;
