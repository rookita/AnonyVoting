<template>
  <div style="margin: 3px auto 0;">

    <a-form :model="formState" name="custom-validation" :rules="rules" :labelCol="{lg: {span: 8}, sm: {span: 7}}"
      :wrapperCol="{lg: {span: 10}, sm: {span: 12}}" style="margin: 40px auto 0;" autocomplete="off"
      v-if="formState.vote">
      <a-form-item label=" " name="pattern" :wrapper-col="{ lg: {span: 10}, sm: {span: 12},  }">
        <a-card title="匿名灵活投票项目信息" :bordered="true" class="information">
          <a-row>
            <a-col :sm="8" :xs="24">投票项目ID：{{formState.ID}}</a-col>
          </a-row>
          <a-row>
            <a-col :sm="8" :xs="24">投票标题：{{formState.title}}</a-col>
          </a-row>
          <a-row>
            <a-col :sm="8" :xs="24">投票截止时间：{{formState.endTime}}</a-col>
          </a-row>
        </a-card>
      </a-form-item>

      <a-form-item label="投票选项" name="pattern" :rules="[{ required: true, message: '请选择投票选项' }]"
        v-if="formState.type == '单选'">
        <a-radio-group size="large" v-model:value="formState['pattern']" style="width: 100%">
          <a-radio :span="8" v-for="item in formState.choices" :key="item.key" :value="item">{{item}}</a-radio>
        </a-radio-group>
      </a-form-item>

      <a-form-item label="投票选项" name="result" :rules="[{ required: true, message: '请选择投票选项' }]" v-else>
        <a-checkbox-group size="large" v-model:value="formState.result" style="width: 100%">
          <a-row>

            <a-checkbox v-for="(item,index) in formState.choices" :key="index" :value="item">{{item}}</a-checkbox>

          </a-row>
        </a-checkbox-group>
      </a-form-item>

      <a-form-item has-feedback label="选票签名" name="signature">
        <a-input size="large" v-model:value="formState.signature" placeholder="输入投票项目签名" type="text"
          autocomplete="off" />
      </a-form-item>

      <a-form-item :wrapperCol="{ span: 24 }" style="text-align: center">
        <a-button type="primary" @click="prevStep">上一步</a-button>
        <a-button type="primary" html-type="submit" style="margin-left: 20px" @click="nextStep">下一步</a-button>
      </a-form-item>

      <a-divider />
      <div class="step-form-style-desc">
        <h3>说明</h3>
        <h4>加入匿名灵活投票事项：请根据以上项目ID返回投票信息完成投票。</h4>
        <p></p>
      </div>
    </a-form>

    <a-form :model="formStateWe" name="custom-validation" :rules="rules" :labelCol="{lg: {span: 7}, sm: {span: 7}}"
      :wrapperCol="{lg: {span: 10}, sm: {span: 12}}" style="margin: 40px auto 0;" autocomplete="off"
      v-if="formStateWe.vote">
      <h5 style="text-align: center;margin-top: 20px;">本地生成加密套件</h5>
      <a-form-item label="加密参数" :rules="[{ required: true }]">
        <a-descriptions bordered="true" :column="{ xxl: 1, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }">
          <a-descriptions-item label="投票地址">{{formStateWe.addr}}</a-descriptions-item>
          <a-descriptions-item label="P">{{formStateWe.P}}</a-descriptions-item>
          <a-descriptions-item label="Q">{{formStateWe.Q}}</a-descriptions-item>
          <a-descriptions-item label="G">{{formStateWe.G}}</a-descriptions-item>
        </a-descriptions>
      </a-form-item>


      <a-form-item has-feedback label="获取加密参数" name="signature">
        <a-button size="large" type="dashed" style="width: 80%" @click="generatepub">
          <PlusOutlined />
          本地下载加密信息文件
        </a-button>
      </a-form-item>

      <a-form-item :wrapperCol="{ span: 24 }" style="text-align: center">
        <a-button type="primary" @click="prevStep">上一步</a-button>
        <a-button type="primary" html-type="submit" style="margin-left: 20px" @click="nextStepWe">上传公钥</a-button>
      </a-form-item>
      <a-divider />
      <div class="step-form-style-desc">
        <h3>说明</h3>
        <h4>加入匿名权重投票事项：请根据以上项目ID返回投票信息完成投票表决。</h4>
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
      ID: '',
      title: '',
      startTime: '',
      endTime: '',
      choices: [],
      signature: '',
      result: [],
      type: '',
      vote: false
    });

    const formStateWe = reactive({
      addr: '',
      P: '',
      Q: '',
      G: '',
      spub: '',
      epub: '',
      vote: false
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
      formState,
      rules,
      validateSignature,
      formStateWe
    };
  },
  mounted() {
    emitter.on("info", msg => {
      console.log("ddddsdsd", msg)
      if (msg.type == 'we') {
        this.formStateWe.addr = msg.addr,
          this.formStateWe.P = msg.encryption[0],
          this.formStateWe.Q = msg.encryption[1],
          this.formStateWe.G = msg.encryption[2],
          this.formStateWe.vote = true
      }
      else {
        this.formState.ID = msg.ID,
          this.formState.title = msg.title,
          this.formState.endTime = msg.ddl,
          this.formState.choices = msg.choice,
          this.formState.vote = true,
          this.formState.type = msg.type
        // this.formState.type = true
      }
    })
  },

  methods: {
    prevStep() {
      //  emitter.off('info')
      this.$emit('prevStep')
      this.reload()
    },
    nextStep() {
      var res = []
      if (this.formState.signature !== '' && this.formState.signature.length == this.formState.signature.split(" ").join("").length && this.formState.pattern) {
        res.push({ ID: this.formState.ID, ballot: this.formState.pattern, signature: this.formState.signature, vote: 'avec' })
        console.log("构造数据", res)
        emitter.emit('upload', res)
        this.$emit('nextStep')
      }
      else if (this.formState.signature !== '' && this.formState.signature.length == this.formState.signature.split(" ").join("").length && this.formState.result.length) {
        res.push({ ID: this.formState.ID, ballot: this.formState.result, signature: this.formState.signature, vote: 'avec' })
        console.log("构造数据", res)
        emitter.emit('upload', res)
        this.$emit('nextStep')
      }
    },

    generatepub() {
      var para = new Object()
      para.P = this.formStateWe.P
      para.Q = this.formStateWe.Q
      para.G = this.formStateWe.G
      var enc = generatekey(para)
      enc.r = Math.round(Math.random() * 100000 + 2).toString()

      var spub = new Object()
      spub.x = enc.ecdsa_pk_x
      spub.y = enc.ecdsa_pk_y
      this.formStateWe.spub = spub
      this.formStateWe.epub = enc.pk
      console.log("sdsdsdsdsd", this.formStateWe.spub, this.formStateWe.epub)

      var addrfile = new Object()
      addrfile.addr = this.formStateWe.addr

      var object = Object.assign({},addrfile,para,enc)
      this.downloadTxt(object)
    },
    downloadTxt(object) {
      let str = JSON.stringify(object)
      let strData = new Blob([str], { type: 'text/plain;charset=utf-8' });
      saveAs(strData, "权重密钥信息.txt");
      message.destroy()
      message.success("请注意保存权重密钥文件")
    },
    nextStepWe() {
      this.$http.post('http://192.168.5.42:8888/voter/we_upload_pk', {
        name:sessionStorage.getItem('user'),
        password:sessionStorage.getItem('pass'),
        uid:sessionStorage.getItem('uid'),
        voteaddr:this.formStateWe.addr,
        spub:Object.values(this.formStateWe.spub),
        epub:this.formStateWe.epub
      }).then((response) => {
        console.log(response)
        if (response.data.result === 'success') {
          this.$emit('nextStep')
        }
        if(response.data.result == 'error1'){
           message.destroy()
           message.warning('请检查登录')
        }
        if(response.data.result == 'error2'){
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