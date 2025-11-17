import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './hooks/useAuth';
import { Layout } from './components/layout/Layout';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';
import { ChatPage } from './pages/ChatPage';
import { ProductsPage } from './pages/ProductsPage';
import { OrdersPage } from './pages/OrdersPage';
import { UsersPage } from './pages/UsersPage';
import { ReviewsPage } from './pages/ReviewsPage';
function ProtectedRoute({
  children
}: {
  children: React.ReactNode;
}) {
  const {
    isAuthenticated
  } = useAuth();
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
}
function AppRoutes() {
  const {
    isAuthenticated
  } = useAuth();
  return <Routes>
      <Route path="/login" element={isAuthenticated ? <Navigate to="/" /> : <LoginPage />} />
      <Route path="/*" element={<ProtectedRoute>
            <Layout>
              <Routes>
                <Route path="/" element={<DashboardPage />} />
                <Route path="/chat" element={<ChatPage />} />
                <Route path="/products" element={<ProductsPage />} />
                <Route path="/orders" element={<OrdersPage />} />
                <Route path="/users" element={<UsersPage />} />
                <Route path="/reviews" element={<ReviewsPage />} />
              </Routes>
            </Layout>
          </ProtectedRoute>} />
    </Routes>;
}
export function App() {
  return <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>;
}