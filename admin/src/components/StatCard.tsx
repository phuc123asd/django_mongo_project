import React from 'react';
import { Card } from './ui/Card';
import { BoxIcon } from 'lucide-react';
export interface StatCardProps {
  title: string;
  value: string | number;
  trend?: string;
  icon: BoxIcon;
  iconColor?: string;
}
export function StatCard({
  title,
  value,
  trend,
  icon: Icon,
  iconColor = 'bg-blue-100 text-blue-600'
}: StatCardProps) {
  const isPositive = trend?.startsWith('+');
  return <Card>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
          {trend && <p className={`text-sm mt-2 ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
              {trend} from last week
            </p>}
        </div>
        <div className={`p-3 rounded-lg ${iconColor}`}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
    </Card>;
}