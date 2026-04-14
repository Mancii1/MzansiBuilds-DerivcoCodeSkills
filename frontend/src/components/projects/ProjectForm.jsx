import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createProject } from '../../api/projects';
import Button from '../common/Button';
import Card from '../common/Card';
import toast from 'react-hot-toast';

const ProjectForm = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    stage: 'planning',
    support_needed: '',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const { data } = await createProject(formData);
      toast.success('Project created!');
      navigate(`/projects/${data.id}`);
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to create project');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Create New Project</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          name="title"
          placeholder="Project Title"
          value={formData.title}
          onChange={handleChange}
          className="w-full p-3 border rounded-lg"
          required
        />
        <textarea
          name="description"
          placeholder="Description"
          value={formData.description}
          onChange={handleChange}
          className="w-full p-3 border rounded-lg"
          rows="4"
          required
        />
        <select
          name="stage"
          value={formData.stage}
          onChange={handleChange}
          className="w-full p-3 border rounded-lg"
        >
          <option value="planning">Planning</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
        <textarea
          name="support_needed"
          placeholder="What kind of help do you need? (optional)"
          value={formData.support_needed}
          onChange={handleChange}
          className="w-full p-3 border rounded-lg"
          rows="2"
        />
        <div className="flex gap-4">
          <Button type="submit" isLoading={loading}>Create Project</Button>
          <Button type="button" variant="secondary" onClick={() => navigate('/dashboard')}>
            Cancel
          </Button>
        </div>
      </form>
    </Card>
  );
};

export default ProjectForm;