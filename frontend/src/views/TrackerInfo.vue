<template>
  <h1 class="header">{{name}}</h1>
  <img  class="graph" src="../../../backend/static/plot.png" alt="" style="margin-top: 100px;">
  <table class="table table-striped">
  <thead>
    <th>Sno</th>
    <th>Date Created</th>
    <th>Note</th>
    <th>Value</th>
    <th>Actions</th>
  </thead>
  <tbody>
<tr v-for="item,index in logs" :key="index">
                <th>{{index}}</th>
                <th>{{item.Timestamp}}</th>
                <th>{{item.note}}</th>
                <th>{{item.value}}</th>
                <th><button class="btn btn-outline-dark"><router-link :to="`/updateLog/${item.logid}/${tid}`" style="text-decoration:none; color: black;">Update</router-link></button>
                </th>
                <th>  <button class="btn btn-outline-dark">  <router-link :to="`/deleteLog/${item.logid}`" style="text-decoration:none; color: black;">Delete</router-link></button></th>
                
            </tr>
  </tbody>
</table>
<button class="btn btn-outline-dark" @click="addlog" tabindex="-1">Click to add Logs</button>

</template>

<script>
import axios from 'axios'
import { useRouter } from 'vue-router'
export default {
Name: 'TrackerInfo',
data(){
    return{
        uid : this.$route.params.uid,
        tid : this.$route.params.tid,
        items : [],
        name : localStorage['tname'],
        logs : [],
    }
},
mounted() {
    let name = ''
    localStorage.setItem('uid',this.uid)
    localStorage.setItem('tid',this.tid)
    
    axios.get('http://localhost:5000/trackerinfo/'+this.uid+'/'+this.tid)
    .then((resp ) => {
        this.items = resp.data
        name = this.items[0]['tracker_info']['trackername']
        this.logs = this.items[1]['logdata']
        localStorage.setItem('tname',name)
    })
    .catch((err) => {
        console.log(err.resp)    
    })

},
setup(){
    const router = useRouter();

    const addlog = async () => {
    await  router.push({name: 'AddLog',params : {uid : localStorage['uid'], tid:  localStorage['tid']}});
    }
    return{
        addlog
    }
}
}
</script>

<style>
.header{
    text-align: center;
    margin-top: 175px;
}
.graph{
    width: 500px;
    height: 500px;
    margin-left: 650px;
}
</style>