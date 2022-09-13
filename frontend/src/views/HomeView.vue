<template>
<body>
<div id="Home">
    <h1 class="header"> Welcome {{name}} </h1>
    <h3>to Quantified Self V2</h3>
        <p></p>
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
        if(err.response.status == 401){
            router.push({name:'Login'})
            alert("Token Expired")
        }
        
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