import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import HomeView from '../views/HomeView.vue'
import ProfileList from '../views/ProfileList.vue'
import ProfileDetail from '../views/ProfileDetail.vue'
import JobList from '../views/JobList.vue'
import ChatList from '../views/ChatList.vue'
import ChatRoom from '../views/ChatRoom.vue'
import JobDetail from '../views/JobDetail.vue'
import Menu from '../views/Menu.vue'
import ApplicationList from '../views/ApplicationList.vue'
import ApplicationDetail from '@/views/ApplicationDetail.vue'
import NotificationView from '../views/NotificationView.vue'
import JobEdit from '@/views/JobEdit.vue'
import JobCreate from '@/views/JobCreate.vue'
import JobApplication from '@/views/JobApplication.vue'
import Dashboard from '@/views/Dashboard.vue'
import MyJobList from '@/views/MyJobList.vue'
import RegisterVIew from '@/views/RegisterVIew.vue'
import ProfileEdit from '@/views/ProfileEdit.vue'
import ApplicationCreate from '@/views/ApplicationCreate.vue'

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/login', component: LoginView },
  { path: '/home', component: HomeView },
  { path: '/profile', component: ProfileList },
  { path: '/profile/:id', component: ProfileDetail },
  { path: '/job', component: JobList },
  { path: '/chat', component: ChatList, name: 'ChatList' },
  { path: '/chat/:id', component: ChatRoom, name: 'ChatRoom' },
  { path: '/job/:id', component: JobDetail },
  { path: '/menu', component: Menu },
  { path: '/application', component: ApplicationList },
  { path: '/application/:id', component: ApplicationDetail },
  { path: '/news', component: NotificationView, name: 'News' },
  { path: '/job/:id/edit', component: JobEdit },
  { path: '/job/create', component: JobCreate },
  { path: '/job/:id/application', component: JobApplication },
  { path: '/dashboard', component: Dashboard },
  { path: '/myjob', component: MyJobList },
  { path: '/register', component: RegisterVIew },
  { path: '/profile/:id/edit', component: ProfileEdit },
  { path: '/job/:id/apply', component: ApplicationCreate },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
