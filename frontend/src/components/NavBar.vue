<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light navbar-fixed-top">
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item" >
        <button class="nav-link btn btn-outline-dark" @click="trackers" tabindex="-1">Your Trackers</button>
      </li> 
      <li class="nav-item">
        <router-link :to="{ name: 'logout' , params : {id : id}}" class="nav-link">Logout</router-link>
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
data(){
  return{
    id : localStorage['id'],
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