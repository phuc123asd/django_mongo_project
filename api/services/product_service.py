from api.models.product import Product
from api.models.productdetail import ProductDetail
from mongoengine.errors import ValidationError, NotUniqueError
from bson.errors import InvalidId

def add_product(payload):
    """
    Hàm này nhận payload đã có đầy đủ thông tin từ GPT và lưu vào DB.
    """
    try:
        # 1. Trích xuất dữ liệu từ payload
        name = payload.get('name')
        price = payload.get('price')
        original_price = payload.get('originalPrice')
        
        # 2. Lấy danh sách URL ảnh từ payload (đã được GPT trích xuất)
        image_urls = payload.get('images', [])
        
        if not image_urls:
            return {
                "success": False,
                "error": "Vui lòng cung cấp ít nhất một hình ảnh cho sản phẩm."
            }
        
        # Lấy ảnh đầu tiên làm ảnh chính
        main_image_url = image_urls[0]
        
        # 3. Tạo và lưu đối tượng Product với đầy đủ thông tin
        product = Product(
            name=name,
            price=price,
            originalPrice=original_price,
            image=main_image_url,
            # Sử dụng các thông tin do GPT suy luận
            category=payload.get('category'),
            brand=payload.get('brand'),
            rating=payload.get('rating', 4.5),
            isNew=payload.get('isNew', True)
        )
        product.save()
        
        # 4. Tạo và lưu đối tượng ProductDetail
        product_detail = ProductDetail(
            product=product,
            images=image_urls,
            rating=payload.get('rating', 4.5),
            reviewCount=payload.get('reviewCount', 0),
            description=payload.get('description'),
            features=payload.get('features', []),
            specifications=payload.get('specifications', {}),
            inStock=payload.get('inStock', True),
            hasARView=payload.get('hasARView', False)
        )
        product_detail.save()
        
        # 5. Trả về kết quả thành công, bao gồm cả danh sách URL ảnh
        return {
            "success": True,
            "action": "add_product",
            "message": f"Đã thêm sản phẩm '{name}' thành công.",
            "product_id": str(product.id),
            "images": image_urls  # <-- Trả về để frontend hiển thị
        }
        
    except ValidationError as e:
        return {
            "success": False,
            "error": f"Dữ liệu không hợp lệ: {e}"
        }
    except NotUniqueError:
        return {
            "success": False,
            "error": f"Sản phẩm với tên '{name}' đã tồn tại."
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Đã xảy ra lỗi không mong muốn: {e}"
        }

def delete_product(product_id):
    """
    Tìm và xóa một sản phẩm dựa trên ID hoặc tên.
    - product_id: có thể là chuỗi ID của MongoDB hoặc tên sản phẩm.
    """
    product_to_delete = None

    # 1. Thử tìm sản phẩm theo tên trước
    product_to_delete = Product.objects(name=product_id).first()

    # 2. Nếu không tìm thấy theo tên, thử tìm theo ID
    if not product_to_delete:
        try:
            product_to_delete = Product.objects(id=product_id).first()
        except InvalidId:
            # ID không hợp lệ (ví dụ: sai định dạng)
            return {
                "success": False,
                "action": "delete_product",
                "error": f"ID sản phẩm '{product_id}' không hợp lệ."
            }

    # 3. Kiểm tra lại lần cuối xem đã tìm thấy sản phẩm chưa
    if not product_to_delete:
        return {
            "success": False,
            "action": "delete_product",
            "error": f"Không tìm thấy sản phẩm nào với ID hoặc tên là '{product_id}'."
        }

    # 4. Nếu tìm thấy, thực hiện xóa
    try:
        product_name = product_to_delete.name
        product_to_delete.delete()
        # Nhờ reverse_delete_rule=CASCADE, ProductDetail liên quan sẽ tự động bị xóa.
        return {
            "success": True,
            "action": "delete_product",
            "message": f"Đã xóa thành công sản phẩm '{product_name}'."
        }
    except Exception as e:
        return {
            "success": False,
            "action": "delete_product",
            "error": f"Đã xảy ra lỗi khi xóa sản phẩm: {e}"
        }

