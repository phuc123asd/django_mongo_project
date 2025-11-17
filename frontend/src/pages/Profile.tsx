import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '../components/ui/Button';
import {
  UserIcon,
  MailIcon,
  ShieldCheckIcon,
  SaveIcon,
  CheckCircleIcon,
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const Profile = () => {
  const { user, isAuthenticated, logout, updateUser } = useAuth();
  const navigate = useNavigate();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    state: '',
    zipCode: '',
  });
  const [isSaving, setIsSaving] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const [errors, setErrors] = useState<{ [key: string]: string }>({});
  const [apiResponse, setApiResponse] = useState<any>(null);

  // Fetch customer info from API
  useEffect(() => {
    const fetchCustomer = async () => {
      const userId = user?.id || localStorage.getItem('customerId');
      if (!userId) return;

      try {
        const res = await fetch(
          `${import.meta.env.VITE_API_URL}/customer/get_customer/${userId}/`
        );
        if (!res.ok) throw new Error('Không lấy được thông tin khách hàng');
        const data = await res.json();
        setFormData({
          name: `${data.first_name} ${data.last_name}`,
          email: data.email,
          phone: data.phone || '',
          address: data.address || '',
          city: data.city || '',
          state: data.province || '',
          zipCode: data.postal_code || '',
        });
      } catch (err) {
        console.error(err);
      }
    };

    if (isAuthenticated) {
      fetchCustomer();
    } else {
      navigate('/login');
    }
  }, [user, isAuthenticated, navigate]);

  const validateForm = () => {
    const newErrors: { [key: string]: string } = {};

    if (!formData.name.trim()) newErrors.name = 'Tên là bắt buộc';
    if (!formData.email.trim()) newErrors.email = 'Email là bắt buộc';
    else if (!/\S+@\S+\.\S+/.test(formData.email))
      newErrors.email = 'Email không hợp lệ';
    if (formData.phone && !/^[\d\s\-+()]+$/.test(formData.phone))
      newErrors.phone = 'Số điện thoại không hợp lệ';
    if (formData.zipCode && !/^\d{5,6}$/.test(formData.zipCode))
      newErrors.zipCode = 'Mã bưu điện phải là 5-6 chữ số';

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    setIsSaving(true);

    const userId = user?.id || localStorage.getItem('customerId');
    if (!userId) return;

    const [first_name, ...last_name_parts] = formData.name.split(' ');
    const last_name = last_name_parts.join(' ');

    const payload = {
      first_name,
      last_name,
      phone: formData.phone,
      address: formData.address,
      city: formData.city,
      province: formData.state,
      postal_code: formData.zipCode,
    };

    try {
      const res = await fetch(
        `${import.meta.env.VITE_API_URL}/customer/up_date/${userId}/`,
        {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
          credentials: 'include',
        }
      );
      if (!res.ok) throw new Error('Cập nhật thất bại');
      const updatedData = await res.json();
      
      // Store the API response for display
      setApiResponse(updatedData);

      updateUser({
        name: `${updatedData.customer.first_name} ${updatedData.customer.last_name}`,
        email: updatedData.customer.email,
        phone: updatedData.customer.phone,
        address: updatedData.customer.address,
        city: updatedData.customer.city,
        state: updatedData.customer.province,
        zipCode: updatedData.customer.postal_code,
      });

      setIsSaving(false);
      setIsEditing(false);
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);
    } catch (err) {
      console.error(err);
      setIsSaving(false);
    }
  };

  const handleCancel = () => {
    setIsEditing(false);
    setErrors({});
    if (user) {
      setFormData({
        name: user.name || '',
        email: user.email || '',
        phone: user.phone || '',
        address: user.address || '',
        city: user.city || '',
        state: user.state || '',
        zipCode: user.zipCode || '',
      });
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  if (!isAuthenticated) return null;

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-12">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-4xl">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Hồ Sơ Của Tôi
          </h1>
          {showSuccess && (
            <div className="flex items-center gap-2 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 px-4 py-2 rounded-lg animate-fade-in">
              <CheckCircleIcon className="w-5 h-5" />
              <span>Cập nhật hồ sơ thành công!</span>
            </div>
          )}
        </div>

        {/* Profile Card */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-4">
              <div className="w-20 h-20 rounded-full bg-indigo-600 flex items-center justify-center text-white text-2xl font-bold">
                {user?.avatar ? (
                  <img
                    src={user.avatar}
                    alt={user.name}
                    className="w-20 h-20 rounded-full"
                  />
                ) : (
                  user?.name?.charAt(0).toUpperCase()
                )}
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                  {user?.name}
                </h2>
                <p className="text-gray-600 dark:text-gray-400">{user?.email}</p>
                {user?.role === 'admin' && (
                  <span className="inline-flex items-center gap-1 px-2 py-1 bg-indigo-100 dark:bg-indigo-900 text-indigo-800 dark:text-indigo-200 rounded-full text-sm mt-2">
                    <ShieldCheckIcon className="w-4 h-4" />
                    Quản Trị Viên
                  </span>
                )}
              </div>
            </div>
          </div>

          <div className="p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                Thông Tin Cá Nhân
              </h3>
              {!isEditing && (
                <Button onClick={() => setIsEditing(true)} variant="outline">
                  Chỉnh Sửa Hồ Sơ
                </Button>
              )}
            </div>

            <form onSubmit={handleSubmit}>
              {/* Name */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Họ và Tên
                </label>
                <div className="relative">
                  <UserIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) =>
                      setFormData({ ...formData, name: e.target.value })
                    }
                    disabled={!isEditing}
                    required
                    className={`w-full pl-10 pr-4 py-2 border rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white disabled:bg-gray-100 dark:disabled:bg-gray-800 ${
                      errors.name
                        ? 'border-red-500'
                        : 'border-gray-300 dark:border-gray-600'
                    }`}
                  />
                </div>
                {errors.name && (
                  <p className="text-red-500 text-sm mt-1">{errors.name}</p>
                )}
              </div>

              {/* Email */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Email
                </label>
                <div className="relative">
                  <MailIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) =>
                      setFormData({ ...formData, email: e.target.value })
                    }
                    disabled={!isEditing}
                    required
                    className={`w-full pl-10 pr-4 py-2 border rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white disabled:bg-gray-100 dark:disabled:bg-gray-800 ${
                      errors.email
                        ? 'border-red-500'
                        : 'border-gray-300 dark:border-gray-600'
                    }`}
                  />
                </div>
                {errors.email && (
                  <p className="text-red-500 text-sm mt-1">{errors.email}</p>
                )}
              </div>

              {/* Phone */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Số Điện Thoại
                </label>
                <input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) =>
                    setFormData({ ...formData, phone: e.target.value })
                  }
                  disabled={!isEditing}
                  placeholder="0912 345 678"
                  className={`w-full px-4 py-2 border rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white disabled:bg-gray-100 dark:disabled:bg-gray-800 ${
                    errors.phone ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
                  }`}
                />
                {errors.phone && (
                  <p className="text-red-500 text-sm mt-1">{errors.phone}</p>
                )}
              </div>

              {/* Address */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Địa Chỉ
                </label>
                <input
                  type="text"
                  value={formData.address}
                  onChange={(e) =>
                    setFormData({ ...formData, address: e.target.value })
                  }
                  disabled={!isEditing}
                  placeholder="123 Đường Chính"
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white disabled:bg-gray-100 dark:disabled:bg-gray-800"
                />
              </div>

              {/* City / State / Zip */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Thành Phố
                  </label>
                  <input
                    type="text"
                    value={formData.city}
                    onChange={(e) =>
                      setFormData({ ...formData, city: e.target.value })
                    }
                    disabled={!isEditing}
                    placeholder="HCM"
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white disabled:bg-gray-100 dark:disabled:bg-gray-800"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Tỉnh/Thành
                  </label>
                  <input
                    type="text"
                    value={formData.state}
                    onChange={(e) =>
                      setFormData({ ...formData, state: e.target.value })
                    }
                    disabled={!isEditing}
                    placeholder="HCM"
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white disabled:bg-gray-100 dark:disabled:bg-gray-800"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Mã Bưu Điện
                  </label>
                  <input
                    type="text"
                    value={formData.zipCode}
                    onChange={(e) =>
                      setFormData({ ...formData, zipCode: e.target.value })
                    }
                    disabled={!isEditing}
                    placeholder="700000"
                    className={`w-full px-4 py-2 border rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white disabled:bg-gray-100 dark:disabled:bg-gray-800 ${
                      errors.zipCode ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
                    }`}
                  />
                  {errors.zipCode && (
                    <p className="text-red-500 text-sm mt-1">{errors.zipCode}</p>
                  )}
                </div>
              </div>

              {isEditing && (
                <div className="mt-6 flex gap-4">
                  <Button
                    type="submit"
                    disabled={isSaving}
                    isLoading={isSaving}
                    leftIcon={<SaveIcon className="w-5 h-5" />}
                  >
                    {isSaving ? 'Đang lưu...' : 'Lưu Thay Đổi'}
                  </Button>
                  <Button type="button" variant="outline" onClick={handleCancel} disabled={isSaving}>
                    Hủy
                  </Button>
                </div>
              )}
            </form>
          </div>

          <div className="p-6 border-t border-gray-200 dark:border-gray-700">
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Quản Lý Tài Khoản
            </h3>
            <div className="flex gap-4">
              <Button variant="outline" onClick={handleLogout}>
                Đăng Xuất
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};