import { Link } from 'react-router-dom';
import { useWishlist } from '../contexts/WishlistContext';
import { useCart } from '../contexts/CartContext';
import { ShoppingCartIcon, TrashIcon, HeartIcon, ShoppingBagIcon } from 'lucide-react';
import { Button } from '../components/ui/Button';

export const Wishlist = () => {
  const { wishlistItems, removeFromWishlist } = useWishlist();
  const { addToCart } = useCart();

  const handleAddToCart = (item: any) => {
    addToCart({
      id: item.id,
      name: item.name,
      price: item.price,
      image: item.image
    });
  };

  const handleAddAllToCart = () => {
    wishlistItems.forEach(item => {
      addToCart({
        id: item.id,
        name: item.name,
        price: item.price,
        image: item.image
      });
    });
  };

  if (wishlistItems.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-2xl mx-auto text-center">
            <div className="mb-8 relative">
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-32 h-32 bg-gradient-to-br from-red-500/20 to-pink-500/20 rounded-full blur-3xl"></div>
              </div>
              <HeartIcon className="w-24 h-24 mx-auto text-gray-300 dark:text-gray-700 relative" />
            </div>
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Danh sách yêu thích trống
            </h1>
            <p className="text-lg text-gray-600 dark:text-gray-400 mb-8">
              Lưu các sản phẩm công nghệ yêu thích của bạn tại đây.
            </p>
            <Link to="/shop">
              <Button size="lg" leftIcon={<ShoppingBagIcon className="w-5 h-5" />}>
                Khám phá sản phẩm
              </Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 py-12">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header Section */}
        <div className="mb-10">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2 flex items-center gap-3">
                <HeartIcon className="w-10 h-10 text-red-500 fill-red-500" />
                Danh sách yêu thích
              </h1>
              <p className="text-gray-600 dark:text-gray-400">
                {wishlistItems.length} sản phẩm đã lưu
              </p>
            </div>
            {wishlistItems.length > 0 && (
              <Button 
                onClick={handleAddAllToCart} 
                size="lg"
                leftIcon={<ShoppingCartIcon className="w-5 h-5" />}
              >
                Thêm tất cả vào giỏ
              </Button>
            )}
          </div>
        </div>

        {/* Wishlist Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {wishlistItems.map((item) => (
            <div 
              key={item.id} 
              className="group bg-white dark:bg-gray-800 rounded-2xl shadow-md hover:shadow-2xl transition-all duration-300 overflow-hidden border border-gray-200 dark:border-gray-700 hover:border-indigo-500 dark:hover:border-indigo-500 transform hover:-translate-y-1"
            >
              {/* Image Container */}
              <div className="relative aspect-square overflow-hidden bg-gray-100 dark:bg-gray-700">
                <Link to={`/product/${item.id}`}>
                  <img 
                    src={item.image} 
                    alt={item.name} 
                    className="w-full h-full object-cover object-center group-hover:scale-110 transition-transform duration-500"
                  />
                </Link>
                {/* Remove Button */}
                <button
                  onClick={() => removeFromWishlist(item.id)}
                  className="absolute top-3 right-3 p-2.5 bg-white/95 dark:bg-gray-800/95 backdrop-blur-sm rounded-full text-red-600 hover:bg-red-600 hover:text-white transition-all duration-200 shadow-lg hover:shadow-xl"
                  aria-label="Remove from wishlist"
                >
                  <TrashIcon className="w-5 h-5" />
                </button>
              </div>

              {/* Content */}
              <div className="p-5">
                <Link to={`/product/${item.id}`}>
                  <div className="mb-3">
                    <span className="text-xs font-semibold text-indigo-600 dark:text-indigo-400 uppercase tracking-wider">
                      {item.category}
                    </span>
                    <h3 className="mt-1 text-lg font-bold text-gray-900 dark:text-white line-clamp-2 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                      {item.name}
                    </h3>
                  </div>
                  <div className="mb-4">
                    <span className="text-2xl font-bold text-gray-900 dark:text-white">
                      ${item.price.toFixed(2)}
                    </span>
                  </div>
                </Link>

                {/* Action Button */}
                <button
                  onClick={() => handleAddToCart(item)}
                  className="w-full py-3 px-4 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-semibold rounded-xl flex items-center justify-center gap-2 transition-all duration-200 shadow-md hover:shadow-lg"
                >
                  <ShoppingCartIcon className="w-5 h-5" />
                  Thêm vào giỏ
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Continue Shopping */}
        <div className="mt-12 text-center">
          <Link to="/shop">
            <Button variant="outline" size="lg" leftIcon={<ShoppingBagIcon className="w-5 h-5" />}>
              Tiếp tục mua sắm
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
};
