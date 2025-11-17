import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useWishlist } from '../contexts/WishlistContext';
import { useReviews } from '../contexts/ReviewContext';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '../components/ui/Button';
import {
  StarIcon,
  TruckIcon,
  ShieldCheckIcon,
  RotateCcwIcon,
  EditIcon,
  AlertCircleIcon,
  CheckCircleIcon,
  BotIcon,
  MessageCircleIcon,
} from 'lucide-react';

// Kiểu dữ liệu từ API
interface ApiProduct {
  id: string;
  name: string;
  price: string;
  originalPrice: string;
  image: string;
  rating?: number;
  category: string;
  brand: string;
  isNew?: boolean;
  detail?: {
    id?: string;
    images?: string[];
    rating?: number;
    reviewCount?: number;
    description?: string;
    features?: string[];
    specifications?: Record<string, string>;
    inStock?: boolean;
    hasARView?: boolean;
    product?: string;
  };
}

// Kiểu review từ API (không còn admin_response)
interface ApiReview {
  id: string;
  product_id: string;
  customer_id: string;
  rating: number;
  comment: string;
  created_at: string;
  updated_at: string;
  user_name?: string;
  user_avatar?: string;
}

// Kiểu phản hồi admin từ API
interface ApiAdminResponse {
  id: string;
  review_id: string;
  response: string;
  admin_id: string;
  admin_name: string;
  created_at: string;
  updated_at: string;
  response_type: 'manual' | 'ai';
}

// Kiểu review nội bộ dùng vào UI (không còn adminResponse)
interface UiReview {
  id: string | number;
  productId: string;
  userId: string;
  userName: string;
  userAvatar?: string;
  rating: number;
  comment: string;
  date: string;
  helpful?: number;
}

// Kiểu phản hồi admin nội bộ dùng vào UI
interface UiAdminResponse {
  id: string;
  reviewId: string;
  response: string;
  adminId: string;
  adminName: string;
  createdAt: string;
  updatedAt: string;
  responseType: 'manual' | 'ai';
}

// Kiểu dữ liệu chuẩn hóa dùng trong app
interface Product {
  id: number;
  apiId?: string;
  name: string;
  price: number;
  originalPrice: number;
  image: string;
  images: string[];
  rating: number;
  reviewCount: number;
  description: string;
  category: string;
  colors: string[];
  stock: number;
  brand: string;
  features: string[];
  specifications: Record<string, string>;
  inStock: boolean;
  hasARView: boolean;
  isNew: boolean;
}

// Mock product data - dùng fallback nếu API fail
const productData: Record<number, Product> = {
  1: {
    id: 1,
    name: 'iPhone 15 Pro',
    price: 999,
    originalPrice: 1099,
    image: 'https://picsum.photos/seed/iphone15/800/600.jpg',
    images: [
      'https://picsum.photos/seed/iphone15-1/800/600.jpg',
      'https://picsum.photos/seed/iphone15-2/800/600.jpg',
      'https://picsum.photos/seed/iphone15-3/800/600.jpg'
    ],
    rating: 4.8,
    reviewCount: 256,
    category: 'Smartphones',
    brand: 'Apple',
    description:
      'iPhone 15 Pro mang đến thiết kế titanium tuyệt đẹp, chip A17 Pro và hệ thống camera tiên tiến. Trải nghiệm sức mạnh nhiếp ảnh chuyên nghiệp trong túi của bạn.',
    features: [
      'Chip A17 Pro cho hiệu suất cực nhanh',
      'Hệ thống camera Pro với camera chính 48MP',
      'Thiết kế titanium với Ceramic Shield',
      'Nút hành động cho phím tắt nhanh',
      'Kết nối USB-C',
      'Pin dùng cả ngày',
    ],
    specifications: {
      Display: 'Màn hình Super Retina XDR 6.1 inch',
      Chip: 'Chip A17 Pro',
      Camera: '48MP Chính | 12MP Siêu rộng | 12MP Telephoto',
      Battery: 'Phát lại video lên đến 23 giờ',
      Storage: '128GB, 256GB, 512GB, 1TB',
      Colors: 'Titanium Tự Nhiên, Titanium Xanh, Titanium Trắng, Titanium Đen',
    },
    inStock: true,
    hasARView: true,
    isNew: true,
    colors: ['Titanium Tự Nhiên', 'Titanium Xanh', 'Titanium Trắng', 'Titanium Đen'],
    stock: 999,
  },
};

