import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/main.css'   // глобальные стили всего приложения

createApp(App).use(router).mount('#app')
