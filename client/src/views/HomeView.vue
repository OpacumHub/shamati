<script setup>
import { onMounted } from 'vue'
import { chapterState, loadDaily } from '../stores/chapter'
import ChapterContent from '../components/ChapterContent.vue'

onMounted(() => {
  document.title = 'Шамати. Бааль Сулам'
  // грузим статью дня только при первом/чистом заходе.
  // если глава уже есть в состоянии (напр. нажали "Случайную") — не перетираем.
  if (!chapterState.chapter) {
    loadDaily()
  }
})
</script>

<template>
  <ChapterContent :chapter="chapterState.chapter" />
</template>