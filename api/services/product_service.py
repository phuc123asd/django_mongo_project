from api.models.product import Product
from api.models.productdetail import ProductDetail
from mongoengine.errors import ValidationError, NotUniqueError
from bson.errors import InvalidId
import cloudinary.uploader
def get_public_id_from_cloudinary_url(url: str):
    """
    Trích public_id từ URL Cloudinary chuẩn.
    Ví dụ:
        url = https://res.cloudinary.com/.../upload/v12345/abcxyz.webp
        => public_id = 'abcxyz'
    """
    try:
        # Tách phần sau /upload/
        after_upload = url.split("/upload/")[-1]      # "v1763887599/se9ok1axdrxuh7drrpfw.webp"

        # Bỏ "v123456/" đi
        parts = after_upload.split("/", 1)
        if parts[0].startswith("v") and parts[0][1:].isdigit():
            file_part = parts[1]  # "se9ok1axdrxuh7drrpfw.webp"
        else:
            file_part = after_upload

        # Bỏ extension (.jpg, .png, .webp...)
        public_id = file_part.rsplit(".", 1)[0]

        return public_id
    except Exception:
        return None

def delete_cloudinary_image(url):
    public_id = get_public_id_from_cloudinary_url(url)
    if not public_id:
        return {"success": False, "error": "Không tách được public_id từ URL"}

    try:
        res = cloudinary.uploader.destroy(public_id)
        return {"success": True, "public_id": public_id, "result": res}
    except Exception as e:
        return {"success": False, "public_id": public_id, "error": str(e)}

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
    Xóa ảnh Cloudinary trước rồi xóa Product + ProductDetail.
    """

    # 1. Tìm sản phẩm
    product = Product.objects(name=product_id).first()
    if not product:
        product = Product.objects(id=product_id).first()

    if not product:
        return {"success": False, "error": "Không tìm thấy sản phẩm"}

    # 2. Gom tất cả ảnh
    image_urls = []

    # Ảnh từ Product
    if hasattr(product, "image") and product.image:
        image_urls.append(product.image)

    if hasattr(product, "images") and product.images:
        image_urls.extend(product.images)

    # Ảnh từ ProductDetail
    details = ProductDetail.objects(product=product)
    for d in details:
        if hasattr(d, "image") and d.image:
            image_urls.append(d.image)
        if hasattr(d, "images") and d.images:
            image_urls.extend(d.images)

    # 3. Xóa ảnh Cloudinary
    cloudinary_results = []
    for url in image_urls:
        result = delete_cloudinary_image(url)
        cloudinary_results.append(result)

    # 4. Xóa dữ liệu DB (CASCADE sẽ tự xóa ProductDetail)
    product_name = product.name
    product.delete()

    return {
        "success": True,
        "message": f"Đã xóa sản phẩm {product_name} và toàn bộ ảnh.",
        "cloudinary_results": cloudinary_results
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

