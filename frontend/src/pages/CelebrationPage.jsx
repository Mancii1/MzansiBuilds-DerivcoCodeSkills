import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FaTrophy } from 'react-icons/fa';
import { getCompletedProjects } from '../api/projects';
import ProjectCard from '../components/projects/ProjectCard';
import Button from '../components/common/Button';
import Spinner from '../components/common/Spinner';

const CelebrationPage = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);

  useEffect(() => {
    fetchProjects();
  }, [page]);

  const fetchProjects = async () => {
    try {
      const { data } = await getCompletedProjects({ page, per_page: 12 });
      setProjects(prev => page === 1 ? data.items : [...prev, ...data.items]);
      setHasMore(data.page < data.pages);
    } catch (error) {
      console.error('Failed to fetch completed projects:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="bg-gradient-to-r from-primary to-primary-dark rounded-3xl p-8 md:p-12 mb-12 text-white"
      >
        <div className="flex items-center gap-4 mb-4">
          <FaTrophy className="text-4xl text-yellow-300" />
          <h1 className="text-4xl md:text-5xl font-display font-bold">Celebration Wall</h1>
        </div>
        <p className="text-xl opacity-90 max-w-2xl">
          Celebrating completed projects from our amazing community. Be inspired by what Mzansi developers are building.
        </p>
        <div className="mt-6">
          <div className="bg-white/20 backdrop-blur-sm rounded-full px-6 py-2 inline-block">
            <span className="font-semibold">{projects.length}</span> Projects Celebrated
          </div>
        </div>
      </motion.div>

      {loading && page === 1 ? (
        <div className="flex justify-center py-20">
          <Spinner size="lg" />
        </div>
      ) : projects.length === 0 ? (
        <div className="text-center py-20 text-gray-500">
          <FaTrophy className="text-6xl text-gray-300 mx-auto mb-4" />
          <p className="text-xl">No completed projects yet. Be the first to finish one!</p>
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

export default CelebrationPage;