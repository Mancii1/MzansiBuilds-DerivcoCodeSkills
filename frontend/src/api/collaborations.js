import api from './client';

export const requestCollaboration = (projectId, message) => 
  api.post(`/projects/${projectId}/collaborate`, { message });
export const getIncomingRequests = (status) => api.get('/collaborations/incoming', { params: { status } });
export const getOutgoingRequests = (status) => api.get('/collaborations/outgoing', { params: { status } });
export const acceptRequest = (requestId) => api.patch(`/collaborations/${requestId}/accept`);
export const rejectRequest = (requestId) => api.patch(`/collaborations/${requestId}/reject`);