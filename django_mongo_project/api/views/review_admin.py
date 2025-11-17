from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models.review import Review
from api.serializers.review import ReviewSerializer
from api.decorators.admin_decorators import require_admin_auth
from mongoengine.errors import DoesNotExist
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@require_admin_auth
def get_all_reviews(request):
    """
    Lấy tất cả đánh giá (admin only).
    """
    try:
        reviews = Review.objects.all().order_by('-created_at')
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching reviews: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@require_admin_auth
def delete_review(request, review_id):
    """
    Xóa đánh giá (admin only).
    """
    try:
        review = Review.objects.get(id=review_id)
        review.delete()
        
        logger.info(f"Admin {request.session.get('admin_email')} deleted review {review_id}")
        
        return Response(
            {"message": "Đánh giá đã được xóa thành công."},
            status=status.HTTP_200_OK
        )
    except DoesNotExist:
        return Response(
            {"error": "Không tìm thấy đánh giá."},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error deleting review: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PATCH'])
@require_admin_auth
def update_review_response(request, review_id):
    """
    Cập nhật phản hồi của admin cho đánh giá (admin only).
    """
    try:
        review = Review.objects.get(id=review_id)
    except DoesNotExist:
        return Response(
            {"error": "Không tìm thấy đánh giá."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    admin_response = request.data.get('admin_response')
    if not admin_response:
        return Response(
            {"error": "Thiếu trường 'admin_response'."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    review.admin_response = admin_response
    review.save()
    
    logger.info(f"Admin {request.session.get('admin_email')} updated response for review {review_id}")
    
    serializer = ReviewSerializer(review)
    return Response(
        {
            "message": "Phản hồi đánh giá đã được cập nhật.",
            "review": serializer.data
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@require_admin_auth
def get_review_statistics(request):
    """
    Lấy thống kê đánh giá (admin only).
    """
    try:
        total_reviews = Review.objects.count()
        
        if total_reviews > 0:
            all_ratings = [review.rating for review in Review.objects.all()]
            avg_rating = sum(all_ratings) / len(all_ratings)
        else:
            avg_rating = 0
        
        return Response({
            "total_reviews": total_reviews,
            "average_rating": round(avg_rating, 2)
        }, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching review statistics: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
