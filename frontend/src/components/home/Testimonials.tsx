import React, { useState } from 'react';
import { ChevronLeftIcon, ChevronRightIcon, StarIcon } from 'lucide-react';
const testimonials = [{
  id: 1,
  name: 'Sarah Johnson',
  role: 'Người Đam Mê Công Nghệ',
  image: 'https://randomuser.me/api/portraits/women/12.jpg',
  content: "Chất lượng sản phẩm thật tuyệt vời! Tôi đã sử dụng MacBook Pro mới để chỉnh sửa video và hiệu suất thật đáng kinh ngạc. Dịch vụ khách hàng cũng rất xuất sắc.",
  rating: 5
}, {
  id: 2,
  name: 'Michael Chen',
  role: 'Lập Trình Viên',
  image: 'https://randomuser.me/api/portraits/men/32.jpg',
  content: "Giao hàng nhanh và sản phẩm đúng như mô tả. Tôi cực kỳ hài lòng với đơn hàng và chắc chắn sẽ mua sắm ở đây lần nữa!",
  rating: 5
}, {
  id: 3,
  name: 'Emily Rodriguez',
  role: 'Nhà Sáng Tạo Nội Dung',
  image: 'https://randomuser.me/api/portraits/women/23.jpg',
  content: 'Chiếc điện thoại tôi mua đã vượt quá mong đợi. Chất lượng camera tuyệt vời và thời lượng pin ấn tượng. Rất đáng mua!',
  rating: 4
}, {
  id: 4,
  name: 'David Kim',
  role: 'Game Thủ',
  image: 'https://randomuser.me/api/portraits/men/46.jpg',
  content: 'Những phụ kiện gaming tôi mua đã thay đổi hoàn toàn setup của tôi. Chất lượng tốt và giá cả cạnh tranh hơn các cửa hàng khác.',
  rating: 5
}, {
  id: 5,
  name: 'Jessica Patel',
  role: 'Sinh Viên',
  image: 'https://randomuser.me/api/portraits/women/37.jpg',
  content: 'Là sinh viên, việc tìm công nghệ chất lượng với giá hợp lý rất quan trọng. Cửa hàng này có lựa chọn tốt nhất và giảm giá cho sinh viên. Laptop của tôi hoàn hảo cho nhu cầu học tập!',
  rating: 4
}];
export const Testimonials = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const nextSlide = () => {
    setCurrentIndex(prevIndex => prevIndex === testimonials.length - 1 ? 0 : prevIndex + 1);
  };
  const prevSlide = () => {
    setCurrentIndex(prevIndex => prevIndex === 0 ? testimonials.length - 1 : prevIndex - 1);
  };
  return <section className="py-16 bg-white dark:bg-gray-900">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Khách Hàng Nói Gì Về Chúng Tôi
          </h2>
          <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Đừng chỉ nghe chúng tôi nói — hãy lắng nghe từ những khách hàng hài lòng
          </p>
        </div>
        <div className="relative max-w-4xl mx-auto">
          <div className="overflow-hidden">
            <div className="flex transition-transform duration-500 ease-in-out" style={{
            transform: `translateX(-${currentIndex * 100}%)`
          }}>
              {testimonials.map(testimonial => <div key={testimonial.id} className="min-w-full px-4">
                  <div className="bg-gray-50 dark:bg-gray-800 rounded-xl p-8 shadow-lg">
                    <div className="flex flex-col md:flex-row md:items-center gap-6">
                      <div className="md:w-1/3 flex flex-col items-center">
                        <img src={testimonial.image} alt={testimonial.name} className="w-24 h-24 rounded-full object-cover mb-4" />
                        <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                          {testimonial.name}
                        </h3>
                        <p className="text-gray-600 dark:text-gray-400 mb-3">
                          {testimonial.role}
                        </p>
                        <div className="flex items-center">
                          {[...Array(5)].map((_, i) => <StarIcon key={i} className={`w-5 h-5 ${i < testimonial.rating ? 'text-amber-400 fill-amber-400' : 'text-gray-300 dark:text-gray-600'}`} />)}
                        </div>
                      </div>
                      <div className="md:w-2/3">
                        <div className="relative">
                          <svg className="absolute top-0 left-0 transform -translate-x-6 -translate-y-6 h-16 w-16 text-indigo-200 dark:text-indigo-700 opacity-50" width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                            <path d="M7.39762 10.3C7.39762 11.0733 7.14888 11.7 6.6514 12.18C6.15392 12.6333 5.52552 12.86 4.76621 12.86C3.84979 12.86 3.09047 12.5533 2.48825 11.94C1.91222 11.3266 1.62421 10.4467 1.62421 9.29999C1.62421 8.07332 1.96459 6.87332 2.64535 5.69999C3.35231 4.49999 4.33418 3.55332 5.59098 2.85999L6.4943 4.25999C5.81354 4.73999 5.26369 5.27332 4.84476 5.85999C4.45201 6.44666 4.19017 7.12666 4.05926 7.89999C4.29491 7.79332 4.56983 7.73999 4.88403 7.73999C5.61716 7.73999 6.21938 7.97999 6.69067 8.45999C7.16197 8.93999 7.39762 9.55333 7.39762 10.3ZM14.6242 10.3C14.6242 11.0733 14.3755 11.7 13.878 12.18C13.3805 12.6333 12.7521 12.86 11.9928 12.86C11.0764 12.86 10.3171 12.5533 9.71484 11.94C9.13881 11.3266 8.85079 10.4467 8.85079 9.29999C8.85079 8.07332 9.19117 6.87332 9.87194 5.69999C10.5789 4.49999 11.5608 3.55332 12.8176 2.85999L13.7209 4.25999C13.0401 4.73999 12.4903 5.27332 12.0713 5.85999C11.6786 6.44666 11.4168 7.12666 11.2858 7.89999C11.5215 7.79332 11.7964 7.73999 12.1106 7.73999C12.8437 7.73999 13.446 7.97999 13.9173 8.45999C14.3886 8.93999 14.6242 9.55333 14.6242 10.3Z" fill="currentColor" />
                          </svg>
                          <p className="relative text-lg md:text-xl text-gray-700 dark:text-gray-300 leading-relaxed">
                            {testimonial.content}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>)}
            </div>
          </div>
          <button onClick={prevSlide} className="absolute top-1/2 left-0 -translate-y-1/2 -translate-x-1/2 bg-white dark:bg-gray-800 rounded-full p-3 shadow-lg text-gray-800 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none" aria-label="Previous testimonial">
            <ChevronLeftIcon className="w-6 h-6" />
          </button>
          <button onClick={nextSlide} className="absolute top-1/2 right-0 -translate-y-1/2 translate-x-1/2 bg-white dark:bg-gray-800 rounded-full p-3 shadow-lg text-gray-800 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none" aria-label="Next testimonial">
            <ChevronRightIcon className="w-6 h-6" />
          </button>
          <div className="flex justify-center mt-8 space-x-2">
            {testimonials.map((_, index) => <button key={index} onClick={() => setCurrentIndex(index)} className={`w-3 h-3 rounded-full focus:outline-none ${index === currentIndex ? 'bg-indigo-600' : 'bg-gray-300 dark:bg-gray-700'}`} aria-label={`Go to testimonial ${index + 1}`} />)}
          </div>
        </div>
      </div>
    </section>;
};