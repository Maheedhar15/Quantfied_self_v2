import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import setAuthHeader from "../src/utils/AuthHeader";

if(localStorage.access_token){
    setAuthHeader(localStorage.getItem('access_token'));
}
else{
    setAuthHeader(false);
}


createApp(App).use(store).use(router).mount('#app')