def update_product(payload):
    """
    Update an existing product based on the provided fields.
    - payload: Contains product_id and fields to update
    """
    try:
        # 1. Get product identifier and fields to update
        product_id = payload.get('product_id')
        if not product_id:
            return {
                "success": False,
                "action": "update_product",
                "error": "Vui lòng cung cấp ID hoặc tên sản phẩm cần cập nhật."
            }
        
        # 2. Find the product by name or ID
        product_to_update = Product.objects(name=product_id).first()
        if not product_to_update:
            try:
                product_to_update = Product.objects(id=product_id).first()
            except InvalidId:
                return {
                    "success": False,
                    "action": "update_product",
                    "error": f"ID sản phẩm '{product_id}' không hợp lệ."
                }
        
        if not product_to_update:
            return {
                "success": False,
                "action": "update_product",
                "error": f"Không tìm thấy sản phẩm với ID hoặc tên '{product_id}'."
            }
        
        # 3. Get the product detail
        product_detail = ProductDetail.objects(product=product_to_update).first()
        if not product_detail:
            return {
                "success": False,
                "action": "update_product",
                "error": f"Không tìm thấy chi tiết sản phẩm cho '{product_id}'."
            }
        
        # 4. Update Product fields if provided
        updated_fields = []
        
        if 'name' in payload:
            product_to_update.name = payload['name']
            updated_fields.append("tên")
            
        if 'price' in payload:
            product_to_update.price = payload['price']
            updated_fields.append("giá")
            
        if 'originalPrice' in payload:
            product_to_update.originalPrice = payload['originalPrice']
            updated_fields.append("giá gốc")
            
        if 'image' in payload:
            product_to_update.image = payload['image']
            updated_fields.append("ảnh chính")
            
        if 'category' in payload:
            product_to_update.category = payload['category']
            updated_fields.append("danh mục")
            
        if 'brand' in payload:
            product_to_update.brand = payload['brand']
            updated_fields.append("thương hiệu")
            
        if 'rating' in payload:
            product_to_update.rating = payload['rating']
            updated_fields.append("đánh giá")
            
        if 'isNew' in payload:
            product_to_update.isNew = payload['isNew']
            updated_fields.append("trạng thái mới")
        
        # 5. Update ProductDetail fields if provided
        if 'images' in payload:
            product_detail.images = payload['images']
            updated_fields.append("danh sách ảnh")
            
        if 'reviewCount' in payload:
            product_detail.reviewCount = payload['reviewCount']
            updated_fields.append("số lượng đánh giá")
            
        if 'description' in payload:
            product_detail.description = payload['description']
            updated_fields.append("mô tả")
            
        if 'features' in payload:
            product_detail.features = payload['features']
            updated_fields.append("tính năng")
            
        if 'specifications' in payload:
            product_detail.specifications = payload['specifications']
            updated_fields.append("thông số kỹ thuật")
            
        if 'inStock' in payload:
            product_detail.inStock = payload['inStock']
            updated_fields.append("tình trạng còn hàng")
            
        if 'hasARView' in payload:
            product_detail.hasARView = payload['hasARView']
            updated_fields.append("tính năng AR")
        
        # 6. Save the changes
        product_to_update.save()
        product_detail.save()
        
        # 7. Return success message
        if updated_fields:
            fields_str = ", ".join(updated_fields)
            return {
                "success": True,
                "action": "update_product",
                "message": f"Đã cập nhật thành công các trường: {fields_str} cho sản phẩm '{product_to_update.name}'.",
                "product_id": str(product_to_update.id)
            }
        else:
            return {
                "success": False,
                "action": "update_product",
                "error": "Không có trường nào được cập nhật. Vui lòng cung cấp ít nhất một trường cần cập nhật."
            }
            
    except ValidationError as e:
        return {
            "success": False,
            "action": "update_product",
            "error": f"Dữ liệu không hợp lệ: {e}"
        }
    except Exception as e:
        return {
            "success": False,
            "action": "update_product",
            "error": f"Đã xảy ra lỗi khi cập nhật sản phẩm: {e}"
        }

