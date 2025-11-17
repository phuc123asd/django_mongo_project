import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { useAuth } from '../hooks/useAuth';
import { SmartphoneIcon } from 'lucide-react';
export function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const {
    login
  } = useAuth();
  const navigate = useNavigate();
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(email, password);
      navigate('/');
    } catch (err) {
      setError('Invalid email or password');
    } finally {
      setLoading(false);
    }
  };
  return <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-full mb-4">
            <SmartphoneIcon className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900">TechStore Admin</h1>
          <p className="text-gray-600 mt-2">Sign in to your dashboard</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input label="Email" type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="admin@techstore.com" required />

          <Input label="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Enter your password" required error={error} />

          <div className="flex items-center">
            <input type="checkbox" id="remember" className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500" />
            <label htmlFor="remember" className="ml-2 text-sm text-gray-600">
              Remember me
            </label>
          </div>

          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign In'}
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Demo credentials: any email and password
          </p>
        </div>
      </Card>
    </div>;
}