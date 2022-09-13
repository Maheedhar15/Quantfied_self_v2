<template>
    <h1>Hello {{name}}</h1>
    <h3>This is your Trackers page</h3>
    <table class="table table-striped">
  <thead>
    <th>Sno</th>
    <th>Tracker name</th>
    <th>Tracker Description</th>
    <th>Tracker settings</th>
    <th>Date Created</th>
    <th>Add tracker log</th>
    <th>Actions</th>
  </thead>
  <tbody>
<tr v-for="item,index in items" :key="index">
                <th>{{index}}</th>
                <th> <router-link :to="`/viewtracker/${id}/${item.trackerid}`" style="text-decoration: none; color: orange;" >{{item.trackername}}</router-link> </th>
                <th>{{item.trackerdesc}}</th>
                <th>{{item.tracker_settings}}</th>
                <th>{{item.datecreated}}</th>
                <th><router-link :to="`/addLog/${id}/${item.trackerid}`" style="text-decoration:none; color: black;"><button class="btn btn-outline-dark">+</button> </router-link> </th>
                <th><button class="btn btn-outline-dark"><router-link :to="`/trackers/${item.trackerid}/Update`" style="text-decoration:none; color: black;">Update</router-link></button>
                </th>
                <th>  <button class="btn btn-outline-dark">  <router-link :to="`/trackers/${item.trackerid}/Delete`" style="text-decoration:none; color: black;">Delete</router-link></button></th>
                
            </tr>
  </tbody>
</table>


<button class="btn btn-outline-dark" @click="createtracker">Click to add trackers</button>
</template>

<script>
import { useRouter } from 'vue-router';
import axios from 'axios';
export default {
Name: 'TrackersView',
mounted() {
    let id = localStorage['id'] 
    return{
        id,
    }
},
data() {
    return {
        name: localStorage.name,
        items : [],
        id : localStorage['id'] 
        
    }
},
methods:{
  getTrackers(){
    const router = useRouter()
    const path = 'http://localhost:5000/trackers/'+ localStorage['id'] 
    axios.get(path)
    .then((res) => {
      this.items = res.data.tracker
  })
 
    .catch((err) => {
      if(err.response.status == 401){
        router.push({name:'Login'})
        alert("Token expired")
      }
    })

    console.log(this.items);
  },
},
setup() {
  const router = useRouter();
  const createtracker = async () => {
    await  router.push({name: 'createtracker',params : {id : localStorage['id']}});
    };
    return{
        createtracker,
    }
},
created() {
  this.getTrackers();
}
}
</script>

<style scoped>


    body {
    background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
    height: 100vh;
  }
  
  @keyframes gradient {
    0% {
      background-position: 0% 50%;
    }
    50% {
      background-position: 100% 50%;
    }
    100% {
      background-position: 0% 50%;
    }
  }
</style>