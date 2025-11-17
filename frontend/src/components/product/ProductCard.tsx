import React from 'react';
import { Link } from 'react-router-dom';
import { ShoppingCartIcon, HeartIcon, StarIcon } from 'lucide-react';
import { useCart } from '../../contexts/CartContext';
import { useWishlist } from '../../contexts/WishlistContext';
interface ProductCardProps {
  id: number;
  name: string;
  price: number;
  originalPrice?: number;
  image: string;
  rating: number;
  category: string;
  isNew?: boolean;
  isFeatured?: boolean;
}
export const ProductCard = ({
  id,
  name,
  price,
  originalPrice,
  image,
  rating,
  category,
  isNew = false,
  isFeatured = false
}: ProductCardProps) => {
  const {
    addToCart
  } = useCart();
  const {
    addToWishlist,
    removeFromWishlist,
    isInWishlist
  } = useWishlist();
  const discount = originalPrice ? Math.round((originalPrice - price) / originalPrice * 100) : 0;
  const inWishlist = isInWishlist(id);
  const handleAddToCart = (e: React.MouseEvent) => {
    e.preventDefault();
    addToCart({
      id,
      name,
      price,
      image
    });
  };
  const handleWishlistToggle = (e: React.MouseEvent) => {
    e.preventDefault();
    if (inWishlist) {
      removeFromWishlist(id);
    } else {
      addToWishlist({
        id,
        name,
        price,
        image,
        category
      });
    }
  };
  return <div className="group relative bg-white dark:bg-gray-800 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden border border-gray-200 dark:border-gray-700 hover:border-indigo-500 dark:hover:border-indigo-500 transform hover:-translate-y-1">
      {/* Badges */}
      <div className="absolute top-3 left-3 z-10 flex flex-col gap-2">
        {isNew && <span className="px-2.5 py-1 bg-gradient-to-r from-blue-500 to-blue-600 text-white text-xs font-semibold rounded-full shadow-md">
            Mới
          </span>}
        {discount > 0 && <span className="px-2.5 py-1 bg-gradient-to-r from-red-500 to-red-600 text-white text-xs font-semibold rounded-full shadow-md">
            -{discount}%
          </span>}
        {isFeatured && <span className="px-2.5 py-1 bg-gradient-to-r from-amber-500 to-orange-500 text-white text-xs font-semibold rounded-full shadow-md">
            Nổi bật
          </span>}
      </div>
      {/* Wishlist button */}
      <button onClick={handleWishlistToggle} className="absolute top-3 right-3 z-10 p-2 bg-white/95 dark:bg-gray-800/95 rounded-full text-gray-600 dark:text-gray-300 hover:text-red-500 dark:hover:text-red-500 hover:bg-white dark:hover:bg-gray-800 backdrop-blur-sm shadow-md transition-all duration-200 hover:scale-110" aria-label="Add to wishlist">
        <HeartIcon className={`w-5 h-5 ${inWishlist ? 'fill-red-500 text-red-500' : ''}`} />
      </button>
      {/* Image */}
      <Link to={`/product/${id}`} className="block relative aspect-square overflow-hidden bg-gray-100 dark:bg-gray-700">
        <img src={image} alt={name} className="w-full h-full object-cover object-center group-hover:scale-110 transition-transform duration-500" />
      </Link>
      {/* Content */}
      <div className="p-5">
        <Link to={`/product/${id}`} className="block">
          <span className="text-xs text-indigo-600 dark:text-indigo-400 font-semibold uppercase tracking-wider">
            {category}
          </span>
          <h3 className="mt-1.5 text-lg font-bold text-gray-900 dark:text-white line-clamp-2 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
            {name}
          </h3>
          {/* Rating */}
          <div className="flex items-center mt-2">
            <div className="flex">
              {[...Array(5)].map((_, i) => <StarIcon key={i} className={`w-4 h-4 ${i < rating ? 'text-amber-400 fill-amber-400' : 'text-gray-300 dark:text-gray-600'}`} />)}
            </div>
            <span className="ml-2 text-sm font-medium text-gray-600 dark:text-gray-400">
              {rating.toFixed(1)}
            </span>
          </div>
          {/* Price */}
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-gray-900 dark:text-white">
              ${price.toFixed(2)}
            </span>
            {originalPrice && <span className="text-sm text-gray-500 dark:text-gray-400 line-through">
                ${originalPrice.toFixed(2)}
              </span>}
          </div>
        </Link>
        {/* Add to cart button */}
        <button onClick={handleAddToCart} className="mt-4 w-full py-3 px-4 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white text-sm font-semibold rounded-xl flex items-center justify-center gap-2 transition-all duration-200 shadow-md hover:shadow-lg" aria-label="Add to cart">
          <ShoppingCartIcon className="w-4 h-4" />
          Thêm vào giỏ
        </button>
      </div>
    </div>;
};