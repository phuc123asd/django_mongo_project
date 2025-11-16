import json

def handle_admin_command(ai_response_string):
    try:
        action_data = json.loads(ai_response_string)
        print(f"✅ Phân tích JSON thành công: {action_data}")

        action = action_data.get("action")
        payload = action_data.get("payload", {})

        if action == "add_product":
            print(f"🚀 HÀNH ĐỘNG: THÊM SẢN PHẨM MỚI")
            print(f"   - Dữ liệu payload: {payload}")
            # TODO: Gọi hàm thêm sản phẩm vào database của bạn ở đây
            # Trả về thông báo thành công cho frontend
            return {
                "success": True, 
                "action": action, 
                "message": f"Đã nhận yêu cầu thêm sản phẩm '{payload.get('name', 'không xác định')}' với giá ${payload.get('price', 0)}."
            }

        elif action == "update_product":
            print(f"✏️ HÀNH ĐỘNG: CẬP NHẬT SẢN PHẨM")
            print(f"   - Dữ liệu payload: {payload}")
            return {
                "success": True, 
                "action": action, 
                "message": f"Đã nhận yêu cầu cập nhật sản phẩm '{payload.get('product_id', 'không xác định')}'."
            }

        # ... (làm tương tự cho các action khác) ...
        elif action == "none":
            # Đây là trường hợp quan trọng nhất để thông báo lỗi cho admin
            message = payload.get("message", "Đã xảy ra lỗi không xác định.")
            print(f"🛑 HÀNH ĐỘNG: KHÔNG THỰC HIỆN (NONE)")
            print(f"   - Thông báo cho Admin: {message}")
            # Trả về lỗi cho frontend để hiển thị
            return {"success": False, "action": action, "error": message}

        else:
            print(f"❓ HÀNH ĐỘNG KHÔNG HỢP LỆ: '{action}'")
            return {"success": False, "action": "none", "error": f"Hành động không hợp lệ: {action}"}

    except json.JSONDecodeError:
        print(f"🚨 LỖI: Không thể phân tích JSON từ AI. Phản hồi nhận được: '{ai_response_string}'")
        return {"success": False, "action": "none", "error": "Phản hồi từ AI không hợp lệ."}
    except Exception as e:
        print(f"🚨 LỖI KHÔNG XÁC ĐỊNH: {e}")
        return {"success": False, "action": "none", "error": "Đã xảy ra lỗi máy chủ."}
