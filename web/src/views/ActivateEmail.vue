<script>
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
import axios from "axios";
import showMessage from "@/utils/message";
export default {
    name: "ActivateEmail",
    components: { Footer, Header },
    methods: {
        activate() {
            const uid = this.$route.params.uid
            const token = this.$route.params.token
            const formData = {
                uid: uid,
                token: token,
            }
            axios
                .post('/api/users/activation/', formData)
                .then(response => {
                    showMessage('账号激活成功,请在登录页登录', 'info', () => {
                        this.$router.push({ name: 'Login' })
                    })
                })
                .catch(error => {
                    const errorData = error.response.data;
                    const errorMessage = Object.values(errorData).flat();
                    for (let i = 0; i < errorMessage.length; i++) {
                        showMessage(errorMessage[i])
                    }
                })
        }
    }
}
</script>

<template>
    <div id="container" class="flex flex-col justify-between text-white text-sm bg-primary-300 min-h-screen">
        <!--        <Header></Header>-->
        <div>
            <div class="text-center text-2xl p-8">
                激活你的账号
            </div>
            <div class="flex items-center justify-center">
                <div class="w-1/4 p-4 bg-gray-100 rounded-lg shadow-lg">
                    <div class="text-black text-center p-4">
                        请点击下方按钮，激活账号
                    </div>
                    <div class="flex justify-center">
                        <button v-on:click="activate" class="bg-green-500 text-white px-4 py-2 rounded">激活账号</button>
                    </div>
                </div>
            </div>
        </div>
        <Footer></Footer>
    </div>
</template>

<style scoped lang="scss"></style>