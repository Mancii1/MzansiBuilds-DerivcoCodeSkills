import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '../../hooks/useAuth';
import { getComments, addComment, deleteComment } from '../../api/comments';
import Button from '../common/Button';
import Spinner from '../common/Spinner';
import EmptyState from '../common/EmptyState';
import toast from 'react-hot-toast';
import { formatDistanceToNow } from 'date-fns';
import { FaTrash, FaComment } from 'react-icons/fa';

const CommentSection = ({ projectId }) => {
  const { user } = useAuth();
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newComment, setNewComment] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchComments();
  }, [projectId]);

  const fetchComments = async () => {
    try {
      const { data } = await getComments(projectId);
      setComments(data);
    } catch {
      toast.error('Failed to load comments');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!user) {
      toast.error('Please log in to comment');
      return;
    }
    if (!newComment.trim()) return;

    setSubmitting(true);
    try {
      const { data } = await addComment(projectId, newComment);
      setComments([data, ...comments]);
      setNewComment('');
      toast.success('Comment added');
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to add comment');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (commentId) => {
    if (!window.confirm('Delete this comment?')) return;
    try {
      await deleteComment(commentId);
      setComments(comments.filter(c => c.id !== commentId));
      toast.success('Comment deleted');
    } catch {
      toast.error('Failed to delete comment');
    }
  };

  if (loading) return <Spinner />;

  return (
    <div className="mt-8">
      <h3 className="text-xl font-semibold mb-4">Comments ({comments.length})</h3>

      <form onSubmit={handleSubmit} className="mb-6">
        <textarea
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          placeholder={user ? 'Write a comment...' : 'Please log in to comment'}
          disabled={!user}
          className="w-full p-3 border rounded-lg resize-none"
          rows="3"
        />
        <div className="flex justify-end mt-2">
          <Button type="submit" isLoading={submitting} disabled={!user}>
            Post Comment
          </Button>
        </div>
      </form>

      <AnimatePresence>
        {comments.length === 0 ? (
          <EmptyState
            icon={FaComment}
            title="No comments yet"
            description="Be the first to share your thoughts on this project."
          />
        ) : (
          <div className="space-y-4">
            {comments.map((comment) => (
              <motion.div
                key={comment.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, x: -30 }}
                className="bg-gray-50 p-4 rounded-lg"
              >
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <span className="font-medium">@{comment.author_username}</span>
                    <span className="text-gray-500 text-sm ml-2">
                      {formatDistanceToNow(new Date(comment.created_at), { addSuffix: true })}
                    </span>
                  </div>
                  {user && user.id === comment.user_id && (
                    <motion.button
                      onClick={() => handleDelete(comment.id)}
                      className="text-gray-400 hover:text-red-500"
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                    >
                      <FaTrash size={14} />
                    </motion.button>
                  )}
                </div>
                <p className="text-gray-700">{comment.content}</p>
              </motion.div>
            ))}
          </div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default CommentSection;