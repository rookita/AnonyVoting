<template>
  <a-card :bordered="false">
    <div style="margin: 60px auto 0;">
      <a-form :model="formState" name="custom-validation" :rules="rules"
        :labelCol="{ lg: { span: 7 }, sm: { span: 7 } }" :wrapperCol="{ lg: { span: 10 }, sm: { span: 12 } }"
        autocomplete="off" @finish="onFinish" @finishFailed="onFinishFailed">
        <h5 style="text-align: center;margin: 30px;">获取匿名投票活动结果</h5>

        <a-form-item has-feedback label="投票ID" name="ID">
          <a-input size="large" v-model:value="formState.ID" placeholder="输入投票项目ID" type="text" autocomplete="off" />
        </a-form-item>


        <a-form-item :wrapperCol="{ span: 24 }" style="text-align: center">
          <a-button type="primary" html-type="submit" @click="nextStep" :loading="formState.click !== ''">下一步</a-button>
        </a-form-item>

      </a-form>

      <a-divider />
      <div class="step-form-style-desc">
        <h3>说明</h3>
        <h4>加入匿名灵活投票或匿名权重投票注意事项：请根据投票项目唯一ID标识输入加入对应投票项目。</h4>
        <p></p>
      </div>
    </div>
  </a-card>

</template>

<script>
import emitter from '@/utils/bus';
import { message } from 'ant-design-vue';
import { defineComponent, reactive } from 'vue';
export default defineComponent({
  setup() {
    const formState = reactive({
      ID: '',
      click: ''
    });

    let validateID = async (_rule, value) => {
      if (value === '') {
        return Promise.reject('请输入正确格式');
      }
      else if (value.length != value.split(" ").join("").length) {
        return Promise.reject('输入包含空格');
      }
      else {
        return Promise.resolve();
      }
    };

    const rules = {
      ID: [{
        required: true,
        validator: validateID,
        trigger: 'change',
      }],
    };

    return {
      formState,
      validateID,
      rules
    };
  },



  methods: {
    // search(msg) {
    //   console.log(msg)
    //   if (msg !== '') {
    //     this.formState.ID = msg
    //     this.send()
    //     // this.formState.click = 'click'
    //   }
    // },
    nextStep() {
      this.formState.click = 'click'
      if (this.formState.ID !== '' && this.formState.ID.length == this.formState.ID.split(" ").join("").length) {
        console.log(this.formState.ID)
        // this.$emit('nextStep')
        this.send()
      }
    },
    send() {
      this.$http.post('http://192.168.5.42:8888/voter/if_add_share', {
        name: sessionStorage.getItem('user'),
        password: sessionStorage.getItem('pass'),
        ID: this.formState.ID,
        uid: sessionStorage.getItem('uid')
      }).then((response) => {
        this.formState.click = ''
        console.log(response)
        if (response.data.result == 'error1') {
          message.destroy()
          message.warning('请检查登录')
        }
        if (response.data.result == 'error2') {
          message.destroy()
          message.warning('没有找到对应投票项目')
        }


        if (response.data.type == 'we') {
          if (response.data.result == 'wait') {
            message.destroy()
            message.warning('请等待全部参与者上传秘密份额')
          }
          // else {
          //   this.$router.push({ name: 'resultwe', params: { info: JSON.stringify(response.data) } })
          // }
          if (response.data.result == 'doshare') {
            this.$router.push({ name: 'resultwe', params: { info: JSON.stringify(response.data) } })
            // emitter.emit('ballotshare', response.data)
            // this.$emit('nextStep')
          }
          if (response.data.result == 'success') {
            this.$router.push({ name: 'weresult', params: { info: JSON.stringify(response.data) } })
            // console.log("jieguo:",response)
            // emitter.emit('resballot', response.data)
            // this.$emit('nextStep')
            // this.$emit('next3Step')
          }
        }
        else {
          if (response.data.result == 'wait') {
            message.destroy()
            message.warning('请等待参与者上传秘密份额达到门限数量')
          }
          // else {
          //   this.$router.push({ name: 'resultavec', params: { info: JSON.stringify(response.data) } })
          // }
          if (response.data.result == 'doshare') {
            this.$router.push({ name: 'resultavec', params: { info: JSON.stringify(response.data) } })
            // emitter.emit('ballotshare', response.data)
            // this.$emit('nextStep')
          }
          if (response.data.result == 'success') {
            this.$router.push({ name: 'avecresult', params: { info: JSON.stringify(response.data) } })
            // console.log("jieguo:",response)
            // emitter.emit('resballot', response.data)
            // this.$emit('nextStep')
            // this.$emit('next3Step')
          }
        }



      })
    }
  }

});
</script>
<style lang="less">
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