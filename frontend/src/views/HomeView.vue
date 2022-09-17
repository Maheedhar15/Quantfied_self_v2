<template>
<body>
<div id="Home">
    <h4>Welcome to QuantifiedSelf, {{name}}. <br>
     Add trackers to your day-to-day activities and track your progressions.
             <br>
             View your current trackers by clicking on the your trackers icon.<br>
            If you have no trackers running currently, get started by adding trackers to your leisure.
            <br>
            <br>
            <br>
            <br> </h4>
            <h2 style="text-align: center;"> Have fun :) </h2>
  </div>    </body>  
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';


export default {
Name: 'HomeView',
mounted() {
    const router = useRouter();
    axios.get('http://localhost:5000/')
    .then((resp ) => console.log(resp.data))
    .catch((err) => {
            console.log(err)
            router.push({name:'login'})
            alert("Token Expired")
    })
},
data() {
    return {
        name: localStorage.name,
    }
},
};

</script>

<style scoped>

.header{    
    top: 0;
    padding: 0;
    margin: 0;
}

body{
    background-color: black;
}
#Home{
    margin-bottom: 250px;
    color: white;
    
}
</style>