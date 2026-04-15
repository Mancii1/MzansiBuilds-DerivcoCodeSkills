import { motion } from 'framer-motion';
import Button from './Button';
import { Link } from 'react-router-dom';

const EmptyState = ({
  icon: Icon,
  title,
  description,
  actionText,
  actionLink,
  onAction,
}) => {
  const ActionButton = () => (
    <Button onClick={onAction} variant="primary">
      {actionText}
    </Button>
  );

  const ActionLink = () => (
    <Link to={actionLink}>
      <Button variant="primary">{actionText}</Button>
    </Link>
  );

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="text-center py-16 px-4"
    >
      <div className="inline-flex items-center justify-center w-20 h-20 bg-primary/10 rounded-full mb-6">
        <Icon className="text-4xl text-primary" />
      </div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600 max-w-md mx-auto mb-6">{description}</p>
      {actionText && (actionLink ? <ActionLink /> : <ActionButton />)}
    </motion.div>
  );
};

export default EmptyState;