import React, { useEffect, useState, createContext, useContext } from 'react';
interface CartItem {
  id: number;
  name: string;
  price: number;
  image: string;
  quantity: number;
  variant?: string;
}
interface CartContextType {
  cartItems: CartItem[];
  addToCart: (item: Omit<CartItem, 'quantity'>) => void;
  removeFromCart: (id: number) => void;
  updateQuantity: (id: number, quantity: number) => void;
  clearCart: () => void;
  cartTotal: number;
  cartCount: number;
}
const CartContext = createContext<CartContextType | undefined>(undefined);
export const CartProvider = ({
  children
}: {
  children: React.ReactNode;
}) => {
  const [cartItems, setCartItems] = useState<CartItem[]>(() => {
    const savedCart = localStorage.getItem('cart');
    return savedCart ? JSON.parse(savedCart) : [];
  });
  useEffect(() => {
    localStorage.setItem('cart', JSON.stringify(cartItems));
  }, [cartItems]);
  const addToCart = (item: Omit<CartItem, 'quantity'>) => {
    setCartItems(prevItems => {
      const existingItem = prevItems.find(i => i.id === item.id);
      if (existingItem) {
        return prevItems.map(i => i.id === item.id ? {
          ...i,
          quantity: i.quantity + 1
        } : i);
      }
      return [...prevItems, {
        ...item,
        quantity: 1
      }];
    });
  };
  const removeFromCart = (id: number) => {
    setCartItems(prevItems => prevItems.filter(item => item.id !== id));
  };
  const updateQuantity = (id: number, quantity: number) => {
    if (quantity <= 0) {
      removeFromCart(id);
      return;
    }
    setCartItems(prevItems => prevItems.map(item => item.id === id ? {
      ...item,
      quantity
    } : item));
  };
  const clearCart = () => {
    setCartItems([]);
  };
  const cartTotal = cartItems.reduce((total, item) => total + item.price * item.quantity, 0);
  const cartCount = cartItems.reduce((count, item) => count + item.quantity, 0);
  return <CartContext.Provider value={{
    cartItems,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart,
    cartTotal,
    cartCount
  }}>
      {children}
    </CartContext.Provider>;
};
export const useCart = () => {
  const context = useContext(CartContext);
  if (context === undefined) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};
