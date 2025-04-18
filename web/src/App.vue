<template>
  <router-view/>
</template>

<script>
import axios from "axios";

export default {
  name:'App',
  beforeCreate() {
    this.$store.commit('initializeStore')
    //设置axios headers
    const token = localStorage.getItem('token')
    if (token){
      axios.defaults.headers.common['Authorization'] = 'JWT '+ token
    }
    else {
      axios.defaults.headers.common['Authorization'] = ''
    }

  },
}
</script>
