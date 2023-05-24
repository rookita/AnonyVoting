<template>
  <div style="margin: 40px auto 0;">
    <a-result
      status="success"
      title="您已经成功加入该投票活动"
      :model="formState"
    >
    <template #subTitle>
      请等待其他投票参与方共同建立系统公钥
    </template>
      <template #extra>
        <a-button key="buy" @click="voting">开始投票</a-button>
      </template>
    </a-result>

    </div>
  </template>
  
  <script>
  import emitter from '@/utils/bus';
  import { defineComponent} from 'vue';
  export default defineComponent({
  inject:['reload'],

    methods:{
      voting(){
        this.$router.push('/voting')
      }
      }
  
  });
  
  </script>