<template>
  <footer class="relative bg-blueGray-200 pt-6 pb-6">

    <div class="container mx-auto px-4">
      <hr class="my-4 border-blueGray-300" />
      <div class="flex flex-wrap items-center md:justify-between justify-center">
        <div class="w-full md:w-6/12 px-4 mx-auto text-center">
          <div class="text-base text-blueGray-500 font-semibold py-1">
            © 2022 <a href="/">AnonyVote</a> for a credible e-voting web.
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>
<script>
export default {
  data() {
    return {
      date: new Date().getFullYear(),
    };
  },
};
</script>
