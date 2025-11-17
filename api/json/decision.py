import json
from api.services.product_service import add_product

def handle_admin_command(ai_response_string):
    try:
        action_data = json.loads(ai_response_string)
        print(f"✅ Phân tích JSON thành công: {action_data}")

        action = action_data.get("action")
        payload = action_data.get("payload", {})

        if action == "add_product":
            print(f"🚀 HÀNH ĐỘNG: THÊM SẢN PHẨM MỚI")
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
            print(f"✏️ HÀNH ĐỘNG: CẬP NHẬT SẢN PHẨM")
            print(f"   - Dữ liệu payload: {payload}")
            # --- SỬA LỖI: Trả về kết quả thay vì `pass` ---
            return {
                "success": True, 
                "action": action, 
                "message": f"Đã nhận yêu cầu cập nhật sản phẩm '{payload.get('product_id', 'không xác định')}'."
            }
        elif action == "none":
            # Đây là trường hợp quan trọng nhất để thông báo lỗi cho admin
            message = payload.get("message", "Đã xảy ra lỗi không xác định.")
            print(f"🛑 HÀNH ĐỘNG: KHÔNG THỰC HIỆN (NONE)")
            print(f"   - Thông báo cho Admin: {message}")
            # --- SỬA LỖI: Trả về kết quả thay vì `pass` ---
            return {"success": False, "action": action, "error": message}
        else:
            print(f"❓ HÀNH ĐỘNG KHÔNG HỢP LỆ: '{action}'")
            # --- SỬA LỖI: Trả về kết quả thay vì `pass` ---
            return {"success": False, "action": "none", "error": f"Hành động không hợp lệ: {action}"}

    except json.JSONDecodeError:
        return {"success": False, "action": "none", "error": "Phản hồi từ AI không hợp lệ."}
    except Exception as e:
        return {"success": False, "action": "none", "error": f"Đã xảy ra lỗi máy chủ: {e}"}