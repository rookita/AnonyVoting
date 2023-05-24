<template>
  <div style="margin: 40px auto 0;">
    <a-result status="success" title="成功发起投票项目" :model="formState">
      <template #subTitle>
        请注意保存返回的该投票项目ID:<a-typography-title :level="2">{{ID}}</a-typography-title>
        该投票项目的合约地址:<a-typography-title :level="4">{{addr}}</a-typography-title>
      </template>

      <template #extra>

        <a-button key="console" type="primary" @click="finish">再次发起</a-button>
        <a-button key="buy" @click="voting">投票</a-button>
      </template>
    </a-result>
  </div>
</template>
  
<script>
import emitter from '@/utils/bus';
import { defineComponent } from 'vue';
export default defineComponent({
  inject: ['reload'],
  data() {
    return {
      ID: '',
      addr: ''
    }
  },
  created() {
    emitter.on("ResID", msg => {
      console.log("sdsd", msg)
      console.log(typeof (msg))
      this.ID = msg.ID,
        this.addr = msg.addr
    });
  },

  methods: {
    finish() {
      // this.$router.push('/avec')
      this.reload()
    },
    voting() {
      this.$router.push('/addvoting')
    }
  }


});

</script>