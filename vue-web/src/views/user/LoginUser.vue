<template>

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
        <h5 class="font-semibold text-center">账户登录</h5>
      </template>

      <a-form id="components-form-demo-normal-login" :rules="rules" :model="formState" name="basic" class="login-form"
        autocomplete="off">

        <a-form-item has-feedback name="username">
          <a-input type="text" placeholder="账户" v-model:value="formState.username" autocomplete="off">
            <template #prefix>
              <user-outlined style="color: rgba(0, 0, 0, 0.45)" type="user" />
            </template>
            <template #suffix>
              <a-tooltip title="这是必要信息">
                <info-circle-outlined style="color: rgba(0, 0, 0, 0.45)" />
              </a-tooltip>
            </template>
          </a-input>
        </a-form-item>

        <a-form-item has-feedback name="password">
          <a-input-password type="text" placeholder="密码" v-model:value="formState.password" autocomplete="off" />
        </a-form-item>

        <a-form-item>
          <a-checkbox style="color: rgba(0, 0, 0, 0.45)" v-model:checked="formState.remember">记住密码</a-checkbox>
          <router-link class="register" to='/register' style="float: right;">注册账户</router-link>
        </a-form-item>

        <a-form-item>

          <a-button style="width:100%;font-size: 15px;" type="primary" html-type="submit" @click="login">登录</a-button>
        </a-form-item>
      </a-form>

      <!-- <p class="font-semibold text-muted text-center">已有账户 <router-link to="/login" class="font-bold text-dark">登录</router-link></p> -->
    </a-card>

  </div>
</template>
<script>

import { message } from 'ant-design-vue';
import md5 from 'js-md5';
import { defineComponent, reactive } from 'vue';
export default defineComponent({
  setup() {
    const formState = reactive({
      username: '',
      password: '',
      remember: false
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
        return Promise.resolve();
      }
    };

    const rules = {
      password: [{
        required: true,
        validator: validatePass,
        trigger: 'change',
      }],
      username: [{
        validator: validateName,
        trigger: 'change',
      }],
    };

    const onFinish = values => {
      console.log('Success:', values);
    };

    const onFinishFailed = errorInfo => {
      console.log('Failed:', errorInfo);
    };

    return {
      rules,
      formState,
      onFinish,
      onFinishFailed,
    };
  },
  mounted() {
    let Base64 = require('js-base64').Base64
    let username = localStorage.getItem("user");
    if (username) {
      this.formState.username = localStorage.getItem("user");
      this.formState.password = Base64.decode(localStorage.getItem("password"));// base64解密
      this.formState.remember = true;
    }
  },
  created() {
    console.log(this.$route.params);
  },

  methods: {
    // str2hex(str) {
    //   if (str === "") {
    //     return "";
    //   }
    //   else {
    //     var arr = [];
    //     //arr.push("0x");
    //     for (var i = 0; i < str.length; i++) {
    //       arr.push(str.charCodeAt(i).toString(16));
    //     }
    //     return arr.join('');
    //   }
    // },

    login() {
      // console.log("dddddd",this.str2hex("ddd"))
      if (this.formState.username === '' || this.formState.password == '' || this.formState.username.length !== this.formState.username.split(" ").join("").length
        || this.formState.password.length !== this.formState.password.split(" ").join("").length) {
        message.destroy()
        message.error('登录错误，请检查输入格式', 3)
      }
      else {
        var pass_word = md5(this.formState.password)
        this.$http.post('http://192.168.5.42:8888/login', {
          name: this.formState.username,
          password: pass_word
        }).then((response) => {
          if (response.data.result === 'success') {
            sessionStorage.setItem('user', this.formState.username)
            sessionStorage.setItem('pass', pass_word)
            sessionStorage.setItem('token', response.data.token)
            sessionStorage.setItem('uid', response.data.uid)
            // sessionStorage.setItem('uid', 'aa')

            if (this.formState.remember) {
              let Base64 = require('js-base64').Base64
              let password = Base64.encode(this.formState.password); // base64加密
              localStorage.setItem("user", this.formState.username);
              localStorage.setItem("password", password);
            }
            else {
              localStorage.removeItem("user");
              localStorage.removeItem("password");
            }

            message.destroy()
            message.success('登录成功', 3)
            this.$router.push('/overview')
          }

          if (response.data.result === 'none') {
            message.destroy()
            message.warning('用户名不存在，请注册', 3)
          }
          if (response.data.result === 'fail') {
            message.destroy()
            message.error('登录失败，密码错误', 3)
          }
          if (response.data.result === 'error') {
            message.destroy()
            message.warning('登录出错', 3)
          }

        }).catch(function (error) { // 请求失败处理
          console.log(error)
        })
      }
    },
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
    width: 100%;
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