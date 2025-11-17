import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import {
  AlertCircleIcon,
  UserIcon,
  MailIcon,
  LockIcon,
  PhoneIcon,
} from 'lucide-react';

export const Register = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirm_password: '',
    first_name: '',
    last_name: '',
    phone: '',
    address: '',
    city: '',
    province: '',
    postal_code: '',
  });

  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (formData.password !== formData.confirm_password) {
      setError('Mật khẩu xác nhận không khớp!');
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/customer/register/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
          first_name: formData.first_name,
          last_name: formData.last_name,
          phone: formData.phone,
          address: formData.address,
          city: formData.city,
          province: formData.province,
          postal_code: formData.postal_code,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Đăng ký thất bại. Vui lòng thử lại!');
      }

      // ✅ Thành công
      setSuccess('Đăng ký thành công! Đang chuyển hướng...');
      console.log('✅ User ID:', data.id);

      // Chuyển hướng sau 2 giây
      setTimeout(() => navigate('/login'), 2000);
    } catch (err: any) {
      setError(err.message || 'Đăng ký thất bại!');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-bold text-gray-900 dark:text-white">
            Tạo tài khoản mới
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600 dark:text-gray-400">
            Đã có tài khoản?{' '}
            <Link
              to="/login"
              className="font-medium text-indigo-600 hover:text-indigo-500 dark:text-indigo-400"
            >
              Đăng nhập
            </Link>
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="rounded-md bg-red-50 dark:bg-red-900/20 p-4">
              <div className="flex">
                <AlertCircleIcon className="h-5 w-5 text-red-400" />
                <div className="ml-3">
                  <p className="text-sm text-red-800 dark:text-red-200">{error}</p>
                </div>
              </div>
            </div>
          )}

          {success && (
            <div className="rounded-md bg-green-50 dark:bg-green-900/20 p-4">
              <p className="text-sm text-green-800 dark:text-green-200">{success}</p>
            </div>
          )}

          <div className="rounded-md shadow-sm space-y-4">
            {/* Họ và Tên */}
            <div>
              <label
                htmlFor="first_name"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
              >
                Họ
              </label>
              <div className="relative">
                <UserIcon className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
                <input
                  id="first_name"
                  name="first_name"
                  type="text"
                  required
                  value={formData.first_name}
                  onChange={handleChange}
                  className="pl-10 w-full border rounded-md p-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                />
              </div>
            </div>

            <div>
              <label
                htmlFor="last_name"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
              >
                Tên
              </label>
              <div className="relative">
                <UserIcon className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
                <input
                  id="last_name"
                  name="last_name"
                  type="text"
                  required
                  value={formData.last_name}
                  onChange={handleChange}
                  className="pl-10 w-full border rounded-md p-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                />
              </div>
            </div>

            {/* Email */}
            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
              >
                Email
              </label>
              <div className="relative">
                <MailIcon className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
                <input
                  id="email"
                  name="email"
                  type="email"
                  required
                  value={formData.email}
                  onChange={handleChange}
                  className="pl-10 w-full border rounded-md p-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                />
              </div>
            </div>

            {/* Mật khẩu */}
            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
              >
                Mật khẩu
              </label>
              <div className="relative">
                <LockIcon className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
                <input
                  id="password"
                  name="password"
                  type="password"
                  required
                  value={formData.password}
                  onChange={handleChange}
                  className="pl-10 w-full border rounded-md p-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                />
              </div>
            </div>

            {/* Xác nhận mật khẩu */}
            <div>
              <label
                htmlFor="confirm_password"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
              >
                Xác nhận mật khẩu
              </label>
              <div className="relative">
                <LockIcon className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
                <input
                  id="confirm_password"
                  name="confirm_password"
                  type="password"
                  required
                  value={formData.confirm_password}
                  onChange={handleChange}
                  className="pl-10 w-full border rounded-md p-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                />
              </div>
            </div>

            {/* Các thông tin khác */}
            <div>
              <label htmlFor="phone" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Số điện thoại
              </label>
              <div className="relative">
                <PhoneIcon className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
                <input
                  id="phone"
                  name="phone"
                  type="text"
                  required
                  value={formData.phone}
                  onChange={handleChange}
                  className="pl-10 w-full border rounded-md p-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                />
              </div>
            </div>

            <div>
              <label htmlFor="address" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Địa chỉ
              </label>
              <input
                id="address"
                name="address"
                type="text"
                required
                value={formData.address}
                onChange={handleChange}
                className="w-full border rounded-md p-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              />
            </div>

            <div>
              <label htmlFor="city" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Thành phố
              </label>
              <input
                id="city"
                name="city"
                type="text"
                required
                value={formData.city}
                onChange={handleChange}
                className="w-full border rounded-md p-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              />
            </div>

            <div>
              <label htmlFor="province" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Tỉnh/Thành
              </label>
              <input
                id="province"
                name="province"
                type="text"
                required
                value={formData.province}
                onChange={handleChange}
                className="w-full border rounded-md p-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              />
            </div>

            <div>
              <label htmlFor="postal_code" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Mã bưu điện
              </label>
              <input
                id="postal_code"
                name="postal_code"
                type="text"
                required
                value={formData.postal_code}
                onChange={handleChange}
                className="w-full border rounded-md p-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              />
            </div>
          </div>

          <div>
            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? 'Đang xử lý...' : 'Đăng ký'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};
