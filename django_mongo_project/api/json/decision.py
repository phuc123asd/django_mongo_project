import json
import logging
from api.models.product import Product
from api.models.order import Order
from api.models.review import Review
from mongoengine.errors import DoesNotExist, ValidationError

logger = logging.getLogger(__name__)


def handle_admin_command(ai_response_string):
    """
    Xử lý các lệnh admin từ AI chatbot và thực thi chúng.
    """
    try:
        action_data = json.loads(ai_response_string)
        logger.info(f"Parsed JSON successfully: {action_data}")

        action = action_data.get("action")
        payload = action_data.get("payload", {})

        if action == "add_product":
            return execute_add_product(payload)
        
        elif action == "update_product":
            return execute_update_product(payload)
        
        elif action == "delete_product":
            return execute_delete_product(payload)
        
        elif action == "approve_order":
            return execute_approve_order(payload)
        
        elif action == "reject_order":
            return execute_reject_order(payload)
        
        elif action == "get_order_status":
            return execute_get_order_status(payload)
        
        elif action == "reply_feedback":
            return execute_reply_feedback(payload)
        
        elif action == "none":
            message = payload.get("message", "Không hiểu yêu cầu.")
            return {"success": False, "action": action, "error": message}
        
        else:
            return {"success": False, "action": "none", "error": f"Hành động không hợp lệ: {action}"}

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return {"success": False, "action": "none", "error": "Phản hồi từ AI không hợp lệ."}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"success": False, "action": "none", "error": f"Lỗi hệ thống: {str(e)}"}


def execute_add_product(payload):
    """
    Thêm sản phẩm mới vào database.
    """
    try:
        name = payload.get('name')
        price = payload.get('price')
        images = payload.get('images', [])
        
        if not name or not price:
            return {
                "success": False,
                "action": "add_product",
                "error": "Thiếu thông tin name hoặc price."
            }
        
        image_url = images[0] if images else "https://via.placeholder.com/400"
        
        product = Product(
            name=name,
            price=price,
            originalPrice=price,
            image=image_url,
            rating=0,
            category=payload.get('category', 'Uncategorized'),
            brand=payload.get('brand', 'Unknown'),
            isNew=True
        )
        product.save()
        
        logger.info(f"Product '{name}' added successfully with ID: {product.id}")
        
        return {
            "success": True,
            "action": "add_product",
            "message": f"✅ Đã thêm sản phẩm '{name}' với giá ${price}. ID: {product.id}"
        }
    
    except Exception as e:
        logger.error(f"Error adding product: {e}")
        return {
            "success": False,
            "action": "add_product",
            "error": f"Lỗi khi thêm sản phẩm: {str(e)}"
        }


def execute_update_product(payload):
    """
    Cập nhật sản phẩm.
    """
    try:
        product_id = payload.get('product_id')
        field = payload.get('field')
        value = payload.get('value')
        
        if not product_id or not field or value is None:
            return {
                "success": False,
                "action": "update_product",
                "error": "Thiếu thông tin product_id, field hoặc value."
            }
        
        product = Product.objects.get(id=product_id)
        setattr(product, field, value)
        product.save()
        
        logger.info(f"Product {product_id} updated: {field} = {value}")
        
        return {
            "success": True,
            "action": "update_product",
            "message": f"✅ Đã cập nhật sản phẩm '{product.name}': {field} = {value}"
        }
    
    except DoesNotExist:
        return {
            "success": False,
            "action": "update_product",
            "error": f"Không tìm thấy sản phẩm với ID: {product_id}"
        }
    except Exception as e:
        logger.error(f"Error updating product: {e}")
        return {
            "success": False,
            "action": "update_product",
            "error": f"Lỗi khi cập nhật sản phẩm: {str(e)}"
        }


def execute_delete_product(payload):
    """
    Xóa sản phẩm.
    """
    try:
        product_id = payload.get('product_id')
        
        if not product_id:
            return {
                "success": False,
                "action": "delete_product",
                "error": "Thiếu thông tin product_id."
            }
        
        product = Product.objects.get(id=product_id)
        product_name = product.name
        product.delete()
        
        logger.info(f"Product '{product_name}' deleted")
        
        return {
            "success": True,
            "action": "delete_product",
            "message": f"✅ Đã xóa sản phẩm '{product_name}'"
        }
    
    except DoesNotExist:
        return {
            "success": False,
            "action": "delete_product",
            "error": f"Không tìm thấy sản phẩm với ID: {product_id}"
        }
    except Exception as e:
        logger.error(f"Error deleting product: {e}")
        return {
            "success": False,
            "action": "delete_product",
            "error": f"Lỗi khi xóa sản phẩm: {str(e)}"
        }


