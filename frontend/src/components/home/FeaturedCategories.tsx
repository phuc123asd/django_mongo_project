import { Link } from 'react-router-dom';
import { SmartphoneIcon, LaptopIcon, WatchIcon, GamepadIcon } from 'lucide-react';
const categories = [{
  id: 1,
  name: 'Smartphones',
  icon: <SmartphoneIcon className="w-8 h-8" />,
  image: 'https://images.unsplash.com/photo-1598327105666-5b89351aff97?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80',
  link: '/shop?category=Smartphones'
}, {
  id: 2,
  name: 'Laptops',
  icon: <LaptopIcon className="w-8 h-8" />,
  image: 'https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80',
  link: '/shop?category=Laptops'
}, {
  id: 3,
  name: 'Smartwatches',
  icon: <WatchIcon className="w-8 h-8" />,
  image: 'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1472&q=80',
  link: '/shop?category=Smartwatches'
}, {
  id: 4,
  name: 'Gaming',
  icon: <GamepadIcon className="w-8 h-8" />,
  image: 'https://images.unsplash.com/photo-1593305841991-05c297ba4575?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1474&q=80',
  link: '/shop?category=Gaming'
}];
export const FeaturedCategories = () => {
  return <section className="py-16 bg-white dark:bg-gray-900">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Mua Sắm Theo Danh Mục
          </h2>
          <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Khám phá bộ sưu tập đa dạng các sản phẩm công nghệ cao cấp
            theo các danh mục phổ biến
          </p>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {categories.map(category => <Link to={category.link} key={category.id} className="group relative overflow-hidden rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
              <div className="aspect-square relative">
                <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-black/10 z-10"></div>
                <img src={category.image} alt={category.name} className="absolute inset-0 w-full h-full object-cover object-center group-hover:scale-110 transition-transform duration-500" />
                <div className="absolute inset-0 flex flex-col justify-end p-6 z-20">
                  <div className="bg-white/20 dark:bg-gray-800/30 backdrop-blur-sm rounded-full p-3 w-fit mb-3 group-hover:bg-indigo-600/80 transition-colors duration-300">
                    {category.icon}
                  </div>
                  <h3 className="text-xl font-bold text-white mb-1">
                    {category.name}
                  </h3>
                  <p className="text-gray-200 text-sm">Mua Ngay</p>
                </div>
              </div>
            </Link>)}
        </div>
      </div>
    </section>;
};