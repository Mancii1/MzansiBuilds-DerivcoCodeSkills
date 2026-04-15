import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useNavigate, useParams } from 'react-router-dom';
import { useProject, useCreateProject, useUpdateProject } from '../../hooks/useProjects';
import Button from '../common/Button';
import Card from '../common/Card';
import Spinner from '../common/Spinner';
import toast from 'react-hot-toast';

const projectSchema = z.object({
  title: z.string().min(1, 'Title is required'),
  description: z.string().min(10, 'Description must be at least 10 characters'),
  stage: z.enum(['planning', 'in_progress', 'completed']),
  support_needed: z.string().optional(),
});

const ProjectForm = () => {
  const { id } = useParams();
  const isEditMode = !!id;
  const navigate = useNavigate();
  
  const { data: project, isLoading: loadingProject } = useProject(id);
  const createProject = useCreateProject();
  const updateProject = useUpdateProject();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm({
    resolver: zodResolver(projectSchema),
    defaultValues: {
      stage: 'planning',
      support_needed: '',
    },
  });

  // Pre-fill form when editing
  useEffect(() => {
    if (isEditMode && project) {
      reset({
        title: project.title,
        description: project.description,
        stage: project.stage,
        support_needed: project.support_needed || '',
      });
    }
  }, [project, isEditMode, reset]);

  const onSubmit = (data) => {
    if (isEditMode) {
      updateProject.mutate(
        { id, data },
        {
          onSuccess: (response) => navigate(`/projects/${response.data.id}`),
        }
      );
    } else {
      createProject.mutate(data, {
        onSuccess: (response) => navigate(`/projects/${response.data.id}`),
      });
    }
  };

  if (isEditMode && loadingProject) {
    return (
      <div className="flex justify-center py-20">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <Card className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">
        {isEditMode ? 'Edit Project' : 'Create New Project'}
      </h1>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <input
            {...register('title')}
            placeholder="Project Title"
            className={`w-full p-3 border rounded-lg ${
              errors.title ? 'border-red-500' : 'border-gray-200'
            }`}
          />
          {errors.title && (
            <p className="mt-1 text-sm text-red-500">{errors.title.message}</p>
          )}
        </div>

        <div>
          <textarea
            {...register('description')}
            placeholder="Description"
            className={`w-full p-3 border rounded-lg ${
              errors.description ? 'border-red-500' : 'border-gray-200'
            }`}
            rows="4"
          />
          {errors.description && (
            <p className="mt-1 text-sm text-red-500">{errors.description.message}</p>
          )}
        </div>

        <div>
          <select
            {...register('stage')}
            className="w-full p-3 border border-gray-200 rounded-lg"
          >
            <option value="planning">Planning</option>
            <option value="in_progress">In Progress</option>
            <option value="completed">Completed</option>
          </select>
        </div>

        <div>
          <textarea
            {...register('support_needed')}
            placeholder="What kind of help do you need? (optional)"
            className="w-full p-3 border border-gray-200 rounded-lg"
            rows="2"
          />
        </div>

        <div className="flex gap-4">
          <Button type="submit" isLoading={isSubmitting}>
            {isEditMode ? 'Update Project' : 'Create Project'}
          </Button>
          <Button type="button" variant="secondary" onClick={() => navigate('/dashboard')}>
            Cancel
          </Button>
        </div>
      </form>
    </Card>
  );
};

export default ProjectForm;