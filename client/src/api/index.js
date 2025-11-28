/**
 * 统一API客户端
 * 提供所有Factory的API调用接口
 */

import axios from 'axios';

// 创建axios实例
const api = axios.create({
    baseURL: 'http://localhost:8000/api',
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json'
    }
});

// 请求拦截器
api.interceptors.request.use(
    (config) => {
        // 可以在这里添加token等
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 响应拦截器
api.interceptors.response.use(
    (response) => response.data,
    (error) => {
        console.error('API Error:', error);
        return Promise.reject(error);
    }
);

// ========== ComputeFactory API ==========
export const computeApi = {
    getPools: () => api.get('/compute/pools'),
    getPoolByType: (poolType) => api.get(`/compute/pools/${poolType}`),
    allocateResource: (data) => api.post('/compute/allocate', data),
    releaseResource: (data) => api.post('/compute/release', data),
    getUsage: () => api.get('/compute/usage')
};

// ========== DataFactory API ==========
export const dataApi = {
    collectEvent: (data) => api.post('/data/events', data),
    getEvents: (params) => api.get('/data/events', { params }),
    getStatistics: () => api.get('/data/events/statistics'),
    addAnnotation: (data) => api.post('/data/label', data),
    getAnnotations: (eventId) => api.get(`/data/annotations/${eventId}`),
    createDataset: (data) => api.post('/data/datasets/create', data),
    getDataset: (datasetId) => api.get(`/data/datasets/${datasetId}`),
    listDatasets: () => api.get('/data/datasets'),
    finalizeDataset: (datasetId) => api.post(`/data/datasets/${datasetId}/finalize`)
};

// ========== EnvironmentFactory API ==========
export const environmentApi = {
    createScenario: (data) => api.post('/env/scenarios', data),
    listScenarios: () => api.get('/env/scenarios'),
    runEnvironment: (data) => api.post('/env/run', data),
    getTrace: (runId) => api.get(`/env/run/${runId}/trace`),
    replay: (runId) => api.get(`/env/run/${runId}/replay`)
};

// ========== TrainingFactory API ==========
export const trainingApi = {
    createJob: (data) => api.post('/training/jobs', data),
    listJobs: () => api.get('/training/jobs'),
    getJobStatus: (jobId) => api.get(`/training/jobs/${jobId}/status`),
    configureReward: (jobId, data) => api.post(`/training/jobs/${jobId}/reward-config`, data),
    promoteModel: (data) => api.post('/training/models/promote', data),
    listModels: () => api.get('/training/models')
};

// ========== EvaluationFactory API ==========
export const evaluationApi = {
    createTaskSet: (data) => api.post('/eval/taskset', data),
    listTaskSets: () => api.get('/eval/taskset'),
    runEvaluation: (data) => api.post('/eval/run', data),
    getResults: (evalId) => api.get(`/eval/results/${evalId}`),
    getDetailedResults: (evalId) => api.get(`/eval/results/${evalId}/details`),
    getBenchmarks: () => api.get('/eval/benchmarks')
};

// ========== RuntimeFactory API ==========
export const runtimeApi = {
    createAgent: (data) => api.post('/runtime', data),
    listAgents: () => api.get('/runtime'),
    createSession: (agentId, data) => api.post(`/runtime/${agentId}/sessions`, data),
    executeStep: (agentId, sessionId, data) => api.post(`/runtime/${agentId}/sessions/${sessionId}/step`, data),
    getHistory: (agentId, sessionId) => api.get(`/runtime/${agentId}/sessions/${sessionId}/history`),
    deployAgent: (agentId, data) => api.post(`/runtime/${agentId}/deploy`, data),
    listDeployments: (agentId) => api.get(`/runtime/${agentId}/deployments`),
    getAuditLogs: (agentId) => api.get(`/runtime/${agentId}/audit-logs`)
};

// ========== ObservabilityFactory API (新增) ==========
export const observabilityApi = {
    // Traces
    listTraces: () => api.get('/observability/traces'),
    getTrace: (traceId) => api.get(`/observability/traces/${traceId}`),

    // Metrics
    getMetrics: (params) => api.get('/observability/metrics', { params }),
    getAgentMetrics: (agentId) => api.get(`/observability/metrics/agent/${agentId}`),

    // Costs
    getCostReport: (params) => api.get('/observability/costs', { params }),
    getCostByAgent: () => api.get('/observability/costs/by-agent'),
    getCostTrend: (days = 7) => api.get(`/observability/costs/trend?days=${days}`)
};

export default api;
