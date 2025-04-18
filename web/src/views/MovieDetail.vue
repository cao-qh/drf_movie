<script>
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
import MovieBox from "@/components/MovieBox.vue";
export default {
    name: "MovieDetail",
    components: { MovieBox, Header, Footer },
}
</script>

<template>
    <div id="container" class="text-white text-sm bg-primary-300 min-h-screen">
        <Header></Header>
        <MovieBox></MovieBox>
        <Footer></Footer>
    </div>
</template>

<style scoped lang="scss"></style>