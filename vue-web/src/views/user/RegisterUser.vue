<template>
  <!-- <a-form
    ref="formRef"
    name="custom-validation"
    :model="formState"
    :rules="rules"
    class="user-layout-login"
    @finish="handleFinish"
    @validate="handleValidate"
    @finishFailed="handleFinishFailed"
  >
    <a-tabs
          :tabBarStyle="{ textAlign: 'center', borderBottom: 'unset' }" centered>
        <a-tab-pane key="tab1" tab="账户注册">
             <a-form-item has-feedback name="name">
      <a-input  size="large" placeholder="账户名" v-model:value="formState.name" type="text" autocomplete="off" />
    </a-form-item>
    


   <a-form-item has-feedback name="pass">
      <a-input-password 
                placeholder="输入密码" v-model:value="formState.pass" type="text" autocomplete="off" />
    </a-form-item>
             <a-form-item has-feedback name="checkPass">
      <a-input-password 
                placeholder="再次输入密码" v-model:value="formState.checkPass" type="text" autocomplete="off" />
    </a-form-item>
        </a-tab-pane>
      </a-tabs>
   
 <a-form-item >
      <a-button  style="width:77%" type="primary" html-type="submit" @click="register">注册</a-button>
      <a-button  style="margin-left: 10px;width: 20%;" @click="resetForm">重置</a-button>
    </a-form-item> 

      <a-form-item>
        <router-link class="register" to='/login' style="float: right;">已有账户登录</router-link>
      </a-form-item>
  </a-form> -->

  <div>

    <!--		 Sign Up Image And Headings-->
    <div class="sign-up-header" style="background-color: #3EA1EC">
      <div class="content">
        <h2 class="mb-5" style="font-size: 42px">AnonyVote</h2>
        <p class="text-lg">基于区块链的在线安全电子投票系统.</p>
      </div>
    </div>
    <!--		 / Sign Up Image And Headings-->

    <!-- Sign Up Form -->
    <a-card :bordered="false" class="card-signup header-solid h-full" :bodyStyle="{ paddingTop: 0 }">
      <template #title>
        <h5 class="font-semibold text-center">账户注册</h5>
      </template>

      <a-form id="components-form-demo-normal-login" ref="formRef" name="custom-validation" :model="formState"
        :rules="rules" class="login-form" @finish="handleFinish" @validate="handleValidate"
        @finishFailed="handleFinishFailed">

        <a-form-item has-feedback name="name">
          <a-input size="large" placeholder="账户名" v-model:value="formState.name" autocomplete="off" />
        </a-form-item>



        <a-form-item has-feedback name="pass">
          <a-input size="large" placeholder="输入密码" v-model:value="formState.pass" type="password" autocomplete="off" />
        </a-form-item>

        <a-form-item has-feedback name="checkPass">
          <a-input size="large" placeholder="再次输入密码" v-model:value="formState.checkPass" type="password"
            autocomplete="off" />
        </a-form-item>


        <a-form-item>
          <a-button style="width:77%;font-size: 15px;" type="primary" html-type="submit" @click="register">注册</a-button>
          <a-button style="margin-left: 10px;width: 20%;font-size: 15px" @click="resetForm">重置</a-button>
        </a-form-item>


      </a-form>

      <p class="font-semibold text-muted text-center">已有账户 <router-link to="/login" class="font-bold text-dark">登录
        </router-link>
      </p>
    </a-card>
    <!-- / Sign Up Form -->

  </div>

</template>
<script>

