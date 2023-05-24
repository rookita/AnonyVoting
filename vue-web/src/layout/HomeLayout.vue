<template>
  <div>
    <navbar/>
    <main>
      <router-view></router-view>
    </main>
    <footer-component />
  </div>
</template>
<script>
import Navbar from "@/components/Headers/IndexNavbar.vue";
import FooterComponent from "@/components/Footers/Footer.vue";
export default {
 
  components: {
    Navbar,
    FooterComponent,
  },
};
</script>

<style scoped lang="scss">
@import "@/assets/styles/tailwind.css";
</style>


