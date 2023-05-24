<template>
  <div style="margin: 40px auto 0;">
    <a-result status="success" title="您的选票已成功上链，请及时点击获取投票结果！" :model="formState" v-if="success">
      <template #subTitle>
        该投票项目的合约地址:<a-typography-title :level="4">{{addr}}</a-typography-title>
      </template>
      <template #extra>
        <a-button key="buy" @click="reslut">查看详情</a-button>
      </template>
    </a-result>

    <a-result status="error" title="该投票项目已经超时，您的选票上链失败" :model="formState" v-if="fail">
      <template #subTitle>
        查询更多投票信息，请及时点击获取结果！
      </template>
      <template #extra>
        <a-button key="buy" @click="reslut">查看详情</a-button>
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
      addr: '',
      success: false,
      fail: false
    }
  },
  created() {
    emitter.on("change1", msg => {
      console.log(msg)
      if (msg.result == 'success') {
        this.success = true
      }
      else {
        this.fail = true
      }
      this.addr = msg.addr
    });
  },

  methods: {
    reslut() {
      this.$router.push('/result')
    }
  }

});

</script>