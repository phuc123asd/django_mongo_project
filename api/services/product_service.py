from api.models.product import Product
from api.models.productdetail import ProductDetail
from mongoengine.errors import ValidationError, NotUniqueError

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