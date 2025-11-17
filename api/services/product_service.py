from api.models.product import Product
from api.models.productdetail import ProductDetail
from mongoengine.errors import ValidationError, NotUniqueError

def add_product(payload):
    """
    Thêm một sản phẩm mới và chi tiết của nó vào MongoDB.
    """
    try:
        # 1. Trích xuất dữ liệu từ payload
        name = payload.get('name')
        price = payload.get('price')
        original_price = payload.get('originalPrice') # Không bắt buộc
        image_names = payload.get('images', []) # Lấy danh sách tên ảnh

        # 2. Xử lý ảnh (Đây là phần quan trọng)
        # Giả sử: bạn có một hàm để upload file và trả về URL
        # Hiện tại, chúng ta sẽ tạo URL giả lập cho mục đích demo
        # !!! QUAN TRỌNG: Thay 'http://your-image-domain.com/' bằng domain lưu trữ ảnh của bạn
        if not image_names:
            return {
                "success": False,
                "error": "Vui lòng cung cấp ít nhất một hình ảnh cho sản phẩm."
            }
        
        # Lấy ảnh đầu tiên làm ảnh chính cho model Product
        main_image_name = image_names[0]
        main_image_url = f"http://your-image-domain.com/{main_image_name}"
        
        # Chuyển tất cả các tên ảnh thành URL cho model ProductDetail
        image_urls = [f"http://your-image-domain.com/{img_name}" for img_name in image_names]

        # 3. Tạo và lưu đối tượng Product
        product = Product(
            name=name,
            price=price,
            originalPrice=original_price,
            image=main_image_url,
            # Các trường khác có thể được thêm vào ở đây hoặc để AI suy luận
            # Ví dụ: category="Smartphones", brand="Apple", isNew=True
        )
        product.save()

        # 4. Tạo và lưu đối tượng ProductDetail liên kết
        product_detail = ProductDetail(
            product=product, # Liên kết với sản phẩm vừa tạo
            images=image_urls,
            # Các trường khác có thể được thêm vào
        )
        product_detail.save()

        return {
            "success": True,
            "message": f"Đã thêm sản phẩm '{name}' thành công.",
            "product_id": str(product.id) # Trả về ID của sản phẩm mới
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
