import json
from typing import Any
from api.services.product_service import add_product, update_product, delete_product  # type: ignore
from api.services.order_service import approve_multiple_orders  # type: ignore
from api.services.order_statistics_service import OrderStatisticsService  # type: ignore

def _objects(model: Any) -> Any:
    """
    MongoEngine exposes `objects` dynamically; help Pylance understand this access.
    """
    return model.objects

def handle_admin_command(ai_response_string):
    try:
        action_data = json.loads(ai_response_string)
        print(f" Phân tích JSON thành công: {action_data}")

        action = action_data.get("action")
        payload = action_data.get("payload", {})

        if action == "add_product":
            print(f" HÀNH ĐỘNG: THÊM SẢN PHẨM MỚI")
            print(f"   - Dữ liệu payload từ AI: {payload}")
            
            # Kiểm tra các trường bắt buộc
            name = payload.get("name")
            price = payload.get("price")
            images = payload.get("images")

            missing_fields = []
            if not name: missing_fields.append("tên sản phẩm")
            if price is None: missing_fields.append("giá sản phẩm")
            if not images: missing_fields.append("hình ảnh sản phẩm")

            if missing_fields:
                error_message = f"Để thêm sản phẩm, vui lòng cung cấp: {', '.join(missing_fields)}."
                print(f"   - Thông báo lỗi: {error_message}")
                return {
                    "success": False,
                    "action": "add_product",
                    "error": error_message
                }
            
            # Nếu đủ thông tin, gọi hàm add_product để thực hiện lưu vào DB
            print("   - Dữ liệu hợp lệ, tiến hành gọi hàm add_product...")
            return add_product(payload)

        elif action == "update_product":
            print(f" HÀNH ĐỘNG: CẬP NHẬT SẢN PHẨM")
            print(f"   - Dữ liệu payload: {payload}")
            # Gọi hàm update_product để thực hiện cập nhật
            return update_product(payload)
        
        elif action == "delete_product":
            print(f" HÀNH ĐỘNG: XÓA SẢN PHẨM")
            print(f"   - Dữ liệu payload từ AI: {payload}")
            
            # Bắt buộc phải có product_id
            product_id = payload.get("product_id")

            if not product_id:
                error_message = "Để xóa sản phẩm, vui lòng cung cấp ID hoặc tên sản phẩm."
                print(f"   - Thông báo lỗi: {error_message}")
                return {
                    "success": False,
                    "action": "delete_product",
                    "error": error_message
                }

            # Nếu có product_id, gọi hàm delete_product để thực hiện
            print(f"   - product_id hợp lệ, tiến hành gọi hàm delete_product...")
            return delete_product(product_id)
        
        elif action == "approve_order":
            print(f" HÀNH ĐỘNG: DUYỆT ĐƠN HÀNG")
            print(f"   - Dữ liệu payload: {payload}")
            
            # Lấy danh sách order_id từ payload
            order_ids = payload.get("order_ids", [])
            
            # Gọi hàm approve_multiple_orders để xử lý
            return approve_multiple_orders(order_ids)
        
        elif action == "statistics":
            print(f" HÀNH ĐỘNG: THỐNG KÊ")
            print(f"   - Dữ liệu payload: {payload}")
            
            # Lấy loại thống kê và các tham số
            stats_type = payload.get("type", "overview")
            days = payload.get("days", 30)
            format_type = payload.get("format", "json")
            print(f"[HANDLE_ADMIN] Loại thống kê: {stats_type}, số ngày: {days}, định dạng: {format_type}")
            
            # Khởi tạo service thống kê
            print(f"[HANDLE_ADMIN] Khởi tạo OrderStatisticsService...")
            stats_service = OrderStatisticsService()
            
            try:
                # Gọi hàm thống kê tương ứng
                print(f"[HANDLE_ADMIN] Gọi hàm thống kê...")
                if stats_type == "overview":
                    print(f"[HANDLE_ADMIN] Gọi get_overview_statistics...")
                    stats_data = stats_service.get_overview_statistics()
                elif stats_type == "revenue":
                    print(f"[HANDLE_ADMIN] Gọi get_revenue_statistics với days={days}...")
                    stats_data = stats_service.get_revenue_statistics(days)
                elif stats_type == "geographical":
                    print(f"[HANDLE_ADMIN] Gọi get_geographical_statistics...")
                    stats_data = stats_service.get_geographical_statistics()
                elif stats_type == "products":
                    print(f"[HANDLE_ADMIN] Gọi get_product_statistics...")
                    stats_data = stats_service.get_product_statistics()
                elif stats_type == "customers":
                    print(f"[HANDLE_ADMIN] Gọi get_customer_statistics...")
                    stats_data = stats_service.get_customer_statistics()
                else:
                    return {
                        "success": False,
                        "action": "statistics",
                        "error": f"Loại thống kê không hợp lệ: {stats_type}"
                    }
                
                # Nếu yêu cầu tóm tắt, tạo tóm tắt từ dữ liệu
                if format_type == "summary":
                    print(f"[HANDLE_ADMIN] Yêu cầu tạo tóm tắt...")
                    summary = create_statistics_summary(stats_type, stats_data)
                    print(f"[HANDLE_ADMIN] Tóm tắt đã tạo: {summary}")
                    return {
                        "success": True,
                        "action": "statistics",
                        "answer": summary
                    }
                
                # Trả về dữ liệu thống kê đầy đủ
                return {
                    "success": True,
                    "action": "statistics",
                    "message": stats_data
                }
                
            except Exception as e:
                return {
                    "success": False,
                    "action": "statistics",
                    "error": f"Lỗi khi lấy thống kê: {str(e)}"
                }
        
        elif action == "none":
            # Đây là trường hợp quan trọng nhất để thông báo lỗi cho admin
            message = payload.get("message", "Đã xảy ra lỗi không xác định.")
            print(f" HÀNH ĐỘNG: KHÔNG THỰC HIỆN (NONE)")
            print(f"   - Thông báo cho Admin: {message}")
            # --- SỬA LỖI: Trả về kết quả thay vì `pass` ---
            return {"success": False, "action": action, "error": message}
        
        else:
            print(f" HÀNH ĐỘNG KHÔNG HỢP LỆ: '{action}'")
            # --- SỬA LỖI: Trả về kết quả thay vì `pass` ---
            return {"success": False, "action": "none", "error": f"Hành động không hợp lệ: {action}"}

    except json.JSONDecodeError:
        return {"success": False, "action": "none", "error": "Phản hồi từ AI không hợp lệ."}
    except Exception as e:
        return {"success": False, "action": "none", "error": f"Đã xảy ra lỗi máy chủ: {e}"}

