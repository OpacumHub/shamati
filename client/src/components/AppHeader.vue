<script setup>
import { NButton, useMessage } from 'naive-ui'
import { useRoute, useRouter } from 'vue-router'
import { chapterState, fetchRandom } from '../stores/chapter'

const message = useMessage()
const route = useRoute()
const router = useRouter()

async function showRandom() {
  try {
    const id = await fetchRandom()
    router.push(`/chapter/${id}`)
  } catch (e) {
    console.error('Ошибка загрузки случайной главы:', e)
    message.error('Не удалось загрузить главу')
  }
}

function goHome() {
  router.push('/')
}

function copyLink() {
  const ch = chapterState.chapter
  if (!ch) {
    message.warning('Сначала откройте главу')
    return
  }
  const url = `${window.location.origin}/chapter/${ch.id}`
  navigator.clipboard.writeText(url)
    .then(() => message.success('Ссылка скопирована'))
    .catch(() => message.error('Не удалось скопировать'))
}
</script>

<template>
    <header class="site-header">
        <h1 class="site-header__title">Шамати</h1>
        <p class="site-header__author">Йегуда Лейб Алеви Ашлаг (Бааль Сулам)</p>

        <div class="site-header__controls">
            <n-button type="primary" size="large" :loading="chapterState.loading" @click="showRandom">
                Случайная статья
            </n-button>

            <n-button type="primary" ghost size="large" @click="copyLink">
                Скопировать ссылку
            </n-button>

            <n-button  v-if="route.path !== '/'"  type="primary" dashed size="large" @click="goHome">
                На главную
            </n-button>
        </div>

    </header>
</template>

<style scoped>
.site-header {
    text-align: center;
    margin-bottom: 24px;
}

.site-header__title {
    font-size: 32px;
    margin-bottom: 4px;
}

.site-header__author {
    color: #888;
    font-size: 16px;
    margin-bottom: 20px;
    font-size: 17px;
}

.site-header__controls {
    display: flex;
    gap: 12px;
    justify-content: center;
}
</style>