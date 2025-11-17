import React, { useEffect, useState, createContext, useContext } from 'react';

interface User {
  _id: string; // MongoDB ObjectId
  id?: string; // For backward compatibility
  email: string;
  first_name?: string;
  last_name?: string;
  name?: string; // Computed from first_name + last_name
  phone?: string;
  address?: string;
  city?: string;
  province?: string;
  state?: string; // For backward compatibility
  postal_code?: string;
  zipCode?: string; // For backward compatibility
  role?: 'customer' | 'admin';
  avatar?: string;
}

// Thêm interface cho Order
interface Order {
  id: string;
  customer: string;
  items: {
    product: string;
    quantity: number;
    price: number;
  }[];
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

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  updateUser: (updates: Partial<User>) => void;
  fetchUserInfo: () => Promise<void>;
  fetchUserOrders: () => Promise<Order[]>; // Thêm hàm lấy danh sách đơn hàng
  isAuthenticated: boolean;
  isAdmin: boolean;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // useEffect này chỉ chạy một lần khi ứng dụng khởi động
  useEffect(() => {
    const initializeAuth = async () => {
      const savedUser = localStorage.getItem('user');
      if (savedUser) {
        try {
          const parsedUser = JSON.parse(savedUser);
          setUser(parsedUser); // Đặt user từ localStorage trước

          // Nếu user đã đăng nhập, tiến hành fetch thông tin chi tiết
          if (parsedUser._id) {
            await fetchUserInfoAfterLogin(parsedUser._id);
          }
        } catch (error) {
          console.error("Lỗi khi phân tích dữ liệu người dùng:", error);
          localStorage.removeItem('user'); // Xóa dữ liệu không hợp lệ
        }
      }
      // Kết thúc quá trình khởi tạo
      setIsLoading(false);
    };

    initializeAuth();
  }, []); // Mảng rỗng để chỉ chạy một lần

  useEffect(() => {
    if (user) localStorage.setItem('user', JSON.stringify(user));
    else localStorage.removeItem('user');
  }, [user]);

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/customer/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
        credentials: 'include',
      });

      const data = await res.json();

      if (!res.ok || data.message !== 'Login successful') {
        throw new Error(data.error || 'Email hoặc mật khẩu không đúng');
      }

      // Lưu thông tin cơ bản trước khi fetch thông tin chi tiết
      const basicUser: User = {
        _id: data.id,
        id: data.id,
        email,
        role: data.role === 'admin' ? 'admin' : 'customer',
        avatar: `https://api.dicebear.com/7.x/identicon/svg?seed=${encodeURIComponent(email)}`,
      };

      setUser(basicUser);
      
      // Fetch thông tin chi tiết sau khi đăng nhập thành công
      await fetchUserInfoAfterLogin(data.id);
    } catch (err) {
      console.error('Login error:', err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (name: string, email: string, password: string) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/customer/register/`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email,
          password,
          first_name: name,
          last_name: '',
          phone: '',
          address: '',
          city: '',
          province: '',
          postal_code: '',
        }),
      });

      const data = await response.json();

      if (!response.ok || data.message !== 'User registered successfully') {
        throw new Error(data.error || 'Đăng ký thất bại');
      }

      // Lưu thông tin cơ bản trước khi fetch thông tin chi tiết
      const basicUser: User = {
        _id: data.id,
        id: data.id,
        email,
        name,
        role: 'customer',
      };

      setUser(basicUser);
      
      // Fetch thông tin chi tiết sau khi đăng ký thành công
      await fetchUserInfoAfterLogin(data.id);
    } catch (error) {
      console.error('Register error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Hàm lấy thông tin người dùng sau khi đăng nhập/đăng ký
  const fetchUserInfoAfterLogin = async (userId: string) => {
    try {
      console.log('Fetching user info for:', userId);
      const response = await fetch(`${import.meta.env.VITE_API_URL}/customer/get_customer/${userId}/`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch user info');
      }
      
      const data = await response.json();
      console.log('User data received:', data);
      
      // Tạo tên đầy đủ từ first_name và last_name
      const fullName = `${data.first_name || ''} ${data.last_name || ''}`.trim();
      
      // Cập nhật thông tin người dùng với dữ liệu từ API
      setUser(prevUser => {
        if (!prevUser) return null;
        
        return {
          ...prevUser,
          ...data,
          name: fullName || prevUser.name,
          state: data.province || prevUser.state, // Map province to state for backward compatibility
          zipCode: data.postal_code || prevUser.zipCode, // Map postal_code to zipCode for backward compatibility
        };
      });
    } catch (error) {
      console.error('Error fetching user info after login:', error);
      // Không throw error ở đây để không làm hỏng quá trình đăng nhập/đăng ký
    }
  };

  // Hàm lấy thông tin người dùng từ API
  const fetchUserInfo = async () => {
    if (!user || !user._id) {
      throw new Error('User not authenticated');
    }
    
    setIsLoading(true);
    try {
      console.log('Fetching user info for:', user._id);
      const response = await fetch(`${import.meta.env.VITE_API_URL}/customer/get_customer/${user._id}/`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch user info');
      }
      
      const data = await response.json();
      console.log('User data received:', data);
      
      // Tạo tên đầy đủ từ first_name và last_name
      const fullName = `${data.first_name || ''} ${data.last_name || ''}`.trim();
      
      // Cập nhật thông tin người dùng với dữ liệu từ API
      setUser(prevUser => {
        if (!prevUser) return null;
        
        return {
          ...prevUser,
          ...data,
          name: fullName || prevUser.name,
          state: data.province || prevUser.state, // Map province to state for backward compatibility
          zipCode: data.postal_code || prevUser.zipCode, // Map postal_code to zipCode for backward compatibility
        };
      });
    } catch (error) {
      console.error('Error fetching user info:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  //  Hàm lấy danh sách đơn hàng của người dùng
  const fetchUserOrders = async (): Promise<Order[]> => {
    if (!user || !user._id) {
      throw new Error('User not authenticated');
    }
    
    try {
      console.log('Fetching orders for user:', user._id);
      const response = await fetch(`${import.meta.env.VITE_API_URL}/order/customer/${user._id}/`, {
      credentials: 'include', // quan trọng: gửi cookie session đi
      headers: {
        'Content-Type': 'application/json'
      }
    });
      
      if (!response.ok) {
        throw new Error('Failed to fetch user orders');
      }
      
      const data = await response.json();
      console.log('Orders data received:', data);
      
      return data; // Trả về mảng các đơn hàng
    } catch (error) {
      console.error('Error fetching user orders:', error);
      throw error;
    }
  };

  const logout = () => {
    setUser(null);
  };

  const updateUser = (updates: Partial<User>) => {
    if (user) setUser({ ...user, ...updates });
  };

  const isAuthenticated = !!user;
  const isAdmin = user?.role === 'admin';

  return (
    <AuthContext.Provider
      value={{ 
        user, 
        login, 
        register, 
        logout, 
        updateUser, 
        fetchUserInfo,
        fetchUserOrders,
        isAuthenticated, 
        isAdmin,
        isLoading
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};
