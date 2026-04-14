import { Link } from 'react-router-dom';
import { FaComment, FaUser } from 'react-icons/fa';
import Card from '../common/Card';
import LikeButton from '../interactions/LikeButton';

const stageColors = {
  planning: 'bg-yellow-100 text-yellow-800',
  in_progress: 'bg-blue-100 text-blue-800',
  completed: 'bg-green-100 text-green-800',
};

const ProjectCard = ({ project }) => {
  return (
    <Card className="h-full flex flex-col">
      <div className="p-6 flex-1">
        <div className="flex items-start justify-between mb-3">
          <span className={`px-3 py-1 rounded-full text-xs font-medium ${stageColors[project.stage]}`}>
            {project.stage?.replace('_', ' ') || 'planning'}
          </span>
          <LikeButton projectId={project.id} initialLikes={project.likes_count} />
        </div>
        
        <Link to={`/projects/${project.id}`}>
          <h3 className="text-xl font-semibold mb-2 hover:text-primary transition-colors">
            {project.title}
          </h3>
        </Link>
        
        <p className="text-gray-600 line-clamp-3 mb-4">{project.description}</p>
        
        {project.support_needed && (
          <div className="bg-primary/5 p-3 rounded-lg mb-4">
            <p className="text-sm font-medium text-primary">🤝 Support Needed</p>
            <p className="text-sm text-gray-700">{project.support_needed}</p>
          </div>
        )}
      </div>
      
      <div className="border-t border-gray-100 p-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center">
            <FaUser className="text-primary text-sm" />
          </div>
          <span className="text-sm font-medium">@{project.owner_username}</span>
        </div>
        <div className="flex items-center gap-3 text-gray-500">
          <span className="flex items-center gap-1 text-sm">
            <FaComment /> {project.comments_count || 0}
          </span>
        </div>
      </div>
    </Card>
  );
};

export default ProjectCard;