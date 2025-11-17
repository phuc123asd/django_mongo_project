import React from 'react';
export interface CardProps {
  children: React.ReactNode;
  className?: string;
  padding?: boolean;
}
export function Card({
  children,
  className = '',
  padding = true
}: CardProps) {
  return <div className={`bg-white rounded-lg shadow-sm border border-gray-200 ${padding ? 'p-6' : ''} ${className}`}>
      {children}
    </div>;
}