import React from 'react';
import { Card } from './ui/Card';
import { Badge } from './ui/Badge';
import { AlertTriangleIcon, TrendingUpIcon, StarIcon } from 'lucide-react';
import { lowStockProducts, topProducts } from '../utils/mockData';
import { formatCurrency, formatNumber } from '../utils/formatters';
export function LowStockAlerts() {
  return <Card>
      <div className="flex items-center mb-4">
        <AlertTriangleIcon className="w-5 h-5 text-yellow-600 mr-2" />
        <h3 className="text-lg font-semibold text-gray-900">
          Low Stock Alerts
        </h3>
      </div>
      <div className="space-y-3">
        {lowStockProducts.map(product => <div key={product.id} className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg border border-yellow-200">
            <div>
              <p className="text-sm font-medium text-gray-900">
                {product.name}
              </p>
              <p className="text-xs text-gray-600 mt-1">
                Only {product.stock} units left (threshold: {product.threshold})
              </p>
            </div>
            <Badge variant="warning">{product.stock} left</Badge>
          </div>)}
      </div>
    </Card>;
}
export function TopProducts() {
  return <Card>
      <div className="flex items-center mb-4">
        <TrendingUpIcon className="w-5 h-5 text-green-600 mr-2" />
        <h3 className="text-lg font-semibold text-gray-900">Top Products</h3>
      </div>
      <div className="space-y-4">
        {topProducts.map((product, index) => <div key={product.id} className="flex items-center justify-between">
            <div className="flex items-center flex-1">
              <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center font-semibold text-sm mr-3">
                {index + 1}
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">
                  {product.name}
                </p>
                <div className="flex items-center mt-1">
                  <StarIcon className="w-3 h-3 text-yellow-500 fill-current mr-1" />
                  <span className="text-xs text-gray-600">
                    {product.rating}
                  </span>
                  <span className="text-xs text-gray-400 mx-2">•</span>
                  <span className="text-xs text-gray-600">
                    {formatNumber(product.sales)} sales
                  </span>
                </div>
              </div>
            </div>
            <div className="text-right">
              <p className="text-sm font-semibold text-gray-900">
                {formatCurrency(product.revenue)}
              </p>
            </div>
          </div>)}
      </div>
    </Card>;
}