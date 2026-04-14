import api from './client';

export const getProjects = (params) => api.get('/projects/feed', { params });
export const getProject = (id) => api.get(`/projects/${id}`);
export const createProject = (data) => api.post('/projects', data);
export const updateProject = (id, data) => api.put(`/projects/${id}`, data);
export const deleteProject = (id) => api.delete(`/projects/${id}`);
export const getCompletedProjects = (params) => api.get('/projects/celebration-wall', { params });