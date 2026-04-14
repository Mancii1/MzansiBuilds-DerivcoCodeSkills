import api from './client';

export const getProfile = () => api.get('/profile');
export const updateProfile = (data) => api.put('/profile', data);
export const getPublicProfile = (userId) => api.get(`/users/${userId}`);