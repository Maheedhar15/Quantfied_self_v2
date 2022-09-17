<template>
    <h1 class="header"> Welcome to QuantifiedSelf V2 </h1>
    <form class="form-signin" @submit.prevent="submit">
 
   <h1 class="h3 mb-3 font-weight-normal reg">Enter your new credentials</h1>
 
   
   <input v-model="data.mail" type="name"  class="form-control" placeholder="Your Mail-ID" required autofocus>
   <input v-model="data.pass" type="name"  class="form-control" placeholder="New Password" required autofocus>
   
   <button class="btn btn-lg btn-outline-dark" style="margin-left: 75px;margin-top: 10px;" type="submit">Submit</button>
   <p class="mt-5 mb-3 text-muted">&copy; 2017-2019</p>
    </form>
 </template>
 
 <script>
 import { reactive } from "vue"
 import axios from "axios"
 import { useRouter } from "vue-router"
 
 export default {
 Name:'ChangePass',
 setup() {
    const data = reactive({
      mail: '',
      pass: ''
    })
    const router = useRouter();
    const submit = async() => {
    axios.post('http://localhost:5000/changepass',{
      mail : data.mail,
      pass : data.pass
    })
    .then((res) => {
         console.log(res.data)
         alert('Your password has been changed, Redirecting you to login page now')
         router.push({name:'login'})


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
 .header{
    display: flex;
    text-align: center;
    margin-top: 100px;
    margin-bottom: -50px;
    flex: 50%;
    justify-content: center;
 }
 .reg{
    margin-top: 50px;
 }
 </style>