def create_statistics_summary(stats_type, stats_data):
    """
    Tạo tóm tắt từ dữ liệu thống kê
    """
    print(f"[SUMMARY] Bắt đầu tạo tóm tắt cho loại: {stats_type}")
    print(f"[SUMMARY] Dữ liệu đầu vào: {type(stats_data)}")
    if stats_type == "overview":
        print(f"[SUMMARY] Tạo tóm tắt cho thống kê tổng quan")
        return f"""
        **Tổng quan đơn hàng:**
        - Tổng số đơn hàng: {stats_data.get('total_orders', 0)}
        - Tổng doanh thu: {stats_data.get('total_revenue', 0):,} $
        - Giá trị đơn hàng trung bình: {stats_data.get('avg_order_value', 0):,} $
        - Đơn hàng hôm nay: {stats_data.get('time_periods', {}).get('today', 0)}
        - Đơn hàng tuần này: {stats_data.get('time_periods', {}).get('this_week', 0)}
        - Đơn hàng tháng này: {stats_data.get('time_periods', {}).get('this_month', 0)}
        """
    
    elif stats_type == "revenue":
        current = stats_data.get('current_period', {})
        previous = stats_data.get('previous_period', {})
        growth = stats_data.get('growth_rate', 0)
        
        return f"""
        **Thống kê doanh thu {stats_data.get('period', '30 ngày')}:**
        - Doanh thu kỳ hiện tại: {current.get('total_revenue', 0):,} $
        - Doanh thu kỳ trước: {previous.get('total_revenue', 0):,} $
        - Tăng trưởng: {growth:.2f}%
        - Số đơn hàng kỳ hiện tại: {current.get('total_orders', 0)}
        - Giá trị đơn hàng trung bình: {current.get('avg_order_value', 0):,} $
        """
    
    elif stats_type == "products":
        top_by_quantity = stats_data.get('top_by_quantity', [])
        top_by_revenue = stats_data.get('top_by_revenue', [])
        
        summary = "**Sản phẩm bán chạy:**\n"
        if top_by_quantity:
            summary += f"- {top_by_quantity[0].get('name', 'N/A')}: {top_by_quantity[0].get('quantity', 0)} sản phẩm\n"
            summary += f"- {top_by_quantity[1].get('name', 'N/A')}: {top_by_quantity[1].get('quantity', 0)} sản phẩm\n"
            summary += f"- {top_by_quantity[2].get('name', 'N/A')}: {top_by_quantity[2].get('quantity', 0)} sản phẩm\n"
        
        summary += "\n**Sản phẩm có doanh thu cao nhất:**\n"
        if top_by_revenue:
            summary += f"- {top_by_revenue[0].get('name', 'N/A')}: {top_by_revenue[0].get('revenue', 0):,} $\n"
            summary += f"- {top_by_revenue[1].get('name', 'N/A')}: {top_by_revenue[1].get('revenue', 0):,} $\n"
            summary += f"- {top_by_revenue[2].get('name', 'N/A')}: {top_by_revenue[2].get('revenue', 0):,} $\n"
        
        return summary
    
    elif stats_type == "customers":
        total_customers = stats_data.get('total_customers', 0)
        new_vs_returning = stats_data.get('new_vs_returning', {})
        top_by_revenue = stats_data.get('top_by_revenue', [])
        
        summary = f"""
        **Thống kê khách hàng:**
        - Tổng số khách hàng: {total_customers}
        - Khách hàng mới: {new_vs_returning.get('new_customers', 0)} ({new_vs_returning.get('new_percentage', 0):.1f}%)
        - Khách hàng quay lại: {new_vs_returning.get('returning_customers', 0)}
        
        **Khách hàng có giá trị cao nhất:**
        """
        
        if top_by_revenue:
            summary += f"- {top_by_revenue[0].get('name', 'N/A')}: {top_by_revenue[0].get('total_revenue', 0):,} $\n"
            summary += f"- {top_by_revenue[1].get('name', 'N/A')}: {top_by_revenue[1].get('total_revenue', 0):,} $\n"
            summary += f"- {top_by_revenue[2].get('name', 'N/A')}: {top_by_revenue[2].get('total_revenue', 0):,} $\n"
        
        return summary
    
    else:
        return f"Đã lấy thống kê loại {stats_type} thành công."

