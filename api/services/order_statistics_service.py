from datetime import datetime, timedelta
from django.db.models import Sum, Count, Avg, Max, Min
from api.models.order import Order, OrderItem
from api.models.product import Product
from api.models.customer import Customer
from collections import defaultdict
import calendar
import json

class OrderStatisticsService:
    """
    Dịch vụ thống kê chi tiết cho colection đơn hàng
    """
    def __init__(self):
        self.today = datetime.utcnow()
        self.yesterday = self.today - timedelta(days=1)
        self.last_week = self.today - timedelta(weeks=1)
        self.last_month = self.today - timedelta(days=30)
        self.last_quarter = self.today - timedelta(days=90)
        self.last_year = self.today - timedelta(days=365)
    
    def get_overview_statistics(self):
        """
        Thống kê tổng quan về đơn hàng
        """
        print(f"[STATS_SERVICE] Bắt đầu lấy thống kê tổng quan")
        
        try:
            # Đếm tổng số đơn hàng
            print(f"[STATS_SERVICE] Đếm tổng số đơn hàng...")
            total_orders = Order.objects.count()
            print(f"[STATS_SERVICE] Tổng số đơn hàng: {total_orders}")
            
            # Tính tổng doanh thu
            print(f"[STATS_SERVICE] Tính tổng doanh thu...")
            revenue_pipeline = [
                {"$group": {"_id": None, "total": {"$sum": "$total_price"}}}
            ]
            revenue_result = list(Order.objects.aggregate(revenue_pipeline))
            
            if revenue_result:
                revenue_value = revenue_result[0]['total']
                print(f"[STATS_SERVICE] Kiểu dữ liệu của doanh thu: {type(revenue_value)}")
                
                try:
                    total_revenue = float(revenue_value.to_decimal())
                except AttributeError:
                    total_revenue = float(revenue_value)
            else:
                total_revenue = 0
            print(f"[STATS_SERVICE] Tổng doanh thu: {total_revenue}")
            
            # Tính giá trị đơn hàng trung bình
            print(f"[STATS_SERVICE] Tính giá trị đơn hàng trung bình...")
            avg_pipeline = [
                {"$group": {"_id": None, "avg": {"$avg": "$total_price"}}}
            ]
            avg_result = list(Order.objects.aggregate(avg_pipeline))
            
            if avg_result:
                avg_value = avg_result[0]['avg']
                print(f"[STATS_SERVICE] Kiểu dữ liệu của giá trị trung bình: {type(avg_value)}")
                
                try:
                    avg_order_value = float(avg_value.to_decimal())
                except AttributeError:
                    avg_order_value = float(avg_value)
            else:
                avg_order_value = 0
            print(f"[STATS_SERVICE] Giá trị đơn hàng trung bình: {avg_order_value}")
            
            # Thống kê theo trạng thái
            print(f"[STATS_SERVICE] Thống kê theo trạng thái...")
            status_stats = {}
            for status in Order.STATUS_CHOICES:
                print(f"[STATS_SERVICE] Đếm đơn hàng với trạng thái: {status}")
                count = Order.objects(status=status).count()
                status_stats[status] = {
                    'count': count,
                    'percentage': round(count / total_orders * 100, 2) if total_orders > 0 else 0
                }
                print(f"[STATS_SERVICE] Trạng thái {status}: {count} đơn hàng ({status_stats[status]['percentage']}%)")
            
            # Thống kê theo khoảng thời gian
            print(f"[STATS_SERVICE] Thống kê theo khoảng thời gian...")
            
            # Đơn hàng hôm nay
            print(f"[STATS_SERVICE] Đếm đơn hàng hôm nay...")
            today_start = self.today.replace(hour=0, minute=0, second=0, microsecond=0)
            today_orders = Order.objects(created_at__gte=today_start).count()
            print(f"[STATS_SERVICE] Đơn hàng hôm nay: {today_orders}")
            
            # Đơn hàng hôm qua
            print(f"[STATS_SERVICE] Đếm đơn hàng hôm qua...")
            yesterday_start = self.yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
            yesterday_end = self.today.replace(hour=0, minute=0, second=0, microsecond=0)
            yesterday_orders = Order.objects(
                created_at__gte=yesterday_start,
                created_at__lt=yesterday_end
            ).count()
            print(f"[STATS_SERVICE] Đơn hàng hôm qua: {yesterday_orders}")
            
            # Đơn hàng tuần này
            print(f"[STATS_SERVICE] Đếm đơn hàng tuần này...")
            this_week_orders = Order.objects(created_at__gte=self.last_week).count()
            print(f"[STATS_SERVICE] Đơn hàng tuần này: {this_week_orders}")
            
            # Đơn hàng tháng này
            print(f"[STATS_SERVICE] Đếm đơn hàng tháng này...")
            this_month_orders = Order.objects(created_at__gte=self.last_month).count()
            print(f"[STATS_SERVICE] Đơn hàng tháng này: {this_month_orders}")
            
            # Chuẩn bị kết quả
            result = {
                'total_orders': total_orders,
                'total_revenue': float(total_revenue),
                'avg_order_value': float(avg_order_value),
                'status_distribution': status_stats,
                'time_periods': {
                    'today': today_orders,
                    'yesterday': yesterday_orders,
                    'this_week': this_week_orders,
                    'this_month': this_month_orders
                }
            }
            
            print(f"[STATS_SERVICE] Đã hoàn thành thống kê tổng quan")
            return result
            
        except Exception as e:
            print(f"[STATS_SERVICE] Lỗi khi lấy thống kê tổng quan: {str(e)}")
            import traceback
            traceback.print_exc()
            # Ném lại exception để các hàm gọi có thể xử lý
            raise
            
    def get_revenue_statistics(self, days=30):
        """
        Thống kê doanh thu theo khoảng thời gian
        """
        print(f"[STATS_SERVICE] Bắt đầu lấy thống kê doanh thu trong {days} ngày")
        try:
            end_date = self.today
            start_date = end_date - timedelta(days=days)
            print(f"[STATS_SERVICE] Khoảng thời gian: từ {start_date} đến {end_date}")
            
            # Doanh thu theo ngày
            daily_pipeline = [
                {"$match": {"created_at": {"$gte": start_date, "$lt": end_date}}},
                {"$group": {
                    "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}},
                    "revenue": {"$sum": "$total_price"},
                    "count": {"$sum": 1}
                }},
                {"$sort": {"_id": 1}}
            ]
            daily_data = list(Order.objects.aggregate(daily_pipeline))
            
            # Chuyển đổi kết quả sang định dạng mong muốn
            daily_revenue = {}
            daily_orders = {}
            for item in daily_data:
                revenue_value = item['revenue']
                try:
                    daily_revenue[item['_id']] = float(revenue_value.to_decimal())
                except AttributeError:
                    daily_revenue[item['_id']] = float(revenue_value)
                daily_orders[item['_id']] = item['count']
            
            # Doanh thu theo tuần
            weekly_pipeline = [
                {"$match": {"created_at": {"$gte": start_date, "$lt": end_date}}},
                {"$group": {
                    "_id": {"$dateToString": {"format": "%Y-W%U", "date": "$created_at"}},
                    "revenue": {"$sum": "$total_price"},
                    "count": {"$sum": 1}
                }},
                {"$sort": {"_id": 1}}
            ]
            weekly_data = list(Order.objects.aggregate(weekly_pipeline))
            
            weekly_revenue = {}
            weekly_orders = {}
            for item in weekly_data:
                revenue_value = item['revenue']
                try:
                    weekly_revenue[item['_id']] = float(revenue_value.to_decimal())
                except AttributeError:
                    weekly_revenue[item['_id']] = float(revenue_value)
                weekly_orders[item['_id']] = item['count']
            
            # Doanh thu theo tháng
            monthly_pipeline = [
                {"$match": {"created_at": {"$gte": start_date, "$lt": end_date}}},
                {"$group": {
                    "_id": {"$dateToString": {"format": "%Y-%m", "date": "$created_at"}},
                    "revenue": {"$sum": "$total_price"},
                    "count": {"$sum": 1}
                }},
                {"$sort": {"_id": 1}}
            ]
            monthly_data = list(Order.objects.aggregate(monthly_pipeline))
            
            monthly_revenue = {}
            monthly_orders = {}
            for item in monthly_data:
                revenue_value = item['revenue']
                try:
                    monthly_revenue[item['_id']] = float(revenue_value.to_decimal())
                except AttributeError:
                    monthly_revenue[item['_id']] = float(revenue_value)
                monthly_orders[item['_id']] = item['count']
            
            # So sánh với kỳ trước
            previous_start_date = start_date - timedelta(days=days)
            current_total = sum(daily_revenue.values())
            
            previous_pipeline = [
                {"$match": {"created_at": {"$gte": previous_start_date, "$lt": start_date}}},
                {"$group": {"_id": None, "total": {"$sum": "$total_price"}}}
            ]
            previous_result = list(Order.objects.aggregate(previous_pipeline))
            
            # --- SỬA LỖI CHÍNH ---
            if previous_result:
                previous_total_value = previous_result[0]['total']
                try:
                    previous_total = float(previous_total_value.to_decimal())
                except AttributeError:
                    previous_total = float(previous_total_value)
            else:
                previous_total = 0
            
            growth_rate = round((current_total - previous_total) / previous_total * 100, 2) if previous_total > 0 else 0
            
            result = {
                'period': f"{days} ngày",
                'current_period': {
                    'total_revenue': current_total,
                    'total_orders': len(daily_data),
                    'avg_order_value': round(current_total / len(daily_data), 2) if len(daily_data) > 0 else 0
                },
                'previous_period': {
                    'total_revenue': previous_total,
                    'total_orders': len(list(Order.objects.aggregate([
                        {"$match": {"created_at": {"$gte": previous_start_date, "$lt": start_date}}},
                        {"$count": "total"}
                    ]))),
                    'avg_order_value': 0  # Có thể tính toán nếu cần
                },
                'growth_rate': growth_rate,
                'daily': {
                    'revenue': daily_revenue,
                    'orders': daily_orders
                },
                'weekly': {
                    'revenue': weekly_revenue,
                    'orders': weekly_orders
                },
                'monthly': {
                    'revenue': monthly_revenue,
                    'orders': monthly_orders
                }
            }
            
            print(f"[STATS_SERVICE] Đã hoàn thành thống kê doanh thu")
            return result
        except Exception as e:
            print(f"[STATS_SERVICE] Lỗi khi lấy thống kê doanh thu: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
    
    def get_geographical_statistics(self):
        """
        Thống kê theo địa lý - ĐÃ SỬA LỖI VÀ TỐI ƯU
        """
        print(f"[STATS_SERVICE] Bắt đầu lấy thống kê theo địa lý")
        try:
            # Thống kê theo tỉnh/thành phố
            province_pipeline = [
                {"$group": {
                    "_id": "$province",
                    "count": {"$sum": 1},
                    "revenue": {"$sum": "$total_price"}
                }},
                {"$sort": {"revenue": -1}}
            ]
            province_data = list(Order.objects.aggregate(province_pipeline))
            
            province_stats = {}
            for item in province_data:
                revenue_value = item['revenue']
                try:
                    province_stats[item['_id']] = {
                        'count': item['count'],
                        'revenue': float(revenue_value.to_decimal())
                    }
                except AttributeError:
                    province_stats[item['_id']] = {
                        'count': item['count'],
                        'revenue': float(revenue_value)
                    }
            
            # Thống kê theo thành phố
            city_pipeline = [
                {"$group": {
                    "_id": "$city",
                    "count": {"$sum": 1},
                    "revenue": {"$sum": "$total_price"}
                }},
                {"$sort": {"revenue": -1}}
            ]
            city_data = list(Order.objects.aggregate(city_pipeline))
            
            city_stats = {}
            for item in city_data:
                revenue_value = item['revenue']
                try:
                    city_stats[item['_id']] = {
                        'count': item['count'],
                        'revenue': float(revenue_value.to_decimal())
                    }
                except AttributeError:
                    city_stats[item['_id']] = {
                        'count': item['count'],
                        'revenue': float(revenue_value)
                    }
            
            # Lấy top 10
            top_provinces = dict(list(province_stats.items())[:10])
            top_cities = dict(list(city_stats.items())[:10])
            
            result = {
                'by_province': province_stats,
                'by_city': city_stats,
                'top_provinces': top_provinces,
                'top_cities': top_cities
            }
            
            print(f"[STATS_SERVICE] Đã hoàn thành thống kê theo địa lý")
            return result
        except Exception as e:
            print(f"[STATS_SERVICE] Lỗi khi lấy thống kê theo địa lý: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
    
    def get_product_statistics(self):
        """
        Thống kê sản phẩm - ĐÃ SỬA LỖI VÀ TỐI ƯU
        """
        print(f"[STATS_SERVICE] Bắt đầu lấy thống kê sản phẩm")
        try:
            # Pipeline để thống kê sản phẩm
            product_pipeline = [
                {"$unwind": "$items"},
                {"$group": {
                    "_id": "$items.product",
                    "quantity": {"$sum": "$items.quantity"},
                    "revenue": {"$sum": {"$multiply": [
                        "$items.quantity",
                        {"$toDecimal": "$items.price"}
                    ]}},
                    "orders": {"$addToSet": "$_id"}
                }},
                {"$addFields": {
                    "orders_count": {"$size": "$orders"}
                }},
                {"$sort": {"revenue": -1}}
            ]
            
            product_stats = list(Order.objects.aggregate(product_pipeline))
            print(f"[STATS_SERVICE] Đã phân tích {len(product_stats)} sản phẩm")
            
            # Lấy thông tin chi tiết sản phẩm
            product_ids = [item['_id'] for item in product_stats]
            products = Product.objects(id__in=product_ids)
            
            product_details = {}
            for product in products:
                product_id = str(product.id)
                product_details[product_id] = {
                    'name': product.name,
                    'category': product.category,
                    'brand': product.brand,
                    'price': float(product.price)
                }
            
            # Chuẩn bị kết quả
            detailed_top_revenue = []
            detailed_top_quantity = []
            detailed_top_orders = []
            
            for item in product_stats[:20]:
                product_id = str(item['_id'])
                details = product_details.get(product_id, {})
                
                # Xử lý revenue (Decimal128)
                revenue_value = item['revenue']
                try:
                    revenue = float(revenue_value.to_decimal())
                except AttributeError:
                    revenue = float(revenue_value)
                
                details['quantity'] = int(item['quantity'])
                details['revenue'] = revenue
                details['orders_count'] = item['orders_count']
                
                detailed_top_revenue.append(details.copy())
                
                # Tạo bản sao cho các danh sách khác
                quantity_details = details.copy()
                detailed_top_quantity.append(quantity_details)
                
                orders_details = details.copy()
                detailed_top_orders.append(orders_details)
            
            # Sắp xếp lại theo số lượng và số đơn hàng
            detailed_top_quantity.sort(key=lambda x: x['quantity'], reverse=True)
            detailed_top_orders.sort(key=lambda x: x['orders_count'], reverse=True)
            
            # Tính hiệu suất theo danh mục và thương hiệu
            category_performance = self._get_category_performance(product_stats, product_details)
            brand_performance = self._get_brand_performance(product_stats, product_details)
            
            result = {
                'top_by_quantity': detailed_top_quantity,
                'top_by_revenue': detailed_top_revenue,
                'top_by_orders': detailed_top_orders,
                'category_performance': category_performance,
                'brand_performance': brand_performance
            }
            
            print(f"[STATS_SERVICE] Đã hoàn thành thống kê sản phẩm")
            return result
        except Exception as e:
            print(f"[STATS_SERVICE] Lỗi khi lấy thống kê sản phẩm: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
    
    def get_customer_statistics(self):
        """
        Thống kê khách hàng - ĐÃ SỬA LỖI VÀ TỐI ƯU CHO MODEL MỚI
        """
        print(f"[STATS_SERVICE] Bắt đầu lấy thống kê khách hàng")
        try:
            # Pipeline để thống kê khách hàng
            customer_pipeline = [
                {"$group": {
                    "_id": "$customer",
                    "orders_count": {"$sum": 1},
                    "total_revenue": {"$sum": "$total_price"},
                    "first_order_date": {"$min": "$created_at"},
                    "last_order_date": {"$max": "$created_at"}
                }},
                {"$sort": {"total_revenue": -1}}
            ]
            
            customer_stats = list(Order.objects.aggregate(customer_pipeline))
            print(f"[STATS_SERVICE] Đã phân tích {len(customer_stats)} khách hàng")
            
            # Lấy thông tin chi tiết khách hàng
            customer_ids = [item['_id'] for item in customer_stats]
            customers = Customer.objects(id__in=customer_ids)
            
            customer_details = {}
            for customer in customers:
                customer_id = str(customer.id)
                customer_details[customer_id] = {
                    'name': f"{customer.first_name} {customer.last_name}".strip(), # Dùng strip() để loại bỏ khoảng trắng thừa
                    'email': customer.email,
                    'phone': customer.phone
                }
            
            # Phân loại khách hàng mới và khách hàng quay lại
            new_customers = 0
            returning_customers = 0
            
            thirty_days_ago = self.today - timedelta(days=30)
            
            for item in customer_stats:
                if item['first_order_date'] >= thirty_days_ago:
                    new_customers += 1
                else:
                    returning_customers += 1
            
            print(f"[STATS_SERVICE] Khách hàng mới: {new_customers}, Khách hàng quay lại: {returning_customers}")
            
            # Chuẩn bị kết quả
            detailed_top_revenue = []
            detailed_top_orders = []
            
            for item in customer_stats[:20]:
                customer_id = str(item['_id'])
                details = customer_details.get(customer_id, {})
                
                # Xử lý total_revenue (Decimal128)
                revenue_value = item['total_revenue']
                try:
                    total_revenue = float(revenue_value.to_decimal())
                except AttributeError:
                    total_revenue = float(revenue_value)
                
                details['orders_count'] = item['orders_count']
                details['total_revenue'] = total_revenue
                details['avg_order_value'] = total_revenue / item['orders_count'] if item['orders_count'] > 0 else 0
                
                detailed_top_revenue.append(details.copy())
                
                # Tạo bản sao cho danh sách theo số đơn hàng
                orders_details = details.copy()
                detailed_top_orders.append(orders_details)
            
            # Sắp xếp lại theo số đơn hàng
            detailed_top_orders.sort(key=lambda x: x['orders_count'], reverse=True)
            
            
            result = {
                'total_customers': len(customer_ids),
                'new_vs_returning': {
                    'new_customers': new_customers,
                    'returning_customers': returning_customers,
                    'new_percentage': round(new_customers / len(customer_ids) * 100, 2) if len(customer_ids) > 0 else 0
                },
                'top_by_orders': detailed_top_orders,
                'top_by_revenue': detailed_top_revenue
            }
            
            print(f"[STATS_SERVICE] Đã hoàn thành thống kê khách hàng")
            return result
        except Exception as e:
            print(f"[STATS_SERVICE] Lỗi khi lấy thống kê khách hàng: {str(e)}")
            import traceback
            traceback.print_exc()
            raise