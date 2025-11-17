import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './contexts/ThemeContext';
import { CartProvider } from './contexts/CartContext';
import { WishlistProvider } from './contexts/WishlistContext';
import { AuthProvider } from './contexts/AuthContext';
import { ReviewProvider } from './contexts/ReviewContext';
import { Layout } from './components/layout/Layout';
import { Home } from './pages/Home';
import { Shop } from './pages/Shop';
import { About } from './pages/About';
import { Contact } from './pages/Contact';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Cart } from './pages/Cart';
import { Wishlist } from './pages/Wishlist';
import { ProductDetail } from './pages/ProductDetail';
import { Checkout } from './pages/Checkout';
import { OrderDetail } from './pages/OrderDetail';
import { Orders } from './pages/Orders';
import { Profile } from './pages/Profile';
export function App() {
  return <ThemeProvider>
      <AuthProvider>
        <ReviewProvider>
          <CartProvider>
            <WishlistProvider>
              <Router>
                <Layout>
                  <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/shop" element={<Shop />} />
                    <Route path="/about" element={<About />} />
                    <Route path="/contact" element={<Contact />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/cart" element={<Cart />} />
                    <Route path="/wishlist" element={<Wishlist />} />
                    <Route path="/product/:id" element={<ProductDetail />} />
                    <Route path="/checkout" element={<Checkout />} />
                    <Route path="/orders" element={<Orders />} />
                    <Route path="/orders/:orderId" element={<OrderDetail />} />
                    <Route path="/profile" element={<Profile />} />
                    <Route path="*" element={<Home />} />
                  </Routes>
                </Layout>
              </Router>
            </WishlistProvider>
          </CartProvider>
        </ReviewProvider>
      </AuthProvider>
    </ThemeProvider>;
}