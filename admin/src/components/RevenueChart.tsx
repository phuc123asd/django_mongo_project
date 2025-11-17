import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Card } from './ui/Card';
import { revenueData } from '../utils/mockData';
import { formatCurrency } from '../utils/formatters';
export function RevenueChart() {
  return <Card>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Revenue Overview
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={revenueData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis dataKey="date" stroke="#6b7280" style={{
          fontSize: '12px'
        }} />
          <YAxis stroke="#6b7280" style={{
          fontSize: '12px'
        }} tickFormatter={value => `$${value / 1000}k`} />
          <Tooltip formatter={(value: number) => formatCurrency(value)} contentStyle={{
          backgroundColor: '#fff',
          border: '1px solid #e5e7eb',
          borderRadius: '8px'
        }} />
          <Line type="monotone" dataKey="revenue" stroke="#2563eb" strokeWidth={2} dot={{
          fill: '#2563eb',
          r: 4
        }} activeDot={{
          r: 6
        }} />
        </LineChart>
      </ResponsiveContainer>
    </Card>;
}