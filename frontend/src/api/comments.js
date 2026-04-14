import api from './client';

export const getComments = (projectId) => api.get(`/projects/${projectId}/comments`);
export const addComment = (projectId, content) => api.post(`/projects/${projectId}/comments`, { content });
export const deleteComment = (commentId) => api.delete(`/projects/comments/${commentId}`);