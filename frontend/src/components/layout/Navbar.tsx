import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTheme } from '../../contexts/ThemeContext';
import { useCart } from '../../contexts/CartContext';
import { useWishlist } from '../../contexts/WishlistContext';
import { useAuth } from '../../contexts/AuthContext';
import { SearchIcon, ShoppingCartIcon, HeartIcon, UserIcon, MenuIcon, XIcon, SunIcon, MoonIcon, LogOutIcon } from 'lucide-react';
export const Navbar = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const {
    theme,
    toggleTheme
  } = useTheme();
  const {
    cartCount
  } = useCart();
  const {
    wishlistCount
  } = useWishlist();
  const {
    isAuthenticated,
    user,
    logout
  } = useAuth();
  const navigate = useNavigate();
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/shop?search=${encodeURIComponent(searchQuery)}`);
      setIsSearchOpen(false);
      setSearchQuery('');
    }
  };
  const handleLogout = () => {
    logout();
    navigate('/');
  };
  return <header className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${isScrolled ? 'bg-white/95 dark:bg-gray-900/95 backdrop-blur-xl shadow-lg border-b border-gray-200 dark:border-gray-800' : 'bg-white dark:bg-gray-900'}`}>
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 md:h-20">
          {/* Logo */}
          <Link to="/" className="flex items-center group">
            <span className="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 dark:from-indigo-400 dark:to-purple-400 bg-clip-text text-transparent group-hover:scale-105 transition-transform">
              TechHub
            </span>
          </Link>
          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-8">
            <Link to="/" className="text-gray-700 dark:text-gray-200 hover:text-indigo-600 dark:hover:text-indigo-400 transition-all font-medium hover:scale-105">
              Trang chủ
            </Link>
            <Link to="/shop" className="text-gray-700 dark:text-gray-200 hover:text-indigo-600 dark:hover:text-indigo-400 transition-all font-medium hover:scale-105">
              Cửa hàng
            </Link>
            <Link to="/about" className="text-gray-700 dark:text-gray-200 hover:text-indigo-600 dark:hover:text-indigo-400 transition-all font-medium hover:scale-105">
              Giới thiệu
            </Link>
            <Link to="/contact" className="text-gray-700 dark:text-gray-200 hover:text-indigo-600 dark:hover:text-indigo-400 transition-all font-medium hover:scale-105">
              Liên hệ
            </Link>
          </nav>
          {/* Right Icons */}
          <div className="flex items-center space-x-3">
            {/* Theme Toggle */}
            <button onClick={toggleTheme} className="p-2 text-gray-700 dark:text-gray-200 hover:text-indigo-600 dark:hover:text-indigo-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full transition-all">
              {theme === 'dark' ? <SunIcon className="w-5 h-5" /> : <MoonIcon className="w-5 h-5" />}
            </button>
            {/* Wishlist */}
            <Link to="/wishlist" className="p-2 text-gray-700 dark:text-gray-200 hover:text-red-600 dark:hover:text-red-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full transition-all relative">
              <HeartIcon className="w-5 h-5" />
              {wishlistCount > 0 && <span className="absolute top-0 right-0 bg-gradient-to-r from-red-500 to-pink-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center shadow-lg">
                  {wishlistCount}
                </span>}
            </Link>
            {/* Cart */}
            <Link to="/cart" className="p-2 text-gray-700 dark:text-gray-200 hover:text-indigo-600 dark:hover:text-indigo-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full transition-all relative">
              <ShoppingCartIcon className="w-5 h-5" />
              {cartCount > 0 && <span className="absolute top-0 right-0 bg-gradient-to-r from-indigo-600 to-purple-600 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center shadow-lg">
                  {cartCount}
                </span>}
            </Link>
            {/* User Menu */}
            {isAuthenticated ? <div className="relative group">
                <button className="flex items-center space-x-2 text-gray-700 dark:text-gray-200 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
                  {user?.avatar ? <img src={user.avatar} alt={user.name} className="w-8 h-8 rounded-full" /> : <UserIcon className="w-5 h-5" />}
                </button>
                <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg py-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
                  <div className="px-4 py-2 border-b border-gray-200 dark:border-gray-700">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      {user?.name}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      {user?.email}
                    </p>
                  </div>
                  <Link to="/profile" className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">
                    Hồ sơ của tôi
                  </Link>
                  <Link to="/orders" className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">
                    Đơn hàng của tôi
                  </Link>
                  <button onClick={handleLogout} className="w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center">
                    <LogOutIcon className="w-4 h-4 mr-2" />
                    Đăng xuất
                  </button>
                </div>
              </div> : <Link to="/login" className="text-gray-700 dark:text-gray-200 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
                <UserIcon className="w-5 h-5" />
              </Link>}
            {/* Mobile menu button */}
            <button className="md:hidden text-gray-700 dark:text-gray-200" onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}>
              {isMobileMenuOpen ? <XIcon className="w-6 h-6" /> : <MenuIcon className="w-6 h-6" />}
            </button>
          </div>
        </div>
        {/* Search Bar */}
        {isSearchOpen && <div className="py-4 border-t border-gray-200 dark:border-gray-700">
            <form onSubmit={handleSearch} className="relative">
              <input type="text" value={searchQuery} onChange={e => setSearchQuery(e.target.value)} placeholder="Tìm kiếm sản phẩm..." className="w-full px-4 py-2 pl-10 pr-4 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-white" autoFocus />
              <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            </form>
          </div>}
      </div>
      {/* Mobile Menu */}
      {isMobileMenuOpen && <div className="md:hidden bg-white dark:bg-gray-900 shadow-lg">
          <div className="px-4 pt-2 pb-4 space-y-3">
            <Link to="/" className="block py-2 text-gray-700 dark:text-gray-200 hover:text-indigo-600 dark:hover:text-indigo-400" onClick={() => setIsMobileMenuOpen(false)}>
              Trang chủ
            </Link>
            <Link to="/shop" className="block py-2 text-gray-700 dark:text-gray-200 hover:text-indigo-600 dark:hover:text-indigo-400" onClick={() => setIsMobileMenuOpen(false)}>
              Cửa hàng
            </Link>
            <Link to="/about" className="block py-2 text-gray-700 dark:text-gray-200 hover:text-indigo-600 dark:hover:text-indigo-400" onClick={() => setIsMobileMenuOpen(false)}>
              Giới thiệu
            </Link>
            <Link to="/contact" className="block py-2 text-gray-700 dark:text-gray-200 hover:text-indigo-600 dark:hover:text-indigo-400" onClick={() => setIsMobileMenuOpen(false)}>
              Liên hệ
            </Link>
            {isAuthenticated && <>
                <Link to="/profile" className="block py-2 text-gray-700 dark:text-gray-200 hover:text-indigo-600 dark:hover:text-indigo-400" onClick={() => setIsMobileMenuOpen(false)}>
                  Hồ sơ của tôi
                </Link>
                <Link to="/orders" className="block py-2 text-gray-700 dark:text-gray-200 hover:text-indigo-600 dark:hover:text-indigo-400" onClick={() => setIsMobileMenuOpen(false)}>
                  Đơn hàng của tôi
                </Link>
                <button onClick={() => {
            handleLogout();
            setIsMobileMenuOpen(false);
          }} className="block w-full text-left py-2 text-gray-700 dark:text-gray-200 hover:text-indigo-600 dark:hover:text-indigo-400">
                  Đăng xuất
                </button>
              </>}
          </div>
        </div>}
    </header>;
};