import json

def handle_admin_command(ai_response_string):
    try:
        action_data = json.loads(ai_response_string)

        # Bước 2: Xử lý trường hợp phản hồi không đầy đủ (VD: {"action": "none"})
        if action_data.get("action") == "none" and "payload" not in action_data:
            print("⚠️ Cảnh báo: AI trả về action 'none' nhưng thiếu payload. Tự động thêm payload mặc định.")
            action_data["payload"] = {
                "reason": "incomplete_response",
                "message": "AI Agent đã trả về một phản hồi không đầy đủ. Vui lòng thử lại với yêu cầu rõ ràng hơn."
            }

        # Bước 3: Switch Case để xử lý hành động
        action = action_data.get("action")
        payload = action_data.get("payload", {})

        if action == "add_product":
            print(f"🚀 HÀNH ĐỘNG: THÊM SẢN PHẨM MỚI")
            print(f"   - Dữ liệu payload: {payload}")
            # TODO: Gọi hàm thêm sản phẩm vào database của bạn ở đây
            # result = products_service.add_product(payload)
            # return JsonResponse({"success": True, "result": result})

        elif action == "update_product":
            print(f"✏️ HÀNH ĐỘNG: CẬP NHẬT SẢN PHẨM")
            print(f"   - Dữ liệu payload: {payload}")
            # TODO: Gọi hàm cập nhật sản phẩm
            # result = products_service.update_product(payload)
            # return JsonResponse({"success": True, "result": result})

        elif action == "delete_product":
            print(f"🗑️ HÀNH ĐỘNG: XÓA SẢN PHẨM")
            print(f"   - Dữ liệu payload: {payload}")
            # TODO: Gọi hàm xóa sản phẩm
            # result = products_service.delete_product(payload)
            # return JsonResponse({"success": True, "result": result})

        elif action == "reply_feedback":
            print(f"💬 HÀNH ĐỘNG: TRẢ LỜI PHẢN HỒI")
            print(f"   - Dữ liệu payload: {payload}")
            # TODO: Gọi hàm trả lời phản hồi
            # result = feedback_service.reply(payload)
            # return JsonResponse({"success": True, "result": result})

        elif action == "approve_order":
            print(f"✅ HÀNH ĐỘNG: DUYỆT ĐƠN HÀNG")
            print(f"   - Dữ liệu payload: {payload}")
            # TODO: Gọi hàm duyệt đơn
            # result = order_service.approve(payload)
            # return JsonResponse({"success": True, "result": result})

        elif action == "reject_order":
            print(f"❌ HÀNH ĐỘNG: TỪ CHỐI ĐƠN HÀNG")
            print(f"   - Dữ liệu payload: {payload}")
            # TODO: Gọi hàm từ chối đơn
            # result = order_service.reject(payload)
            # return JsonResponse({"success": True, "result": result})

        elif action == "get_order_status":
            print(f"🔍 HÀNH ĐỘNG: KIỂM TRA TÌNH TRẠNG ĐƠN HÀNG")
            print(f"   - Dữ liệu payload: {payload}")
            # TODO: Gọi hàm kiểm tra trạng thái
            # result = order_service.get_status(payload)
            # return JsonResponse({"success": True, "result": result})

        elif action == "none":
            # Đây là trường hợp quan trọng nhất để thông báo lỗi cho admin
            reason = payload.get("reason", "unknown")
            message = payload.get("message", "Đã xảy ra lỗi không xác định.")
            print(f"🛑 HÀNH ĐỘNG: KHÔNG THỰC HIỆN (NONE)")
            print(f"   - Lý do: {reason}")
            print(f"   - Thông báo cho Admin: {message}")
            # Trả về lỗi cho frontend để hiển thị

        else:
            # Xử lý nếu AI trả về một action không nằm trong danh sách
            print(f"❓ HÀNH ĐỘNG KHÔNG HỢP LỆ: '{action}'")

    except json.JSONDecodeError:
        # Xử lý nếu AI không trả về JSON hợp lệ
        print(f"🚨 LỖI: Không thể phân tích JSON từ AI. Phản hồi nhận được: '{ai_response_string}'")
    except Exception as e:
        # Bắt các lỗi khác
        print(f"🚨 LỖI KHÔNG XÁC ĐỊNH: {e}")
