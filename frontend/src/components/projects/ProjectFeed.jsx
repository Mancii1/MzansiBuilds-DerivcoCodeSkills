import { useProjects } from '../../hooks/useProjects';
import ProjectCard from './ProjectCard';
import SkeletonCard from '../common/SkeletonCard';

const ProjectFeed = ({ limit }) => {
  const { data, isLoading, error } = useProjects({ per_page: limit || 6 });

  if (error) return <div className="text-red-500 text-center">Could not load projects</div>;
  if (!isLoading && (!data || data.items.length === 0))
    return <div className="text-gray-500 text-center">No projects yet.</div>;

  return (
    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      {isLoading
        ? Array.from({ length: limit || 6 }).map((_, i) => <SkeletonCard key={i} />)
        : data.items.map((project) => <ProjectCard key={project.id} project={project} />)}
    </div>
  );
};

export default ProjectFeed;