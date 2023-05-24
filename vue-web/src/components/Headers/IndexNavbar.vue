<template>

  <nav
    class="top-0 fixed z-50 w-full flex flex-wrap items-center justify-between px-2 py-3 navbar-expand-lg bg-white shadow">
    <div class="container px-4 mx-auto flex flex-wrap items-center justify-between">
      <div class="w-full relative flex justify-between lg:w-auto lg:static lg:block lg:justify-start">
        <router-link to="/">
          <span
            class="text-blueGray-700 text-base font-bold leading-relaxed inline-block mr-4 py-2 whitespace-nowrap uppercase">
            AnonyVote
          </span>
        </router-link>

        <button
          class="cursor-pointer text-xl leading-none px-3 py-1 border border-solid border-transparent rounded bg-transparent block lg:hidden outline-none focus:outline-none"
          type="button" v-on:click="setNavbarOpen">
          <i class="fas fa-bars"></i>
        </button>
      </div>

      <div class="lg:flex flex-grow items-center" :class="[navbarOpen ? 'block' : 'hidden']"
        id="example-navbar-warning">

        <ul class="flex flex-col lg:flex-row list-none lg:ml-auto">
          <li class="flex items-center">

            <index-dropdown />
          </li>

          <li class="flex items-center">
            <router-link to="/support">
              <span class="hover:text-blueGray-500 text-blueGray-700 px-4 py-2 flex items-center  uppercase font-bold">
                <i class="text-blueGray-400 fas fa-info-circle leading-lg mr-2"></i>技术支持</span>
            </router-link>
          </li>

          <li class="flex items-center">
            <router-link to="/about">
              <span class="hover:text-blueGray-500 text-blueGray-700 px-4 py-2 flex items-center  uppercase font-bold">
                <i class="text-blueGray-400 far fa-file-alt text-lg leading-lg mr-2" />
                操作指南</span>
            </router-link>
          </li>

          <li class="flex items-center">
            <router-link to="/contact">
              <span class="hover:text-blueGray-500 text-blueGray-700 px-4 py-2 flex items-center  uppercase font-bold">
                <i class="text-blueGray-400 fas fa-phone-alt leading-lg mr-2"></i>
                <font-awesome-icon icon="fa-regular fa-phone" />
                联系我们
              </span>
            </router-link>
          </li>


          <li class="flex items-center">
            <router-link to="/login">
              <button
                class="bg-emerald-500 text-white active:bg-emerald-600 font-bold uppercase px-4 py-2 rounded shadow hover:shadow-lg outline-none focus:outline-none lg:mr-2 lg:mb-0 ml-3 mb-3 ease-linear transition-all duration-150"
                type="button" style="background-color:rgb(62, 161, 236);"> 登录
              </button>
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import IndexDropdown from "@/components/Dropdowns/IndexDropdown.vue";

export default {
  data() {
    return {
      navbarOpen: false,
    };
  },
  methods: {
    setNavbarOpen: function () {
      this.navbarOpen = !this.navbarOpen;
    },
  },
  components: {
    IndexDropdown,
  },
};
</script>
