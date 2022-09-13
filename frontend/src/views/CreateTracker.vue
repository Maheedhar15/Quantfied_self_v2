<template>
    <a href="/trackers/{{name}}" style="text-decoration: none;"><h4 style="text-align:right">Back to Trackers</h4></a>

    <h1 style="margin-top: 107px; text-align: center;">Create your tracker here</h1>
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
        <button type="submit" class="btn btn-outline-dark">create tracker</button>
      </form>
</template>

<script>
import { useRouter } from 'vue-router';
import { reactive } from 'vue'
export default {
Name: 'CreateTracker',

setup() {

  const data = reactive({
    tname: '',
    tdesc: '',
    ttype: '',
    tsettings: ''
  })
   const router = useRouter();
   const submit = async () => {
      await fetch('http://localhost:5000/createtracker/'+localStorage['id'],{
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