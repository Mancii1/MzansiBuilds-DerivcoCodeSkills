import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FaPlus, FaInbox, FaCheck, FaTimes, FaUserPlus, FaProjectDiagram, FaCheckCircle } from 'react-icons/fa';
import { useAuth } from '../hooks/useAuth';
import { useProjects } from '../hooks/useProjects';
import { getIncomingRequests, acceptRequest, rejectRequest } from '../api/collaborations';
import ProjectCard from '../components/projects/ProjectCard';
import Button from '../components/common/Button';
import Card from '../components/common/Card';
import SkeletonCard from '../components/common/SkeletonCard';
import EmptyState from '../components/common/EmptyState';
import Spinner from '../components/common/Spinner';
import toast from 'react-hot-toast';
import { formatDistanceToNow } from 'date-fns';

// Stats Card Component
const StatsCard = ({ icon: Icon, label, value, color }) => (
  <Card className="p-6">
    <div className="flex items-center gap-4">
      <div className={`p-3 rounded-full ${color}`}>
        <Icon className="text-2xl text-white" />
      </div>
      <div>
        <p className="text-2xl font-bold">{value}</p>
        <p className="text-gray-600">{label}</p>
      </div>
    </div>
  </Card>
);

// Collaboration Request Item
const RequestItem = ({ request, onAccept, onReject, isLoading }) => (
  <div className="flex items-center justify-between p-4 border rounded-lg">
    <div className="flex-1">
      <p className="font-medium">
        <Link to={`/projects/${request.project_id}`} className="hover:text-primary">
          {request.project_title}
        </Link>
      </p>
      <p className="text-sm text-gray-600">
        From <span className="font-medium">@{request.requester_username}</span> •{' '}
        {formatDistanceToNow(new Date(request.created_at), { addSuffix: true })}
      </p>
      {request.message && <p className="text-sm text-gray-500 mt-1">{request.message}</p>}
    </div>
    <div className="flex gap-2 ml-4">
      <Button
        size="sm"
        variant="primary"
        onClick={() => onAccept(request.id)}
        isLoading={isLoading === `accept-${request.id}`}
      >
        <FaCheck />
      </Button>
      <Button
        size="sm"
        variant="danger"
        onClick={() => onReject(request.id)}
        isLoading={isLoading === `reject-${request.id}`}
      >
        <FaTimes />
      </Button>
    </div>
  </div>
);

const Dashboard = () => {
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [actionLoading, setActionLoading] = useState(null);

  // Fetch user's projects
  const { data: projectsData, isLoading: projectsLoading } = useProjects({ per_page: 100 });

  // Fetch incoming collaboration requests
  const { data: requests, isLoading: requestsLoading } = useQuery({
    queryKey: ['incoming-requests'],
    queryFn: () => getIncomingRequests('pending').then(res => res.data),
  });

  // Accept request mutation
  const acceptMutation = useMutation({
    mutationFn: acceptRequest,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['incoming-requests'] });
      toast.success('Request accepted!');
      setActionLoading(null);
    },
    onError: (err) => {
      toast.error(err.response?.data?.error || 'Failed to accept');
      setActionLoading(null);
    },
  });

  // Reject request mutation
  const rejectMutation = useMutation({
    mutationFn: rejectRequest,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['incoming-requests'] });
      toast.success('Request rejected');
      setActionLoading(null);
    },
    onError: (err) => {
      toast.error(err.response?.data?.error || 'Failed to reject');
      setActionLoading(null);
    },
  });

  const handleAccept = (id) => {
    setActionLoading(`accept-${id}`);
    acceptMutation.mutate(id);
  };

  const handleReject = (id) => {
    setActionLoading(`reject-${id}`);
    rejectMutation.mutate(id);
  };

  // Calculate stats
  const allProjects = projectsData?.items || [];
  const totalProjects = allProjects.length;
  const completedProjects = allProjects.filter(p => p.stage === 'completed').length;
  const activeCollaborations = allProjects.reduce((acc, p) => acc + (p.collaborators_count || 0), 0);

  // Recent activity (mock or real - here we show placeholder for simplicity)
  const recentActivity = [
    // In a real app, you'd fetch an activity feed from the backend
    // For now, we can leave it empty or show a placeholder
  ];

  if (!user) return null;

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-display font-bold mb-2">
            Welcome back, <span className="text-primary">{user.username}</span>!
          </h1>
          <p className="text-gray-600">Your MzansiBuilds dashboard</p>
        </div>
        <Link to="/projects/new">
          <Button>
            <FaPlus className="mr-2" /> New Project
          </Button>
        </Link>
      </div>

      {/* Stats Cards */}
      <div className="grid md:grid-cols-3 gap-6">
        <StatsCard
          icon={FaProjectDiagram}
          label="Total Projects"
          value={projectsLoading ? '...' : totalProjects}
          color="bg-primary"
        />
        <StatsCard
          icon={FaUserPlus}
          label="Active Collaborations"
          value={projectsLoading ? '...' : activeCollaborations}
          color="bg-blue-500"
        />
        <StatsCard
          icon={FaCheckCircle}
          label="Completed Projects"
          value={projectsLoading ? '...' : completedProjects}
          color="bg-green-500"
        />
      </div>

      {/* Collaboration Requests Section */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Collaboration Requests</h2>
        {requestsLoading ? (
          <div className="flex justify-center py-8">
            <Spinner />
          </div>
        ) : requests && requests.length > 0 ? (
          <Card className="divide-y">
            {requests.map(request => (
              <RequestItem
                key={request.id}
                request={request}
                onAccept={handleAccept}
                onReject={handleReject}
                isLoading={actionLoading}
              />
            ))}
          </Card>
        ) : (
          <Card className="p-8 text-center text-gray-500">
            No pending collaboration requests.
          </Card>
        )}
      </div>

      {/* Recent Projects Feed */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Your Recent Projects</h2>
        {projectsLoading ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {Array.from({ length: 3 }).map((_, i) => <SkeletonCard key={i} />)}
          </div>
        ) : allProjects.length === 0 ? (
          <EmptyState
            icon={FaInbox}
            title="No projects yet"
            description="Create your first project to start building and collaborating."
            actionText="Create Project"
            actionLink="/projects/new"
          />
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {allProjects.slice(0, 3).map((project, index) => (
              <motion.div
                key={project.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
              >
                <ProjectCard project={project} />
              </motion.div>
            ))}
          </div>
        )}
        {allProjects.length > 3 && (
          <div className="text-center mt-6">
            <Link to="/projects" className="text-primary hover:underline">
              View all projects →
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;