<template>
  <div style="margin: 3px auto 0;">
    <a-form :model="formState" name="custom-validation" :rules="rules" :labelCol="{lg: {span: 7}, sm: {span: 7}}"
      :wrapperCol="{lg: {span: 10}, sm: {span: 12}}" style="margin: 40px auto 0;" autocomplete="off">
      <h5 style="text-align: center;margin-top: 20px;">本地生成匿名灵活投票加密套件</h5>
      <a-form-item label="加密参数" :rules="[{ required: true }]">
        <a-descriptions bordered="true" :column="{ xxl: 1, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }">
          <a-descriptions-item label="投票地址">{{formState.addr}}</a-descriptions-item>
          <a-descriptions-item label="P">{{formState.P}}</a-descriptions-item>
          <a-descriptions-item label="Q">{{formState.Q}}</a-descriptions-item>
          <a-descriptions-item label="G">{{formState.G}}</a-descriptions-item>
          <a-descriptions-item label="投票人数n">{{formState.n}}</a-descriptions-item>
          <a-descriptions-item label="门限人数k">{{formState.k}}</a-descriptions-item>
        </a-descriptions>
      </a-form-item>


      <a-form-item has-feedback label="获取加密参数" name="signature">
        <a-button size="large" type="dashed" style="width: 80%" @click="generatepub" :disabled="formState.epub != ''">
          <PlusOutlined />
          本地下载加密信息文件
        </a-button>
      </a-form-item>

      <a-form-item :wrapperCol=" { span: 24 }" style="text-align: center">
        <a-button type="primary" @click="prevStep">上一步</a-button>
        <a-button type="primary" html-type="submit" style="margin-left: 20px" @click="nextStep">上传公钥</a-button>
      </a-form-item>
      <a-divider />
      <div class="step-form-style-desc">
        <h3>说明</h3>
        <h4>加入匿名灵活投票事项：请根据以上项目ID返回投票信息完成投票表决。</h4>
      </div>
    </a-form>
  </div>
</template>
<script>
import emitter from '@/utils/bus';
import { defineComponent, reactive } from 'vue';
import { message } from 'ant-design-vue';
import { saveAs } from 'file-saver'
export default defineComponent({
  inject: ['reload'],
  setup() {
    const formState = reactive({
      addr: '',
      P: '',
      Q: '',
      G: '',
      n: '',
      k: '',
      rpub: '',
      epub: '',

    });
    let validateSignature = async (_rule, value) => {
      if (value === '') {
        return Promise.reject('请根据要求操作');
      }
      else {
        return Promise.resolve();
      }
    }
    const rules = {
      signature: [{
        required: true,
        validator: validateSignature,
        trigger: 'change',
      }],
    };

    return {
      rules,
      validateSignature,
      formState
    };
  },
  // mounted() {
  //   emitter.on("infowe", msg => {
  //     console.log("ddddsdsd", msg)
  //     this.info(msg)

  //   })
  // },
  created() {
    // var res = []
    // res = this.$route.params.info
    // emitter.emit('infowe', this.$route.params.info)
    // this.weinfo(this.$route.params.info)

    // this.$emit('nextStep')
    console.log("chancan", this.$route.params.info)
    this.weinfo(this.$route.params.info)

  },

  methods: {
    weinfo(msg) {
      msg = JSON.parse(msg)
      console.log("ddddsdsd", msg.addr)
      this.formState.addr = msg.addr,
        this.formState.P = msg.encryption[0],
        this.formState.Q = msg.encryption[1],
        this.formState.G = msg.encryption[2],
        this.formState.n = msg.encryption[3],
        this.formState.k = msg.encryption[4]
      // this.formState.vote = true
    },

    prevStep() {
      //  emitter.off('info')
      // this.$emit('prevStep')
      // this.reload()
      this.$router.push('/addvoting')
    },
    generatepub() {
      var para = new Object()
      para.P = this.formState.P
      para.Q = this.formState.Q
      para.G = this.formState.G

      var enc = generatekey1(para)
      // enc.r = Math.round(Math.random() * 100000 + 2).toString()

      // var spub = new Object()
      // spub.x = enc.ecdsa_pk_x
      // spub.y = enc.ecdsa_pk_y
      this.formState.rpub = enc.ring_pk
      this.formState.epub = enc.elgamal_pk

      console.log("sdsdsdsdsd", this.formState.rpub, this.formState.epub)

      var addrfile = new Object()
      addrfile.addr = this.formState.addr

      var object = Object.assign({}, addrfile, para, enc)
      this.downloadTxt(object)
    },
    downloadTxt(object) {
      let str = JSON.stringify(object)
      let strData = new Blob([str], { type: 'text/plain;charset=utf-8' });
      saveAs(strData, "匿名灵活投票密钥信息.txt");
      message.destroy()
      message.success("请注意保存匿名灵活投票密钥文件")
    },
    nextStep() {
      console.log("this.formState.rpub", this.formState.epub, typeof (this.formState.epub))
      console.log("this.formState.rpub", this.formState.rpub, typeof (this.formState.rpub))
      this.$http.post('http://192.168.5.42:8888/voteravc/avc_upload_pk', {
        name: sessionStorage.getItem('user'),
        password: sessionStorage.getItem('pass'),
        uid: sessionStorage.getItem('uid'),
        voteaddr: this.formState.addr,
        rpub: this.formState.rpub,
        epub: this.formState.epub
      }).then((response) => {
        console.log(response)
        if (response.data.result === 'success') {
          this.$emit('nextStep')
        }
        if (response.data.result == 'error1') {
          message.destroy()
          message.warning('请检查登录')
        }
        if (response.data.result == 'error2') {
          message.destroy()
          message.warning('上链失败')
          this.reload()
        }
        // if(response.data.result == 'error3'){
        //    message.destroy()
        //    message.warning('没有投票权限！')
        // }
      }).catch(function (error) { // 请求失败处理
        console.log(error)
      })
      // console.log("sdsdsdsdsd",enc)
      // this.$emit('nextStep')

    },
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
  margin: 4px auto 1px;

  .ant-row:not(:last-child) {
    margin-bottom: 24px;
  }
}
</style>