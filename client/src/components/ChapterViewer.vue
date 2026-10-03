<script setup>
import { NCard, NButton } from 'naive-ui'
</script>

<template>
  <n-card title="Шамати" class="chapter-card">
    <p>Нажми кнопку, чтобы открыть главу.</p>
    <n-button type="primary" size="large">
      Выбрать главу
    </n-button>
  </n-card>
</template>

<style scoped>
.chapter-card {
  max-width: 700px;
  width: 100%;
}
</style>