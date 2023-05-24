<template>
  <a-config-provider :locale="locale">
    <router-view v-if="isRouterAlive"></router-view>
  </a-config-provider>
</template>

<script>
  import zhCN from 'ant-design-vue/es/locale/zh_CN';
  import dayjs from 'dayjs';
  import 'dayjs/locale/zh-cn';
  dayjs.locale('zh-cn');

  export default {
    provide (){
      return{
        reload:this.reload
      }
    },

    data() {
      return {
        locale: zhCN,
        isRouterAlive:true
      };
    },
    
    methods:{
      reload() {
        this.isRouterAlive = false
        this.$nextTick(function(){
          this.isRouterAlive =true
        })
      }
    }
  };
</script>