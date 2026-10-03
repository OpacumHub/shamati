<script setup>
import { NCard, NSkeleton } from 'naive-ui'

defineProps({
  chapter: {
    type: Object,
    default: null,
  },
  loading: {
    type: Boolean,
    default: false,
  },
})
</script>

<template>
  <n-card class="chapter">
    <!-- идёт загрузка — показываем скелетон -->
    <template v-if="loading">
      <n-skeleton text style="width: 60%; height: 28px" />
      <n-skeleton text style="width: 40%; margin-top: 12px" />
      <n-skeleton text :repeat="8" style="margin-top: 20px" />
    </template>

    <!-- глава загружена -->
    <template v-else-if="chapter">
      <h1 class="chapter__title">
        {{ chapter.number }}. {{ chapter.title }}
      </h1>
      <p v-if="chapter.heard" class="chapter__heard" v-html="chapter.heard"></p>

      <div class="chapter__body" v-html="chapter.content_html"></div>

      <div v-if="chapter.footnotes && chapter.footnotes.length" class="chapter__footnotes">
        <h3>Примечания</h3>
        <ol>
          <li v-for="fn in chapter.footnotes" :key="fn.n" :id="`fn-${fn.n}`">
            {{ fn.text }}
          </li>
        </ol>
      </div>
    </template>
  </n-card>
</template>

<style scoped>
.chapter__heard { color: #888; font-style: italic; margin-bottom: 20px; font-size: 17px; }
.chapter__title { font-size: 24px; margin-bottom: 8px; }
.chapter__heard :deep(sup) { font-size: 0.7em; }
.chapter__heard :deep(a) { color: #0077ff; text-decoration: none; }
.chapter__body { line-height: 1.7; font-size: 17px; }
.chapter__body :deep(p) { margin-bottom: 16px; }
.chapter__footnotes { margin-top: 32px; padding-top: 16px; border-top: 1px solid #eee; font-size: 14px; color: #555; }
.chapter__footnotes ol { padding-left: 24px; }
.chapter__footnotes li { margin-bottom: 8px; }
</style>