import React from 'react';
import { Navbar } from './Navbar';
import { Footer } from './Footer';
import { Chatbot } from '../Chatbot';
interface LayoutProps {
  children: React.ReactNode;
}
export const Layout = ({
  children
}: LayoutProps) => {
  return <div className="flex flex-col min-h-screen bg-white dark:bg-gray-900 transition-colors duration-300">
      <Navbar />
      <main className="flex-grow pt-16 md:pt-20">{children}</main>
      <Footer />
      <Chatbot />
    </div>;
};