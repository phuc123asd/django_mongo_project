import React from 'react';
import { Card } from '../components/ui/Card';
import { StarIcon } from 'lucide-react';
export function ReviewsPage() {
  return <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Reviews</h1>
        <p className="text-gray-600 mt-1">
          Monitor customer feedback and ratings
        </p>
      </div>

      <Card className="text-center py-12">
        <StarIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          Reviews Management
        </h3>
        <p className="text-gray-600">
          This page will contain review management features including
          moderation, responses, and analytics.
        </p>
      </Card>
    </div>;
}