<template>
  <div style="margin: 3px auto 0;">
    <a-form :model="formStateWe" name="custom-validation" :rules="rules" :labelCol="{lg: {span: 7}, sm: {span: 7}}"
      :wrapperCol="{lg: {span: 10}, sm: {span: 12}}" style="margin: 40px auto 0;" autocomplete="off">
      <h5 style="text-align: center;margin-top: 20px;">匿名权重投票活动信息</h5>
      <a-form-item label="投票信息">
        <a-descriptions bordered="true" :column="{ xxl: 1, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }">
          <a-descriptions-item label="投票地址">{{formStateWe.addr}}</a-descriptions-item>
          <a-descriptions-item label="决策主题">{{formStateWe.title}}</a-descriptions-item>
          <a-descriptions-item label="决策内容">{{formStateWe.content}}</a-descriptions-item>
          <a-descriptions-item label="投票截止时间">{{formStateWe.endTime}}</a-descriptions-item>
          <!-- <a-descriptions-item label="您的投票权重">{{formStateWe.weight}}</a-descriptions-item> -->
        </a-descriptions>

        <a-descriptions bordered="true" :column="{ xxl: 1, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }"
          style="margin-top: 20px;">
          <a-descriptions-item label="您的投票权重">{{formStateWe.weight}}</a-descriptions-item>
          <a-descriptions-item label="构建的加密公钥">{{formStateWe.PK}}</a-descriptions-item>
          <a-descriptions-item label="构建的加密公钥列表">{{formStateWe.PKlist}}</a-descriptions-item>
        </a-descriptions>
      </a-form-item>



      <a-form-item label="表决意愿" name="choice" has-feedback :rules="[{ required: true, message: '请选择投票选项' }]">
        <a-radio-group size="large" v-model:value="formStateWe.choice" style="width: 100%">
          <a-radio :span="8" value="1">同意</a-radio>
          <a-radio :span="8" value="-1">反对</a-radio>
          <a-radio :span="8" value="0">弃权</a-radio>
        </a-radio-group>
      </a-form-item>

      <a-form-item label="加密选票" has-feedback>
        <a-upload :showUploadList="false" :beforeUpload="beforeUpload" accept=".txt" name="file">
          <a-button size="large" html-type="submit" :disabled="formStateWe.choice === ''">
            <upload-outlined></upload-outlined>
            本地读取加密信息并生成选票
          </a-button>
        </a-upload>
      </a-form-item>

      <a-form-item label="选票信息">
        <a-descriptions bordered="true" :column="{ xxl: 1, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }"
          style="margin-top: 20px;">
          <a-descriptions-item label="权重表决加密">{{formStateWe.rawballot}}</a-descriptions-item>
          <a-descriptions-item label="选票签名">{{formStateWe.signature}}</a-descriptions-item>

        </a-descriptions>
      </a-form-item>

      <a-form-item :wrapperCol="{ span: 24 }" style="text-align: center">
        <a-button type="primary" @click="prevStep">上一步</a-button>
        <a-button type="primary" html-type="submit" style="margin-left: 20px" @click="nextStepWe">下一步</a-button>
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
import { message } from 'ant-design-vue';
import { defineComponent, reactive } from 'vue';
export default defineComponent({
  inject: ['reload'],
  setup() {
    const formStateWe = reactive({
      addr: '',
      title: '',
      content: '',
      endTime: '',
      weight: '',
      spub: '',
      PKlist: [],
      PK: '',
      rawballot: '',
      signature: '',
      choice: '',
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
      rules,
      validateSignature,
      formStateWe
    };
  },
  created() {
    console.log("chancan", this.$route.params.info)
    this.weinfo(this.$route.params.info)
  },

  methods: {
    weinfo(msg) {
      msg = JSON.parse(msg)
      this.formStateWe.addr = msg.addr,
        this.formStateWe.title = msg.voteinfo[0],
        this.formStateWe.content = msg.voteinfo[2],
        this.formStateWe.endTime = msg.voteinfo[1],
        this.formStateWe.weight = msg.weight,
        this.formStateWe.PKlist = msg.PKlist,
        this.formStateWe.PK = msg.PK
    },
    beforeUpload(file) {
      // console.log('上传前校验--文件类型', file)
      // this.fileList = [file]
      // console.log('选择了文件beforeUpload', this.fileList)
      if (this.formStateWe.choice != '') {
        this.read(file);
        return false
      }
      else {
        message.destroy()
        message.warning("请先选择表决意愿！")
      }
    },
    read(f) {
      const reader = new FileReader();
      reader.readAsText(f, 'UTF-8');
      reader.onload = fileReader => {
        const fileData = fileReader.target.result;
        var parafile = JSON.parse(fileData)
        // console.log(para, typeof (para));
        // console.log(JSON.parse(reader.result));
        // 上面的两个输出相同
        var index = this.formStateWe.addr.indexOf(parafile.addr)
        console.log("indexshism", index)
        if (index == -1) {
          message.destroy()
          message.warning("文件上传错误，不是当前投票活动参数")
        }
        else {
          var para = new Object()
          para.P = parafile.P
          para.Q = parafile.Q
          para.G = parafile.G

          if (this.formStateWe.PK == '') {
            var PK = generatepub(para, this.formStateWe.PKlist, this.formStateWe.PKlist.length)
            console.log("系统公钥建立：", PK)
            this.formStateWe.PK = PK
            this.setPK()
          }
          // C[i] = encrypt(para, r, PK, m[i], 0)

          var mi = this.formStateWe.choice * this.formStateWe.weight
          this.formStateWe.rawballot = JSON.stringify(encrypt(para, parafile.r, this.formStateWe.PK, mi, 0))

          var ecdsa_pubs = new Object()
          ecdsa_pubs.x = parafile.ecdsa_pk_x
          ecdsa_pubs.y = parafile.ecdsa_pk_y
          this.formStateWe.signature = sign(this.formStateWe.rawballot, parafile.ecdsa_sk, ecdsa_pubs)
          this.formStateWe.spub = JSON.stringify(ecdsa_pubs)

          // signs[i] = sign(jsonC[i], man[i].ecdsa_sk, ecdsa_pubs[i])
          console.log("选票和签名", this.formStateWe.rawballot, this.formStateWe.signature)
        }
      };
    },

    setPK() {
      this.$http.post('http://192.168.5.42:8888/voterwe/upload_wePK', {
        PK: this.formStateWe.PK,
        addr: this.formStateWe.addr,
      }).then((response) => {
        console.log(response)
      })
    },

    prevStep() {
      //  emitter.off('info')
      // this.$emit('prevStep')
      // this.reload()
      this.$router.push('/voting')
    },
    nextStepWe() {
      console.log(this.formStateWe.PK)
      // this.$emit('nextStep')
      if (this.formStateWe.choice) {
        if (this.formStateWe.signature == '') {
          message.destroy()
          message.warning("请点击并上传本地加密信息文件")
        }
        // console.log(JSON.parse(this.formStateWe.rawballot))
        // this.$emit('nextStep')
        this.addweballot()
      }
    },
    addweballot() {
      this.$http.post('http://192.168.5.42:8888/voterwe/add_we_ballot', {
        name: sessionStorage.getItem('user'),
        password: sessionStorage.getItem('pass'),
        uid: sessionStorage.getItem('uid'),
        ballotstr: this.formStateWe.rawballot,
        signature: JSON.stringify(this.formStateWe.signature),
        weight: this.formStateWe.weight,
        addr: this.formStateWe.addr,
        spub: this.formStateWe.spub,
        PK: this.formStateWe.PK
      }).then((response) => {
        console.log(response)
        if (response.data.result == 'success') {
          emitter.emit('change', response.data)
          console.log("jieguo:", response)
          emitter.emit('info1', response.data)
          this.$emit('nextStep')
        }
        if (response.data.result == 'error1') {
          message.destroy()
          message.warning('请检查登录')
        }
        if (response.data.result == 'error2') {
          message.destroy()
          message.warning('没有找到对应投票项目')
        }
        if (response.data.result == 'error3') {
          emitter.emit('change', response.data)
          // this.$emit('nextStep')
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
  margin: 4px auto 1px;

  .ant-row:not(:last-child) {
    margin-bottom: 24px;
  }
}
</style>