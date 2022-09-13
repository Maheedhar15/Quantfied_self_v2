<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light navbar-fixed-top">
  <router-link to="trackers/{{id}}" class="navbar-brand">Your trackers</router-link>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item">
        <router-link to="/about" class="nav-link" tabindex="-1">about</router-link>
      </li>
      <li class="nav-item">
        <router-link to="/logout/{{id}}" class="nav-link" tabindex="-1">logout</router-link>
      </li>
    </ul>
  </div>
</nav>
</template>

<script>
export default {
name: 'NavSecure',

data() {
    return {
        id : localStorage.getItem('id')
    }
}
}
</script>

<style>

</style>