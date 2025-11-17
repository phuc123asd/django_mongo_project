import React from 'react';
import { UsersIcon, ShoppingCartIcon, PackageIcon, StarIcon } from 'lucide-react';
import { StatCard } from '../components/StatCard';
import { RevenueChart } from '../components/RevenueChart';
import { OrdersTable } from '../components/OrdersTable';
import { LowStockAlerts, TopProducts } from '../components/ProductList';
import { RecentReviews } from '../components/ReviewCard';
import { userStats, orderStats, productStats, reviewStats } from '../utils/mockData';
import { formatCurrency, formatNumber } from '../utils/formatters';
export function DashboardPage() {
  return <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">
          Welcome back, Admin
        </h1>
        <p className="text-gray-600 mt-1">
          Here's what's happening with your store today
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard title="Total Users" value={formatNumber(userStats.total)} trend={userStats.trend} icon={UsersIcon} iconColor="bg-blue-100 text-blue-600" />
        <StatCard title="Total Orders" value={formatNumber(orderStats.total)} trend={orderStats.trend} icon={ShoppingCartIcon} iconColor="bg-green-100 text-green-600" />
        <StatCard title="Revenue" value={formatCurrency(orderStats.revenue)} trend={orderStats.trend} icon={PackageIcon} iconColor="bg-purple-100 text-purple-600" />
        <StatCard title="Avg Rating" value={reviewStats.avgRating} trend={`+${reviewStats.trend}`} icon={StarIcon} iconColor="bg-yellow-100 text-yellow-600" />
      </div>

      {/* Revenue Chart */}
      <RevenueChart />

      {/* Recent Orders */}
      <OrdersTable />

      {/* Two Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <LowStockAlerts />
        <TopProducts />
      </div>

      {/* Recent Reviews */}
      <RecentReviews />
    </div>;
}