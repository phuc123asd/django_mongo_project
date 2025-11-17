import React from 'react';
import { Link } from 'react-router-dom';

type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost';
type ButtonSize = 'sm' | 'md' | 'lg';
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  fullWidth?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  isLoading?: boolean;
  as?: typeof Link;
  to?: string;
}
export const Button = ({
  variant = 'primary',
  size = 'md',
  fullWidth = false,
  leftIcon,
  rightIcon,
  isLoading = false,
  className = '',
  children,
  disabled,
  as,
  to,
  ...props
}: ButtonProps) => {
  const baseStyles = 'inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transform hover:scale-105 active:scale-95';
  const variantStyles = {
    primary: 'bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white shadow-md hover:shadow-xl',
    secondary: 'bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-900 dark:text-white shadow-sm hover:shadow-md',
    outline: 'border-2 border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-200 hover:border-indigo-500 dark:hover:border-indigo-500',
    ghost: 'hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-200'
  };
  const sizeStyles = {
    sm: 'text-xs px-4 py-2',
    md: 'text-sm px-5 py-2.5',
    lg: 'text-base px-7 py-3.5'
  };
  const disabledStyles = 'opacity-60 cursor-not-allowed hover:scale-100';
  const widthStyles = fullWidth ? 'w-full' : '';

  const combinedClassName = `
    ${baseStyles} 
    ${variantStyles[variant]} 
    ${sizeStyles[size]} 
    ${disabled || isLoading ? disabledStyles : ''} 
    ${widthStyles} 
    ${className}
  `;

  const content = (
    <>
      {isLoading && <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>}
      {!isLoading && leftIcon && <span className="mr-2">{leftIcon}</span>}
      {children}
      {!isLoading && rightIcon && <span className="ml-2">{rightIcon}</span>}
    </>
  );

  if (as === Link && to) {
    const { onClick: propsOnClick, ...restProps } = props;
    
    const handleLinkClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
      if (disabled || isLoading) {
        e.preventDefault();
        return;
      }
      if (propsOnClick) {
        propsOnClick(e as any);
      }
    };

    return <Link 
      to={to} 
      className={combinedClassName}
      aria-disabled={disabled || isLoading}
      {...(restProps as any)}
      onClick={handleLinkClick}
    >
      {content}
    </Link>;
  }

  return <button className={combinedClassName} disabled={disabled || isLoading} {...props}>
      {content}
    </button>;
};