import React from 'react';
import { Card } from './ui/Card';
import { Badge } from './ui/Badge';
import { recentOrders } from '../utils/mockData';
import { formatCurrency, formatDate } from '../utils/formatters';
export function OrdersTable() {
  return <Card padding={false}>
      <div className="p-6 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900">Recent Orders</h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Order ID
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Customer
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Product
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Amount
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Date
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {recentOrders.map(order => <tr key={order.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {order.id}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {order.customer}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {order.product}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">
                  {formatCurrency(order.amount)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <Badge variant={order.status === 'completed' ? 'success' : 'warning'}>
                    {order.status}
                  </Badge>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {formatDate(order.date)}
                </td>
              </tr>)}
          </tbody>
        </table>
      </div>
    </Card>;
}