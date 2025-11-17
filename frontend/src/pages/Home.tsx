import { HeroSection } from '../components/home/HeroSection';
import { FeaturedCategories } from '../components/home/FeaturedCategories';
import { PromoBanner } from '../components/home/PromoBanner';
import { Testimonials } from '../components/home/Testimonials';
import { BrandsShowcase } from '../components/home/BrandsShowcase';
export const Home = () => {
  return <div>
      <HeroSection />
      <FeaturedCategories />
      <PromoBanner />
      <Testimonials />
      <BrandsShowcase />
    </div>;
};