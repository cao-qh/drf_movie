<script>
import Footer from "@/components/Footer.vue";
import Header from "@/components/Header.vue";
import axios from "axios";
import showMessage from "@/utils/message";

export default {
    name: "MovieBox",
    data: function () {
        return {
            movie: {},
            collectStatus: false,
            collectMessage: '',
            downloadInfo: false,
            userInfo: '',
            catalogueList:[]
        }
    },
    components: { Footer, Header },
    mounted() {
        const movie_id = this.$route.params.id
        this.get_movie_info(movie_id)
        //判断一下用户是否登录
        if (!this.$store.state.isLogin) {
            this.collectStatus = false
            this.collectMessage = '添加收藏'
        }
        else {
            this.get_collect_status(movie_id)
        }
    },
    methods: {
        get_movie_info(movie_id) {
            axios
                .get('/api/movie/' + movie_id)
                .then(response => {
                    this.movie = response.data
                    this.catalogueList = this.movie.catalogue.split('\r\n')
                })
        },
        //获取收藏状态
        get_collect_status(movie_id) {
            axios
                .get('/api/collects/' + movie_id + '/is_collected/')
                .then(response => {
                    this.collectStatus = response.data.is_collected
                    if (this.collectStatus) {
                        this.collectMessage = '取消收藏'
                    }
                    else {
                        this.collectMessage = '添加收藏'
                    }
                })
        },
        //收藏或取消收藏
        collect_or_cancle(movie_id) {
            if (!this.$store.state.isLogin) {
                showMessage('请先登录', 'error', () => {
                    this.$router.push({
                        name: 'Login'
                    })
                })
                return
            }
            if (this.collectStatus) {
                this.cancle_collect_movie(movie_id)
            } else {
                this.collect_movie(movie_id)
            }
        },
        //取消收藏功能
        cancle_collect_movie(movie_id) {
            axios
                .delete('/api/collects/' + movie_id + '/')
                .then(response => {
                    const status_code = response.data.status_code
                    const message = response.data.message
                    if (status_code === 0) {
                        this.collectStatus = false
                        this.collectMessage = '添加收藏'
                    }
                    showMessage(message)
                })
                .catch(error => {
                    showMessage('取消收藏失败')
                })
        },
        //收藏功能
        collect_movie(movie_id) {
            axios
                .post('/api/collects/', { movie_id: movie_id })
                .then(response => {
                    const status_code = response.data.status_code
                    const message = response.data.message
                    if (status_code === 0) {
                        this.collectStatus = true
                        this.collectMessage = '取消收藏'
                        showMessage(message, 'info')
                    } else {
                        showMessage(message, 'error')
                    }
                })
                .catch(error => {
                    showMessage('收藏失败')
                })
        },
        //判断用户状态
        check_member_status() {
            if (!this.$store.state.isLogin) {
                showMessage('请先登录')
                return
            }
            axios
                .get('/api/users/me/')
                .then(response => {
                    this.userInfo = response.data
                    if (this.userInfo.profile.is_upgrade) {
                        this.downloadInfo = true
                    }
                    else {
                        this.$router.push({
                            name: 'MemberCard'
                        })
                    }

                })
        }

    }
}
</script>

<template>
    <div class="flex items-center justify-center">
        <div class="w-full px-2" style="max-width:1440px">
            <div id="main" class="bg-primary-300 p-6 text-black">
                <div class="flex rounded bg-white mx-4 py-6">
                    <div class="mx-6">
                        <div style="min-height:259px;max-height:300px;height:274px">
                            <img referrerPolicy="no-referrer" class="h-full w-full" :src="movie.image_url" />
                        </div>
                        <button v-on:click="collect_or_cancle(movie.id)" id="collect"
                            :class="collectStatus ? 'bg-gray-500' : 'bg-blue-500'"
                            class="copy text-white w-full px-4 py-2 mt-2 text-sm rounded border">{{ collectMessage
                            }}</button>
                    </div>
                    <div id="info" data-movie-id="443">
                        <ul>
                            <li class="text-lg font-semibold">{{ movie.course_name }} </li>
                            <li>作者: {{ movie.author }}</li>
                            <li>作者简介: {{ movie.author_info }}</li>
                            <li>发布日期: {{ movie.release_date }}</li>                   
                            <li>集数: {{ movie.duration }}</li>
                            <li>评分: {{ movie.rate }}</li>
                            <li>简介: {{ movie.review }}</li>
                        </ul>
                    </div>
                </div>
                <div class="rounded bg-white mx-4 my-4 py-6">
                    <div class="px-6">
                        <h1 class="text-lg mb-6 font-semibold">目录</h1>
                        <p v-for="catalogue in catalogueList" :key="catalogue" class="mb-2">{{ catalogue }}</p>
                    </div>
                </div>
                <div id="download_info" class="rounded bg-white mx-4 mt-4 py-6">
                    <h1 class="text-lg mb-6 font-semibold px-6">网盘地址</h1>
                    <div class="px-6">
                        <div v-if="movie.download_info" class="px-6">
                            <div v-if="downloadInfo">{{ movie.download_info }}</div>
                            <div v-else
                                class="flex justify-center items-center mx-6 rounded h-28 bg-gradient-to-r bg-gray-700">
                                <button v-on:click="check_member_status" id="check_member"
                                    class="rounded text-center bg-blue-500 text-white p-2">点击查看网盘信息</button>
                            </div>
                        </div>
                        <div v-else>
                            暂无网盘信息
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">
#info ul li {
  margin-bottom: 5px;
}
</style>
