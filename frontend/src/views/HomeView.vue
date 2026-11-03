<script setup>
import AppHeader from '../components/common/AppHeader.vue'
import Footer from '../components/common/Footer.vue'
import AboutSection from '../components/home/AboutSection.vue'
import AchievementSection from '../components/home/AchievementSection.vue'
import AchievementSlider from '../components/home/AchievementSlider.vue'
import AppDownloadSection from '../components/home/AppDownloadSection.vue'
import AudienceSection from '../components/home/AudienceSection.vue'
import ExperienceSection from '../components/home/ExperienceSection.vue'
import FaqSection from '../components/home/FaqSection.vue'
import FeaturesSection from '../components/home/FeaturesSection.vue'
import HeroSection from '../components/home/HeroSection.vue'
import HomeCtaSection from '../components/home/HomeCtaSection.vue'
import ProblemSection from '../components/home/ProblemSection.vue'
import StepsSection from '../components/home/StepsSection.vue'
</script>

<template>
  <div class="min-h-screen w-full overflow-x-clip bg-kids-bg">
    <AppHeader />
    <main>
      <HeroSection />
      <ProblemSection />
      <AboutSection />
      <FeaturesSection />
      <AchievementSlider />
      <StepsSection />
      <ExperienceSection />
      <AppDownloadSection />
      <AchievementSection />
      <AudienceSection />
      <FaqSection />
      <HomeCtaSection />
    </main>
    <Footer />
  </div>
</template>
