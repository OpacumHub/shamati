<script setup>
import { NConfigProvider } from 'naive-ui'
import ChapterViewer from './components/ChapterViewer.vue'
</script>

<template>
  <n-config-provider>
    <div class="page">
      <ChapterViewer />
    </div>
  </n-config-provider>
</template>