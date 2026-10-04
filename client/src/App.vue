<script setup>
import { NConfigProvider, NMessageProvider, NTooltip, NButton } from 'naive-ui'
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
          <div class="how-it-works">
            <n-tooltip :style="{ maxWidth: '420px' }" trigger="click">
              <template #trigger>
                <n-button quaternary>Как это работает?</n-button>
              </template>
              Глава дня меняется ежедневно и едина для всех читателей. Её номер определяется недельной главой Торы и сегодняшней датой.
            </n-tooltip>
          </div>
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
.how-it-works {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}
</style>