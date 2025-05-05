<script>
import axios from "axios";
import Page from "@/components/Page.vue";

export default {
  name: "MovieList",
  data: function () {
    return {
      info: ''
    }
  },
  components: { Page },
  mounted() {
    //axios发送请求
    this.get_movie_data()
  },

  methods: {
    get_movie_data: function () {
      let url = '/api/movie/'
      const page = Number(this.$route.query.page);
      const search = this.$route.query.search;
      const category_id = this.$route.query.category_id;
      const region = this.$route.query.region;
      const params = new URLSearchParams();
      if (page) {
        params.append('page', page)
      }
      if (search) {
        params.append('movie_name', search)
      }
      if (category_id) {
        params.append('category_id', category_id)
      }
      if (region) {
        params.append('region', region)
      }
      url = url + "?" + params.toString()
      //axios发送请求
      axios
        .get(url)
        .then(response => (this.info = response.data))
        .catch(error => {
          console.log(error)
        })
    },
  },
  watch: {
    //监听路由变化
    $route() {
      this.get_movie_data()
    }
  }
}
</script>

<template>
  <div class="flex items-center justify-center">
    <div class="w-full px-2" style="max-width:1440px">
      <div id=movie-list class="p-2 grid grid-cols-2 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div class=movie v-for="movie in info.results" :key="movie.id">
          <a :href="'/movie/' + movie.id">
            <div class=relative>
              <div style="min-height:259px;max-height:300px;height:274px">
                <img referrerPolicy="no-referrer" :src="movie.image_url" alt="" class="rounded h-full w-full">
              </div>
              <div v-if="movie.is_top" class="rounded absolute top-0 bg-purple-600 px-1 text-sm">置顶</div>
              <div v-if="movie.quality == 1" class="rounded absolute bottom-0 right-0 bg-blue-500 px-1 text-sm">720p</div>
              <div v-else-if="movie.quality == 2" class="rounded absolute bottom-0 right-0 bg-blue-500 px-1 text-sm">1080p
              </div>
              <div v-else-if="movie.quality == 3" class="rounded absolute bottom-0 right-0 bg-blue-500 px-1 text-sm">4k
              </div>
            </div>
            <p>{{ movie.course_name }} 共{{ movie.duration }}课时</p>
            <p class="text-sm text-primary-200">{{ movie.author_info }}中文</p>
          </a>
        </div>
      </div>
    </div>
  </div>
  <Page :info="info"></Page>

</template>

<style scoped lang="scss"></style>