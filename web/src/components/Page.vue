<script>
export default {
  name: "Page",
  data: function () {
    return {
      current: 1
    }
  },
  props: ['info'],
  computed: {
    lastPage() {
      let pageSize = 9
      return Math.ceil(this.info.count / pageSize)
    },
    prePage() {
      if (this.current > 1) {
        return this.current - 1
      }
      else return 1
    },
    nextPage() {
      if (this.current < this.lastPage) {
        return this.current + 1
      }
      else return this.current
    },
    pages() {
      const pages = []
      for (let i = 1; i <= this.lastPage; i++) {
        if (i === 1 || i === this.lastPage || (i >= this.current - 1 && i <= this.current + 1)) {
          pages.push(i)
        } else if (pages[pages.length - 1] != '...') {
          pages.push('...')
        }

      }
      return pages
    }
  },
  mounted() {
    this.current = this.getPageFromUrl()
  },
  methods: {
    getPageFromUrl() {
      const page = Number(this.$route.query.page)
      return page ? page : 1
    },
    goToPage(page) {
      this.current = page
      //获取当前所有参数
      const params = { ...this.$route.query };
      params.page = page
      console.log(params)
      this.$router.push({ query: params })
    }
  },
}
</script>

<template>
  <div id="footer" class="flex items-center justify-center text-gray-500 pb-4">
    <!-- 上一页 -->
    <span v-if="info.previous" @click="goToPage(prePage)" class="page-link">
      <button class="w-8 h-8 rounded mx-1 my-1 text-gray-600 bg-gray-500">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mx-auto" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd"
            d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
            clip-rule="evenodd" />
        </svg>
      </button>
    </span>
    <!-- 遍历每一页 -->
    <a v-for="page in pages" :key="page" class=page-link>
      <button v-if="page === '...'" class="w-8 h-8 rounded mx-1 my-1 bg-gray-300 text-black">{{ page }}</button>
      <button v-else-if="page === current" class="w-8 h-8 rounded mx-1 my-1 bg-blue-500 text-white">{{ page }}</button>
      <button v-else @click="goToPage(page)" class="w-8 h-8 rounded mx-1 my-1 bg-gray-300 text-black">{{ page }}</button>
    </a>
    <!-- 下一页 -->
    <a v-if="info.next" @click="goToPage(nextPage)" class="page-link">
      <button class="w-8 h-8 rounded mx-1 my-1 bg-gray-300">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mx-auto" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd"
            d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
            clip-rule="evenodd" />
        </svg>
      </button>
    </a>
  </div>
</template>

<style scoped lang="scss"></style>