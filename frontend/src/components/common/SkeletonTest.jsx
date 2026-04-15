const SkeletonText = ({ lines = 3, className = '' }) => (
  <div className={`space-y-2 ${className}`}>
    {Array.from({ length: lines }).map((_, i) => (
      <div
        key={i}
        className="h-4 bg-gray-200 rounded animate-pulse"
        style={{ width: i === lines - 1 ? '70%' : '100%' }}
      />
    ))}
  </div>
);

export default SkeletonText;