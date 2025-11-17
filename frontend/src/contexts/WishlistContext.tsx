import React, { useEffect, useState, createContext, useContext } from 'react';
interface WishlistItem {
  id: number;
  name: string;
  price: number;
  image: string;
  category: string;
}
interface WishlistContextType {
  wishlistItems: WishlistItem[];
  addToWishlist: (item: WishlistItem) => void;
  removeFromWishlist: (id: number) => void;
  isInWishlist: (id: number) => boolean;
  wishlistCount: number;
}
const WishlistContext = createContext<WishlistContextType | undefined>(undefined);
export const WishlistProvider = ({
  children
}: {
  children: React.ReactNode;
}) => {
  const [wishlistItems, setWishlistItems] = useState<WishlistItem[]>(() => {
    const savedWishlist = localStorage.getItem('wishlist');
    return savedWishlist ? JSON.parse(savedWishlist) : [];
  });
  useEffect(() => {
    localStorage.setItem('wishlist', JSON.stringify(wishlistItems));
  }, [wishlistItems]);
  const addToWishlist = (item: WishlistItem) => {
    setWishlistItems(prevItems => {
      const exists = prevItems.find(i => i.id === item.id);
      if (exists) return prevItems;
      return [...prevItems, item];
    });
  };
  const removeFromWishlist = (id: number) => {
    setWishlistItems(prevItems => prevItems.filter(item => item.id !== id));
  };
  const isInWishlist = (id: number) => {
    return wishlistItems.some(item => item.id === id);
  };
  const wishlistCount = wishlistItems.length;
  return <WishlistContext.Provider value={{
    wishlistItems,
    addToWishlist,
    removeFromWishlist,
    isInWishlist,
    wishlistCount
  }}>
      {children}
    </WishlistContext.Provider>;
};
export const useWishlist = () => {
  const context = useContext(WishlistContext);
  if (context === undefined) {
    throw new Error('useWishlist must be used within a WishlistProvider');
  }
  return context;
};