// src/pages/ProjectPage.jsx
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { useProject } from '../hooks/useProjects';
import Card from '../components/common/Card';
import Spinner from '../components/common/Spinner';
import LikeButton from '../components/interactions/LikeButton';
import CommentSection from '../components/interactions/CommentSection';
import CollaborationRequest from '../components/interactions/CollaborationRequest';
import MilestoneTracker from '../components/milestones/MilestoneTracker';
import { FaUser, FaCalendar, FaEdit } from 'react-icons/fa';
import { formatDistanceToNow } from 'date-fns';

const ProjectPage = () => {
  const { id } = useParams();
  const { user } = useAuth();
  const { data: project, isLoading, error } = useProject(id);

  if (isLoading) {
    return (
      <div className="flex justify-center py-20">
        <Spinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center text-red-500 py-20">
        Project not found or failed to load.
      </div>
    );
  }

  if (!project) return null;

  const isOwner = user && user.id === project.user_id;

  const stageColors = {
    planning: 'bg-yellow-100 text-yellow-800',
    in_progress: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800',
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <Card>
        <div className="flex justify-between items-start mb-4">
          <h1 className="text-3xl font-display font-bold">{project.title}</h1>
          <div className="flex items-center gap-3">
            <LikeButton projectId={project.id} initialLikes={project.likes_count} />
            {isOwner && (
              <Link
                to={`/projects/${project.id}/edit`}
                className="flex items-center gap-1 text-primary hover:underline"
              >
                <FaEdit /> Edit
              </Link>
            )}
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-4 mb-4">
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${stageColors[project.stage]}`}>
            {project.stage.replace('_', ' ')}
          </span>
          <div className="flex items-center gap-2 text-gray-600">
            <FaUser />
            <span>@{project.owner_username}</span>
          </div>
          <div className="flex items-center gap-2 text-gray-600">
            <FaCalendar />
            <span>
              {formatDistanceToNow(new Date(project.created_at), { addSuffix: true })}
            </span>
          </div>
        </div>

        <p className="text-gray-700 whitespace-pre-wrap mb-6">{project.description}</p>

        {project.support_needed && (
          <div className="bg-primary/5 p-4 rounded-lg mb-6">
            <h3 className="font-semibold text-primary mb-1">🤝 Support Needed</h3>
            <p className="text-gray-700">{project.support_needed}</p>
          </div>
        )}

        {!isOwner && <CollaborationRequest projectId={project.id} />}
      </Card>

      {isOwner && (
        <Card>
          <MilestoneTracker projectId={project.id} />
        </Card>
      )}

      <Card>
        <CommentSection projectId={project.id} />
      </Card>
    </div>
  );
};

export default ProjectPage;