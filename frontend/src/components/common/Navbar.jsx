import { Link, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaBars, FaTimes, FaUser, FaSignOutAlt, FaPlus } from 'react-icons/fa';
import { useAuth } from '../../hooks/useAuth';
import Button from './Button';

const Navbar = () => {
  const { user, logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
    setIsOpen(false);
  };

  return (
    <nav className="bg-white shadow-sm sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2">
            <span className="text-2xl font-display font-bold">
              <span className="text-primary">Mzansi</span>
              <span className="text-secondary">Builds</span>
            </span>
          </Link>

          <div className="hidden md:flex items-center gap-6">
            <Link to="/celebration-wall" className="text-gray-700 hover:text-primary font-medium">
              🎉 Celebration Wall
            </Link>
            {user ? (
              <>
                <Link to="/dashboard" className="text-gray-700 hover:text-primary font-medium">
                  Dashboard
                </Link>
                <Link to="/profile" className="text-gray-700 hover:text-primary font-medium">
                  Profile
                </Link>
                <Button variant="primary" onClick={() => navigate('/projects/new')} size="sm">
                  <FaPlus className="mr-1" /> New Project
                </Button>
                <div className="relative group">
                  <button className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                    <FaUser className="text-primary" />
                  </button>
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg py-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all">
                    <Link to="/profile" className="block px-4 py-2 hover:bg-gray-50">Profile Settings</Link>
                    <button onClick={handleLogout} className="w-full text-left px-4 py-2 text-red-600 hover:bg-red-50">
                      Sign Out
                    </button>
                  </div>
                </div>
              </>
            ) : (
              <>
                <Link to="/login">
                  <Button variant="ghost">Sign In</Button>
                </Link>
                <Link to="/register">
                  <Button variant="primary">Get Started</Button>
                </Link>
              </>
            )}
          </div>

          <button className="md:hidden" onClick={() => setIsOpen(!isOpen)}>
            {isOpen ? <FaTimes size={24} /> : <FaBars size={24} />}
          </button>
        </div>
      </div>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden border-t"
          >
            <div className="container mx-auto px-4 py-4 space-y-3">
              <Link to="/celebration-wall" className="block py-2" onClick={() => setIsOpen(false)}>
                🎉 Celebration Wall
              </Link>
              {user ? (
                <>
                  <Link to="/dashboard" className="block py-2" onClick={() => setIsOpen(false)}>Dashboard</Link>
                  <Link to="/profile" className="block py-2" onClick={() => setIsOpen(false)}>Profile</Link>
                  <Button variant="primary" className="w-full justify-center" onClick={() => { navigate('/projects/new'); setIsOpen(false); }}>
                    <FaPlus className="mr-1" /> New Project
                  </Button>
                  <button onClick={handleLogout} className="w-full text-left py-2 text-red-600">
                    <FaSignOutAlt className="inline mr-2" /> Sign Out
                  </button>
                </>
              ) : (
                <>
                  <Link to="/login" className="block py-2" onClick={() => setIsOpen(false)}>Sign In</Link>
                  <Link to="/register" className="block py-2" onClick={() => setIsOpen(false)}>Get Started</Link>
                </>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
};

export default Navbar;