const defaultProduct: Product = {
  id: 1,
  name: 'Default Product',
  price: 0,
  originalPrice: 0,
  image: '',
  images: [],
  rating: 0,
  reviewCount: 0,
  description: '',
  category: '',
  colors: [],
  stock: 0,
  brand: '',
  features: [],
  specifications: {},
  inStock: true,
  hasARView: false,
  isNew: false,
};

function normalizeProduct(apiData: ApiProduct): Product {
  const detail = apiData.detail || {};

  // Colors từ specifications nếu có
  const colors = detail.specifications?.Colors
    ? detail.specifications.Colors.split(',').map((c) => c.trim())
    : [];

  return {
    ...defaultProduct,
    id: Number(apiData.id) || defaultProduct.id,
    apiId: apiData.id,
    name: apiData.name || defaultProduct.name,
    price: Number(apiData.price) || defaultProduct.price,
    originalPrice: Number(apiData.originalPrice) || defaultProduct.originalPrice,
    image: apiData.image || defaultProduct.image,
    images: detail.images || [defaultProduct.image],
    rating: detail.rating ?? apiData.rating ?? defaultProduct.rating,
    reviewCount: detail.reviewCount ?? defaultProduct.reviewCount,
    category: apiData.category || defaultProduct.category,
    brand: apiData.brand || defaultProduct.brand,
    description: detail.description || defaultProduct.description,
    features: detail.features || defaultProduct.features,
    specifications: detail.specifications || defaultProduct.specifications,
    inStock: detail.inStock ?? true,
    hasARView: detail.hasARView ?? false,
    isNew: apiData.isNew ?? false,
    colors,
    stock: detail.inStock ? 999 : 0,
  };
}

// Hàm chuyển đổi từ API review sang UI review (không còn adminResponse)
function normalizeApiReview(apiReview: ApiReview): UiReview {
  // Nếu API đã trả về user_name và user_avatar, sử dụng chúng
  if (apiReview.user_name && apiReview.user_avatar) {
    return {
      id: apiReview.id,
      productId: apiReview.product_id,
      userId: apiReview.customer_id,
      userName: apiReview.user_name,
      userAvatar: apiReview.user_avatar,
      rating: apiReview.rating,
      comment: apiReview.comment,
      date: apiReview.created_at,
      helpful: 0,
    };
  }
  
  // Nếu không, trích xuất thông tin từ customer_id (format cũ: "Tên <email>")
  const match = apiReview.customer_id.match(/^([^<]+)</);
  const userName = match ? match[1].trim() : apiReview.customer_id;
  
  // Trích xuất email từ customer_id
  const emailMatch = apiReview.customer_id.match(/<([^>]+)>/);
  const userEmail = emailMatch ? emailMatch[1] : '';
  
  // Tạo avatar từ email
  const userAvatar = `https://ui-avatars.com/api/?name=${encodeURIComponent(userName)}&background=random`;
  
  return {
    id: apiReview.id,
    productId: apiReview.product_id,
    userId: userEmail,
    userName,
    userAvatar,
    rating: apiReview.rating,
    comment: apiReview.comment,
    date: apiReview.created_at,
    helpful: 0,
  };
}

// Hàm chuyển đổi từ API admin response sang UI admin response
function normalizeApiAdminResponse(apiResponse: ApiAdminResponse): UiAdminResponse {
  return {
    id: apiResponse.id,
    reviewId: apiResponse.review_id,
    response: apiResponse.response,
    adminId: apiResponse.admin_id,
    adminName: apiResponse.admin_name,
    createdAt: apiResponse.created_at,
    updatedAt: apiResponse.updated_at,
    responseType: apiResponse.response_type,
  };
}