import md5 from 'js-md5';
import { message } from 'ant-design-vue';
import { defineComponent, reactive, ref } from 'vue';
import { nanoid } from 'nanoid'
import { saveAs } from 'file-saver'
export default defineComponent({
  setup() {
    const formRef = ref();
    const formState = reactive({
      name: '',
      pass: '',
      checkPass: ''
    });

    let validateName = async (_rule, value) => {
      if (value === '') {
        return Promise.reject('请输入正确格式账户名');
      }
      else if (value.length != value.split(" ").join("").length) {
        return Promise.reject('输入包含空格');
      }
      else {
        return Promise.resolve();
      }
    };
    let validatePass = async (_rule, value) => {
      if (value === '') {
        return Promise.reject('请输入初始密码');
      }
      else if (value.length != value.split(" ").join("").length) {
        return Promise.reject('输入包含空格');
      }
      else {
        if (formState.checkPass !== '') {
          formRef.value.validateFields('checkPass');
        }
        return Promise.resolve();
      }
    };

    let validatePass2 = async (_rule, value) => {
      if (value === '') {
        return Promise.reject('请再次输入初始密码');
      }
      if (value !== formState.pass) {
        return Promise.reject("两次密码不一样！");
      }
      if (value.length != value.split(" ").join("").length) {
        return Promise.reject('输入包含空格');
      }
      else {
        return Promise.resolve();
      }
    };

    const rules = {
      pass: [{
        required: true,
        validator: validatePass,
        trigger: 'change',
      }],
      checkPass: [{
        validator: validatePass2,
        trigger: 'change',
      }],
      name: [{
        validator: validateName,
        trigger: 'change',
      }],
    };

    const handleFinish = values => {
      console.log(values, formState);
    };

    const handleFinishFailed = errors => {
      console.log(errors);
    };

    const resetForm = () => {
      formRef.value.resetFields();
    };

    const handleValidate = (...args) => {
      console.log(args);
    };

    return {
      formState,
      formRef,
      rules,
      handleFinishFailed,
      handleFinish,
      resetForm,
      handleValidate,
    };
  },

  methods: {
    //   downloadTxt() {
    //   let str = '王佳伟Vue字符串保存到txt文件下载到电脑案例'
    //   let strData = new Blob([str], { type: 'text/plain;charset=utf-8' });
    //   saveAs(strData, "测试文件下载.txt");
    // },
    register() {

      var Uid = nanoid(6)
      console.log(Uid)
      // console.log(sessionStorage.getItem('user'))
      if (this.formState.name.length !== this.formState.name.split(" ").join("").length || this.formState.pass.length !== this.formState.pass.split(" ").join("").length
        || this.formState.checkPass.length !== this.formState.checkPass.split(" ").join("").length || this.formState.name == ''
        || this.formState.pass == '' || this.formState.checkPass == '' || this.formState.pass !== this.formState.checkPass) {
        message.destroy()
        message.error('注册失败，请检查输入格式', 5)
      }

      else {
        var pass_word = md5(this.formState.pass)
        console.log(pass_word)
        this.$http.post('http://192.168.5.42:8888/register', {
          name: this.formState.name,
          password: pass_word,
          uid: Uid,
        }).then((response) => {
          console.log(response)
          if (response.data.result === 'success') {
            message.destroy()
            message.success('注册成功，请登录！', 2)
            // this.$router.push('/login');
            this.$router.push({ name: 'login', params: { id: 1, name: 'yizuodao' } })
          }
          else if (response.data.result === 'exist') {
            message.destroy()
            message.warning('该用户名已注册', 3)
          }
          else {
            message.destroy()
            message.error('注册失败', 2)
          }
        }).catch(function (error) { // 请求失败处理
          console.log(error)
        })
      }
    }
  }

});
</script>

<style lang="less" scoped>
.user-layout-login {
  label {
    font-size: 14px;
  }

  .getCaptcha {
    display: block;
    width: 100%;
    height: 40px;
  }

  .forge-password {
    font-size: 14px;
  }

  button.login-button {
    padding: 0 15px;
    font-size: 16px;
    height: 40px;
    width: 50%;
  }

  .user-login-other {
    text-align: left;
    margin-top: 24px;
    line-height: 22px;

    .item-icon {
      font-size: 24px;
      color: rgba(0, 0, 0, 0.2);
      margin-left: 16px;
      vertical-align: middle;
      cursor: pointer;
      transition: color 0.3s;

      &:hover {
        color: #1890ff;
      }
    }

    .register {
      float: right;
    }
  }
}
</style>