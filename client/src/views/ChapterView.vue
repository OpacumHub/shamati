<script setup>
import { watch } from 'vue'
import { useRoute } from 'vue-router'
import { NResult, NButton } from 'naive-ui'
import { chapterState, loadById } from '../stores/chapter'
import ChapterContent from '../components/ChapterContent.vue'

const route = useRoute()
const notFound = ref(false)

import { ref } from 'vue'

watch(
  () => route.params.id,
  async (id) => {
    const ok = await loadById(id)
    notFound.value = !ok
    if (ok) document.title = `Шамати — ${chapterState.chapter.title}`
    else document.title = 'Шамати — глава не найдена'
  },
  { immediate: true },
)
</script>

<template>
  <n-result
    v-if="notFound"
    status="404"
    title="Глава не найдена"
    description="Возможно, ссылка неверна."
  >
  
  </n-result>
  <ChapterContent v-else :chapter="chapterState.chapter" :loading="chapterState.loading" />
</template>