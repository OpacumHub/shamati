import { reactive } from 'vue'
import axios from 'axios'

// общее реактивное состояние текущей показанной главы
export const chapterState = reactive({
  chapter: null,     // показанная глава
  loading: false,
})

// показать случайную главу (меняет только контент, не адрес)
export async function loadRandom() {
  chapterState.loading = true
  try {
    const { data } = await axios.get('/api/chapters/random')
    chapterState.chapter = data
  } catch (e) {
    console.error('Ошибка загрузки случайной главы:', e)
  } finally {
    chapterState.loading = false
  }
}

// показать главу по id (для страницы /chapter/:id)
export async function loadById(id) {
  chapterState.loading = true
  try {
    const { data } = await axios.get(`/api/chapters/${id}`)
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

// статья дня (пока заглушка — временно случайная; в блоке Торы заменим на дату+seed)
export async function loadDaily() {
  chapterState.loading = true
  try {
    // TODO: заменить на /api/chapters/daily когда сделаем Тора-seed
    const { data } = await axios.get('/api/chapters/random')
    chapterState.chapter = data
  } catch (e) {
    console.error('Ошибка загрузки статьи дня:', e)
  } finally {
    chapterState.loading = false
  }
}