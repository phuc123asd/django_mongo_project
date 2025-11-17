import { Link } from 'react-router-dom';
import { Button } from '../ui/Button';
import { ArrowRightIcon, SparklesIcon } from 'lucide-react';
export const HeroSection = () => {
  return <section className="relative bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 overflow-hidden">
      <div className="absolute inset-0 bg-black/20"></div>
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-white/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-white/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32 relative z-10">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          <div className="text-white">
            <div className="inline-flex items-center px-4 py-2 bg-white/20 backdrop-blur-sm rounded-full text-sm font-medium mb-6">
              <SparklesIcon className="w-4 h-4 mr-2" />
              Hàng Mới Về
            </div>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 leading-tight">
              Công Nghệ Thế Hệ Mới <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-300">
                Cho Cuộc Sống Hiện Đại
              </span>
            </h1>
            <p className="text-lg md:text-xl mb-8 text-gray-100 max-w-lg">
              Khám phá điện thoại, laptop và phụ kiện mới nhất với
              công nghệ tiên tiến và thiết kế cao cấp.
            </p>
            <div className="flex flex-wrap gap-4">
              <Button as={Link} to="/shop" size="lg" rightIcon={<ArrowRightIcon className="w-5 h-5" />} className="bg-white text-indigo-600 hover:bg-gray-100 shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all duration-300">
                Mua Ngay
              </Button>
            </div>
            <div className="grid grid-cols-3 gap-6 mt-12 pt-8 border-t border-white/20">
              <div>
                <div className="text-3xl font-bold">50K+</div>
                <div className="text-sm text-gray-200">Khách Hàng</div>
              </div>
              <div>
                <div className="text-3xl font-bold">100K+</div>
                <div className="text-sm text-gray-200">Sản Phẩm Đã Bán</div>
              </div>
              <div>
                <div className="text-3xl font-bold">4.9★</div>
                <div className="text-sm text-gray-200">Đánh Giá</div>
              </div>
            </div>
          </div>
          <div className="hidden md:block">
            <div className="relative">
              <img src="https://images.unsplash.com/photo-1604297643300-5362c8d679f0?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTM5fHxtYWMlMjBib29rfGVufDB8fDB8fHww&auto=format&fit=crop&q=60&w=600" alt="Latest iPhone Pro" className="rounded-lg shadow-2xl transform rotate-2 hover:rotate-0 transition-transform duration-500" />
              <img src="https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80" alt="MacBook Pro" className="absolute -bottom-16 -left-16 w-64 rounded-lg shadow-2xl transform -rotate-6 hover:rotate-0 transition-transform duration-500" />
            </div>
          </div>
        </div>
      </div>
      <div className="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-white dark:from-gray-900 to-transparent"></div>
    </section>;
};