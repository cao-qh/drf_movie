<script>
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
import showMessage from "@/utils/message";
import axios from "axios";

export default {
  name: "PasswordReset",
  components: {Footer, Header},
  data:function (){
    return{
      uid:'',
      token:'',
      new_password:'',
      re_new_password:''
    }
  },
  methods:{
    passwordReset(){
      const uid =this.$route.params.uid
      const token = this.$route.params.token
      const new_password = this.new_password.trim()
      const re_new_password = this.re_new_password.trim()
      if (new_password != re_new_password){
        showMessage('两次密码输入不一致!','error')
        return
      }
      const formData = {
        uid:uid,
        token:token,
        new_password:new_password,
        re_new_password:re_new_password
      }
      axios
          .post('/api/users/reset_password_confirm/',formData)
          .then(response =>{
            showMessage('密码重置成功','info',()=>{
              this.$router.push({
                name:'Login'
              })
            })
          })
          .catch(error=>{
            console.log(error);
            const errorData = error.response.data;
            const errorMessage = Object.values(errorData).flat();
            for (let i=0;i<errorMessage.length;i++){
              showMessage(errorMessage[i])
            }
          })
    }
  }
}
</script>

<template>
    <div id="container" class="text-white text-sm bg-primary-300 min-h-screen pb-4">
        <Header></Header>
        <div class="text-center text-2xl p-8">
            重置密码
        </div>
        <div class="flex items-center justify-center">
            <div class="w-1/4 p-4 bg-gray-100 rounded-lg shadow-lg">
                <div class="text-black text-center p-4">
                    <p>新密码</p>
                    <div>
                      <input v-model="new_password" class="outline-0 h-9 rounded border border-green-500 " type="password">
                    </div>
                </div>
              <div class="text-black text-center p-4">
                    <p>确认密码</p>
                    <div>
                      <input v-model="re_new_password" class="outline-0 h-9 rounded border border-green-500 " type="password">
                    </div>
                </div>
                <div class="flex justify-center">
                    <button v-on:click="passwordReset" class="bg-green-500 text-white px-4 py-2 rounded">提交</button>
                </div>
            </div>
        </div>
        <Footer></Footer>
    </div>
</template>

<style scoped lang="scss">

</style>