import { reactive } from 'vue'
import axios from 'axios'

// искусственная задержка (мс) — чтобы скелетон был виден
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

// общее реактивное состояние текущей показанной главы
export const chapterState = reactive({
  chapter: null,     // показанная глава
  loading: false,        // общая загрузка (скелетон)
  randomLoading: false,  // только кнопка "Случайная"
})

// загрузить случайную главу В СОСТОЯНИЕ и вернуть её id (для перехода)
export async function fetchRandom() {
  chapterState.loading = true
  chapterState.randomLoading = true
  try {
    const { data } = await axios.get('/api/chapters/random')
    await delay(300)                 // искусственная секунда для скелетона
    chapterState.chapter = data       // кладём сразу, чтобы не грузить повторно
    return data.id
  } finally {
    chapterState.loading = false
    chapterState.randomLoading = false
  }
}

// показать главу по id (для страницы /chapter/:id)
export async function loadById(id) {
  // уже загружена эта глава (напр. пришли через "Случайную") — не грузим повторно
  if (chapterState.chapter && String(chapterState.chapter.id) === String(id)) {
    return true
  }
  chapterState.loading = true
  try {
    const { data } = await axios.get(`/api/chapters/${id}`)
    await delay(300)                 // искусственная секунда для скелетона
    chapterState.chapter = data
    return true
  } catch (e) {
    console.error('Ошибка загрузки главы:', e)
    chapterState.chapter = null
    return false
  } finally {
    chapterState.loading = false
  }
}

// статья дня
export async function loadDaily() {
  chapterState.loading = true
  try {
    const { data } = await axios.get('/api/chapters/daily')   // было /random
    await delay(300)                 // искусственная секунда для скелетона
    chapterState.chapter = data
  } catch (e) {
    console.error('Ошибка загрузки статьи дня:', e)
  } finally {
    chapterState.loading = false
  }
}

// export async function loadDaily() {
//   chapterState.loading = true
//   try {
//     // TODO: заменить на /api/chapters/daily когда сделаем Тора-seed
//     const { data } = await axios.get('/api/chapters/random')
//     chapterState.chapter = data
//   } catch (e) {
//     console.error('Ошибка загрузки статьи дня:', e)
//   } finally {
//     chapterState.loading = false
//   }
// }

