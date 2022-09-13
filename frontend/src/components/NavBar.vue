<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light navbar-fixed-top">
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item" v-if="flag1" >
        <router-link to="/" class="nav-link" tabindex="-1"  >Login</router-link>
      </li>
      <li class="nav-item" v-if="flag2">
        <router-link to="/register" class="nav-link" tabindex="-1">Register</router-link>
      </li>
      
    </ul>
  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item" v-if="!flag2">
        <button class="nav-link btn btn-outline-danger" @click="trackers" tabindex="-1">Your Trackers</button>
      </li> 
      <li class="nav-item" >
        <router-link to="/about" class="nav-link" tabindex="-1">about</router-link>
      </li>
      <li class="nav-item" >
        <button @click="logout" class="nav-link btn btn-outline-danger" tabindex="-1">logout</button>
      </li>
      
    </ul>
  </div>
  </div>
</nav>
</template>

<script>
import { useRouter } from 'vue-router';
export default {
Name: 'NavBar',
created() {
    let flag1 = false;
    let flag2 = false;
    if(this.$route.name == 'Register'){
      flag1 = true;
    }
    if(this.$route.name == 'Login'){
      flag2 = true;
    }
    
    let id = localStorage.id;
    return {
      flag1,
      flag2,
      id
    }
},
setup() {
  const router = useRouter();
  const logout = async () => {
    await  router.push({name: 'logout',params : {id : localStorage['id']}});
    }
  const trackers = async () => {
    await  router.push({name: 'Trackers',params : {id : localStorage['id']}});
    }
  return{
    logout,
    trackers
  }
}
}
</script>

<style>
.navbar{
  position: fixed;
  top: 0;
}
nav{
    width:100%;
}
</style>