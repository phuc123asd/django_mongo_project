import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboardIcon, MessageSquareIcon, PackageIcon, ShoppingCartIcon, UsersIcon, StarIcon } from 'lucide-react';
const navigation = [{
  name: 'Dashboard',
  href: '/',
  icon: LayoutDashboardIcon
}, {
  name: 'AI Chat',
  href: '/chat',
  icon: MessageSquareIcon
}, {
  name: 'Products',
  href: '/products',
  icon: PackageIcon
}, {
  name: 'Orders',
  href: '/orders',
  icon: ShoppingCartIcon
}, {
  name: 'Users',
  href: '/users',
  icon: UsersIcon
}, {
  name: 'Reviews',
  href: '/reviews',
  icon: StarIcon
}];
export function Sidebar() {
  const location = useLocation();
  return <div className="w-64 bg-gray-900 text-white min-h-screen flex flex-col">
      <div className="p-6">
        <h1 className="text-2xl font-bold">TechStore Admin</h1>
        <p className="text-gray-400 text-sm mt-1">E-commerce Dashboard</p>
      </div>

      <nav className="flex-1 px-4 space-y-1">
        {navigation.map(item => {
        const isActive = location.pathname === item.href;
        const Icon = item.icon;
        return <Link key={item.name} to={item.href} className={`flex items-center px-4 py-3 rounded-lg transition-colors ${isActive ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-800 hover:text-white'}`}>
              <Icon className="w-5 h-5 mr-3" />
              {item.name}
            </Link>;
      })}
      </nav>

      <div className="p-4 border-t border-gray-800">
        <div className="flex items-center">
          <div className="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center font-medium">
            A
          </div>
          <div className="ml-3">
            <p className="text-sm font-medium">Admin User</p>
            <p className="text-xs text-gray-400">admin@techstore.com</p>
          </div>
        </div>
      </div>
    </div>;
}