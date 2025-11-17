import React from 'react';
export interface AvatarProps {
  src?: string;
  alt?: string;
  fallback?: string;
  size?: 'sm' | 'md' | 'lg';
}
export function Avatar({
  src,
  alt = '',
  fallback = 'U',
  size = 'md'
}: AvatarProps) {
  const sizes = {
    sm: 'w-8 h-8 text-xs',
    md: 'w-10 h-10 text-sm',
    lg: 'w-12 h-12 text-base'
  };
  if (src) {
    return <img src={src} alt={alt} className={`${sizes[size]} rounded-full object-cover`} />;
  }
  return <div className={`${sizes[size]} rounded-full bg-blue-600 text-white flex items-center justify-center font-medium`}>
      {fallback}
    </div>;
}