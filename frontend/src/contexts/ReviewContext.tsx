import React, { createContext, useContext, useState, useEffect } from 'react';

export interface Review {
  id: number;
  productId: number;
  userId: number;
  userName: string;
  userAvatar: string;
  rating: number;
  date: string;
  comment: string;
  helpful: number;
}

interface ReviewContextType {
  reviews: Review[];
  getProductReviews: (productId: number) => Review[];
  addReview: (review: Omit<Review, 'id' | 'date' | 'helpful'>) => void;
  updateReview: (reviewId: number, comment: string, rating: number) => void;
  deleteReview: (reviewId: number) => void;
  markHelpful: (reviewId: number) => void;
}

const ReviewContext = createContext<ReviewContextType | undefined>(undefined);

const initialReviews: Review[] = [
  {
    id: 1,
    productId: 1,
    userId: 1,
    userName: 'John Smith',
    userAvatar: 'https://randomuser.me/api/portraits/men/1.jpg',
    rating: 5,
    date: '2024-01-15',
    comment: 'Absolutely love this phone! The camera quality is outstanding and the titanium design feels premium. Best iPhone yet!',
    helpful: 24
  },
  {
    id: 2,
    productId: 1,
    userId: 2,
    userName: 'Sarah Johnson',
    userAvatar: 'https://randomuser.me/api/portraits/women/2.jpg',
    rating: 4,
    date: '2024-01-10',
    comment: 'Great phone overall. The A17 Pro chip is incredibly fast. Only minor complaint is the price, but you get what you pay for.',
    helpful: 18
  },
  {
    id: 3,
    productId: 1,
    userId: 3,
    userName: 'Michael Chen',
    userAvatar: 'https://randomuser.me/api/portraits/men/3.jpg',
    rating: 5,
    date: '2024-01-05',
    comment: 'The battery life is impressive and the USB-C port is a welcome change. Highly recommend for anyone upgrading from an older iPhone.',
    helpful: 32
  }
];

export const ReviewProvider = ({ children }: { children: React.ReactNode }) => {
  const [reviews, setReviews] = useState<Review[]>(() => {
    const savedReviews = localStorage.getItem('reviews');
    return savedReviews ? JSON.parse(savedReviews) : initialReviews;
  });

  useEffect(() => {
    localStorage.setItem('reviews', JSON.stringify(reviews));
  }, [reviews]);

  const getProductReviews = (productId: number) => {
    return reviews.filter(review => review.productId === productId);
  };

  const addReview = (review: Omit<Review, 'id' | 'date' | 'helpful'>) => {
    const newReview: Review = {
      ...review,
      id: Date.now(),
      date: new Date().toISOString().split('T')[0],
      helpful: 0
    };
    setReviews(prev => [newReview, ...prev]);
  };

  const updateReview = (reviewId: number, comment: string, rating: number) => {
    setReviews(prev => 
      prev.map(review => 
        review.id === reviewId 
          ? { ...review, comment, rating, date: new Date().toISOString().split('T')[0] }
          : review
      )
    );
  };

  const deleteReview = (reviewId: number) => {
    setReviews(prev => prev.filter(review => review.id !== reviewId));
  };

  const markHelpful = (reviewId: number) => {
    setReviews(prev => 
      prev.map(review => 
        review.id === reviewId 
          ? { ...review, helpful: review.helpful + 1 }
          : review
      )
    );
  };

  return (
    <ReviewContext.Provider value={{ 
      reviews, 
      getProductReviews, 
      addReview, 
      updateReview, 
      deleteReview, 
      markHelpful 
    }}>
      {children}
    </ReviewContext.Provider>
  );
};

export const useReviews = () => {
  const context = useContext(ReviewContext);
  if (context === undefined) {
    throw new Error('useReviews must be used within a ReviewProvider');
  }
  return context;
};
