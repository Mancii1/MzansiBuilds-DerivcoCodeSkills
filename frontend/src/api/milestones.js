import api from './client';

export const getMilestones = (projectId) => api.get(`/projects/${projectId}/milestones`);
export const createMilestone = (projectId, data) => api.post(`/projects/${projectId}/milestones`, data);
export const updateMilestone = (milestoneId, data) => api.put(`/projects/milestones/${milestoneId}`, data);
export const deleteMilestone = (milestoneId) => api.delete(`/projects/milestones/${milestoneId}`);
export const toggleMilestone = (milestoneId) => api.patch(`/projects/milestones/${milestoneId}/toggle`);
export const getProgress = (projectId) => api.get(`/projects/${projectId}/progress`);