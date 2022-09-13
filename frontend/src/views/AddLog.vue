<template>
    
    <h1 style="margin-top: 107px; text-align: center;color:  ;">Log the values into the tracker</h1>
    <form @submit.prevent="submit" style="margin-right: 522px;margin-top: 29px; margin-left: 519px" method="POST">
        <div class="form-group">
          <label for="exampleInputEmail1" required style="color:  ;">Note</label>
          <input type="name" class="form-control" v-model="data.note" id="exampleInputEmail1" aria-describedby="emailHelp" name="Note" placeholder="Note" style="border-radius: 20px;">
        </div>

        <div class="form-group" v-if="this.trackertype==='Numerical'" >
            <label for="exampleInputPassword1" required style="color:  ;">Enter the Value</label>
            <input type="value" class="form-control" v-model="data.value" id="exampleInputPassword1" name="value" placeholder="Value"  style="border-radius: 20px;" required>
          </div>

        <div class="multiple-choice" v-else>
        <label for="value" style="color:  ;">Check the value</label>
        <div class="form-check">

            <div v-for="item,index in this.trackersettings" :key="index">
              <input type="radio" name="value" v-model="data.value" :value="`${item}`" required>
              <label>{{item}}</label>
              </div>
                

          </div>
        </div>

        <button type="submit" class="btn btn-outline-dark"  style="border-radius: 15px;">submit</button>
      </form>  
</template>

<script>
import { reactive } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
export default {
Name: 'AddLog',
data(){
    return{
        uid : this.$route.params.uid,
        tid : this.$route.params.tid,
        items : [],
        trackertype: '',
        trackersettings: []
    }
},
mounted() {
    localStorage.setItem('uid',this.uid)
    localStorage.setItem('tid',this.tid)
    axios.get('http://localhost:5000/addLog/'+this.uid+'/'+this.tid)
    .then((resp ) => {
        
        this.items = resp.data
        
        this.trackertype = this.items[0]['data']['trackertype']
        this.trackersettings =this.items[1]['tracker_settings']
        console.log(this.trackertype,this.trackersettings)
    })
    .catch((err) => {
        console.log(err.resp)    
    })
},
setup() {
const router = useRouter();
const data = reactive({
  note: '',
  value: ''
})

 const submit = async () => {
    await fetch("http://localhost:5000/addLog/"+localStorage['uid']+'/'+localStorage['tid'],{
       method: 'POST',
       headers: {'Content-Type' : 'application/json','Access-Control-Allow-Origin': '*'},
       body: JSON.stringify(data)
    }).then(resp => resp.json())
    .then(data => {
      console.log(data)
      router.push({name: 'Trackers', params: {id : localStorage['id']}})
      alert('The log has been successfully added')
      ;})
    .catch(error => { console.log(error)
     })


    
 }
return {
    data,
    submit,
 }
}
}
</script>

<style>

</style>