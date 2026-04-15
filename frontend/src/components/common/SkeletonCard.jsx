import Card from './Card';

const SkeletonCard = () => (
  <Card className="h-full flex flex-col animate-pulse">
    <div className="p-6 flex-1">
      <div className="flex items-start justify-between mb-3">
        <div className="h-6 w-20 bg-gray-200 rounded-full" />
        <div className="h-6 w-6 bg-gray-200 rounded-full" />
      </div>
      <div className="h-7 w-3/4 bg-gray-200 rounded mb-2" />
      <div className="h-7 w-1/2 bg-gray-200 rounded mb-4" />
      <div className="space-y-2 mb-4">
        <div className="h-4 w-full bg-gray-200 rounded" />
        <div className="h-4 w-5/6 bg-gray-200 rounded" />
        <div className="h-4 w-4/6 bg-gray-200 rounded" />
      </div>
      <div className="bg-gray-100 p-3 rounded-lg">
        <div className="h-4 w-24 bg-gray-200 rounded mb-2" />
        <div className="h-4 w-full bg-gray-200 rounded" />
      </div>
    </div>
    <div className="border-t border-gray-100 p-4 flex items-center justify-between">
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 bg-gray-200 rounded-full" />
        <div className="h-4 w-16 bg-gray-200 rounded" />
      </div>
      <div className="h-4 w-8 bg-gray-200 rounded" />
    </div>
  </Card>
);

export default SkeletonCard;