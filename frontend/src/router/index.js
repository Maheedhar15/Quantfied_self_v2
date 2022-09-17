import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView'
import RegisterView from '../views/RegisterView'
import TrackersView from '@/views/TrackersView';
import CreateTracker from '@/views/CreateTracker'
import DeleteTracker from '@/views/DeleteTracker'
import UpdateTracker from '@/views/UpdateTracker'
import AddLog from '@/views/AddLog'
import TrackerInfo from '@/views/TrackerInfo'
import UpdateLog from '@/views/UpdateLog'
import DeleteLog from '@/views/DeleteLog'
import LogOut from '@/views/LogOut'
import ForgotPass1 from '@/views/ForgotPass1'
import VerifyPass from '@/views/VerifyPass'
import ChangePass from '@/views/ChangePass'


const routes = [
  {
    path: '/',
    name: 'login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  {
    path: '/dashboard/:id',
    name: 'Dashboard',
    component: HomeView
  },
  {
    path: '/trackers/:id',
    name:'Trackers',
    component: TrackersView
  },

  {
    path: '/logout/:id',
    name: 'logout',
    component: LogOut
  },
  {
    path: '/createtracker/:id',
    name: 'createtracker',
    component: CreateTracker
  },
  {
    path: '/trackers/:id/Delete',
    name: 'tdelete',
    component: DeleteTracker
  },
  {
    path: '/trackers/:id/Update',
    name: 'tupdate',
    component: UpdateTracker
  },
  {
    path: '/addLog/:uid/:tid',
    name: 'AddLog',
    component: AddLog
    
  },
  {
    path: '/updateLog/:l_id/:tid',
    name: 'UpdateLog',
    component : UpdateLog
  },
  {
    path: '/deleteLog/:l_id',
    name: 'DeleteLog',
    component : DeleteLog
  },
  {
    path: '/viewtracker/:uid/:tid',
    name: 'Trackerinfo',
    component: TrackerInfo
  },
  {
    path: '/forgotpass1',
    name: 'forgotpass1',
    component: ForgotPass1
  },
  {
    path:'/verifypass',
    name: 'verifypass',
    component: VerifyPass
  },
  {
    path:'/changepass',
    name: 'changepass',
    component: ChangePass
  },


]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
