<template>
  <div style="margin: 60px auto 0;">
  <a-form
      :model="formState"
       name="custom-validation"
      :rules="rules"
      :labelCol="{lg: {span: 7}, sm: {span: 7}}"
      :wrapperCol="{lg: {span: 10}, sm: {span: 12}}"
      autocomplete="off"
      @finish="onFinish"
      @finishFailed="onFinishFailed"
  >
  
    <a-form-item has-feedback label="投票ID" name="ID">
      <a-input size="large" v-model:value="formState.ID" placeholder="输入投票项目ID" type="text" autocomplete="off" />
    </a-form-item>
    

    <a-form-item :wrapperCol="{ span: 24 }"
                 style="text-align: center">
      <a-button type="primary" html-type="submit" @click="nextStep">下一步</a-button>
    </a-form-item>

  </a-form>
  
  <a-divider />
  <div class="step-form-style-desc">
    <h3>说明</h3>
    <h4>加入匿名灵活投票或匿名权重投票注意事项：请根据投票项目唯一ID标识输入加入对应投票项目。</h4>
    <p></p>
  </div>
</div>
</template>

<script>
import emitter from '@/utils/bus';
import { message } from 'ant-design-vue';
import { defineComponent, reactive} from 'vue';
export default defineComponent({
  setup() {
    const formState = reactive({
      ID: '',
    });

    let validateID = async (_rule, value) => {
      if (value ==='') {
        return Promise.reject('请输入正确格式');
      } 
      else if(value.length != value.split(" ").join("").length){
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

  // created(){
  //   var x=341
  //   console.log("sdsdsadasda",this.$route.params.id)
  //   this.formState.ID = x

  //   this.nextStep1()
  // },

  methods:{
    // nextStep1(){
    //   console.log("wwwwwwwww",this.$route.params.id)
    // },
    nextStep(){
      if(this.formState.ID !== '' && this.formState.ID.length == this.formState.ID.split(" ").join("").length){
        console.log(this.formState.ID)
        // this.$emit('nextStep')
        this.send()
      }
    },
    send(){
      this.$http.post('http://192.168.5.42:8888/voter/start_vote', {
        name:sessionStorage.getItem('user'),
        password:sessionStorage.getItem('pass'),
        ID:this.formState.ID,
        uid:sessionStorage.getItem('uid')
      }).then((response) =>{
        console.log(response)
        if(response.data.result == 'error1'){
           message.destroy()
           message.warning('请检查登录')
        }
        if(response.data.result == 'error2'){
           message.destroy()
           message.warning('没有找到对应投票项目')
        }
        if(response.data.result == 'error3'){
           message.destroy()
           message.warning('没有该投票活动的投票权限！')
        }
        if(response.data.result == 'hasvote'){
           message.destroy()
           message.warning('您已经投票，请点击获取投票结果！')
        }
        if(response.data.result == 'add'){
          this.$router.push('/addvoting')
          message.destroy()
          message.warning('请先加入投票！')
        }
        if(response.data.result == 'wait'){
          message.destroy()
          message.warning('请等待系统建立公钥')
        }
        if(response.data.result == 'success'){
          console.log("jieguo:",response)
          emitter.emit('info1',response.data)
          this.$emit('nextStep')
        }
        
      })
    }
  }

});
</script>
<style lang="less">
.step-form-style-desc {
  padding: 0 56px;
  color: rgba(0,0,0,.45);

  h3 {
    margin: 0 0 12px;
    color: rgba(0,0,0,.45);
    font-size: 16px;
    line-height: 32px;
  }

  h4 {
    margin: 0 0 4px;
    color: rgba(0,0,0,.45);
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