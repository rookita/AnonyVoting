<template>
<div style="margin: 40px auto 0;">
  <a-result
    status="success"
    title="您的选票已成功上链"
    :model="formState"
    v-if="success"
  >
  <template #subTitle>
    查询更多投票信息以及获取投票结果请点击详情
  </template>
    <template #extra>
      
      <a-button key="console" type="primary" @click="finish">再次投票</a-button>
      <a-button key="buy" @click="reslut">查看详情</a-button>
    </template>
  </a-result>

   <a-result
    status="error"
    title="该投票项目已经超时，您的选票上链失败"
    :model="formState"
    v-if="fail"
  >
  <template #subTitle>
    查询更多投票信息以及获取投票结果请点击详情
  </template>
    <template #extra>
      
      <a-button key="console" type="primary" @click="finish">再次投票</a-button>
      <a-button key="buy" @click="reslut">查看详情</a-button>
    </template>
  </a-result>
  </div>
</template>

<script>
import emitter from '@/utils/bus';
import { defineComponent} from 'vue';
export default defineComponent({
inject:['reload'],
 data () {
    return {
      success:false,
      fail:false
    }
  },
  created(){
    emitter.on("change",msg=>{
      console.log(msg)
      if(msg == 'success'){
        this.success = true
      }
      else{
        this.fail = true
      }
    });
  },

  methods:{
  finish(){
      // this.$router.push('/avec')
      this.reload()
    },
    reslut(){
      this.$router.push('/result')
    }
    }

});

</script>