import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { PackageIcon, ChevronRightIcon, AlertCircleIcon, RefreshCwIcon } from 'lucide-react';

// Interface cho Order từ API
interface OrderItem {
  product: string;
  quantity: number;
  price: number;
}

interface Order {
  id: string;
  customer: string;
  items: OrderItem[];
  total_price: number;
  status: string;
  shipping_address: string;
  city: string;
  province: string;
  postal_code: string;
  phone: string;
  created_at: string;
  updated_at: string;
}

export const Orders = () => {
  const { user, fetchUserOrders } = useAuth();
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  // Hàm lấy danh sách đơn hàng
  const loadOrders = async () => {
    if (!user) {
      setLoading(false);
      return;
    }

    try {
      const userOrders = await fetchUserOrders();
      setOrders(userOrders);
      setError(null); // Xóa lỗi cũ nếu có
    } catch (err) {
      console.error('Error loading orders:', err);
      setError('Không thể tải danh sách đơn hàng');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  // Tải lại danh sách đơn hàng
  const handleRefresh = async () => {
    setRefreshing(true);
    await loadOrders();
  };

  useEffect(() => {
    loadOrders();
  }, [user, fetchUserOrders]);

  // Hàm xác định màu sắc cho trạng thái đơn hàng
  const getStatusClass = (status: string) => {
    switch (status) {
      case 'Đã Giao':
        return 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200';
      case 'Đang Vận Chuyển':
        return 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200';
      case 'Đang Xử Lý':
        return 'bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200';
      default:
        return 'bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-200';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-white dark:bg-gray-900 py-12 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Đang tải đơn hàng...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-white dark:bg-gray-900 py-12 flex items-center justify-center">
        <div className="text-center">
          <AlertCircleIcon className="mx-auto h-24 w-24 text-red-400 mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            Lỗi tải dữ liệu
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mb-8">{error}</p>
          <button
            onClick={handleRefresh}
            disabled={refreshing}
            className="inline-flex items-center gap-2 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <RefreshCwIcon className={`w-5 h-5 ${refreshing ? 'animate-spin' : ''}`} />
            {refreshing ? 'Đang tải lại...' : 'Thử lại'}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 py-12">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Đơn Hàng Của Tôi
          </h1>
          {orders.length > 0 && (
            <button
              onClick={handleRefresh}
              disabled={refreshing}
              className="inline-flex items-center gap-2 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 disabled:opacity-50"
            >
              <RefreshCwIcon className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
              {refreshing ? 'Đang tải...' : 'Tải lại'}
            </button>
          )}
        </div>

        {orders.length === 0 ? (
          <div className="text-center py-16">
            <PackageIcon className="mx-auto h-24 w-24 text-gray-400 dark:text-gray-600 mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Chưa có đơn hàng
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mb-8">
              Bắt đầu mua sắm để xem đơn hàng tại đây
            </p>
            <Link
              to="/shop"
              className="inline-block px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Bắt Đầu Mua Sắm
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {orders.map((order) => (
              <Link
                key={order.id}
                to={`/orders/${order.id}`}
                className="block bg-gray-50 dark:bg-gray-800 rounded-lg p-6 hover:shadow-lg transition-all duration-200 hover:scale-[1.02] border border-transparent hover:border-indigo-200 dark:hover:border-indigo-800"
              >
                <div className="flex items-center justify-between">
                  <div className="flex-grow">
                    <div className="flex items-center gap-4 mb-2">
                      <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                        Đơn hàng #{order.id}
                      </h3>
                      <span
                        className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusClass(
                          order.status
                        )}`}
                      >
                        {order.status}
                      </span>
                    </div>
                    <div className="flex gap-6 text-sm text-gray-600 dark:text-gray-400">
                      <span>Ngày: {new Date(order.created_at).toLocaleDateString('vi-VN')}</span>
                      <span>{order.items.length} sản phẩm</span>
                      <span className="font-medium text-gray-900 dark:text-white">
                        ${order.total_price.toFixed(2)}
                      </span>
                    </div>
                    {/* Hiển thị địa chỉ giao hàng */}
                    <div className="mt-2 text-sm text-gray-500 dark:text-gray-500">
                      <span className="font-medium">Giao đến:</span> {order.shipping_address}, {order.city}, {order.province}
                    </div>
                  </div>
                  <ChevronRightIcon className="w-6 h-6 text-gray-400" />
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
