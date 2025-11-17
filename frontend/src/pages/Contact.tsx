import React, { useState, lazy } from 'react';
import { Button } from '../components/ui/Button';
import { MapPinIcon, PhoneIcon, MailIcon, ClockIcon, SendIcon } from 'lucide-react';
export const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    setIsSubmitting(false);
    setIsSubmitted(true);
    setFormData({
      name: '',
      email: '',
      subject: '',
      message: ''
    });
    // Reset success message after 5 seconds
    setTimeout(() => setIsSubmitted(false), 5000);
  };
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };
  const contactInfo = [{
    icon: <MapPinIcon className="w-6 h-6" />,
    title: 'Ghé Thăm',
    content: '123 Đường Xuân Hồng, Hồ Chí Minh, Việt Nam'
  }, {
    icon: <PhoneIcon className="w-6 h-6" />,
    title: 'Gọi Cho Chúng Tôi',
    content: '+84 (032) 511-6160'
  }, {
    icon: <MailIcon className="w-6 h-6" />,
    title: 'Email',
    content: 'support@techhub.com'
  }, {
    icon: <ClockIcon className="w-6 h-6" />,
    title: 'Giờ Làm Việc',
    content: 'Thứ 2-6: 9:00-18:00 (GMT+7)'
  }];
  return <div className="bg-white dark:bg-gray-900">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-r from-indigo-600 to-purple-600 py-20">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl mx-auto text-center text-white">
            <h1 className="text-4xl md:text-5xl font-bold mb-6">
              Liên Hệ Với Chúng Tôi
            </h1>
            <p className="text-xl text-indigo-100">
              Có thắc mắc? Chúng tôi rất muốn nghe từ bạn. Gửi tin nhắn cho chúng tôi và
              chúng tôi sẽ phản hồi sớm nhất có thể.
            </p>
          </div>
        </div>
      </section>
      {/* Contact Info Cards */}
      <section className="py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
            {contactInfo.map((info, index) => <div key={index} className="bg-gray-50 dark:bg-gray-800 rounded-lg p-6 text-center">
                <div className="inline-flex items-center justify-center w-12 h-12 bg-indigo-100 dark:bg-indigo-900 rounded-full text-indigo-600 dark:text-indigo-400 mb-4">
                  {info.icon}
                </div>
                <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">
                  {info.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  {info.content}
                </p>
              </div>)}
          </div>
          {/* Contact Form & Map */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Contact Form */}
            <div>
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">
                Gửi Tin Nhắn Cho Chúng Tôi
              </h2>
              {isSubmitted && <div className="mb-6 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
                  <p className="text-green-800 dark:text-green-200">
                    Cảm ơn tin nhắn của bạn! Chúng tôi sẽ phản hồi sớm.
                  </p>
                </div>}
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Tên Của Bạn
                  </label>
                  <input type="text" id="name" name="name" required value={formData.name} onChange={handleChange} className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-white" placeholder="Nguyễn Văn A" />
                </div>
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Địa Chỉ Email
                  </label>
                  <input type="email" id="email" name="email" required value={formData.email} onChange={handleChange} className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-white" placeholder="email@example.com" />
                </div>
                <div>
                  <label htmlFor="subject" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Tiêu Đề
                  </label>
                  <input type="text" id="subject" name="subject" required value={formData.subject} onChange={handleChange} className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-white" placeholder="Chúng tôi có thể giúp gì cho bạn?" />
                </div>
                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Nội Dung
                  </label>
                  <textarea id="message" name="message" required rows={6} value={formData.message} onChange={handleChange} className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-white resize-none" placeholder="Cho chúng tôi biết thêm về câu hỏi của bạn..." />
                </div>
                <Button type="submit" disabled={isSubmitting} className="w-full" rightIcon={<SendIcon className="w-5 h-5" />}>
                  {isSubmitting ? 'Đang gửi...' : 'Gửi Tin Nhắn'}
                </Button>
              </form>
            </div>
            {/* Map */}
            <div>
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">
                Vị Trí Của Chúng Tôi
              </h2>
              <div className="bg-gray-200 dark:bg-gray-800 rounded-lg overflow-hidden h-96">
                <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3919.2048315846364!2d106.65100607485716!3d10.795618289354287!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3175293588d1a07b%3A0xa1b6b52e7a1260d2!2zMTIzIFh1w6JuIEjhu5NuZywgUGjGsOG7nW5nIDQsIFTDom4gQsOsbmgsIFRow6BuaCBwaOG7kSBI4buTIENow60gTWluaCwgVmnhu4d0IE5hbQ!5e0!3m2!1svi!2s!4v1763046133652!5m2!1svi!2s"  width="100%" height="100%" style={{
                border: 0
              }} allowFullScreen loading="lazy" referrerPolicy="no-referrer-when-downgrade" title="Vị trí TechHub" />
              </div>
              {/* FAQ Section */}
              <div className="mt-8 bg-gray-50 dark:bg-gray-800 rounded-lg p-6">
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
                  Câu Hỏi Thường Gặp
                </h3>
                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium text-gray-900 dark:text-white mb-1">
                      Thời gian giao hàng là bao lâu?
                    </h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Chúng tôi miễn phí giao hàng cho đơn hàng trên 1.000.000đ. Giao hàng tiêu chuẩn
                      mất 3-5 ngày làm việc.
                    </p>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900 dark:text-white mb-1">
                      Chính sách đổi trả như thế nào?
                    </h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Chúng tôi có chính sách đổi trả trong vòng 30 ngày cho tất cả sản phẩm. Sản phẩm
                      phải trong tình trạng ban đầu.
                    </p>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900 dark:text-white mb-1">
                      Có bảo hành không?
                    </h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Tất cả sản phẩm đều có bảo hành 1 năm từ nhà sản xuất.
                      Có thể mua thêm bảo hành mở rộng.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>;
};