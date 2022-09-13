<template>
    <div class="app">
  
    </div>
  </template>
  
  <script>
  import { useRouter } from 'vue-router'
  import axios from 'axios'
  export default {
  Name: 'LogOut',
  data() {
  },
  created(){
      const router = useRouter();
      const path = 'http://localhost:5000/logout'
      axios.get(path)
      .then((resp)=>{
          console.log(resp.data)
          router.push({name: 'Login'})
          alert('You have been Successfully Logged out')
      })
      .catch((err) => console.log(err.response) )
  }
  
  }
  </script>
  
  <style>
  
  </style>