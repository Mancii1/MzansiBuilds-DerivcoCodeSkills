import api from './client';

export const toggleLike = (projectId) => api.post(`/projects/${projectId}/like`);
export const getLikes = (projectId) => api.get(`/projects/${projectId}/likes`);