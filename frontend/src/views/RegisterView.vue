<template>
   <form class="form-signin" @submit.prevent="submit">

  <h1 class="h3 mb-3 font-weight-normal header">Please Register</h1>

  <input v-model="data.name" class="form-control" placeholder="Name" required>
  
  <input v-model="data.mail" type="email"  class="form-control" placeholder="Email address" required autofocus>
  
  <input v-model="data.password" type="password"  class="form-control" placeholder="Password" required>
  <button class="btn btn-lg btn-primary btn-block" type="submit">Submit</button>
  <p class="mt-5 mb-3 text-muted">&copy; 2017-2019</p>
   </form>
</template>

<script>
import { reactive } from "vue"
import { useRouter } from "vue-router"

export default {
Name:'RegisterView',
setup() {
   const data = reactive({
     name: '',
     mail: '',
     password: '' 
   })
   const router = useRouter();
   const submit = async () => {
      await fetch('http://localhost:5000/register',{
         method: 'POST',
         headers: {'Access-Control-Allow-Origin' : '*','Content-Type' : 'application/json'},
         body: JSON.stringify(data)
      });
      alert('You will be redirected to the login page now');
      await router.push('/');
   }

   return {
      data,
      submit,

   }
}
}
</script>

<style>
.header{
   margin-top:250px
}
</style>