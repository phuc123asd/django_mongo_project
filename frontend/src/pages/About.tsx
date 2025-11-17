import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { UsersIcon, TrophyIcon, HeartIcon, ZapIcon, ArrowRightIcon } from 'lucide-react';
export const About = () => {
  const stats = [{
    label: 'Năm Hoạt Động',
    value: '10+'
  }, {
    label: 'Khách Hàng Hài Lòng',
    value: '50K+'
  }, {
    label: 'Sản Phẩm Đã Bán',
    value: '100K+'
  }, {
    label: 'Quốc Gia Phục Vụ',
    value: '25+'
  }];
  const values = [{
    icon: <TrophyIcon className="w-8 h-8" />,
    title: 'Chất Lượng Đầu Tiên',
    description: 'Chúng tôi chỉ cung cấp sản phẩm cao cấp, chính hãng từ các thương hiệu uy tín.'
  }, {
    icon: <HeartIcon className="w-8 h-8" />,
    title: 'Tập Trung Khách Hàng',
    description: "Sự hài lòng của bạn là ưu tiên hàng đầu. Chúng tôi luôn sẵn sàng hỗ trợ từng bước."
  }, {
    icon: <ZapIcon className="w-8 h-8" />,
    title: 'Đổi Mới',
    description: 'Chúng tôi luôn đi đầu xu hướng công nghệ để mang đến những sản phẩm tốt nhất.'
  }, {
    icon: <UsersIcon className="w-8 h-8" />,
    title: 'Cộng Đồng',
    description: 'Tham gia cùng hàng nghìn người đam mê công nghệ tin tưởng TechHub.'
  }];
  const team = [{
    name: 'Sarah Johnson',
    role: 'Giám Đốc Điều Hành & Nhà Sáng Lập',
    image: 'https://randomuser.me/api/portraits/women/1.jpg'
  }, {
    name: 'Michael Chen',
    role: 'Giám Đốc Công Nghệ',
    image: 'https://randomuser.me/api/portraits/men/2.jpg'
  }, {
    name: 'Emily Rodriguez',
    role: 'Trưởng Phòng Thành Công Khách Hàng',
    image: 'https://randomuser.me/api/portraits/women/3.jpg'
  }, {
    name: 'David Kim',
    role: 'Quản Lý Sản Phẩm',
    image: 'https://randomuser.me/api/portraits/men/4.jpg'
  }];
  return <div className="bg-white dark:bg-gray-900">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-r from-indigo-600 to-purple-600 py-20">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl mx-auto text-center text-white">
            <h1 className="text-4xl md:text-5xl font-bold mb-6">
              Về TechHub
            </h1>
            <p className="text-xl text-indigo-100">
              Điểm đến tin cậy của bạn cho các sản phẩm công nghệ cao cấp từ năm
              2014
            </p>
          </div>
        </div>
      </section>
      {/* Stats Section */}
      <section className="py-16 bg-gray-50 dark:bg-gray-800">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => <div key={index} className="text-center">
                <div className="text-4xl font-bold text-indigo-600 dark:text-indigo-400 mb-2">
                  {stat.value}
                </div>
                <div className="text-gray-600 dark:text-gray-400">
                  {stat.label}
                </div>
              </div>)}
          </div>
        </div>
      </section>
      {/* Story Section */}
      <section className="py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">
                Câu Chuyện Của Chúng Tôi
              </h2>
              <div className="space-y-4 text-gray-600 dark:text-gray-400">
                <p>
                  Được thành lập vào năm 2014, TechHub bắt đầu với sứ mệnh đơn giản: làm cho
                  công nghệ cao cấp trở nên dễ tiếp cận với mọi người. Từ một cửa hàng trực tuyến
                  nhỏ, chúng tôi đã phát triển thành điểm đến tin cậy cho những người đam mê
                  công nghệ trên toàn thế giới.
                </p>
                <p>
                  Chúng tôi tin rằng công nghệ nên nâng cao chất lượng cuộc sống, không làm phức tạp
                  thêm. Đó là lý do tại sao chúng tôi cẩn thận tuyển chọn sản phẩm, đảm bảo
                  mỗi sản phẩm đáp ứng tiêu chuẩn cao về chất lượng, đổi mới và giá trị.
                </p>
                <p>
                  Ngày nay, chúng tôi tự hào phục vụ hơn 50.000 khách hàng hài lòng tại
                  25 quốc gia, cung cấp mọi thứ từ smartphone mới nhất đến phụ kiện
                  tiên tiến. Nhưng cam kết của chúng tôi vẫn không đổi: sản phẩm đặc biệt,
                  dịch vụ xuất sắc và niềm đam mê công nghệ thúc đẩy mọi việc chúng tôi làm.
                </p>
              </div>
            </div>
            <div className="relative">
              <img src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80" alt="Team collaboration" className="rounded-lg shadow-xl" />
            </div>
          </div>
        </div>
      </section>
      {/* Values Section */}
      <section className="py-16 bg-gray-50 dark:bg-gray-800">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Giá Trị Cốt Lõi
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
              Những nguyên tắc cốt lõi định hướng mọi hoạt động của TechHub
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {values.map((value, index) => <div key={index} className="bg-white dark:bg-gray-900 rounded-lg p-6 text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-indigo-100 dark:bg-indigo-900 rounded-full text-indigo-600 dark:text-indigo-400 mb-4">
                  {value.icon}
                </div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
                  {value.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  {value.description}
                </p>
              </div>)}
          </div>
        </div>
      </section>
      {/* Team Section */}
      <section className="py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Gặp Gỡ Đội Ngũ
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
              Những con người đam mê đằng sau TechHub
            </p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {team.map((member, index) => <div key={index} className="text-center">
                <img src={member.image} alt={member.name} className="w-32 h-32 rounded-full mx-auto mb-4 object-cover" />
                <h3 className="text-lg font-bold text-gray-900 dark:text-white">
                  {member.name}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  {member.role}
                </p>
              </div>)}
          </div>
        </div>
      </section>
      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-indigo-600 to-purple-600">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-6">
            Sẵn Sàng Trải Nghiệm Sự Khác Biệt TechHub?
          </h2>
          <p className="text-xl text-indigo-100 mb-8 max-w-2xl mx-auto">
            Tham gia cùng hàng nghìn khách hàng hài lòng và khám phá tại sao TechHub
            là điểm đến hàng đầu cho những người đam mê công nghệ.
          </p>
          <Button as={Link} to="/shop" size="lg" className="bg-white text-indigo-600 hover:bg-gray-100" rightIcon={<ArrowRightIcon className="w-5 h-5" />}>
            Bắt Đầu Mua Sắm
          </Button>
        </div>
      </section>
    </div>;
};