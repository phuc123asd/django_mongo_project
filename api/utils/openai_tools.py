from typing import List, Dict

ADMIN_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_product",
            "description": "Thêm một sản phẩm mới vào cơ sở dữ liệu Astra",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Tên sản phẩm"
                    },
                    "price": {
                        "type": "number",
                        "description": "Giá bán hiện tại (bằng số)"
                    },
                    "images": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Danh sách URL hình ảnh của sản phẩm. Nếu admin tải ảnh lên, lấy URL từ tin nhắn."
                    },
                    "originalPrice": {
                        "type": "number",
                        "description": "Giá gốc của sản phẩm (thường cao hơn giá bán)"
                    },
                    "category": {
                        "type": "string",
                        "description": "Danh mục sản phẩm (VD: Smartphones, Laptops, Audio)"
                    },
                    "brand": {
                        "type": "string",
                        "description": "Thương hiệu sản phẩm (VD: Apple, Samsung, Dell)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Mô tả hấp dẫn về sản phẩm"
                    },
                    "features": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Danh sách các tính năng nổi bật. Dạng mảng các chuỗi. Ví dụ: ['Màn hình Super Retina XDR', 'Chip A18 Pro']"
                    },
                    "specifications": {
                        "type": "object",
                        "description": "Thông số kỹ thuật chi tiết dạng key-value. Ví dụ: {'Dung lượng': '256GB', 'RAM': '8GB', 'Màu sắc': 'Titan Sa Mạc'}",
                        "additionalProperties": {
                            "type": "string"
                        }
                    },
                    "rating": {
                        "type": "number",
                        "description": "Đánh giá sao (từ 0 đến 5.0)"
                    },
                    "reviewCount": {
                        "type": "number",
                        "description": "Số lượng đánh giá"
                    },
                    "isNew": {
                        "type": "boolean",
                        "description": "Sản phẩm có phải mới ra mắt không"
                    },
                    "inStock": {
                        "type": "boolean",
                        "description": "Sản phẩm có đang còn hàng không"
                    },
                    "hasARView": {
                        "type": "boolean",
                        "description": "Sản phẩm có hỗ trợ xem AR không"
                    }
                },
                "required": ["name", "price", "images"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_product",
            "description": "Cập nhật, thay đổi hoặc chỉnh sửa thông tin của sản phẩm đã có",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "Tên, mã ID hoặc đoạn mô tả nhận diện sản phẩm cần cập nhật (VD: 'iPhone 15 Pro', '65eef123')"
                    },
                    "name": {"type": "string", "description": "Tên mới nếu muốn đổi"},
                    "price": {"type": "number", "description": "Giá bán mới"},
                    "originalPrice": {"type": "number", "description": "Giá gốc mới"},
                    "images": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Cập nhật danh sách URL ảnh (Bao gồm các ảnh cũ muốn giữ lại trích từ yêu cầu (VD: Giữ lại...) VÀ ảnh admin mới upload)"
                    },
                    "category": {"type": "string", "description": "Danh mục mới"},
                    "brand": {"type": "string", "description": "Thương hiệu mới"},
                    "description": {"type": "string", "description": "Mô tả mới"},
                    "features": {"type": "array", "items": {"type": "string"}},
                    "specifications": {
                        "type": "object",
                        "additionalProperties": {"type": "string"}
                    },
                    "inStock": {"type": "boolean", "description": "Cập nhật tình trạng tồn kho"}
                },
                "required": ["product_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_product",
            "description": "Xóa một sản phẩm khỏi cơ sở dữ liệu",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "Tên hoặc ID của sản phẩm cần xóa"
                    }
                },
                "required": ["product_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "approve_order",
            "description": "Duyệt đơn hàng, thay đổi trạng thái sang Đang Vận Chuyển",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Danh sách ID đơn hàng cần duyệt. Truyền mảng rỗng [] nếu muốn duyệt tất cả đơn đang chờ."
                    }
                },
                "required": ["order_ids"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_statistics",
            "description": "Xem thống kê tổng quan, doanh thu, sản phẩm, và khách hàng",
            "parameters": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["overview", "revenue", "geographical", "products", "customers"],
                        "description": "Loại báo cáo thống kê cần xem"
                    },
                    "days": {
                        "type": "number",
                        "description": "Số ngày để lọc (mặc định 30)"
                    }
                },
                "required": ["type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "navigate_page",
            "description": "Chuyển, mở, điều hướng giao diện UI của Admin sang trang tương ứng khi họ có yêu cầu 'mở trang...', 'đi đến...', v.v.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "enum": ["/", "/products", "/orders", "/users", "/chat"],
                        "description": "Đường dẫn route React Router"
                    }
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_orders_list",
            "description": "Lấy danh sách các đơn hàng hiện có trong hệ thống",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "Lọc trạng thái đơn hàng (VD: 'chờ duyệt', 'đang giao', 'hoàn thành'). Bỏ trống để lấy tất cả."
                    },
                    "limit": {
                        "type": "number",
                        "description": "Số lượng đơn hàng hiển thị mặc định (VD: 10, 20)."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_order_status",
            "description": "Cập nhật trạng thái của một đơn hàng cụ thể",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "ID hoặc mã đơn hàng cần cập nhật"
                    },
                    "new_status": {
                        "type": "string",
                        "description": "Trạng thái mới cần cập nhật (VD: 'Chờ giao hàng', 'Hoàn thành', 'Hủy')"
                    }
                },
                "required": ["order_id", "new_status"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_users_list",
            "description": "Lấy danh sách người dùng/khách hàng",
            "parameters": {
                "type": "object",
                "properties": {
                    "role": {
                        "type": "string",
                        "description": "Lọc theo quyền (VD: 'user', 'admin'). Bỏ trống để lấy tất cả."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_user_role",
            "description": "Cập nhật hoặc thay đổi phân quyền của một người dùng",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID, email hoặc tên người dùng cần cấu hình"
                    },
                    "new_role": {
                        "type": "string",
                        "description": "Quyền mới áp dụng (VD: 'admin', 'user', 'blocked')"
                    }
                },
                "required": ["user_id", "new_role"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_product_stock",
            "description": "Cập nhật nhanh tình trạng còn hàng (inStock) của sản phẩm",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "ID hoặc tên sản phẩm cần kiểm tra/cập nhật tồn kho"
                    },
                    "in_stock": {
                        "type": "boolean",
                        "description": "True nếu còn hàng, False nếu hết hàng"
                    }
                },
                "required": ["product_id", "in_stock"]
            }
        }
    }
]
