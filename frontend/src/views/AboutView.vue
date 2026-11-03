<script setup>
import AppHeader from '../components/common/AppHeader.vue'
import Footer from '../components/common/Footer.vue'
import AboutCTA from '../components/about/AboutCTA.vue'
import AboutFAQ from '../components/about/AboutFAQ.vue'
import AboutFeaturesSection from '../components/about/AboutFeaturesSection.vue'
import AboutHero from '../components/about/AboutHero.vue'
import AITechnologySection from '../components/about/AITechnologySection.vue'
import DeviceRequirementsSection from '../components/about/DeviceRequirementsSection.vue'
import DeviceSetupGuide from '../components/about/DeviceSetupGuide.vue'
import HowToUseSection from '../components/about/HowToUseSection.vue'
import MissionSection from '../components/about/MissionSection.vue'
import ScrollReveal from '../components/about/ScrollReveal.vue'
</script>

<template>
  <div class="about-page min-h-screen w-full overflow-x-clip bg-kids-bg">
    <AppHeader />
    <main>
      <AboutHero />
      <ScrollReveal><MissionSection /></ScrollReveal>
      <ScrollReveal><AITechnologySection /></ScrollReveal>
      <ScrollReveal><AboutFeaturesSection /></ScrollReveal>
      <ScrollReveal><DeviceRequirementsSection /></ScrollReveal>
      <ScrollReveal><DeviceSetupGuide /></ScrollReveal>
      <ScrollReveal><HowToUseSection /></ScrollReveal>
      <ScrollReveal><AboutFAQ /></ScrollReveal>
      <ScrollReveal><AboutCTA /></ScrollReveal>
    </main>
    <Footer />
  </div>
</template>

<style>
html:has(.about-page) {
  scroll-behavior: smooth;
}

@media (prefers-reduced-motion: reduce) {
  html:has(.about-page) {
    scroll-behavior: auto;
  }
}
</style>
