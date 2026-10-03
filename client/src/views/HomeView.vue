<script setup>
import { onMounted } from 'vue'
import { chapterState, loadDaily } from '../stores/chapter'
import ChapterContent from '../components/ChapterContent.vue'

onMounted(() => {
  document.title = 'Шамати. Бааль Сулам'
  loadDaily()                    // главная = всегда статья дня
})
</script>

<template>
  <ChapterContent :chapter="chapterState.chapter" :loading="chapterState.loading" />
</template>