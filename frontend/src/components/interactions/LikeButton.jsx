import { useState } from 'react';
import { FaHeart } from 'react-icons/fa';
import { toggleLike } from '../../api/likes';
import { useAuth } from '../../hooks/useAuth';
import toast from 'react-hot-toast';

const LikeButton = ({ projectId, initialLikes = 0, initialLiked = false }) => {
  const [liked, setLiked] = useState(initialLiked);
  const [likesCount, setLikesCount] = useState(initialLikes);
  const [loading, setLoading] = useState(false);
  const { user } = useAuth();

  const handleToggle = async () => {
    if (!user) {
      toast.error('Please log in to like projects');
      return;
    }
    if (loading) return;
    setLoading(true);
    try {
      const { data } = await toggleLike(projectId);
      setLiked(data.liked);
      setLikesCount(prev => data.liked ? prev + 1 : prev - 1);
    } catch (err) {
      toast.error('Failed to update like');
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={handleToggle}
      disabled={loading}
      className="flex items-center gap-1 text-gray-500 hover:text-red-500 transition-colors"
    >
      <FaHeart className={liked ? 'text-red-500' : ''} />
      <span>{likesCount}</span>
    </button>
  );
};

export default LikeButton;