def execute_approve_order(payload):
    """
    Duyệt đơn hàng (chuyển sang trạng thái Đang Vận Chuyển).
    """
    try:
        order_id = payload.get('order_id')
        
        if not order_id:
            return {
                "success": False,
                "action": "approve_order",
                "error": "Thiếu thông tin order_id."
            }
        
        order = Order.objects.get(id=order_id)
        order.status = 'Đang Vận Chuyển'
        order.save()
        
        logger.info(f"Order {order_id} approved")
        
        return {
            "success": True,
            "action": "approve_order",
            "message": f"✅ Đã duyệt đơn hàng {order_id}. Trạng thái: Đang Vận Chuyển"
        }
    
    except DoesNotExist:
        return {
            "success": False,
            "action": "approve_order",
            "error": f"Không tìm thấy đơn hàng với ID: {order_id}"
        }
    except Exception as e:
        logger.error(f"Error approving order: {e}")
        return {
            "success": False,
            "action": "approve_order",
            "error": f"Lỗi khi duyệt đơn hàng: {str(e)}"
        }


def execute_reject_order(payload):
    """
    Từ chối đơn hàng (xóa đơn hàng).
    """
    try:
        order_id = payload.get('order_id')
        reason = payload.get('reason', 'Không nêu lý do')
        
        if not order_id:
            return {
                "success": False,
                "action": "reject_order",
                "error": "Thiếu thông tin order_id."
            }
        
        order = Order.objects.get(id=order_id)
        order.delete()
        
        logger.info(f"Order {order_id} rejected. Reason: {reason}")
        
        return {
            "success": True,
            "action": "reject_order",
            "message": f"✅ Đã từ chối và xóa đơn hàng {order_id}. Lý do: {reason}"
        }
    
    except DoesNotExist:
        return {
            "success": False,
            "action": "reject_order",
            "error": f"Không tìm thấy đơn hàng với ID: {order_id}"
        }
    except Exception as e:
        logger.error(f"Error rejecting order: {e}")
        return {
            "success": False,
            "action": "reject_order",
            "error": f"Lỗi khi từ chối đơn hàng: {str(e)}"
        }


def execute_get_order_status(payload):
    """
    Kiểm tra trạng thái đơn hàng.
    """
    try:
        order_id = payload.get('order_id')
        
        if not order_id:
            return {
                "success": False,
                "action": "get_order_status",
                "error": "Thiếu thông tin order_id."
            }
        
        order = Order.objects.get(id=order_id)
        
        return {
            "success": True,
            "action": "get_order_status",
            "message": f"📦 Đơn hàng {order_id}:\n- Trạng thái: {order.status}\n- Tổng tiền: ${order.total_price}\n- Khách hàng: {order.customer.email if order.customer else 'Unknown'}"
        }
    
    except DoesNotExist:
        return {
            "success": False,
            "action": "get_order_status",
            "error": f"Không tìm thấy đơn hàng với ID: {order_id}"
        }
    except Exception as e:
        logger.error(f"Error getting order status: {e}")
        return {
            "success": False,
            "action": "get_order_status",
            "error": f"Lỗi khi kiểm tra đơn hàng: {str(e)}"
        }


def execute_reply_feedback(payload):
    """
    Trả lời đánh giá/phản hồi.
    """
    try:
        feedback_id = payload.get('feedback_id')
        reply = payload.get('reply')
        
        if not feedback_id or not reply:
            return {
                "success": False,
                "action": "reply_feedback",
                "error": "Thiếu thông tin feedback_id hoặc reply."
            }
        
        review = Review.objects.get(id=feedback_id)
        review.admin_response = reply
        review.save()
        
        logger.info(f"Replied to review {feedback_id}")
        
        return {
            "success": True,
            "action": "reply_feedback",
            "message": f"✅ Đã trả lời đánh giá {feedback_id}"
        }
    
    except DoesNotExist:
        return {
            "success": False,
            "action": "reply_feedback",
            "error": f"Không tìm thấy đánh giá với ID: {feedback_id}"
        }
    except Exception as e:
        logger.error(f"Error replying to feedback: {e}")
        return {
            "success": False,
            "action": "reply_feedback",
            "error": f"Lỗi khi trả lời đánh giá: {str(e)}"
        }
