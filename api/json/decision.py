import json
from api.services.product_service import *
from api.services.order_service import *
from api.services.order_statistics_service import OrderStatisticsService

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
                        "type": stats_type,
                        "summary": summary
                    }
                
                # Trả về dữ liệu thống kê đầy đủ
                return {
                    "success": True,
                    "action": "statistics",
                    "type": stats_type,
                    "data": stats_data
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
        - Tổng doanh thu: {stats_data.get('total_revenue', 0):,} VNĐ
        - Giá trị đơn hàng trung bình: {stats_data.get('avg_order_value', 0):,} VNĐ
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
        - Doanh thu kỳ hiện tại: {current.get('total_revenue', 0):,} VNĐ
        - Doanh thu kỳ trước: {previous.get('total_revenue', 0):,} VNĐ
        - Tăng trưởng: {growth:.2f}%
        - Số đơn hàng kỳ hiện tại: {current.get('total_orders', 0)}
        - Giá trị đơn hàng trung bình: {current.get('avg_order_value', 0):,} VNĐ
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
            summary += f"- {top_by_revenue[0].get('name', 'N/A')}: {top_by_revenue[0].get('revenue', 0):,} VNĐ\n"
            summary += f"- {top_by_revenue[1].get('name', 'N/A')}: {top_by_revenue[1].get('revenue', 0):,} VNĐ\n"
            summary += f"- {top_by_revenue[2].get('name', 'N/A')}: {top_by_revenue[2].get('revenue', 0):,} VNĐ\n"
        
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
            summary += f"- {top_by_revenue[0].get('name', 'N/A')}: {top_by_revenue[0].get('total_revenue', 0):,} VNĐ\n"
            summary += f"- {top_by_revenue[1].get('name', 'N/A')}: {top_by_revenue[1].get('total_revenue', 0):,} VNĐ\n"
            summary += f"- {top_by_revenue[2].get('name', 'N/A')}: {top_by_revenue[2].get('total_revenue', 0):,} VNĐ\n"
        
        return summary
    
    else:
        return f"Đã lấy thống kê loại {stats_type} thành công."