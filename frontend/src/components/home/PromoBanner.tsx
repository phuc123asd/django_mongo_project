import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../ui/Button';
export const PromoBanner = () => {
  return <section className="py-12 bg-gray-900 text-white">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-black to-indigo-900">
          <div className="absolute inset-0">
            <img src="https://images.unsplash.com/photo-1550745165-9bc0b252726f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80" alt="Black Friday Sale" className="w-full h-full object-cover object-center opacity-40" />
          </div>
          <div className="relative z-10 flex flex-col lg:flex-row items-center justify-between p-8 md:p-12 lg:p-16">
            <div className="mb-8 lg:mb-0 text-center lg:text-left">
              <span className="inline-block px-3 py-1 bg-indigo-600 text-white text-sm font-medium rounded-full mb-4">
                Ưu Đãi Có Thời Hạn
              </span>
              <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
                Khuyến Mãi <span className="text-indigo-400">Black Friday</span>
              </h2>
              <p className="text-lg md:text-xl text-gray-300 mb-6 max-w-xl">
                Giảm giá lên đến 50% cho các sản phẩm công nghệ cao cấp. Ưu đãi có hiệu lực
                đến ngày 30 tháng 11.
              </p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 text-center">
                <span className="block text-4xl font-bold mb-1">15</span>
                <span className="block text-sm text-gray-300">Ngày</span>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 text-center">
                <span className="block text-4xl font-bold mb-1">08</span>
                <span className="block text-sm text-gray-300">Giờ</span>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 text-center">
                <span className="block text-4xl font-bold mb-1">23</span>
                <span className="block text-sm text-gray-300">Phút</span>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 text-center">
                <span className="block text-4xl font-bold mb-1">42</span>
                <span className="block text-sm text-gray-300">Giây</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>;
};