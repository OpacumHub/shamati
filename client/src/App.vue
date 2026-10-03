<script setup>
import { NConfigProvider, NMessageProvider } from 'naive-ui'
import AppHeader from './components/AppHeader.vue'

const themeOverrides = {
  common: {
    primaryColor: '#0077ff',
    primaryColorHover: '#2b8fff',
    primaryColorPressed: '#0062d6',
  },
}
</script>

<template>
  <n-config-provider :theme-overrides="themeOverrides">
    <n-message-provider placement="bottom">
      <div class="page">
        <div class="container">
          <AppHeader />
          <router-view />
        </div>
      </div>
    </n-message-provider>
  </n-config-provider>
</template>

<style scoped>
.container {
  max-width: 720px;
  width: 100%;
}
</style>