import React from 'react';
import { Card } from '../components/ui/Card';
import { PackageIcon } from 'lucide-react';
export function ProductsPage() {
  return <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Products</h1>
        <p className="text-gray-600 mt-1">Manage your product inventory</p>
      </div>

      <Card className="text-center py-12">
        <PackageIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          Products Management
        </h3>
        <p className="text-gray-600">
          This page will contain product management features including
          inventory, pricing, and categories.
        </p>
      </Card>
    </div>;
}