import React from 'react';
import { SparklesIcon } from 'lucide-react';
export interface WelcomeScreenProps {
  onPromptClick: (prompt: string) => void;
}
const suggestedPrompts = [{
  title: 'Analyze Recent Orders',
  prompt: 'Show me a summary of recent orders and sales trends'
}, {
  title: 'Review Insights',
  prompt: 'What are customers saying in recent reviews?'
}, {
  title: 'Low Stock Alert',
  prompt: 'Which products need restocking?'
}, {
  title: 'Top Products',
  prompt: 'Show me the best-selling products this month'
}];
export function WelcomeScreen({
  onPromptClick
}: WelcomeScreenProps) {
  return <div className="flex flex-col items-center justify-center h-full px-4 py-12">
      <div className="max-w-2xl w-full text-center space-y-8">
        {/* Hero Section */}
        <div className="space-y-4">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-3xl shadow-lg mb-4">
            <SparklesIcon className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Hello, Admin
          </h1>
          <p className="text-xl text-gray-600">
            How can I help you manage TechStore today?
          </p>
        </div>

        {/* Suggested Prompts */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-12">
          {suggestedPrompts.map((item, index) => <button key={index} onClick={() => onPromptClick(item.prompt)} className="group p-6 bg-white border-2 border-gray-200 rounded-2xl hover:border-blue-500 hover:shadow-lg transition-all duration-200 text-left">
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-blue-100 to-purple-100 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
                  <SparklesIcon className="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                    {item.title}
                  </h3>
                  <p className="text-sm text-gray-600 mt-1">{item.prompt}</p>
                </div>
              </div>
            </button>)}
        </div>

        {/* Footer Note */}
        <div className="mt-12 pt-8 border-t border-gray-200">
          <p className="text-sm text-gray-500">
            💡 I can analyze orders, summarize reviews, track inventory, and
            provide product insights
          </p>
        </div>
      </div>
    </div>;
}