import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { getMilestones, createMilestone, toggleMilestone, deleteMilestone } from '../../api/milestones';
import Button from '../common/Button';
import Spinner from '../common/Spinner';
import EmptyState from '../common/EmptyState';
import toast from 'react-hot-toast';
import { FaTrash, FaCheck, FaTasks } from 'react-icons/fa';

const MilestoneTracker = ({ projectId }) => {
  const [milestones, setMilestones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newTitle, setNewTitle] = useState('');
  const [adding, setAdding] = useState(false);

  useEffect(() => {
    fetchMilestones();
  }, [projectId]);

  const fetchMilestones = async () => {
    try {
      const { data } = await getMilestones(projectId);
      setMilestones(data);
    } catch {
      toast.error('Failed to load milestones');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = async (e) => {
    e.preventDefault();
    if (!newTitle.trim()) return;
    setAdding(true);
    try {
      const { data } = await createMilestone(projectId, { title: newTitle });
      setMilestones([...milestones, data]);
      setNewTitle('');
      toast.success('Milestone added');
    } catch {
      toast.error('Failed to add milestone');
    } finally {
      setAdding(false);
    }
  };

  const handleToggle = async (id) => {
    try {
      const { data } = await toggleMilestone(id);
      setMilestones(milestones.map(m => m.id === id ? data : m));
    } catch {
      toast.error('Failed to update milestone');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this milestone?')) return;
    try {
      await deleteMilestone(id);
      setMilestones(milestones.filter(m => m.id !== id));
      toast.success('Milestone deleted');
    } catch {
      toast.error('Failed to delete milestone');
    }
  };

  if (loading) return <Spinner />;

  const completed = milestones.filter(m => m.completed).length;
  const total = milestones.length;
  const progress = total ? (completed / total) * 100 : 0;

  return (
    <div>
      <h3 className="text-xl font-semibold mb-2">Milestones</h3>

      {total > 0 && (
        <div className="mb-4">
          <div className="flex justify-between text-sm mb-1">
            <span>Progress</span>
            <span>{completed}/{total}</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <motion.div
              className="bg-primary h-2 rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.3 }}
            />
          </div>
        </div>
      )}

      <form onSubmit={handleAdd} className="flex gap-2 mb-4">
        <input
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          placeholder="Add a milestone"
          className="flex-1 p-2 border rounded-lg"
        />
        <Button type="submit" isLoading={adding}>Add</Button>
      </form>

      {milestones.length === 0 ? (
        <EmptyState
          icon={FaTasks}
          title="No milestones yet"
          description="Break down your project into manageable steps to track progress."
        />
      ) : (
        <AnimatePresence>
          <ul className="space-y-2">
            {milestones.map(m => (
              <motion.li
                key={m.id}
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="flex items-center justify-between p-2 border rounded-lg"
              >
                <div className="flex items-center gap-2">
                  <motion.button
                    onClick={() => handleToggle(m.id)}
                    className={`w-5 h-5 border rounded flex items-center justify-center ${
                      m.completed ? 'bg-primary border-primary text-white' : 'border-gray-300'
                    }`}
                    whileTap={{ scale: 0.9 }}
                  >
                    {m.completed && (
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ type: 'spring', stiffness: 500, damping: 15 }}
                      >
                        <FaCheck size={12} />
                      </motion.div>
                    )}
                  </motion.button>
                  <span className={m.completed ? 'line-through text-gray-500' : ''}>
                    {m.title}
                  </span>
                </div>
                <motion.button
                  onClick={() => handleDelete(m.id)}
                  className="text-gray-400 hover:text-red-500"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                >
                  <FaTrash size={14} />
                </motion.button>
              </motion.li>
            ))}
          </ul>
        </AnimatePresence>
      )}
    </div>
  );
};

export default MilestoneTracker;