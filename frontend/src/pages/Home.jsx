import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { FaRocket, FaUsers, FaTrophy } from 'react-icons/fa';
import Button from '../components/common/Button';
import ProjectFeed from '../components/projects/ProjectFeed';

const Home = () => {
  return (
    <div className="space-y-16">
      <section className="relative">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center max-w-4xl mx-auto py-16"
        >
          <h1 className="text-5xl md:text-6xl font-display font-bold mb-6">
            Build <span className="gradient-text">Together</span> in{' '}
            <span className="text-primary">Mzansi</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Connect with South African developers, showcase your projects, and find collaborators to bring ideas to life.
          </p>
          <div className="flex gap-4 justify-center">
            <Link to="/register">
              <Button size="lg">Get Started</Button>
            </Link>
            <Link to="/celebration-wall">
              <Button variant="secondary" size="lg">View Showcase</Button>
            </Link>
          </div>
        </motion.div>
        
        <div className="absolute top-20 left-10 w-64 h-64 bg-primary/5 rounded-full blur-3xl -z-10" />
        <div className="absolute bottom-20 right-10 w-80 h-80 bg-accent/10 rounded-full blur-3xl -z-10" />
      </section>

      <section className="grid md:grid-cols-3 gap-8">
        {[
          { icon: FaRocket, title: 'Showcase Work', desc: 'Post your projects and track progress with milestones.' },
          { icon: FaUsers, title: 'Find Collaborators', desc: 'Connect with skilled developers who can help you build.' },
          { icon: FaTrophy, title: 'Celebrate Wins', desc: 'Completed projects shine on our Celebration Wall.' },
        ].map(({ icon: Icon, title, desc }, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="bg-white p-6 rounded-2xl shadow-md text-center"
          >
            <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <Icon className="text-2xl text-primary" />
            </div>
            <h3 className="text-xl font-semibold mb-2">{title}</h3>
            <p className="text-gray-600">{desc}</p>
          </motion.div>
        ))}
      </section>

      <section>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-3xl font-display font-bold">Latest Projects</h2>
          <Link to="/dashboard" className="text-primary hover:underline font-medium">
            View all →
          </Link>
        </div>
        <ProjectFeed limit={6} />
      </section>
    </div>
  );
};

export default Home;