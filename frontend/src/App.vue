<template>
<div id="app">
<NavBar  v-if="flag" />

<main>
  <router-view/>
</main>
</div>
</template>

<script>

import NavBar from './components/NavBar.vue';

export default {
  components: { NavBar },

  data(){
  return{
    flag1 : false,
    flag2 : false,
    flag: false
  }
},
  mounted() {
    let id = localStorage.id;
    this.getrouteflags();
    return {
      id
    }
},
  methods : {
    getrouteflags: function(){
      console.log(this.$route.query.name)
      if(this.$route.name == 'register'){
        this.flag1 = true;
      }
      if(this.$route.name == 'login'){
        this.flag2 = true;
      }
      this.flag = this.flag1 || this.flag2;
      console.log(this.flag1,this.flag2)
    }
  }
}
</script>

<style>
nav{
  
}
#app{
  width: 100%;
  height: 100%;
}
html,
body {
  height: 100%;
  min-height: 75rem;
}

body {
  justify-content: center;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
  align-items: center;
  padding-top: 40px;
  padding-bottom: 40px;
  background-color: #f5f5f5;
  background-image: '../../backend/static/plot.png';
}

.form-signin {
  width: 100%;
  max-width: 330px;
  padding: 15px;
  margin: auto;
}
.form-signin .checkbox {
  font-weight: 400;
}
.form-signin .form-control {
  position: relative;
  box-sizing: border-box;
  height: auto;
  padding: 10px;
  font-size: 16px;
}
.form-signin .form-control:focus {
  z-index: 2;
}
.form-signin input[type="email"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}
.form-signin input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
body,html{
   padding: 0;
   margin: 0;
   min-height: 100vh;
   width: 100%;
}
html{
   background-color: white;
}

</style>
