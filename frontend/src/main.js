import { createApp } from 'vue'
import { createI18n } from 'vue-i18n'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElIcons from '@element-plus/icons-vue'

import router from './router'
import zh from './i18n/zh.json'
import zhHK from './i18n/zh-HK.json'
import en from './i18n/en.json'
import './styles/theme.css'
import App from './App.vue'
import pinia from './stores'
import { useAuthStore, registerAuthStoreInstance } from './stores/auth'

const i18n = createI18n({
  legacy: false,
  locale: 'zh-HK',
  fallbackLocale: 'en',
  messages: { 'zh-HK': zhHK, 'zh': zh, 'en':en }
})

const app = createApp(App)
for (const [key, component] of Object.entries(ElIcons)) app.component(`i-ep-${key}`, component)

app.use(pinia).use(router).use(i18n).use(ElementPlus)

const authStore = useAuthStore(pinia)
registerAuthStoreInstance(authStore)
authStore.ensureSession()

app.mount('#app')
