import { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { requestCollaboration } from '../../api/collaborations';
import Button from '../common/Button';
import toast from 'react-hot-toast';

const CollaborationRequest = ({ projectId }) => {
  const { user } = useAuth();
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [requested, setRequested] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!user) {
      toast.error('Please log in to request collaboration');
      return;
    }
    setLoading(true);
    try {
      await requestCollaboration(projectId, message);
      setRequested(true);
      toast.success('Collaboration request sent!');
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to send request');
    } finally {
      setLoading(false);
    }
  };

  if (requested) {
    return (
      <div className="bg-green-50 text-green-800 p-4 rounded-lg text-center">
        ✓ Collaboration request sent!
      </div>
    );
  }

  return (
    <div className="border-t pt-6 mt-6">
      <h3 className="font-semibold mb-2">Interested in collaborating?</h3>
      <form onSubmit={handleSubmit}>
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Introduce yourself and how you can help (optional)"
          className="w-full p-3 border rounded-lg mb-3"
          rows="2"
        />
        <Button type="submit" isLoading={loading}>
          Request Collaboration
        </Button>
      </form>
    </div>
  );
};

export default CollaborationRequest;