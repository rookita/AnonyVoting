<template>
  <div style="margin: 40px auto 0;">
    <a-result status="success" title="您已经成功上传该投票活动的解密份额" :model="formState">
      <template #subTitle>
        请等待其他投票参与方共同建立系统公钥，请及时关注获取投票结果。
      </template>
      <template #extra>
        <a-button key="buy" @click="result">获取结果</a-button>
      </template>
    </a-result>

  </div>
</template>
  
<script>
import { defineComponent } from 'vue';
export default defineComponent({
  inject: ['reload'],

  methods: {
    result() {
      this.$router.push('/result')
    }
  }

});

</script>