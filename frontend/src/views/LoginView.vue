<template>
<div id="app">
   <h1 class="header"> Welcome to QuantifiedSelf V2 </h1>
   <div id="form">
       <form class="form-signin" @submit.prevent="submit">

  <h1 class="h3 mb-3 font-weight-normal">Please sign in</h1>
  
  <input type="email" v-model="data.mail"  class="form-control" placeholder="Email address" required autofocus>
  
  <input type="password" v-model="data.password" class="form-control" placeholder="Password" required>
  <button class="btn btn-outline-dark" type="submit">Sign in</button>
  <p class="or">If you are new, Register here</p>
  <router-link to="Register"><button class="btn btn-outline-dark" id="reg">Register</button></router-link>
  <p class="mt-5 mb-3 text ">&copy; 2017-2019</p>
</form>
   </div>


</div>
</template>

<script>
import { reactive } from 'vue'
import setAuthHeader from '@/utils/AuthHeader';
import { useRouter } from 'vue-router';

export default {
Name: 'LoginView',

setup() {

  const data = reactive({
    mail: '',
    password: ''
  })
   const router = useRouter();
   const submit = async () => {
      await fetch('http://localhost:5000/login',{
         method: 'POST',
         headers: {'Content-Type' : 'application/json','Access-Control-Allow-Origin': '*'},
         body: JSON.stringify(data)
      }).then(resp => resp.json())
      .then(data => {console.log(data);
         localStorage.setItem('access_token', data['access_token']);
         localStorage.setItem('id', data['id']);
         localStorage.setItem('name', data['name']);

         setAuthHeader(data['access_token']);
         router.push({name: 'Dashboard',params : {id : localStorage['id']}});
      })
      .catch(error => { 
         if(error){
            router.push({name:'Login'})
            alert("Wrong Password, Please try again")
         }
       })


      
   }
  return {
      data,
      submit,
   }
}
};

</script>


<style scoped>
:root {
    --primary: #d8185b;
    --secondary: #8c38ff;
    --dark: #131a26;
    --light: #eee;
}
#form{
   justify-content: center;
   margin-top: 50px  ;

}
.header{
   display: flex;
   text-align: center;
   margin-top: 100px;
   margin-bottom: -50px;
   flex: 50%;
   justify-content: center;
}
#app{
   width: 100%;
}
input:hover{
   opacity: 0.9;
}
button{
   margin-left: 79px;
}
.or{
   margin-left:45px;
}
#reg{
   margin-top: -10px;
}


</style>