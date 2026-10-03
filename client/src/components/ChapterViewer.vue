<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { NCard, NButton } from 'naive-ui'

// реактивное состояние: сюда ляжет пришедшая глава (пока ничего = null)
const chapter = ref(null)
// флаг загрузки — чтобы показать "идёт запрос" и заблокировать кнопку
const loading = ref(false)

// метод: сходить на API за случайной главой
async function loadChapter() {
  loading.value = true                // начали загрузку
  try {
    const response = await axios.get('/api/chapters/random')
    chapter.value = response.data     // кладём данные в реактивное состояние
  } catch (error) {
    console.error('Ошибка загрузки главы:', error)
  } finally {
    loading.value = false             // загрузка завершена (в любом случае)
  }
}
</script>

<template>
  <n-card title="Шамати" class="chapter-card">
    <n-button
      type="primary"
      size="large"
      :loading="loading"
      @click="loadChapter"
    >
      Выбрать главу
    </n-button>

    <!-- временный вывод: покажем сырые данные, если глава загружена -->
    <pre v-if="chapter" class="debug">{{ chapter }}</pre>
  </n-card>
</template>

<style scoped>
.chapter-card {
  max-width: 700px;
  width: 100%;
}
.debug {
  margin-top: 16px;
  padding: 12px;
  background: #f0f0f0;
  border-radius: 6px;
  white-space: pre-wrap;
  word-break: break-word;
  font-size: 12px;
}
</style>