import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { CheckCircleIcon, TruckIcon, PackageIcon, MapPinIcon, AlertCircleIcon, RefreshCwIcon } from 'lucide-react';

// Interface cho dữ liệu sản phẩm trong đơn hàng
interface OrderItem {
  product: string;
  quantity: number;
  price: number;
}

// Interface cho dữ liệu đơn hàng từ API
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

export const OrderDetail = () => {
  const { orderId } = useParams<{ orderId: string }>();
  const [order, setOrder] = useState<Order | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Hàm lấy thông tin đơn hàng từ API
  const fetchOrder = async () => {
    if (!orderId) {
      setError('ID đơn hàng không hợp lệ');
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/order/${orderId}/`, {
        credentials: 'include', // <-- THÊM DÒNG NÀY
      });
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Không tìm thấy đơn hàng');
        }
        throw new Error(`Lỗi ${response.status}: ${response.statusText}`);
      }
      
      const data: Order = await response.json();
      setOrder(data);
    } catch (err) {
      console.error('Error fetching order:', err);
      setError((err as Error).message || 'Không thể tải thông tin đơn hàng');
    } finally {
      setLoading(false);
    }
  };

  // Tải lại thông tin đơn hàng
  const handleRefresh = () => {
    fetchOrder();
  };

  // Tải thông tin đơn hàng khi component được mount
  useEffect(() => {
    fetchOrder();
  }, [orderId]);

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

  // Hiển thị trạng thái tải
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-12 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Đang tải thông tin đơn hàng...</p>
        </div>
      </div>
    );
  }

  // Hiển thị trạng thái lỗi
  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-12 flex items-center justify-center">
        <div className="text-center">
          <AlertCircleIcon className="mx-auto h-24 w-24 text-red-400 mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            Lỗi
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mb-8">{error}</p>
          <button
            onClick={handleRefresh}
            className="inline-flex items-center gap-2 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
          >
            <RefreshCwIcon className="w-5 h-5" />
            Thử lại
          </button>
        </div>
      </div>
    );
  }

  // Hiển thị trạng thái không tìm thấy đơn hàng
  if (!order) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-12 flex items-center justify-center">
        <div className="text-center">
          <PackageIcon className="mx-auto h-24 w-24 text-gray-400 mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            Không tìm thấy đơn hàng
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mb-8">
            Đơn hàng bạn tìm kiếm không tồn tại hoặc đã bị xóa.
          </p>
          <Link to="/orders" className="inline-block px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
            Xem tất cả đơn hàng
          </Link>
        </div>
      </div>
    );
  }

  // Tính toán giá tạm tính và thuế
  const subtotal = order.total_price / 1.1;
  const tax = order.total_price - subtotal;

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-12">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        {/* Success Message */}
        <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-6 mb-8">
          <div className="flex items-center">
            <CheckCircleIcon className="w-8 h-8 text-green-600 dark:text-green-400 mr-4" />
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                Thông tin đơn hàng
              </h2>
              <p className="text-gray-600 dark:text-gray-400">
                Cảm ơn bạn đã mua hàng. Đơn hàng của bạn đã được nhận và đang được xử lý.
              </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Order Details */}
          <div className="lg:col-span-2 space-y-6">
            {/* Order Info */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
                Chi Tiết Đơn Hàng
              </h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Mã Đơn Hàng
                  </p>
                  <p className="font-medium text-gray-900 dark:text-white">
                    #{order.id}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Ngày Đặt Hàng
                  </p>
                  <p className="font-medium text-gray-900 dark:text-white">
                    {new Date(order.created_at).toLocaleDateString('vi-VN')}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Trạng Thái
                  </p>
                  <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getStatusClass(order.status)}`}>
                    {order.status}
                  </span>
                </div>
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Khách Hàng
                  </p>
                  <p className="font-medium text-gray-900 dark:text-white">
                    {order.customer}
                  </p>
                </div>
              </div>
            </div>

            {/* Order Items */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
                Sản Phẩm Đã Đặt
              </h3>
              <div className="space-y-4">
                {order.items.map((item, index) => (
                  <div key={index} className="flex gap-4">
                    <div className="w-20 h-20 bg-gray-200 dark:bg-gray-700 rounded flex items-center justify-center">
                      <PackageIcon className="w-8 h-8 text-gray-400 dark:text-gray-500" />
                    </div>
                    <div className="flex-grow">
                      <h4 className="font-medium text-gray-900 dark:text-white">
                        {item.product}
                      </h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        Số lượng: {item.quantity}
                      </p>
                      <p className="font-medium text-gray-900 dark:text-white">
                        ${item.price.toFixed(2)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Shipping Address */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center">
                <MapPinIcon className="w-5 h-5 mr-2" />
                Địa Chỉ Giao Hàng
              </h3>
              <div className="text-gray-600 dark:text-gray-400">
                <p>{order.shipping_address}</p>
                <p>
                  {order.city}, {order.province}, {order.postal_code}
                </p>
                <p>Điện thoại: {order.phone}</p>
              </div>
            </div>
          </div>

          {/* Order Summary */}
          <div className="lg:col-span-1">
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 sticky top-24">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-6">
                Tóm Tắt Đơn Hàng
              </h3>
              <div className="space-y-4 mb-6">
                <div className="flex justify-between text-gray-600 dark:text-gray-400">
                  <span>Tạm tính</span>
                  <span>${subtotal.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-gray-600 dark:text-gray-400">
                  <span>Phí vận chuyển</span>
                  <span>Miễn phí</span>
                </div>
                <div className="flex justify-between text-gray-600 dark:text-gray-400">
                  <span>Thuế</span>
                  <span>${tax.toFixed(2)}</span>
                </div>
                <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
                  <div className="flex justify-between text-xl font-bold text-gray-900 dark:text-white">
                    <span>Tổng cộng</span>
                    <span>${order.total_price.toFixed(2)}</span>
                  </div>
                </div>
              </div>
              <Button as={Link} to="/shop" className="w-full mb-4">
                Tiếp Tục Mua Sắm
              </Button>
              <Button as={Link} to="/orders" variant="outline" className="w-full">
                Xem Tất Cả Đơn Hàng
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};