export const ProductDetail: React.FC = () => {
  const params = useParams<{ id: string }>();
  const paramId = params.id || '1';
  const productIdNumeric = parseInt(paramId || '1', 10);

  const [selectedImage, setSelectedImage] = useState(0);
  const [newReviewRating, setNewReviewRating] = useState(5);
  const [newReviewComment, setNewReviewComment] = useState('');
  const [editingReviewId, setEditingReviewId] = useState<string | number | null>(null);
  const [editRating, setEditRating] = useState(5);
  const [editComment, setEditComment] = useState('');
  const [sortBy, setSortBy] = useState<'newest' | 'oldest' | 'highest' | 'lowest' | 'helpful'>('newest');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [reviewsLoading, setReviewsLoading] = useState(false);
  const [reviewsError, setReviewsError] = useState<string | null>(null);
  const [notification, setNotification] = useState<{
    type: 'success' | 'error';
    message: string;
    show: boolean;
  }>({ type: 'success', message: '', show: false });

  // State để quản lý phản hồi admin (đơn giản hơn)
  const [adminResponses, setAdminResponses] = useState<Record<string, UiAdminResponse[]>>({});
  const [showAdminResponse, setShowAdminResponse] = useState<Record<string, boolean>>({});

  // Loại bỏ isInWishlist vì không sử dụng
  const { getProductReviews } = useReviews();
  const { isAuthenticated, user } = useAuth();

  const [product, setProduct] = useState<Product>(defaultProduct);
  const [reviews, setReviews] = useState<UiReview[]>([]);

  // Hàm tải reviews từ API
  const fetchReviews = useCallback(async (productId: string) => {
    setReviewsLoading(true);
    setReviewsError(null);
    
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/review/get_by_id/${productId}/`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const apiReviews: ApiReview[] = await response.json();
      
      // Chuyển đổi dữ liệu từ API sang định dạng UI
      const normalizedReviews = apiReviews.map(normalizeApiReview);
      
      setReviews(normalizedReviews);
      
      // Tải phản hồi admin cho mỗi review
      normalizedReviews.forEach(review => {
        fetchAdminResponses(String(review.id));
      });
    } catch (err) {
      console.error('Fetch reviews error:', err);
      setReviewsError(`Không thể tải đánh giá: ${(err as Error).message}`);
      
      // Fallback to context if API fails
      try {
        const ctxReviews = getProductReviews ? getProductReviews(productIdNumeric) : [];
        const normalized: UiReview[] = (ctxReviews || []).map((r: unknown) => {
          const review = r as Record<string, unknown>;
          return {
            id: (review.id as string | number) ?? (review._id as string | number) ?? Math.random().toString(36).slice(2),
            productId: (review.productId as string) ?? String(paramId),
            userId: (review.userId as string) ?? (review.customer_id as string) ?? ((review.customerId as string) ?? 'unknown'),
            userName: (review.userName as string) ?? (review.customer_name as string) ?? 'Người dùng',
            userAvatar: (review.userAvatar as string) ?? (review.avatar as string | undefined),
            rating: (review.rating as number) ?? 5,
            comment: (review.comment as string) ?? '',
            date: (review.date as string) ?? (review.created_at as string) ?? new Date().toISOString(),
            helpful: (review.helpful as number) ?? (review.helpful_count as number) ?? 0,
          };
        });
        setReviews(normalized);
      } catch (ctxErr) {
        console.warn('getProductReviews fallback error', ctxErr);
        setReviews([]);
      }
    } finally {
      setReviewsLoading(false);
    }
  }, [getProductReviews, productIdNumeric, paramId]);

  // Hàm tải phản hồi admin cho một review cụ thể
  const fetchAdminResponses = async (reviewId: string) => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/review/${reviewId}/responses/`);      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const apiResponses: ApiAdminResponse[] = await response.json();
      
      // Chuyển đổi dữ liệu từ API sang định dạng UI
      const normalizedResponses = apiResponses.map(normalizeApiAdminResponse);
      
      setAdminResponses(prev => ({
        ...prev,
        [reviewId]: normalizedResponses
      }));
    } catch (err) {
      console.error('Fetch admin responses error:', err);
      // Không hiển thị lỗi cho người dùng, chỉ log ra console
    }
  };

  // Hàm hiển thị thông báo
  const showNotification = (type: 'success' | 'error', message: string) => {
    setNotification({ type, message, show: true });
    setTimeout(() => {
      setNotification(prev => ({ ...prev, show: false }));
    }, 3000);
  };

  // Hàm xử lý việc hiển thị/ẩn phản hồi admin
  const toggleAdminResponse = (reviewId: string) => {
    setShowAdminResponse(prev => ({
      ...prev,
      [reviewId]: !prev[reviewId]
    }));
  };

  useEffect(() => {
    const fetchProduct = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/products/${paramId}/`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data: ApiProduct = await response.json();
        const normalized = normalizeProduct(data);
        setProduct(normalized);
        
        // Sau khi tải sản phẩm thành công, tải reviews
        if (normalized.apiId) {
          fetchReviews(normalized.apiId);
        }
      } catch (err) {
        console.error('Fetch product error:', err);
        setError(`Không thể tải sản phẩm: ${(err as Error).message}. Sử dụng dữ liệu mẫu.`);
        const fallback = productData[productIdNumeric] || defaultProduct;
        setProduct(fallback);
        
        // Vẫn thử tải reviews với ID gốc
        fetchReviews(paramId);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [paramId, productIdNumeric, fetchReviews]);

  // Fallback: Nếu không có reviews từ API, thử lấy từ context
  useEffect(() => {
    if (reviews.length === 0 && !reviewsLoading && !reviewsError) {
      try {
        const ctxReviews = getProductReviews ? getProductReviews(productIdNumeric) : [];
        const normalized: UiReview[] = (ctxReviews || []).map((r: unknown) => {
          const review = r as Record<string, unknown>;
          return {
            id: (review.id as string | number) ?? (review._id as string | number) ?? Math.random().toString(36).slice(2),
            productId: (review.productId as string) ?? String(paramId),
            userId: (review.userId as string) ?? (review.customer_id as string) ?? ((review.customerId as string) ?? 'unknown'),
            userName: (review.userName as string) ?? (review.customer_name as string) ?? 'Người dùng',
            userAvatar: (review.userAvatar as string) ?? (review.avatar as string | undefined),
            rating: (review.rating as number) ?? 5,
            comment: (review.comment as string) ?? '',
            date: (review.date as string) ?? (review.created_at as string) ?? new Date().toISOString(),
            helpful: (review.helpful as number) ?? (review.helpful_count as number) ?? 0,
          };
        });
        setReviews(normalized);
      } catch (err) {
        console.warn('getProductReviews fallback error', err);
        setReviews([]);
      }
    }
  }, [getProductReviews, productIdNumeric, paramId, reviews.length, reviewsLoading, reviewsError]);

  // Sort reviews according to sortBy
  const sortedReviews = [...reviews].sort((a, b) => {
    switch (sortBy) {
      case 'newest':
        return new Date(b.date).getTime() - new Date(a.date).getTime();
      case 'oldest':
        return new Date(a.date).getTime() - new Date(b.date).getTime();
      case 'highest':
        return b.rating - a.rating;
      case 'lowest':
        return a.rating - b.rating;
      case 'helpful':
        return (b.helpful ?? 0) - (a.helpful ?? 0);
      default:
        return 0;
    }
  });

  // Stats calculation
  const calculateReviewStats = () => {
    if (reviews.length === 0) {
      return { averageRating: 0, totalReviews: 0, ratingDistribution: [0, 0, 0, 0, 0] };
    }
    const totalRating = reviews.reduce((s, r) => s + r.rating, 0);
    const averageRating = totalRating / reviews.length;
    const ratingDistribution = [0, 0, 0, 0, 0];
    reviews.forEach((r) => {
      const idx = Math.max(0, Math.min(4, r.rating - 1));
      ratingDistribution[idx] += 1;
    });
    return {
      averageRating: Math.round(averageRating * 10) / 10,
      totalReviews: reviews.length,
      ratingDistribution,
    };
  };

  const reviewStats = calculateReviewStats();

  // --- CẬP NHẬT: submit review to backend API at /api/review/add/ ---
  const handleSubmitReview = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isAuthenticated || !user) {
      showNotification('error', 'Vui lòng đăng nhập để gửi đánh giá.');
      return;
    }
    if (newReviewComment.trim().length < 10) {
      showNotification('error', 'Vui lòng viết đánh giá ít nhất 10 ký tự.');
      return;
    }

    setIsSubmitting(true);

    try {
      // Lấy ID sản phẩm từ API nếu có, nếu không dùng paramId
      const productApiId = product.apiId ?? paramId ?? String(product.id);
      
      // Sử dụng ID người dùng từ AuthContext
      const customerId = user.id;
      
      // Tạo body theo định dạng API mới yêu cầu
      const body = {
        product_id: productApiId,
        customer_id: customerId,
        rating: newReviewRating,
        comment: newReviewComment.trim(),
      };

      const resp = await fetch(`${import.meta.env.VITE_API_URL}/review/add/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });

      if (!resp.ok) {
        // Thử đọc thông báo lỗi nếu có
        const errorText = await resp.text();
        throw new Error(`Lỗi server: ${resp.status} ${errorText}`);
      }

      // Tải lại danh sách reviews từ API để có dữ liệu mới nhất
      if (product.apiId) {
        await fetchReviews(product.apiId);
      } else {
        await fetchReviews(paramId);
      }
      
      // Hiển thị thông báo thành công
      showNotification('success', 'Đánh giá của bạn đã được gửi thành công!');
      
      // Xóa form
      setNewReviewComment('');
      setNewReviewRating(5);
    } catch (err) {
      console.error('Submit review error:', err);
      showNotification('error', 'Gửi đánh giá thất bại: ' + (err as Error).message);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Handle editing (local only unless you provide API endpoints for update)
  const handleEditReview = (reviewId: string | number, currentComment: string, currentRating: number) => {
    setEditingReviewId(reviewId);
    setEditComment(currentComment);
    setEditRating(currentRating);
  };

  const handleUpdateReview = (reviewId: string | number) => {
    if (editComment.trim().length < 10) {
      showNotification('error', 'Vui lòng viết đánh giá ít nhất 10 ký tự.');
      return;
    }
    // Update locally. If you have an API for update, call it here.
    setReviews((prev) =>
      prev.map((r) => (r.id === reviewId ? { ...r, comment: editComment.trim(), rating: editRating, date: new Date().toISOString() } : r))
    );
    setEditingReviewId(null);
    showNotification('success', 'Đã cập nhật đánh giá!');
  };

  // Loading và Error UI
  if (loading) {
    return (
      <div className="min-h-screen bg-white dark:bg-gray-900 py-12 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Đang tải sản phẩm...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-white dark:bg-gray-900 py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6 mb-8">
            <h2 className="text-lg font-semibold text-red-800 dark:text-red-200 mb-2">Lỗi tải dữ liệu</h2>
            <p className="text-red-600 dark:text-red-400">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="mt-4 inline-flex items-center px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
            >
              Thử lại
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 py-12">
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
        {/* Breadcrumb */}
        <nav className="flex mb-8 text-sm">
          <Link to="/" className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300">
            Trang Chủ
          </Link>
          <span className="mx-2 text-gray-500">/</span>
          <Link to="/shop" className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300">
            Cửa Hàng
          </Link>
          <span className="mx-2 text-gray-500">/</span>
          <span className="text-gray-900 dark:text-white">{product.name}</span>
        </nav>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 mb-16">
          {/* Product Images */}
          <div>
            <div className="mb-4 rounded-lg overflow-hidden bg-gray-100 dark:bg-gray-800">
              <img src={product.images[selectedImage] || product.image} alt={product.name} className="w-full h-96 object-cover" />
            </div>
            {product.images.length > 0 && (
              <div className="grid grid-cols-3 gap-4">
                {product.images.map((image, index) => (
                  <button
                    key={index}
                    onClick={() => setSelectedImage(index)}
                    className={`rounded-lg overflow-hidden border-2 ${
                      selectedImage === index ? 'border-indigo-600' : 'border-gray-200 dark:border-gray-700'
                    }`}
                  >
                    <img src={image} alt={`${product.name} view ${index + 1}`} className="w-full h-24 object-cover" />
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Product Info */}
          <div>
            <div className="mb-4">
              <span className="text-sm text-indigo-600 dark:text-indigo-400 font-medium">{product.brand}</span>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white mt-2 mb-4">{product.name}</h1>
              <div className="flex items-center gap-4 mb-4">
                <div className="flex items-center">
                  {[...Array(5)].map((_, i) => (
                    <StarIcon
                      key={i}
                      className={`w-5 h-5 ${i < Math.floor(product.rating) ? 'text-amber-400 fill-amber-400' : 'text-gray-300 dark:text-gray-600'}`}
                    />
                  ))}
                </div>
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  {product.rating} ({product.reviewCount} đánh giá)
                </span>
              </div>
            </div>

            <div className="mb-6">
              <div className="flex items-baseline gap-4">
                <span className="text-4xl font-bold text-gray-900 dark:text-white">${product.price}</span>
                {product.originalPrice > 0 && <span className="text-2xl text-gray-500 line-through">${product.originalPrice}</span>}
              </div>
            </div>

            <p className="text-gray-600 dark:text-gray-400 mb-6">{product.description}</p>
            {/* Features */}
            <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
                <div className="flex items-center gap-2">
                  <TruckIcon className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                  <span className="text-sm text-gray-600 dark:text-gray-400">Miễn phí vận chuyển</span>
                </div>
                <div className="flex items-center gap-2">
                  <ShieldCheckIcon className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                  <span className="text-sm text-gray-600 dark:text-gray-400">Bảo hành 1 năm</span>
                </div>
                <div className="flex items-center gap-2">
                  <RotateCcwIcon className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                  <span className="text-sm text-gray-600 dark:text-gray-400">Đổi trả trong 30 ngày</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Tabs Section */}
        <div className="border-t border-gray-200 dark:border-gray-700 pt-12">
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Chi Tiết Sản Phẩm</h2>
            <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-6">
              <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Tính Năng Chính</h3>
              <ul className="space-y-2">
                {product.features.map((feature, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-indigo-600 dark:text-indigo-400 mr-2">•</span>
                    <span className="text-gray-600 dark:text-gray-400">{feature}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Thông Số Kỹ Thuật</h2>
            <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Object.entries(product.specifications).map(([key, value]) => (
                  <div key={key} className="border-b border-gray-200 dark:border-gray-700 pb-2 last:border-b-0">
                    <span className="font-semibold text-gray-900 dark:text-white">{key}:</span>
                    <span className="ml-2 text-gray-600 dark:text-gray-400">{value}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Reviews Section */}
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Đánh Giá Khách Hàng</h2>

            {/* Review Statistics */}
            {reviews.length > 0 && (
              <div className="bg-gradient-to-br from-indigo-50 to-purple-50 dark:from-gray-800 dark:to-gray-800 rounded-lg p-6 mb-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="flex items-center gap-4">
                    <div className="text-center">
                      <div className="text-5xl font-bold text-gray-900 dark:text-white">{reviewStats.averageRating.toFixed(1)}</div>
                      <div className="flex justify-center my-2">
                        {[...Array(5)].map((_, i) => (
                          <StarIcon key={i} className={`w-5 h-5 ${i < Math.round(reviewStats.averageRating) ? 'text-amber-400 fill-amber-400' : 'text-gray-300 dark:text-gray-600'}`} />
                        ))}
                      </div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {reviewStats.totalReviews} {reviewStats.totalReviews === 1 ? 'đánh giá' : 'đánh giá'}
                      </p>
                    </div>
                    <div className="flex-grow">
                      {[5, 4, 3, 2, 1].map((rating) => {
                        const count = reviewStats.ratingDistribution[rating - 1];
                        const percentage = reviewStats.totalReviews > 0 ? (count / reviewStats.totalReviews) * 100 : 0;
                        return (
                          <div key={rating} className="flex items-center gap-2 mb-1">
                            <span className="text-sm text-gray-600 dark:text-gray-400 w-8">
                              {rating} <StarIcon className="w-3 h-3 inline text-amber-400" />
                            </span>
                            <div className="flex-grow bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                              <div className="bg-amber-400 h-2 rounded-full transition-all duration-300" style={{ width: `${percentage}%` }} />
                            </div>
                            <span className="text-sm text-gray-600 dark:text-gray-400 w-8">{count}</span>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                  <div className="flex items-center justify-center md:justify-end">
                    <div className="text-center md:text-right">
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">Muốn chia sẻ trải nghiệm của bạn?</p>
                      {isAuthenticated ? (
                        <button
                          onClick={() => document.getElementById('review-form')?.scrollIntoView({ behavior: 'smooth' })}
                          className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 font-semibold"
                        >
                          Viết Đánh Giá →
                        </button>
                      ) : (
                        <Link to="/login" className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 font-semibold">
                          Đăng Nhập để Đánh Giá →
                        </Link>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Reviews Loading State */}
            {reviewsLoading && (
              <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-6 mb-6 text-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mx-auto mb-4"></div>
                <p className="text-gray-600 dark:text-gray-400">Đang tải đánh giá...</p>
              </div>
            )}

            {/* Reviews Error State */}
            {reviewsError && (
              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6 mb-6">
                <h3 className="text-lg font-semibold text-red-800 dark:text-red-200 mb-2">Lỗi tải đánh giá</h3>
                <p className="text-red-600 dark:text-red-400 mb-4">{reviewsError}</p>
                <button
                  onClick={() => {
                    if (product.apiId) {
                      fetchReviews(product.apiId);
                    } else {
                      fetchReviews(paramId);
                    }
                  }}
                  className="inline-flex items-center px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
                >
                  Thử lại
                </button>
              </div>
            )}

            {/* Sort Controls */}
            {!reviewsLoading && !reviewsError && reviews.length > 0 && (
              <div className="flex items-center justify-between mb-6">
                <p className="text-gray-600 dark:text-gray-400">Hiển thị {sortedReviews.length} {sortedReviews.length === 1 ? 'đánh giá' : 'đánh giá'}</p>
                <div className="flex items-center gap-2">
                  <label className="text-sm text-gray-600 dark:text-gray-400">Sắp xếp:</label>
                  <select
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value as 'newest' | 'oldest' | 'highest' | 'lowest' | 'helpful')}
                    className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="newest">Mới nhất</option>
                    <option value="oldest">Cũ nhất</option>
                    <option value="highest">Đánh giá cao nhất</option>
                    <option value="lowest">Đánh giá thấp nhất</option>
                    <option value="helpful">Hữu ích nhất</option>
                  </select>
                </div>
              </div>
            )}

            {/* Add Review Form */}
            {isAuthenticated ? (
              <div id="review-form" className="bg-gray-50 dark:bg-gray-800 rounded-lg p-6 mb-6 border-2 border-transparent hover:border-indigo-500/30 transition-colors">
                <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Viết Đánh Giá</h3>
                <form onSubmit={handleSubmitReview}>
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Xếp hạng</label>
                    <div className="flex gap-2">
                      {[1, 2, 3, 4, 5].map((star) => (
                        <button key={star} type="button" onClick={() => setNewReviewRating(star)} className="focus:outline-none">
                          <StarIcon className={`w-8 h-8 ${star <= newReviewRating ? 'text-amber-400 fill-amber-400' : 'text-gray-300 dark:text-gray-600'}`} />
                        </button>
                      ))}
                    </div>
                  </div>
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Đánh Giá Của Bạn <span className="text-red-500">*</span>
                    </label>
                    <textarea
                      value={newReviewComment}
                      onChange={(e) => setNewReviewComment(e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500"
                      rows={4}
                      required
                      minLength={10}
                      placeholder="Chia sẻ trải nghiệm của bạn về sản phẩm này (tối thiểu 10 ký tự)..."
                    />
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">{newReviewComment.length}/500 ký tự {newReviewComment.length < 10 && '(tối thiểu 10)'}</p>
                  </div>
                  <Button type="submit" disabled={isSubmitting || newReviewComment.trim().length < 10} isLoading={isSubmitting}>
                    {isSubmitting ? 'Đang gửi...' : 'Gửi Đánh Giá'}
                  </Button>
                </form>
              </div>
            ) : (
              <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-6 mb-6 text-center">
                <p className="text-gray-600 dark:text-gray-400 mb-4">Vui lòng đăng nhập để viết đánh giá</p>
                <Link to="/login" className="inline-flex items-center justify-center px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition-colors">
                  Đăng Nhập
                </Link>
              </div>
            )}

            {/* Reviews List */}
            <div className="space-y-6">
              {!reviewsLoading && !reviewsError && sortedReviews.length === 0 && (
                <div className="text-center py-12">
                  <div className="text-gray-400 dark:text-gray-600 mb-4">
                    <StarIcon className="w-16 h-16 mx-auto" />
                  </div>
                  <p className="text-gray-600 dark:text-gray-400 text-lg mb-2">Chưa có đánh giá</p>
                  <p className="text-gray-500 dark:text-gray-500 text-sm">Hãy là người đầu tiên chia sẻ trải nghiệm về sản phẩm này!</p>
                </div>
              )}
              {!reviewsLoading && !reviewsError && sortedReviews.map((review) => (
                <div key={String(review.id)} className="bg-gray-50 dark:bg-gray-800 rounded-lg p-6">
                  {editingReviewId === review.id ? (
                    <div>
                      <div className="mb-4">
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Xếp hạng</label>
                        <div className="flex gap-2">
                          {[1, 2, 3, 4, 5].map((star) => (
                            <button key={star} type="button" onClick={() => setEditRating(star)} className="focus:outline-none">
                              <StarIcon className={`w-6 h-6 ${star <= editRating ? 'text-amber-400 fill-amber-400' : 'text-gray-300 dark:text-gray-600'}`} />
                            </button>
                          ))}
                        </div>
                      </div>
                      <textarea value={editComment} onChange={(e) => setEditComment(e.target.value)} className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white mb-4" rows={4} />
                      <div className="flex gap-2">
                        <Button onClick={() => handleUpdateReview(review.id)}>Lưu</Button>
                        <Button variant="outline" onClick={() => setEditingReviewId(null)}>
                          Hủy
                        </Button>
                      </div>
                    </div>
                  ) : (
                    <div className="flex items-start gap-4">
                      <img src={review.userAvatar} alt={review.userName} className="w-12 h-12 rounded-full" />
                      <div className="flex-grow">
                        <div className="flex items-center justify-between mb-2">
                          <div>
                            <h4 className="font-semibold text-gray-900 dark:text-white">{review.userName}</h4>
                            <p className="text-sm text-gray-500 dark:text-gray-400">{new Date(review.date).toLocaleDateString()}</p>
                          </div>
                          <div className="flex items-center gap-2">
                            <div className="flex">
                              {[...Array(5)].map((_, i) => (
                                <StarIcon key={i} className={`w-4 h-4 ${i < review.rating ? 'text-amber-400 fill-amber-400' : 'text-gray-300 dark:text-gray-600'}`} />
                              ))}
                            </div>
                            {user && String(user.id) === String(review.userId) && (
                              <div className="flex gap-2 ml-4">
                                <button
                                  onClick={() => handleEditReview(review.id, review.comment, review.rating)}
                                  className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                                >
                                  <EditIcon className="w-4 h-4" />
                                </button>
                              </div>
                            )}
                          </div>
                        </div>
                        <p className="text-gray-600 dark:text-gray-400 mb-3">{review.comment}</p>
                        
                        {/* Nút xem phản hồi admin */}
                        {adminResponses[String(review.id)] && adminResponses[String(review.id)].length > 0 && (
                          <button
                            onClick={() => toggleAdminResponse(String(review.id))}
                            className="flex items-center gap-1 text-sm text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 mb-2"
                          >
                            <MessageCircleIcon className="w-4 h-4" />
                            {showAdminResponse[String(review.id)] ? 'Ẩn phản hồi từ cửa hàng' : `Xem ${adminResponses[String(review.id)].length} phản hồi từ cửa hàng`}
                          </button>
                        )}
                        
                        {/* Phản hồi admin từ cửa hàng */}
                        {showAdminResponse[String(review.id)] && adminResponses[String(review.id)] && (
                          <div className="space-y-3">
                            {adminResponses[String(review.id)].map((response) => (
                              <div key={response.id} className="p-4 bg-indigo-50 dark:bg-indigo-900/20 rounded-lg border border-indigo-200 dark:border-indigo-800">
                                <div className="flex items-start gap-3">
                                  <div className="flex-shrink-0 w-8 h-8 bg-indigo-600 rounded-full flex items-center justify-center">
                                    {response.responseType === 'ai' ? (
                                      <BotIcon className="w-4 h-4 text-white" />
                                    ) : (
                                      <div className="w-4 h-4 bg-white rounded-full"></div>
                                    )}
                                  </div>
                                  <div className="flex-grow">
                                    <div className="flex items-center gap-2 mb-1">
                                      <h5 className="font-medium text-indigo-900 dark:text-indigo-200">{response.adminName}</h5>
                                      <span className="text-xs text-indigo-600 dark:text-indigo-400 bg-indigo-100 dark:bg-indigo-900/40 px-2 py-0.5 rounded-full">
                                        {response.responseType === 'ai' ? 'AI Assistant' : 'Admin'}
                                      </span>
                                    </div>
                                    <p className="text-sm text-indigo-800 dark:text-indigo-300 whitespace-pre-line">
                                      {response.response}
                                    </p>
                                    <p className="text-xs text-indigo-600 dark:text-indigo-400 mt-2">
                                      {new Date(response.createdAt).toLocaleDateString()} - Phản hồi được tạo bởi {response.responseType === 'ai' ? 'AI' : 'admin'}
                                    </p>
                                  </div>
                                </div>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};