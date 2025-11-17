import React from 'react';
import { Card } from './ui/Card';
import { StarIcon } from 'lucide-react';
import { recentReviews } from '../utils/mockData';
import { formatDate } from '../utils/formatters';
export function RecentReviews() {
  return <Card>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Recent Reviews
      </h3>
      <div className="space-y-4">
        {recentReviews.map(review => <div key={review.id} className="border-b border-gray-200 last:border-0 pb-4 last:pb-0">
            <div className="flex items-start justify-between mb-2">
              <div>
                <p className="text-sm font-medium text-gray-900">
                  {review.customer}
                </p>
                <p className="text-xs text-gray-600">{review.product}</p>
              </div>
              <div className="flex items-center">
                {[...Array(5)].map((_, i) => <StarIcon key={i} className={`w-4 h-4 ${i < review.rating ? 'text-yellow-500 fill-current' : 'text-gray-300'}`} />)}
              </div>
            </div>
            <p className="text-sm text-gray-700 mb-2">{review.comment}</p>
            <p className="text-xs text-gray-500">{formatDate(review.date)}</p>
          </div>)}
      </div>
    </Card>;
}