def execute_tool_call(action, payload):
    try:
        print(f" [EXECUTE TOOL] Hành động: {action} - Payload: {payload}")
        
        if action == "add_product":
            name = payload.get("name")
            price = payload.get("price")
            images = payload.get("images")
            missing = [k for k, v in {"name": name, "price": price, "images": images}.items() if not v]
            if missing:
                return {"success": False, "action": action, "error": f"Vui lòng cung cấp: {', '.join(missing)}"}
            return add_product(payload)
            
        elif action == "update_product":
            if not payload.get("product_id"):
                return {"success": False, "action": action, "error": "Vui lòng cung cấp ID sản phẩm cần cập nhật."}
            return update_product(payload)
            
        elif action == "delete_product":
            product_id = payload.get("product_id")
            if not product_id:
                return {"success": False, "action": action, "error": "Vui lòng cung cấp ID sản phẩm cần xóa."}
            return delete_product(product_id)
            
        elif action == "approve_order":
            order_ids = payload.get("order_ids", [])
            return approve_multiple_orders(order_ids)
            
        elif action == "get_statistics":
            stats_type = payload.get("type", "overview")
            days = payload.get("days", 30)
            start_date_str = payload.get("startDate")
            end_date_str = payload.get("endDate")
            
            kwargs = {}
            if start_date_str or end_date_str:
                from datetime import datetime
                if start_date_str:
                    try:
                        kwargs['start_date'] = datetime.strptime(start_date_str, "%Y-%m-%d")
                    except ValueError: pass
                if end_date_str:
                    try:
                        # Ensure we include the entire end day 
                        kw_end = datetime.strptime(end_date_str, "%Y-%m-%d")
                        kwargs['end_date'] = kw_end.replace(hour=23, minute=59, second=59)
                    except ValueError: pass
            else:
                kwargs['days'] = days

            stats_service = OrderStatisticsService()
            
            if stats_type == "overview":
                stats_data = stats_service.get_overview_statistics()
            elif stats_type == "revenue":
                stats_data = stats_service.get_revenue_statistics(**kwargs)
            elif stats_type == "geographical":
                stats_data = stats_service.get_geographical_statistics()
            elif stats_type == "products":
                stats_data = stats_service.get_product_statistics()
            elif stats_type == "customers":
                stats_data = stats_service.get_customer_statistics()
            else:
                return {"success": False, "action": "statistics", "error": "Invalid type parameter"}
            
            summary = create_statistics_summary(stats_type, stats_data)
            return {
                "success": True, 
                "action": "statistics", 
                "answer": summary,
                "raw_data": stats_data
            }
            
        elif action == "navigate_page":
            path = payload.get("path")
            return {"success": True, "action": "navigate", "payload": {"path": path}, "message": f"Đang chuyển hướng đến {path}"}
            
        elif action == "get_orders_list":
            status = payload.get("status")
            limit = payload.get("limit", 10)
            from api.models.order import Order  # type: ignore
            from mongoengine import Q  # type: ignore
            try:
                if status:
                    orders = _objects(Order)(status__iexact=status).order_by('-created_at').limit(limit)
                else:
                    orders = _objects(Order)().order_by('-created_at').limit(limit)
                
                order_list = []
                for o in orders:
                    customer_name = "Unknown"
                    if o.customer:
                        customer_name = f"{o.customer.first_name} {o.customer.last_name}"
                        
                    order_list.append({
                        "id": str(o.id),
                        "customerName": customer_name,
                        "phone": o.phone,
                        "status": o.status,
                        "total": str(o.total_price),
                        "paymentMethod": o.payment_method,
                        "date": o.created_at.strftime("%Y-%m-%d %H:%M") if o.created_at else ""
                    })
                return {"success": True, "action": "get_orders_list", "message": "Đã lấy danh sách đơn hàng thành công", "answer": json.dumps(order_list, ensure_ascii=False)}
            except Exception as e:
                return {"success": False, "action": "get_orders_list", "error": f"Lỗi truy vấn: {e}"}
                
        elif action == "update_order_status":
            order_id = payload.get("order_id")
            new_status = payload.get("new_status")
            if not order_id or not new_status:
                return {"success": False, "action": action, "error": "Thiếu ID đơn hàng hoặc trạng thái mới"}
            from api.models.order import Order  # type: ignore
            try:
                order = _objects(Order)(id=order_id).first()
                if not order:
                    return {"success": False, "action": action, "error": f"Không tìm thấy đơn hàng {order_id}"}
                order.status = new_status
                order.save()
                return {"success": True, "action": action, "message": f"Đã cập nhật đơn hàng {order_id} thành {new_status}"}
            except Exception as e:
                return {"success": False, "action": action, "error": f"Lỗi cập nhật: {e}"}
                
        elif action == "get_users_list":
            role = payload.get("role")
            from api.models.customer import Customer  # type: ignore
            try:
                # Hiện tại Customer không có field role rõ ràng, tạm thời return danh sách
                users = _objects(Customer)().limit(20)
                
                user_list = [{"id": str(u.id), "name": f"{u.first_name} {u.last_name}", "email": u.email, "role": "N/A", "phone": getattr(u, 'phone', '')} for u in users]
                return {"success": True, "action": "get_users_list", "message": "Đã lấy danh sách khách hàng", "answer": json.dumps(user_list, ensure_ascii=False)}
            except Exception as e:
                return {"success": False, "action": "get_users_list", "error": f"Lỗi truy vấn: {e}"}
                
        elif action == "update_user_role":
            user_id = payload.get("user_id")
            new_role = payload.get("new_role")
            if not user_id or not new_role:
                return {"success": False, "action": action, "error": "Thiếu ID hoặc Role mới"}
            from api.models.customer import Customer  # type: ignore
            try:
                # Tìm bằng ID, nếu lỗi thì tìm bằng Email/Name
                from bson.errors import InvalidId  # type: ignore
                user = None
                try:
                    user = _objects(Customer)(id=user_id).first()
                except InvalidId:
                    user = _objects(Customer)(email=user_id).first() or _objects(Customer)(first_name__icontains=user_id).first()
                    
                if not user:
                    return {"success": False, "action": action, "error": f"Không tìm thấy người dùng {user_id}"}
                
                # Hiện tại DB chưa có field role, có thể pass hoặc thông báo cho frontend
                return {"success": True, "action": action, "message": f"Hệ thống hiện chưa hỗ trợ lưu role cho Customer. Đã ghi nhận yêu cầu cấp quyền {new_role} cho {user.first_name}."}
            except Exception as e:
                return {"success": False, "action": action, "error": f"Lỗi cập nhật: {e}"}
                
        elif action == "update_product_stock":
            product_id = payload.get("product_id")
            in_stock = payload.get("in_stock")
            if not product_id or in_stock is None:
                return {"success": False, "action": action, "error": "Thiếu thông tin sản phẩm hoặc trạng thái tồn kho"}
            from api.models.product import Product  # type: ignore
            from api.models.productdetail import ProductDetail  # type: ignore
            try:
                product = _objects(Product)(name__iexact=product_id).first()
                if not product:
                    from bson.errors import InvalidId  # type: ignore
                    try:
                        product = _objects(Product)(id=product_id).first()
                    except InvalidId:
                        return {"success": False, "action": action, "error": "Không tìm thấy sản phẩm"}
                
                detail = _objects(ProductDetail)(product=product).first()
                if detail:
                    detail.inStock = in_stock
                    detail.save()
                    status_text = "Còn hàng" if in_stock else "Hết hàng"
                    return {"success": True, "action": action, "message": f"Sản phẩm {product.name} đã cập nhật kho thành: {status_text}"}
                else:
                    return {"success": False, "action": action, "error": "Sản phẩm này không có file chi tiết"}
            except Exception as e:
                return {"success": False, "action": action, "error": f"Lỗi cập nhật kho: {e}"}
                
        elif action == "draw_chart":
            # Just pass the chart data payload back to the UI at the top level
            result = {
                "success": True, 
                "action": "draw_chart", 
                "answer": payload.get("description", "Dưới đây là biểu đồ bạn yêu cầu:")
            }
            result.update(payload)
            return result
            
        else:
             return {"success": False, "action": "none", "error": f"Hành động không hợp lệ: {action}"}
             
    except Exception as e:
        print(f" Lỗi khi thực thi {action}: {e}")
        return {"success": False, "action": action, "error": f"Lỗi thực thi dữ liệu máy chủ: {e}"}
