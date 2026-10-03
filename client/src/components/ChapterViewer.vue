<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { NCard, NButton, NSpin } from 'naive-ui'

const chapter = ref(null)
const loading = ref(false)

async function loadChapter() {
  loading.value = true
  try {
    const response = await axios.get('/api/chapters/random')
    chapter.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки главы:', error)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="viewer">
    <div class="controls">
      <n-button
        type="primary"
        size="large"
        :loading="loading"
        @click="loadChapter"
      >
        Выбрать главу
      </n-button>
    </div>

    <!-- пока главы нет и не грузим — подсказка -->
    <p v-if="!chapter && !loading" class="hint">
      Нажми кнопку, чтобы открыть главу.
    </p>

    <!-- глава загружена — показываем -->
    <n-card v-if="chapter" class="chapter">
      <h1 class="chapter__title">
        {{ chapter.number }}. {{ chapter.title }}
      </h1>
      <p v-if="chapter.heard" class="chapter__heard">
        {{ chapter.heard }}
      </p>

      <!-- тело главы: это готовый HTML из базы -->
      <div class="chapter__body" v-html="chapter.content_html"></div>

      <!-- сноски, если есть -->
      <div v-if="chapter.footnotes && chapter.footnotes.length" class="chapter__footnotes">
        <h3>Примечания</h3>
        <ol>
          <li v-for="fn in chapter.footnotes" :key="fn.n" :id="`fn-${fn.n}`">
            {{ fn.text }}
          </li>
        </ol>
      </div>
    </n-card>
  </div>
</template>

<style scoped>
.viewer {
  max-width: 720px;
  width: 100%;
}
.controls {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}
.hint {
  text-align: center;
  color: #888;
}
.chapter__title {
  font-size: 24px;
  margin-bottom: 8px;
}
.chapter__heard {
  color: #888;
  font-style: italic;
  margin-bottom: 20px;
}
.chapter__body {
  line-height: 1.7;
  font-size: 17px;
}
.chapter__body :deep(p) {
  margin-bottom: 16px;
}
.chapter__footnotes {
  margin-top: 32px;
  padding-top: 16px;
  border-top: 1px solid #eee;
  font-size: 14px;
  color: #555;
}
.chapter__footnotes li {
  margin-bottom: 8px;
}
</style>