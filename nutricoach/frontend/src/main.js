import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router.js'
import { useThemeStore } from './stores/theme.js'

const app = createApp(App)
app.use(createPinia())

const themeStore = useThemeStore()
themeStore.init()

app.use(router)
app.mount('#app')
