import React from 'react';
const brands = [{
  id: 1,
  name: 'Apple',
  logo: 'https://cdn-icons-png.flaticon.com/128/5977/5977575.png'
}, {
  id: 2,
  name: 'Samsung',
  logo: 'https://cdn-icons-png.flaticon.com/128/16183/16183659.png'
}, {
  id: 3,
  name: 'Dell',
  logo: 'https://cdn-icons-png.flaticon.com/128/882/882726.png'
}, {
  id: 4,
  name: 'Microsoft',
  logo: 'https://cdn-icons-png.flaticon.com/512/732/732221.png'
}, {
  id: 5,
  name: 'Google',
  logo: 'https://cdn-icons-png.flaticon.com/512/2702/2702602.png'
}, {
  id: 6,
  name: 'Nvdia',
  logo: 'https://cdn-icons-png.flaticon.com/128/882/882731.png'
}];
export const BrandsShowcase = () => {
  return <section className="py-12 bg-gray-50 dark:bg-gray-800">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Thương Hiệu Uy Tín
          </h2>
        </div>
        <div className="flex flex-wrap justify-center items-center gap-8 md:gap-16">
          {brands.map(brand => <div key={brand.id} className="w-24 h-24 flex items-center justify-center grayscale hover:grayscale-0 transition-all duration-300">
              <img src={brand.logo} alt={brand.name} className="max-h-12 max-w-full" />
            </div>)}
        </div>
      </div>
    </section>;
};