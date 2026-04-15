const SkeletonAvatar = ({ size = 'md' }) => {
  const sizes = {
    sm: 'w-8 h-8',
    md: 'w-10 h-10',
    lg: 'w-16 h-16',
  };
  return <div className={`${sizes[size]} bg-gray-200 rounded-full animate-pulse`} />;
};

export default SkeletonAvatar;