from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models.product import Product
from api.models.customer import Customer
from api.models.order import Order
from api.models.review import Review
from api.decorators.admin_decorators import require_admin_auth
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@require_admin_auth
def get_dashboard_statistics(request):
    """
    Lấy tất cả thống kê cho admin dashboard.
    Returns:
        - User stats
        - Order stats
        - Product stats
        - Review stats
        - Revenue data
        - Recent orders
        - Low stock products
        - Top products
        - Recent reviews
    """
    try:
        total_customers = Customer.objects.count()
        
        total_orders = Order.objects.count()
        pending_orders = Order.objects.filter(status='Đang Xử Lý').count()
        shipping_orders = Order.objects.filter(status='Đang Vận Chuyển').count()
        completed_orders = Order.objects.filter(status='Đã Giao').count()
        
        total_revenue = sum(float(order.total_price) for order in Order.objects.all())
        
        total_products = Product.objects.count()
        
        total_reviews = Review.objects.count()
        if total_reviews > 0:
            all_ratings = [review.rating for review in Review.objects.all()]
            avg_rating = sum(all_ratings) / len(all_ratings)
        else:
            avg_rating = 0
        
        recent_orders = []
        for order in Order.objects.all().order_by('-created_at')[:5]:
            customer_name = f"{order.customer.first_name} {order.customer.last_name}" if order.customer else "Unknown"
            product_name = order.items[0].product.name if order.items and len(order.items) > 0 else "N/A"
            
            recent_orders.append({
                "id": str(order.id),
                "customer": customer_name,
                "product": product_name,
                "amount": float(order.total_price),
                "status": order.status.lower().replace(' ', '_'),
                "date": order.created_at.strftime('%Y-%m-%d')
            })
        
        recent_reviews_data = []
        for review in Review.objects.all().order_by('-created_at')[:5]:
            customer_name = f"{review.customer.first_name} {review.customer.last_name}" if review.customer else "Anonymous"
            
            recent_reviews_data.append({
                "id": str(review.id),
                "customer": customer_name,
                "product": str(review.product_id),
                "rating": review.rating,
                "comment": review.comment,
                "date": review.created_at.strftime('%Y-%m-%d')
            })
        
        product_list = []
        for product in Product.objects.all()[:10]:
            product_list.append({
                "id": str(product.id),
                "name": product.name,
                "price": float(product.price),
                "rating": product.rating,
                "category": product.category,
                "brand": product.brand
            })
        
        return Response({
            "userStats": {
                "total": total_customers,
                "active": total_customers,
                "recent": 0,
                "trend": "+0%"
            },
            "orderStats": {
                "total": total_orders,
                "pending": pending_orders,
                "completed": completed_orders,
                "revenue": total_revenue,
                "trend": "+0%"
            },
            "productStats": {
                "total": total_products,
                "lowStock": 0,
                "outOfStock": 0,
                "trend": "+0%"
            },
            "reviewStats": {
                "avgRating": round(avg_rating, 2),
                "total": total_reviews,
                "recent": 0,
                "trend": "+0.0"
            },
            "revenueData": [
                {"date": "Mon", "revenue": 0},
                {"date": "Tue", "revenue": 0},
                {"date": "Wed", "revenue": 0},
                {"date": "Thu", "revenue": 0},
                {"date": "Fri", "revenue": 0},
                {"date": "Sat", "revenue": 0},
                {"date": "Sun", "revenue": 0}
            ],
            "recentOrders": recent_orders,
            "lowStockProducts": [],
            "topProducts": product_list[:4],
            "recentReviews": recent_reviews_data
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        logger.error(f"Error fetching dashboard statistics: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
