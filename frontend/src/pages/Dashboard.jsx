import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FaPlus, FaInbox } from 'react-icons/fa';
import { useAuth } from '../hooks/useAuth';
import { getProjects } from '../api/projects';
import ProjectCard from '../components/projects/ProjectCard';
import Button from '../components/common/Button';
import Spinner from '../components/common/Spinner';

const Dashboard = () => {
  const { user } = useAuth();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);

  useEffect(() => {
    fetchProjects();
  }, [page]);

  const fetchProjects = async () => {
    try {
      const { data } = await getProjects({ page, per_page: 12 });
      setProjects(prev => page === 1 ? data.items : [...prev, ...data.items]);
      setHasMore(data.page < data.pages);
    } catch (error) {
      console.error('Failed to fetch projects:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-display font-bold mb-2">
            Welcome back, <span className="text-primary">{user?.username}</span>!
          </h1>
          <p className="text-gray-600">Explore projects from the community</p>
        </div>
        <Link to="/projects/new">
          <Button>
            <FaPlus className="mr-2" /> New Project
          </Button>
        </Link>
      </div>

      {loading && page === 1 ? (
        <div className="flex justify-center py-20">
          <Spinner size="lg" />
        </div>
      ) : projects.length === 0 ? (
        <div className="text-center py-20">
          <FaInbox className="text-6xl text-gray-300 mx-auto mb-4" />
          <h3 className="text-xl font-semibold mb-2">No projects yet</h3>
          <p className="text-gray-600 mb-4">Be the first to showcase your work!</p>
          <Link to="/projects/new">
            <Button>Create a Project</Button>
          </Link>
        </div>
      ) : (
        <>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((project, index) => (
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
          
          {hasMore && (
            <div className="text-center mt-10">
              <Button onClick={() => setPage(p => p + 1)} isLoading={loading} variant="secondary">
                Load More
              </Button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default Dashboard;