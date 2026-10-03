<script setup>
import { NConfigProvider } from 'naive-ui'
import ChapterViewer from './components/ChapterViewer.vue'

// переопределение темы Naive UI
const themeOverrides = {
   common: {
    primaryColor: '#0077ff',
    primaryColorHover: '#2b8fff',   // светлее — при наведении
    primaryColorPressed: '#0062d6', // темнее — при нажатии
  },
}

</script>

<template>
  <n-config-provider :theme-overrides="themeOverrides">
    <div class="page">
      <ChapterViewer />
    </div>
  </n-config-provider>
</template>