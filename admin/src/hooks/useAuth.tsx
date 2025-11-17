import React, { useState, createContext, useContext } from 'react';
interface AuthContextType {
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}
const AuthContext = createContext<AuthContextType | undefined>(undefined);
export function AuthProvider({
  children
}: {
  children: ReactNode;
}) {
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return localStorage.getItem('isAuthenticated') === 'true';
  });
  const login = async (email: string, password: string) => {
    // Mock authentication - in production, this would call an API
    if (email && password) {
      setIsAuthenticated(true);
      localStorage.setItem('isAuthenticated', 'true');
    } else {
      throw new Error('Invalid credentials');
    }
  };
  const logout = () => {
    setIsAuthenticated(false);
    localStorage.removeItem('isAuthenticated');
  };
  return <AuthContext.Provider value={{
    isAuthenticated,
    login,
    logout
  }}>
      {children}
    </AuthContext.Provider>;
}
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}