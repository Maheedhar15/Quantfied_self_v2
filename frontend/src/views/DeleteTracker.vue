<template>
  <div class="app">

  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import axios from 'axios'
export default {
Name: 'DeleteTracker',
data() {
    return{
        id: this.$route.params.id
    }
},
created(){
    const router = useRouter();
    const path = 'http://localhost:5000/trackers/delete/'+ this.id
    axios.get(path)
    .then((resp)=>{
        console.log(resp.data)
        router.push({name: 'Trackers', params: {id : localStorage['id']}})
        alert('The tracker has been successfully Deleted')
    })
    .catch((err) => console.log(err.response) )
}

}
</script>

<style>

</style>