<template>
  <div class="cx-app">
    <AppHeader />
    <MemberFlightCard />
    <main class="cx-main cx-container">
      <router-view />
    </main>
    <AppFooter />
  </div>
</template>

<script setup>
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
import MemberFlightCard from '@/components/MemberFlightCard.vue'
</script>

<style>
.cx-app { background: var(--bg); min-height: 100vh; }
.cx-container { max-width: 1280px; margin: 0 auto; padding: 0 16px; }
.cx-main { padding-top: 12px; padding-bottom: 24px; }
</style>
