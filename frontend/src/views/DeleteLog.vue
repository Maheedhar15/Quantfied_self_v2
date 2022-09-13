<template>
    <div class="app">
  
    </div>
  </template>
  
  <script>
  import { useRouter } from 'vue-router'
  import axios from 'axios'
  export default {
  Name: 'DeleteLog',
  data() {
      return{
          lid: this.$route.params.l_id
      }
  },
  created(){
      const router = useRouter();
      const path = 'http://localhost:5000/deleteLog/'+ this.lid
      axios.get(path)
      .then((resp)=>{
          console.log(resp.data)
          router.push({name: 'Trackers', params: {id : localStorage['id']}})
          alert('The Log has been successfully Deleted')
      })
      .catch((err) => console.log(err.response) )
  }
  
  }
  </script>
  
  <style>
  
  </style>