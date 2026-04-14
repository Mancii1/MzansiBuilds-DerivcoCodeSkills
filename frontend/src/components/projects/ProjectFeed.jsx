import { useState, useEffect } from 'react';
import { getProjects } from '../../api/projects';
import ProjectCard from './ProjectCard';
import Spinner from '../common/Spinner';

const ProjectFeed = ({ limit }) => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const { data } = await getProjects({ per_page: limit || 6 });
        setProjects(data.items);
      } catch (err) {
        console.error('Failed to fetch projects:', err);
        setError('Could not load projects');
      } finally {
        setLoading(false);
      }
    };
    fetchProjects();
  }, [limit]);

  if (loading) return <Spinner />;
  if (error) return <div className="text-red-500 text-center">{error}</div>;
  if (projects.length === 0) return <div className="text-gray-500 text-center">No projects yet.</div>;

  return (
    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      {projects.map((project) => (
        <ProjectCard key={project.id} project={project} />
      ))}
    </div>
  );
};

export default ProjectFeed;