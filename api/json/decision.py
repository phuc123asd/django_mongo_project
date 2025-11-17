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
            
            # --- BẮT ĐẦU PHẦN XỬ LÝ VÀ KIỂM TRA ---
            name = payload.get("name")
            price = payload.get("price")
            images = payload.get("images")

            # Kiểm tra các trường bắt buộc
            missing_fields = []
            if not name:
                missing_fields.append("tên sản phẩm")
            if price is None: # Kiểm tra specifically cho None, vì 0 có thể là giá hợp lệ
                missing_fields.append("giá sản phẩm")
            if not images or len(images) < 4:
                missing_fields.append("ít nhất 4 hình ảnh sản phẩm")

            if missing_fields:
                # Nếu có trường thiếu, trả về lỗi yêu cầu bổ sung
                error_message = f"Để thêm sản phẩm, vui lòng cung cấp: {', '.join(missing_fields)}."
                print(f"   - Thông báo lỗi: {error_message}")
                return {
                    "success": False,
                    "action": "add_product",
                    "error": error_message
                }
            # --- KẾT THÚC PHẦN XỬ LÝ VÀ KIỂM TRA ---

            # Nếu đủ thông tin, trả về thông báo thành công
            return {
                "success": True, 
                "action": action, 
                "message": f"Đã nhận yêu cầu thêm sản phẩm '{name}' với giá ${price}."
            }

        elif action == "update_product":
            print(f"✏️ HÀNH ĐỘNG: CẬP NHẬT SẢN PHẨM")
            print(f"   - Dữ liệu payload: {payload}")
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
