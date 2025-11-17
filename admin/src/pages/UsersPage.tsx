import React from 'react';
import { Card } from '../components/ui/Card';
import { UsersIcon } from 'lucide-react';
export function UsersPage() {
  return <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Users</h1>
        <p className="text-gray-600 mt-1">Manage customer accounts</p>
      </div>

      <Card className="text-center py-12">
        <UsersIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          User Management
        </h3>
        <p className="text-gray-600">
          This page will contain user management features including customer
          profiles, activity, and permissions.
        </p>
      </Card>
    </div>;
}