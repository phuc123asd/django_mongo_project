import React from 'react';
import { Link } from 'react-router-dom';
import { FacebookIcon, TwitterIcon, InstagramIcon, YoutubeIcon, MapPinIcon, PhoneIcon, MailIcon } from 'lucide-react';
export const Footer = () => {
  return <footer className="bg-gray-100 dark:bg-gray-900 pt-12 pb-8">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        {/* Newsletter */}
        <div className="mb-12 p-6 bg-indigo-600 dark:bg-indigo-700 rounded-xl shadow-lg">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div className="mb-6 md:mb-0">
              <h3 className="text-xl font-bold text-white mb-2">
                Đăng ký nhận tin
              </h3>
              <p className="text-indigo-100">
                Nhận tin tức mới nhất và ưu đãi độc quyền
              </p>
            </div>
            <div className="flex w-full md:w-auto">
              <input type="email" placeholder="Email của bạn" className="flex-grow px-4 py-3 rounded-l-lg focus:outline-none" aria-label="Email address" />
              <button className="px-6 py-3 bg-gray-900 hover:bg-black text-white font-medium rounded-r-lg transition-colors" aria-label="Subscribe">
                Đăng ký
              </button>
            </div>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-8">
          {/* Company Info */}
          <div>
            <h4 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
              TechHub
            </h4>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Điểm đến hàng đầu cho các sản phẩm công nghệ và phụ kiện cao cấp.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400">
                <FacebookIcon className="w-5 h-5" />
                <span className="sr-only">Facebook</span>
              </a>
              <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400">
                <TwitterIcon className="w-5 h-5" />
                <span className="sr-only">Twitter</span>
              </a>
              <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400">
                <InstagramIcon className="w-5 h-5" />
                <span className="sr-only">Instagram</span>
              </a>
              <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400">
                <YoutubeIcon className="w-5 h-5" />
                <span className="sr-only">YouTube</span>
              </a>
            </div>
          </div>
          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
              Liên kết nhanh
            </h4>
            <ul className="space-y-2">
              <li>
                <Link to="/shop" className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
                  Cửa hàng
                </Link>
              </li>
              <li>
                <Link to="/about" className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
                  Giới thiệu
                </Link>
              </li>
              <li>
                <Link to="/contact" className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
                  Liên hệ
                </Link>
              </li>
              <li>
                <Link to="/blog" className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
                  Blog
                </Link>
              </li>
              <li>
                <Link to="/faq" className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
                  Câu hỏi thường gặp
                </Link>
              </li>
            </ul>
          </div>
          {/* Customer Service */}
          <div>
            <h4 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
              Dịch vụ khách hàng
            </h4>
            <ul className="space-y-2">
              <li>
                <Link to="/shipping" className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
                  Chính sách giao hàng
                </Link>
              </li>
              <li>
                <Link to="/returns" className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
                  Đổi trả & Hoàn tiền
                </Link>
              </li>
              <li>
                <Link to="/warranty" className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
                  Bảo hành
                </Link>
              </li>
              <li>
                <Link to="/privacy" className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
                  Chính sách bảo mật
                </Link>
              </li>
              <li>
                <Link to="/terms" className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
                  Điều khoản dịch vụ
                </Link>
              </li>
            </ul>
          </div>
          {/* Contact Info */}
          <div>
            <h4 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
              Liên hệ với chúng tôi
            </h4>
            <ul className="space-y-3">
              <li className="flex items-start">
                <MapPinIcon className="w-5 h-5 text-indigo-600 dark:text-indigo-400 mr-2 mt-0.5" />
                <span className="text-gray-600 dark:text-gray-400">
                  123 Tech Street, San Francisco, CA 94107
                </span>
              </li>
              <li className="flex items-center">
                <PhoneIcon className="w-5 h-5 text-indigo-600 dark:text-indigo-400 mr-2" />
                <span className="text-gray-600 dark:text-gray-400">
                  +1 (555) 123-4567
                </span>
              </li>
              <li className="flex items-center">
                <MailIcon className="w-5 h-5 text-indigo-600 dark:text-indigo-400 mr-2" />
                <span className="text-gray-600 dark:text-gray-400">
                  support@techhub.com
                </span>
              </li>
            </ul>
          </div>
        </div>
        {/* Bottom Bar */}
        <div className="pt-8 border-t border-gray-200 dark:border-gray-800">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-600 dark:text-gray-400 text-sm mb-4 md:mb-0">
              © {new Date().getFullYear()} TechHub. Bản quyền đã được bảo hộ.
            </p>
            <div className="flex space-x-4">
              <img src="https://cdn-icons-png.flaticon.com/512/196/196578.png" alt="Visa" className="h-8 w-auto" />
              <img src="https://cdn-icons-png.flaticon.com/512/196/196561.png" alt="MasterCard" className="h-8 w-auto" />
              <img src="https://cdn-icons-png.flaticon.com/512/196/196565.png" alt="PayPal" className="h-8 w-auto" />
              <img src="https://cdn-icons-png.flaticon.com/512/196/196539.png" alt="Apple Pay" className="h-8 w-auto" />
            </div>
          </div>
        </div>
      </div>
    </footer>;
};