// src/hooks/useProjects.js
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getProjects, getProject, createProject, updateProject } from '../api/projects';
import toast from 'react-hot-toast';

export const useProjects = (params) => {
  return useQuery({
    queryKey: ['projects', params],
    queryFn: () => getProjects(params).then(res => res.data),
    keepPreviousData: true,
  });
};

export const useProject = (id) => {
  return useQuery({
    queryKey: ['project', id],
    queryFn: () => getProject(id).then(res => res.data),
    enabled: !!id,
  });
};

export const useCreateProject = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createProject,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
      toast.success('Project created!');
    },
    onError: (err) => {
      toast.error(err.response?.data?.error || 'Failed to create project');
    },
  });
};

export const useUpdateProject = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }) => updateProject(id, data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
      queryClient.invalidateQueries({ queryKey: ['project', data.data.id] });
      toast.success('Project updated!');
    },
    onError: (err) => {
      toast.error(err.response?.data?.error || 'Failed to update project');
    },
  });
};