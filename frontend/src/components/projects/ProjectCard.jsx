// src/components/projects/ProjectCard.jsx

import { Link } from 'react-router-dom';
import { FaComment, FaUser } from 'react-icons/fa';
import Card from '../common/Card';
import LikeButton from '../interactions/LikeButton';
import { formatDistanceToNow } from 'date-fns';

const stageColors = {
  planning: 'bg-yellow-100 text-yellow-800',
  in_progress: 'bg-blue-100 text-blue-800',
  completed: 'bg-green-100 text-green-800',
};

const ProjectCard = ({ project }) => {
  // Guard clause – prevent rendering if project prop is missing
  if (!project) return null;

  return (
    <Card className="h-full flex flex-col">
      <div className="p-6 flex-1">
        {/* Stage badge and like button */}
        <div className="flex items-start justify-between mb-3">
          <span
            className={`px-3 py-1 rounded-full text-xs font-medium ${
              stageColors[project.stage] || 'bg-gray-100 text-gray-800'
            }`}
          >
            {project.stage?.replace('_', ' ') || 'planning'}
          </span>
          <LikeButton projectId={project.id} initialLikes={project.likes_count} />
        </div>

        {/* Title with link to detail page */}
        <Link to={`/projects/${project.id}`}>
          <h3 className="text-xl font-semibold mb-2 hover:text-primary transition-colors line-clamp-2">
            {project.title}
          </h3>
        </Link>

        {/* Description */}
        <p className="text-gray-600 line-clamp-3 mb-4">{project.description}</p>

        {/* Support needed section (optional) */}
        {project.support_needed && (
          <div className="bg-primary/5 p-3 rounded-lg mb-4">
            <p className="text-sm font-medium text-primary">🤝 Support Needed</p>
            <p className="text-sm text-gray-700 line-clamp-2">{project.support_needed}</p>
          </div>
        )}
      </div>

      {/* Footer: owner info, timestamp, comment count */}
      <div className="border-t border-gray-100 p-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center">
            <FaUser className="text-primary text-sm" />
          </div>
          <span className="text-sm font-medium">@{project.owner_username}</span>
          <span className="text-xs text-gray-400">
            {formatDistanceToNow(new Date(project.created_at), { addSuffix: true })}
          </span>
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