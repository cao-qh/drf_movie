<script>
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
import axios from "axios";
export default {
  name: "MemberCard",
  components: {Footer, Header},
  data :function (){
    return{
      info:'',
      pay_url:'',
      last_time:'',
      die_time:'',
      userInfo:''
    }
  },
  mounted() {
    this.get_card_info()
    this.get_dieTime()
  },
  methods:{
    get_card_info(){
      axios
          .get('api/cards/')
          .then(response=>{
            this.info = response.data
          })
    },
    pay(card){
      axios
          .get('/api/alipay/?card_id='+card.id)
          .then(response =>{
            console.log(response.data)
            window.location.href = response.data
          })
    },
    get_dieTime(){
      axios
          .get('/api/users/me/')
          .then(response =>{
            this.userInfo = response.data
            if (this.userInfo.profile.expire_time && this.userInfo.profile.is_upgrade){
              this.formatDieTime(this.userInfo.profile.expire_time)
              this.calculateMembershipDaysLeft(this.userInfo.profile.expire_time)
            }
          })

    },
    formatDieTime(dateTimeString) {
    // 创建一个新的 Date 对象（假设 dateTimeString 是有效的 ISO 8601 字符串）
    const date = new Date(dateTimeString);

    // 使用 Intl.DateTimeFormat 来格式化日期
    const formatter = new Intl.DateTimeFormat('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    });

    // 获取格式化的日期字符串
    this.die_time = formatter.format(date);
  },
    calculateMembershipDaysLeft(expiryDateString) {
      // 将到期日期字符串转换为 Date 对象
      const expiryDate = new Date(expiryDateString);
      // 获取今天的日期
      const today = new Date();
      // 计算时间差（毫秒）
      const timeDifference = expiryDate - today;
      // 将时间差转换为天数（1天 = 1000毫秒 * 60秒 * 60分钟 * 24小时）
      const daysLeft = Math.ceil(timeDifference / (1000 * 60 * 60 * 24));
      // 更新组件数据
      this.last_time = daysLeft;
    },
  }
}
</script>

<template>
<div id="container" class="text-white text-sm bg-primary-300 min-h-screen pb-4">
    <Header></Header>
        <div id="main" class="bg-primary-300 p-12 text-black">
            <div class="grid grid-cols-3 gap-3">
                <div v-for="card in info.results" v-bind="card" class="flex flex-col justify-center items-center bg-white rounded-lg px-6 max-w-xl">
                    <div class="text-4xl text-center">
                        {{ card.card_name }}
                    </div>
                    <div class="text-4xl text-center">
                        ￥{{ card.card_price }} 元
                    </div>
                    <button v-on:click="pay(card)"  data-pay_type="alipay" class="card w-24 rounded-3xl bg-purple-600 text-white text-lg p-2 mx-8 my-2">购买</button>
                </div>
                <div>
                <ul style="color: azure">您的会员过期时间:{{die_time}}</ul>
                  <ul style="color: azure">您的会员剩余时间:{{last_time}}天</ul>
                </div>
            </div>

        </div>

    <Footer></Footer>
</div>
</template>

<style scoped lang="scss">

</style>