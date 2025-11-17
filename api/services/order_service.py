# api/services/order_service.py
from api.models.order import Order
from bson.errors import InvalidId
from mongoengine.errors import DoesNotExist

def approve_multiple_orders(order_ids):
    """
    Duyệt nhiều đơn hàng hoặc tất cả đơn hàng.
    
    Args:
        order_ids: Mảng chứa các ID đơn hàng cần duyệt. Nếu mảng rỗng, sẽ duyệt tất cả đơn hàng có trạng thái "Đang Xử Lý".
    
    Returns:
        dict: Kết quả xử lý với thông báo chi tiết
    """
    try:
        # Nếu không có order_ids, duyệt tất cả đơn hàng đang xử lý
        if not order_ids:
            orders_to_approve = Order.objects(status='Đang Xử Lý')
            if not orders_to_approve:
                return {
                    "success": False,
                    "action": "approve_order",
                    "error": "Không có đơn hàng nào đang chờ xử lý."
                }
            
            # Cập nhật trạng thái tất cả đơn hàng
            count = 0
            for order in orders_to_approve:
                order.status = 'Đang Vận Chuyển'
                order.save()
                count += 1
                
            return {
                "success": True,
                "action": "approve_order",
                "message": f"Đã duyệt thành công {count} đơn hàng. Trạng thái đã được cập nhật thành 'Đang Vận Chuyển'."
            }
        
        # Nếu có order_ids, chỉ duyệt các đơn hàng trong danh sách
        approved_count = 0
        failed_orders = []
        
        for order_id in order_ids:
            try:
                order = Order.objects(id=order_id).first()
                if not order:
                    failed_orders.append(f"Đơn hàng {order_id} không tồn tại")
                    continue
                    
                if order.status != 'Đang Xử Lý':
                    failed_orders.append(f"Đơn hàng {order_id} không ở trạng thái 'Đang Xử Lý'")
                    continue
                    
                order.status = 'Đang Vận Chuyển'
                order.save()
                approved_count += 1
                
            except InvalidId:
                failed_orders.append(f"ID đơn hàng {order_id} không hợp lệ")
            except Exception as e:
                failed_orders.append(f"Lỗi khi duyệt đơn hàng {order_id}: {str(e)}")
        
        if approved_count == 0:
            error_message = "Không thể duyệt bất kỳ đơn hàng nào. " + "; ".join(failed_orders)
            return {
                "success": False,
                "action": "approve_order",
                "error": error_message
            }
        
        message = f"Đã duyệt thành công {approved_count} đơn hàng."
        if failed_orders:
            message += f" Lỗi: {'; '.join(failed_orders)}"
            
        return {
            "success": True,
            "action": "approve_order",
            "message": message
        }
        
    except Exception as e:
        return {
            "success": False,
            "action": "approve_order",
            "error": f"Đã xảy ra lỗi khi duyệt đơn hàng: {str(e)}"
        }