<template>
  <div style="margin: 60px auto 0;">
    <h5 style="text-align: center;margin-top: 20px;">确认匿名灵活投票发起信息</h5>
    <a-form :model="formState" name="custom-validation" :rules="rules" :labelCol="{lg: {span: 7}, sm: {span: 7}}"
      :wrapperCol="{lg: {span: 10}, sm: {span: 20}}" style="margin: 30px;" autocomplete="off">

      <a-form-item label=" ">
        <a-descriptions bordered="true" :column="{ xxl: 1, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }">
          <a-descriptions-item label="投票标题">{{formState.title}}</a-descriptions-item>
          <a-descriptions-item label="投票时间">{{formState.startTime}} - - {{formState.endTime}}</a-descriptions-item>
          <a-descriptions-item label="投票选项">{{formState.choices}}</a-descriptions-item>
          <a-descriptions-item label="投票类型">{{formState.type}}</a-descriptions-item>
          <a-descriptions-item label="P">{{formState.P}}</a-descriptions-item>
          <a-descriptions-item label="Q">{{formState.Q}}</a-descriptions-item>
          <a-descriptions-item label="G">{{formState.G}}</a-descriptions-item>
          <a-descriptions-item label="投票者">{{formState.voters}}</a-descriptions-item>
          <a-descriptions-item label="投票人数">{{formState.n}}</a-descriptions-item>
          <a-descriptions-item label="门限人数">{{formState.k}}</a-descriptions-item>
        </a-descriptions>
      </a-form-item>


      <a-form-item :wrapperCol="{ span: 24 }" style="text-align: center">
        <a-button type="primary" @click="prevStep">上一步</a-button>
        <a-button type="primary" html-type="submit" style="margin-left: 8px" @click="nextStep"
          :loading="formState.click !== ''">下一步</a-button>
      </a-form-item>
    </a-form>

    <a-divider />
    <div class="step-form-style-desc">
      <h3>说明</h3>
      <h4>发起匿名权重投票事项</h4>
      <p>如果需要，这里可以放一些关于产品的常见问题说明。如果需要，这里可以放一些关于产品的常见问题说明。如果需要，这里可以放一些关于产品的常见问题说明。</p>
    </div>

  </div>


</template>
<script>
import emitter from '@/utils/bus';
import { defineComponent, reactive } from 'vue';
export default defineComponent({
  setup() {
    const formState = reactive({
      title: '',
      startTime: '',
      endTime: '',
      choices: '',
      type: '',
      P: '',
      Q: '',
      G: '',
      voters: '',
      voter: [],
      click: ''
    });
    return {
      formState,
    };
  },
  created() {
    emitter.on("Res", msg => {
      console.log("res", msg)
      this.formState.title = msg[0].Title
      this.formState.startTime = msg[0].startTime
      this.formState.endTime = msg[0].endTime
      this.formState.choices = msg[1]
    });
    emitter.on("Res1", msg => {
      this.formState.P = msg[0]
      this.formState.Q = msg[1]
      this.formState.G = msg[2]
    });
    emitter.on("Res2", msg => {
      console.log(msg[3])
      this.formState.voters = msg[0]
      this.formState.n = msg[1]
      this.formState.k = msg[2]
      if (msg[3] == 1) {
        this.formState.type = "单选"
      }
      if (msg[3] == 2) {
        this.formState.type = "多选"
      }
      if (msg[3] == 3) {
        this.formState.type = "分数"
      }
      this.formState.voter = msg[4]
    });
  },

  methods: {
    prevStep() {
      this.$emit('prevStep')
    },
    nextStep() {
      this.formState.click = 'click'
      this.send()
      // this.$emit('nextStep')
      console.log('2')
    },
    send() {
      console.log(this.formState.title)
      this.$http.post('http://192.168.5.42:8888/manager/create', {
        name: sessionStorage.getItem('user'),
        password: sessionStorage.getItem('pass'),
        title: this.formState.title,
        startTime: this.formState.startTime,
        endTime: this.formState.endTime,
        choice: this.formState.choices,
        type: this.formState.type,
        P: this.formState.P,
        Q: this.formState.Q,
        G: this.formState.G,
        n: this.formState.n,
        k: this.formState.k,
        voters: this.formState.voter,
      }).then((response) => {
        this.formState.click = ''
        console.log(response)
        if (response.data.result == 'success') {
          var res = []
          res = response.data
          emitter.emit('ResID', res)
          this.$emit('nextStep')
        }
      })
    }
  }

});
</script>
  
<style lang="less" scoped>
.information {
  line-height: 22px;
  margin-top: 24px;
  // padding: 5px 10px;
  background-color: #fafafa;
  // max-width: 500px;
  margin: 4px auto 10px;

  .ant-row:not(:last-child) {
    margin-bottom: 24px;
  }
}

.step-form-style-desc {
  padding: 0 56px;
  color: rgba(0, 0, 0, .45);

  h3 {
    margin: 0 0 12px;
    color: rgba(0, 0, 0, .45);
    font-size: 16px;
    line-height: 32px;
  }

  h4 {
    margin: 0 0 4px;
    color: rgba(0, 0, 0, .45);
    font-size: 14px;
    line-height: 22px;
  }

  p {
    margin-top: 0;
    margin-bottom: 12px;
    line-height: 22px;
  }
}
</style>
