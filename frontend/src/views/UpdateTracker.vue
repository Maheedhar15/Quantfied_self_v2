<template>
    <router-link :to="`/trackers/{{u_id}}`" style="text-decoration: none;"><h4 style="text-align:right">Back to Trackers</h4></router-link>

    <h1 style="margin-top: 107px; text-align: center;">Update your tracker here</h1>
    <form @submit.prevent="submit" style="margin-right: 522px;margin-top: 29px; margin-left: 519px" method="POST" action='/trackers/{{name}}/create'>
        <div class="form-group">
          <label for="exampleInputEmail1">Tracker name</label>
          <input type="name" v-model="data.tname" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Name of your tracker" required>
        </div>
        <div class="form-group">
          <label for="exampleInputPassword1">Tracker Description</label>
          <input type="name" v-model="data.tdesc" class="form-control" id="exampleInputPassword1" placeholder="Tracker Description" required>
        </div>
        <div class="form-group">
          <label for="inputState">Tracker type</label>
          <select v-model="data.ttype" class="form-control" required>
            <option selected>Choose...</option>
            <option>Numerical</option>
            <option>Multiple Choice</option>
            <option>Range based</option>
          </select>
        </div>
        <div class="form-group">
          <label for="exampleFormControlTextarea1" >Tracker settings</label>
          <textarea v-model="data.tsettings" class="form-control" id="exampleFormControlTextarea1" rows="3" placeholder="Tracker settings(Enter different settings as comma separated values)"></textarea>
          <small>If your tracker type is Numerical, dont enter anything in this box</small>
        </div>   
        <button type="submit" class="btn btn-outline-dark">Update tracker</button>
      </form>
</template>

<script>
import { useRouter } from 'vue-router';
import { reactive } from 'vue'
export default {
Name: 'UpdateTracker',
data(){
    return{
        id: this.$route.params.id,
        u_id: localStorage['id']
    }
},
mounted(){
  localStorage.setItem('tracker_id',this.id)
},
setup() {
  const data = reactive({
    tname: '',
    tdesc: '',
    ttype: '',
    tsettings: ''
  })
   const router = useRouter();
   const submit = async () => {
      await fetch('http://localhost:5000/trackers/update/'+ localStorage['tracker_id'],{
         method: 'POST',
         headers: {'Content-Type' : 'application/json','Access-Control-Allow-Origin': '*'},
         body: JSON.stringify(data)
      }).then(resp => resp.json())
      .then(data => {console.log(data);
      })
      .catch(error => { console.log(error) })


      await router.push({name: 'Trackers',params : {id : localStorage['id']}});
   }
  return {
      data,
      submit,
   }
}
};

</script>

<style >
    body {
      background-image: '../static/plot.png';
    }

</style>