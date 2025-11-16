import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createNotivue } from 'notivue'

import App from './App.vue'
import router from './router'

// Import Notivue styles
import 'notivue/notifications.css'
import 'notivue/animations.css'

// Import permission directives
import { vPermission, vRole } from './directives/permission'

const app = createApp(App)

// Register permission directives
app.directive('permission', vPermission)
app.directive('role', vRole)

const notivue = createNotivue({
  position: 'top-right',
  limit: 4,
  enqueue: true,
  notifications: {
    global: {
      duration: 3000
    }
  }
})

app.use(createPinia())
app.use(router)
app.use(notivue)

app.mount('#app')