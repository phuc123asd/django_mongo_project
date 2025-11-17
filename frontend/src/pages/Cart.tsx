import React from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../contexts/CartContext';
// Import useAuth để kiểm tra trạng thái đăng nhập
import { useAuth } from '../contexts/AuthContext'; 
import { Button } from '../components/ui/Button';
import { TrashIcon, MinusIcon, PlusIcon, ShoppingBagIcon, LogInIcon } from 'lucide-react'; // Thêm LogInIcon

export const Cart = () => {
  const {
    cartItems,
    removeFromCart,
    updateQuantity,
    cartTotal
  } = useCart();

  // Lấy trạng thái xác thực từ AuthContext
  const { isAuthenticated } = useAuth();

  if (cartItems.length === 0) {
    return <div className="min-h-screen bg-white dark:bg-gray-900 py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center py-16">
            <ShoppingBagIcon className="mx-auto h-24 w-24 text-gray-400 dark:text-gray-600 mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Giỏ hàng của bạn đang trống
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mb-8">
              Thêm sản phẩm để bắt đầu!
            </p>
            <Button as={Link} to="/shop">
              Tiếp tục mua sắm
            </Button>
          </div>
        </div>
      </div>;
  }

  return <div className="min-h-screen bg-white dark:bg-gray-900 py-12">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
          Giỏ hàng
        </h1>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Cart Items */}
          <div className="lg:col-span-2">
            <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-6">
              {cartItems.map(item => <div key={item.id} className="flex flex-col sm:flex-row gap-4 py-6 border-b border-gray-200 dark:border-gray-700 last:border-b-0">
                  <img src={item.image} alt={item.name} className="w-full sm:w-32 h-32 object-cover rounded-lg" />
                  <div className="flex-grow">
                    <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                      {item.name}
                    </h3>
                    {item.variant && <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                        Phiên bản: {item.variant}
                      </p>}
                    <p className="text-xl font-bold text-indigo-600 dark:text-indigo-400">
                      ${item.price.toFixed(2)}
                    </p>
                  </div>
                  <div className="flex sm:flex-col items-center sm:items-end justify-between sm:justify-start gap-4">
                    <div className="flex items-center border border-gray-300 dark:border-gray-600 rounded-lg">
                      <button onClick={() => updateQuantity(item.id, item.quantity - 1)} className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-l-lg">
                        <MinusIcon className="w-4 h-4 text-gray-600 dark:text-gray-400" />
                      </button>
                      <span className="px-4 py-2 text-gray-900 dark:text-white">
                        {item.quantity}
                      </span>
                      <button onClick={() => updateQuantity(item.id, item.quantity + 1)} className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-r-lg">
                        <PlusIcon className="w-4 h-4 text-gray-600 dark:text-gray-400" />
                      </button>
                    </div>
                    <button onClick={() => removeFromCart(item.id)} className="text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300">
                      <TrashIcon className="w-5 h-5" />
                    </button>
                  </div>
                </div>)}
            </div>
          </div>
          {/* Order Summary */}
          <div className="lg:col-span-1">
            <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-6 sticky top-24">
              <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6">
                Tóm tắt đơn hàng
              </h2>
              <div className="space-y-4 mb-6">
                <div className="flex justify-between text-gray-600 dark:text-gray-400">
                  <span>Tạm tính</span>
                  <span>${cartTotal.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-gray-600 dark:text-gray-400">
                  <span>Phí vận chuyển</span>
                  <span>Miễn phí</span>
                </div>
                <div className="flex justify-between text-gray-600 dark:text-gray-400">
                  <span>Thuế</span>
                  <span>${(cartTotal * 0.1).toFixed(2)}</span>
                </div>
                <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
                  <div className="flex justify-between text-xl font-bold text-gray-900 dark:text-white">
                    <span>Tổng cộng</span>
                    <span>${(cartTotal * 1.1).toFixed(2)}</span>
                  </div>
                </div>
              </div>

              {/* --- PHẦN THÊM VÀO ĐỂ KIỂM TRA ĐĂNG NHẬP --- */}
              {isAuthenticated ? (
                <Button as={Link} to="/checkout" className="w-full mb-4">
                  Tiến hành thanh toán
                </Button>
              ) : (
                <div className="mb-4 p-4 bg-yellow-100 dark:bg-yellow-900/30 border border-yellow-300 dark:border-yellow-600 rounded-lg text-center">
                  <p className="text-sm font-medium text-yellow-800 dark:text-yellow-200 mb-2">
                    Bạn cần đăng nhập để thanh toán.
                  </p>
                  <Button as={Link} to="/login" variant="outline" className="w-full">
                    <LogInIcon className="w-4 h-4 mr-2" />
                    Đăng nhập / Đăng ký
                  </Button>
                </div>
              )}

              <Button as={Link} to="/shop" variant="outline" className="w-full">
                Tiếp tục mua sắm
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>;
};