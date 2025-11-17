import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../contexts/CartContext';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '../components/ui/Button';
import { LockIcon, CheckCircleIcon, QrCodeIcon, DollarSignIcon, SmartphoneIcon, AlertCircleIcon, CopyIcon } from 'lucide-react';

export const Checkout = () => {
  const {
    cartItems,
    cartTotal,
    clearCart
  } = useCart();
  const {
    isAuthenticated,
    user,
    isLoading: authLoading
  } = useAuth();
  const navigate = useNavigate();
  const [isProcessing, setIsProcessing] = useState(false);
  const [step, setStep] = useState(1);
  const [notification, setNotification] = useState<{
    type: 'success' | 'error';
    message: string;
    show: boolean;
  }>({ type: 'success', message: '', show: false });
  
  const [shippingInfo, setShippingInfo] = useState({
    fullName: '',
    email: '',
    address: '',
    city: '',
    state: '',
    zipCode: '',
    phone: ''
  });
  
  const [paymentInfo, setPaymentInfo] = useState({
    method: 'cod',
    momoPhone: '',
    qrCode: '' // Không cần thiết nữa nhưng giữ lại để tương thích
  });

  // Thông tin tài khoản ngân hàng của bạn
  const bankInfo = {
    accountName: "VO LE HOANG PHUC", // Tên chủ tài khoản
    accountNumber: "104879691506", // Số tài khoản
    bankName: "Vietinbank", // Tên ngân hàng
    branch: "HCM", // Chi nhánh
    qrCodeImage: "https://res.cloudinary.com/dze6buir3/image/upload/v1763204147/x2nrgf58xndhcfjpxj9w.jpg" // Đường dẫn đến hình ảnh QR code của bạn
  };

  // useEffect được đơn giản hóa, chỉ còn nhiệm vụ điền form
  useEffect(() => {
    if (isAuthenticated && user) {
      console.log('User data in Checkout:', user);
      setShippingInfo({
        fullName: user.name || user.first_name || '',
        email: user.email || '',
        address: user.address || '',
        city: user.city || '',
        state: user.state || user.province || '',
        zipCode: user.zipCode || user.postal_code || '',
        phone: user.phone || ''
      });
    }
  }, [isAuthenticated, user]);

  // Hàm hiển thị thông báo
  const showNotification = (type: 'success' | 'error', message: string) => {
    setNotification({ type, message, show: true });
    setTimeout(() => {
      setNotification(prev => ({ ...prev, show: false }));
    }, 3000);
  };

  // Hàm sao chép thông tin tài khoản
  const copyBankInfo = () => {
    const info = `STK: ${bankInfo.accountName}\nSố tài khoản: ${bankInfo.accountNumber}\nNgân hàng: ${bankInfo.bankName}\nChi nhánh: ${bankInfo.branch}\nSố tiền: $${total.toFixed(2)}`;
    
    navigator.clipboard.writeText(info).then(() => {
      showNotification('success', 'Đã sao chép thông tin tài khoản');
    }).catch(err => {
      console.error('Failed to copy:', err);
      showNotification('error', 'Không thể sao chép thông tin');
    });
  };

  const handleShippingSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setStep(2);
  };

  // CẬP NHẬT: Hàm xử lý thanh toán với API mới
    // CẬP NHẬT: Hàm xử lý thanh toán đã tối ưu
  const handlePaymentSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsProcessing(true);
    
    try {
      const orderData = {
        customer: user?._id || user?.id,
        items: cartItems.map(item => ({
          product: item.id,
          quantity: item.quantity,
          price: item.price
        })),
        shipping_address: shippingInfo.address,
        city: shippingInfo.city,
        province: shippingInfo.state,
        postal_code: shippingInfo.zipCode,
        phone: shippingInfo.phone
      };
      
      const response = await fetch(`${import.meta.env.VITE_API_URL}/order/create/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(orderData)
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || JSON.stringify(errorData));
      }
      
      const result = await response.json();
      const order = result.order; // API trả về object order trực tiếp
      
      // QUAN TRỌNG: Xóa giỏ hàng ngay sau khi đơn hàng được tạo thành công
      // Điều này ngăn người dùng tạo lại đơn hàng
      clearCart(); 

      // Xử lý theo từng phương thức thanh toán
      if (paymentInfo.method === 'momo') {
        // Mô phỏng thanh toán MoMo
        showNotification('success', 'Đang chuyển đến cổng thanh toán MoMo...');
        setTimeout(() => {
          // Trong thực tế, bạn sẽ chuyển đến URL thanh toán MoMo thực tế
          // Hiện tại, chúng ta sẽ chuyển đến trang chi tiết đơn hàng
          navigate(`/orders/${order.id}`);
        }, 2000);

      } else if (paymentInfo.method === 'qr') {
        // Thanh toán chuyển khoản
        showNotification('success', 'Đơn hàng đã tạo. Vui lòng xem thông tin chuyển khoản ở trang chi tiết đơn hàng.');
        // Chuyển ngay đến trang chi tiết để xem thông tin chuyển khoản
        navigate(`/orders/${order.id}`);

      } else {
        // Thanh toán khi nhận hàng (COD)
        showNotification('success', 'Đặt hàng thành công!');
        setTimeout(() => {
          navigate(`/orders/${order.id}`);
        }, 1500);
      }
    } catch (error) {
      console.error('Payment error:', error);
      
      // Xử lý lỗi một cách an toàn
      let errorMessage = 'Đã xảy ra lỗi không xác định.';
      if (error instanceof Error) {
        errorMessage = error.message;
      }
      
      showNotification('error', `Đã xảy ra lỗi: ${errorMessage}`);
      } finally {
        setIsProcessing(false);
    }
  };

  if (authLoading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-12 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Đang tải thông tin...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated || cartItems.length === 0) {
    navigate('/cart');
    return null;
  }

  const tax = cartTotal * 0.1;
  const total = cartTotal + tax;

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-12">
      {/* Notification */}
      {notification.show && (
        <div className={`fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg flex items-center gap-2 ${
          notification.type === 'success' 
            ? 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400' 
            : 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400'
        }`}>
          {notification.type === 'success' ? (
            <CheckCircleIcon className="w-5 h-5" />
          ) : (
            <AlertCircleIcon className="w-5 h-5" />
          )}
          <span>{notification.message}</span>
        </div>
      )}

      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
          Thanh Toán
        </h1>
        
        {/* Progress Steps */}
        <div className="mb-8">
          <div className="flex items-center justify-center">
            <div className="flex items-center">
              <div className={`flex items-center justify-center w-10 h-10 rounded-full ${step >= 1 ? 'bg-indigo-600 text-white' : 'bg-gray-300 dark:bg-gray-700 text-gray-600 dark:text-gray-400'}`}>
                {step > 1 ? <CheckCircleIcon className="w-6 h-6" /> : '1'}
              </div>
              <div className={`w-20 h-1 ${step >= 2 ? 'bg-indigo-600' : 'bg-gray-300 dark:bg-gray-700'}`} />
              <div className={`flex items-center justify-center w-10 h-10 rounded-full ${step >= 2 ? 'bg-indigo-600 text-white' : 'bg-gray-300 dark:bg-gray-700 text-gray-600 dark:text-gray-400'}`}>
                2
              </div>
            </div>
          </div>
          <div className="flex justify-center mt-2 gap-24">
            <span className="text-sm text-gray-600 dark:text-gray-400">
              Giao Hàng
            </span>
            <span className="text-sm text-gray-600 dark:text-gray-400">
              Thanh Toán
            </span>
          </div>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2">
            {step === 1 ? (
              <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6">
                  Thông Tin Giao Hàng
                </h2>
                <form onSubmit={handleShippingSubmit}>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Họ và Tên
                      </label>
                      <input 
                        type="text" 
                        required 
                        value={shippingInfo.fullName} 
                        onChange={e => setShippingInfo({
                          ...shippingInfo,
                          fullName: e.target.value
                        })} 
                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white" 
                      />
                    </div>
                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Email
                      </label>
                      <input 
                        type="email" 
                        required 
                        value={shippingInfo.email} 
                        onChange={e => setShippingInfo({
                          ...shippingInfo,
                          email: e.target.value
                        })} 
                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white" 
                      />
                    </div>
                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Địa Chỉ
                      </label>
                      <input 
                        type="text" 
                        required 
                        value={shippingInfo.address} 
                        onChange={e => setShippingInfo({
                          ...shippingInfo,
                          address: e.target.value
                        })} 
                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white" 
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Thành Phố
                      </label>
                      <input 
                        type="text" 
                        required 
                        value={shippingInfo.city} 
                        onChange={e => setShippingInfo({
                          ...shippingInfo,
                          city: e.target.value
                        })} 
                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white" 
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Tỉnh/Thành
                      </label>
                      <input 
                        type="text" 
                        required 
                        value={shippingInfo.state} 
                        onChange={e => setShippingInfo({
                          ...shippingInfo,
                          state: e.target.value
                        })} 
                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white" 
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Mã Bưu Điện
                      </label>
                      <input 
                        type="text" 
                        required 
                        value={shippingInfo.zipCode} 
                        onChange={e => setShippingInfo({
                          ...shippingInfo,
                          zipCode: e.target.value
                        })} 
                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white" 
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Số Điện Thoại
                      </label>
                      <input 
                        type="tel" 
                        required 
                        value={shippingInfo.phone} 
                        onChange={e => setShippingInfo({
                          ...shippingInfo,
                          phone: e.target.value
                        })} 
                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white" 
                      />
                    </div>
                  </div>
                  <Button type="submit" className="w-full mt-6">
                    Tiếp Tục Thanh Toán
                  </Button>
                </form>
              </div>
            ) : (
              <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
                  <LockIcon className="w-5 h-5 mr-2 text-green-600" />
                  Phương Thức Thanh Toán
                </h2>
                <form onSubmit={handlePaymentSubmit}>
                  <div className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      {/* Thanh toán khi nhận hàng */}
                      <div 
                        className={`border rounded-lg p-4 cursor-pointer transition-colors ${
                          paymentInfo.method === 'cod' 
                            ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/20' 
                            : 'border-gray-300 dark:border-gray-600 hover:border-gray-400'
                        }`}
                        onClick={() => setPaymentInfo({ ...paymentInfo, method: 'cod' })}
                      >
                        <div className="flex flex-col items-center">
                          <DollarSignIcon className="w-8 h-8 text-indigo-600 mb-2" />
                          <h3 className="font-medium text-gray-900 dark:text-white">Tiền Mặt</h3>
                          <p className="text-sm text-gray-600 dark:text-gray-400 text-center mt-1">
                            Thanh toán khi nhận hàng
                          </p>
                        </div>
                        {paymentInfo.method === 'cod' && (
                          <div className="mt-2 flex justify-center">
                            <CheckCircleIcon className="w-5 h-5 text-indigo-600" />
                          </div>
                        )}
                      </div>

                      {/* Thanh toán qua Momo */}
                      <div 
                        className={`border rounded-lg p-4 cursor-pointer transition-colors ${
                          paymentInfo.method === 'momo' 
                            ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/20' 
                            : 'border-gray-300 dark:border-gray-600 hover:border-gray-400'
                        }`}
                        onClick={() => setPaymentInfo({ ...paymentInfo, method: 'momo' })}
                      >
                        <div className="flex flex-col items-center">
                          <SmartphoneIcon className="w-8 h-8 text-indigo-600 mb-2" />
                          <h3 className="font-medium text-gray-900 dark:text-white">Ví MoMo</h3>
                          <p className="text-sm text-gray-600 dark:text-gray-400 text-center mt-1">
                            Thanh toán qua ví điện tử
                          </p>
                        </div>
                        {paymentInfo.method === 'momo' && (
                          <div className="mt-2 flex justify-center">
                            <CheckCircleIcon className="w-5 h-5 text-indigo-600" />
                          </div>
                        )}
                      </div>

                      {/* Thanh toán qua QR Code */}
                      <div 
                        className={`border rounded-lg p-4 cursor-pointer transition-colors ${
                          paymentInfo.method === 'qr' 
                            ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/20' 
                            : 'border-gray-300 dark:border-gray-600 hover:border-gray-400'
                        }`}
                        onClick={() => setPaymentInfo({ ...paymentInfo, method: 'qr' })}
                      >
                        <div className="flex flex-col items-center">
                          <QrCodeIcon className="w-8 h-8 text-indigo-600 mb-2" />
                          <h3 className="font-medium text-gray-900 dark:text-white">Chuyển Khoản</h3>
                          <p className="text-sm text-gray-600 dark:text-gray-400 text-center mt-1">
                            Quét mã để thanh toán
                          </p>
                        </div>
                        {paymentInfo.method === 'qr' && (
                          <div className="mt-2 flex justify-center">
                            <CheckCircleIcon className="w-5 h-5 text-indigo-600" />
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Hiển thị thông tin bổ sung theo từng phương thức */}
                    {paymentInfo.method === 'momo' && (
                      <div className="mt-4 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                          Số điện thoại MoMo
                        </label>
                        <input 
                          type="tel" 
                          placeholder="Nhập số điện thoại đã đăng ký MoMo" 
                          value={paymentInfo.momoPhone} 
                          onChange={e => setPaymentInfo({
                            ...paymentInfo,
                            momoPhone: e.target.value
                          })} 
                          className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white" 
                        />
                      </div>
                    )}

                    {paymentInfo.method === 'qr' && (
                      <div className="mt-4 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                        <div className="text-center">
                          <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">
                            Quét mã QR để thanh toán
                          </p>
                          
                          {/* Hình ảnh QR Code cố định của bạn */}
                          <img 
                            src={bankInfo.qrCodeImage} 
                            alt="Bank QR Code" 
                            className="mx-auto w-48 h-48 object-contain mb-4 border-2 border-gray-200 rounded-lg"
                          />
                          
                          {/* Thông tin tài khoản ngân hàng */}
                          <div className="bg-white dark:bg-gray-800 rounded-lg p-4 mb-4">
                            <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
                              Thông tin chuyển khoản
                            </h4>
                            <div className="text-left space-y-1 text-sm text-gray-600 dark:text-gray-400">
                              <p><span className="font-medium">Ngân hàng:</span> {bankInfo.bankName}</p>
                              <p><span className="font-medium">Chủ tài khoản:</span> {bankInfo.accountName}</p>
                              <p><span className="font-medium">Số tài khoản:</span> {bankInfo.accountNumber}</p>
                              <p><span className="font-medium">Chi nhánh:</span> {bankInfo.branch}</p>
                              <p><span className="font-medium">Số tiền:</span> <span className="text-lg font-bold text-indigo-600 dark:text-indigo-400">${total.toFixed(2)}</span></p>
                            </div>
                          </div>
                          
                          {/* Nút sao chép thông tin */}
                          <button
                            type="button"
                            onClick={copyBankInfo}
                            className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-lg transition-colors"
                          >
                            <CopyIcon className="w-4 h-4" />
                            Sao chép thông tin
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                  <div className="flex gap-4 mt-6">
                    <Button type="button" variant="outline" onClick={() => setStep(1)} className="flex-1">
                      Quay Lại
                    </Button>
                    <Button type="submit" disabled={isProcessing} className="flex-1">
                      {isProcessing ? 'Đang Xử Lý...' : 'Đặt Hàng'}
                    </Button>
                  </div>
                </form>
              </div>
            )}
          </div>
          
          {/* Order Summary */}
          <div className="lg:col-span-1">
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 sticky top-24">
              <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6">
                Tóm Tắt Đơn Hàng
              </h2>
              <div className="space-y-4 mb-6">
                {cartItems.map(item => (
                  <div key={item.id} className="flex gap-4">
                    <img src={item.image} alt={item.name} className="w-16 h-16 object-cover rounded" />
                    <div className="flex-grow">
                      <h3 className="text-sm font-medium text-gray-900 dark:text-white">
                        {item.name}
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        SL: {item.quantity}
                      </p>
                      <p className="text-sm font-medium text-gray-900 dark:text-white">
                        ${(item.price * item.quantity).toFixed(2)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
              <div className="border-t border-gray-200 dark:border-gray-700 pt-4 space-y-2">
                <div className="flex justify-between text-gray-600 dark:text-gray-400">
                  <span>Tạm Tính</span>
                  <span>${cartTotal.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-gray-600 dark:text-gray-400">
                  <span>Phí Vận Chuyển</span>
                  <span>Miễn Phí</span>
                </div>
                <div className="flex justify-between text-gray-600 dark:text-gray-400">
                  <span>Thuế</span>
                  <span>${tax.toFixed(2)}</span>
                </div>
                <div className="border-t border-gray-200 dark:border-gray-700 pt-2">
                  <div className="flex justify-between text-xl font-bold text-gray-900 dark:text-white">
                    <span>Tổng Cộng</span>
                    <span>${total.toFixed(2)}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
