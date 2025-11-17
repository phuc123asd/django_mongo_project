// Mock data for demonstration purposes

export const userStats = {
  total: 1234,
  active: 856,
  recent: 45,
  trend: '+12%'
};
export const orderStats = {
  total: 2891,
  pending: 23,
  completed: 2868,
  revenue: 145890,
  trend: '+8%'
};
export const productStats = {
  total: 156,
  lowStock: 8,
  outOfStock: 3,
  trend: '+5%'
};
export const reviewStats = {
  avgRating: 4.5,
  total: 892,
  recent: 34,
  trend: '+0.2'
};
export const revenueData = [{
  date: 'Mon',
  revenue: 18500
}, {
  date: 'Tue',
  revenue: 22300
}, {
  date: 'Wed',
  revenue: 19800
}, {
  date: 'Thu',
  revenue: 25100
}, {
  date: 'Fri',
  revenue: 28900
}, {
  date: 'Sat',
  revenue: 31200
}, {
  date: 'Sun',
  revenue: 26400
}];
export const recentOrders = [{
  id: 'ORD-001',
  customer: 'John Doe',
  product: 'iPhone 15 Pro',
  amount: 1299,
  status: 'completed',
  date: '2024-01-15'
}, {
  id: 'ORD-002',
  customer: 'Jane Smith',
  product: 'Samsung Galaxy S24',
  amount: 999,
  status: 'pending',
  date: '2024-01-15'
}, {
  id: 'ORD-003',
  customer: 'Mike Johnson',
  product: 'AirPods Pro',
  amount: 249,
  status: 'completed',
  date: '2024-01-14'
}, {
  id: 'ORD-004',
  customer: 'Sarah Williams',
  product: 'iPad Air',
  amount: 599,
  status: 'completed',
  date: '2024-01-14'
}, {
  id: 'ORD-005',
  customer: 'Tom Brown',
  product: 'MacBook Pro',
  amount: 2499,
  status: 'pending',
  date: '2024-01-13'
}];
export const lowStockProducts = [{
  id: 1,
  name: 'iPhone 15 Pro Max',
  stock: 3,
  threshold: 10
}, {
  id: 2,
  name: 'Samsung Galaxy Buds',
  stock: 5,
  threshold: 15
}, {
  id: 3,
  name: 'Apple Watch Series 9',
  stock: 2,
  threshold: 10
}, {
  id: 4,
  name: 'Google Pixel 8',
  stock: 4,
  threshold: 12
}];
export const topProducts = [{
  id: 1,
  name: 'iPhone 15 Pro',
  sales: 234,
  rating: 4.8,
  revenue: 303666
}, {
  id: 2,
  name: 'Samsung Galaxy S24',
  sales: 189,
  rating: 4.6,
  revenue: 188811
}, {
  id: 3,
  name: 'AirPods Pro',
  sales: 456,
  rating: 4.7,
  revenue: 113544
}, {
  id: 4,
  name: 'iPad Air',
  sales: 167,
  rating: 4.5,
  revenue: 100033
}];
export const recentReviews = [{
  id: 1,
  product: 'iPhone 15 Pro',
  customer: 'John Doe',
  rating: 5,
  comment: 'Amazing phone! The camera quality is outstanding and the performance is incredible.',
  date: '2024-01-15'
}, {
  id: 2,
  product: 'Samsung Galaxy S24',
  customer: 'Jane Smith',
  rating: 4,
  comment: 'Great phone overall, but battery life could be better. Display is gorgeous.',
  date: '2024-01-14'
}, {
  id: 3,
  product: 'AirPods Pro',
  customer: 'Mike Johnson',
  rating: 5,
  comment: "Best earbuds I've ever owned. Noise cancellation is top-notch.",
  date: '2024-01-14'
}];