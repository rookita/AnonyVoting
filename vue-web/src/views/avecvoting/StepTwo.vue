<template>
  <div style="margin: 3px auto 0;">
    <a-form :model="formState" name="custom-validation" :rules="rules" :labelCol="{ lg: { span: 8 }, sm: { span: 7 } }"
      :wrapperCol="{ lg: { span: 10 }, sm: { span: 12 } }" style="margin: 40px auto 0;" autocomplete="off">
      <h5 style="text-align: center;margin-top: 20px;">匿名灵活投票活动信息</h5>
      <!-- <a-form-item label=" " name="pattern" :wrapper-col="{ lg: {span: 10}, sm: {span: 12},  }">
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
      </a-form-item> -->

      <a-form-item label="投票信息">
        <a-descriptions bordered="true" :column="{ xxl: 1, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }">
          <a-descriptions-item label="投票地址">{{ formState.addr }}</a-descriptions-item>
          <a-descriptions-item label="投票标题">{{ formState.title }}</a-descriptions-item>
          <a-descriptions-item label="投票截止时间">{{ formState.endTime }}</a-descriptions-item>
          <!-- <a-descriptions-item label="您的投票权重">{{formStateWe.weight}}</a-descriptions-item> -->
        </a-descriptions>

        <a-descriptions bordered="true" :column="{ xxl: 1, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }"
          style="margin-top: 20px;">
          <a-descriptions-item label="构建的加密公钥">{{ formState.PK }}</a-descriptions-item>
          <a-descriptions-item label="构建的加密公钥列表">{{ formState.PKlist }}</a-descriptions-item>
        </a-descriptions>
      </a-form-item>

      <a-form-item label="投票选项" name="pattern" :rules="[{ required: true, message: '请选择投票选项' }]"
        v-if="formState.type == '单选'">
        <a-radio-group size="large" v-model:value="formState['pattern']" style="width: 100%">
          <a-radio :span="8" v-for="item in formState.choices" :key="item.key" :value="item">{{ item }}</a-radio>
        </a-radio-group>
      </a-form-item>

      <a-form-item label="投票选项" name="result" :rules="[{ required: true, message: '请选择投票选项' }]"
        v-if="formState.type == '多选'">
        <a-checkbox-group size="large" v-model:value="formState.result" style="width: 100%">
          <a-row>

            <a-checkbox v-for="(item, index) in formState.choices" :key="index" :value="item">{{ item }}</a-checkbox>

          </a-row>
        </a-checkbox-group>
      </a-form-item>

      <a-form-item label="投票选项" name="score" :rules="[{ required: true, message: '请选择投票选项' }]"
        v-if="formState.type == '分数'" v-for="(domain, index) in formState.score" :key="domain.key">
        <!-- <a-checkbox-group size="large" v-model:value="formState.result" style="width: 100%"> -->
        <!-- <a-row> -->

        <a-descriptions-item>{{ domain.item }}
          <a-rate v-model:value="domain.value" />
        </a-descriptions-item>

        <!-- <a-rate v-for="(item,index) in formState.choices" :key="index" v-model:value="formState['result']">{{item}}
          <a-descriptions-item v-model:value="formState.result" />
        </a-rate> -->


        <!-- </a-row> -->
        <!-- </a-checkbox-group> -->
      </a-form-item>

      <a-form-item label="加密选票" has-feedback>
        <a-upload :showUploadList="false" :beforeUpload="beforeUpload" accept=".txt" name="file">
          <a-button size="large" html-type="submit">
            <upload-outlined></upload-outlined>
            本地读取加密信息并生成选票
          </a-button>
        </a-upload>
      </a-form-item>


      <a-form-item label="选票信息">
        <a-descriptions bordered="true" :column="{ xxl: 1, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }"
          style="margin-top: 20px;">
          <a-descriptions-item label="选票加密">{{ formState.rawballot }}</a-descriptions-item>
          <a-descriptions-item label="选票签名">{{ formState.signature }}</a-descriptions-item>

        </a-descriptions>
      </a-form-item>

      <!-- <a-form-item has-feedback label="选票签名" name="signature">
        <a-input size="large" v-model:value="formState.signature" placeholder="输入投票项目签名" type="text"
          autocomplete="off" />
      </a-form-item> -->

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
  </div>
</template>
<script>
import emitter from '@/utils/bus';
import { message } from 'ant-design-vue';
import { defineComponent, reactive, ref } from 'vue';
export default defineComponent({
  inject: ['reload'],
  setup() {
    const formState = reactive({
      addr: '',
      title: '',
      endTime: '',
      PKlist: [],
      PK: '',
      rawballot: '',
      signature: '',
      choices: [],
      type: '',
      result: [],
      score: [],
      // pattern: '',
      n: '',
      k: '',
      allrpub: [],
      m: '',
    });

    let validateSignature = async (_rule, value) => {
      if (value === '') {
        return Promise.reject('请输入正确格式账户名');
      }
      else if (value.length != value.split(" ").join("").length) {
        return Promise.reject('输入包含空格');
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
    };
  },
  created() {
    console.log("chancan", this.$route.params.info)
    this.avcinfo(this.$route.params.info)
    // this.formState.score = new Array(this.formState.choices.length)
  },


  methods: {
    avcinfo(msg) {
      msg = JSON.parse(msg)
      this.formState.addr = msg.addr,
        this.formState.title = msg.voteinfo[0],
        this.formState.type = msg.voteinfo[2],
        this.formState.endTime = msg.voteinfo[1],
        this.formState.PKlist = msg.PKlist,
        this.formState.PK = msg.PK,
        this.formState.choices = msg.choice,
        this.formState.n = msg.para[3],
        this.formState.k = msg.para[4],
        this.formState.allrpub = msg.rpub
      var i;
      for (i in this.formState.choices) {
        this.formState.score.push({
          value: 0,
          item: this.formState.choices[i],
          key: Date.now(),
        })
      }
    },
    prevStep() {
      //  emitter.off('info')
      // this.$emit('prevStep')
      // this.reload()
      this.$router.push('/voting')
    },
    str2hex(str) {
      if (str === "") {
        return "";
      }
      else {
        var arr = [];
        //arr.push("0x");
        for (var i = 0; i < str.length; i++) {
          var tmp;
          tmp = str.charCodeAt(i).toString(16)
          if (tmp.length < 3) {  //两字节
            tmp = '00' + tmp
          }
          arr.push(tmp);
        }
        return arr.join('');
      }
    },

    beforeUpload(file) {
      // console.log('上传前校验--文件类型', file)
      // this.fileList = [file]
      // console.log('选择了文件beforeUpload', this.fileList)
      this.read(file);
      return false
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
        var index = this.formState.addr.indexOf(parafile.addr)
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

          if (this.formState.PK == '') {
            var PK = generatepub(para, this.formState.PKlist, this.formState.PKlist.length)
            console.log("系统公钥建立：", PK)
            this.formState.PK = PK
            this.setPK()
          }
          // C[i] = encrypt(para, r, PK, m[i], 0)

          if (this.formState.type == '单选') {
            // this.formState.m = encodeURIComponent(this.formState['pattern'])
            this.formState.m = this.formState['pattern']
          }
          if (this.formState.type == '多选') {
            this.formState.m = this.formState.result.map(a => encodeURIComponent(a)).toString()
          }
          if (this.formState.type == '分数') {
            this.formState.m = this.formState.score.map(a => a.value).toString()
          }
          // console.log("raw message:", this.formState.m)
          console.time("sort");
          this.formState.rawballot = JSON.stringify(encrypt1(para, this.formState.n, this.formState.k, this.formState.PK, this.str2hex(this.formState.m), this.formState.PK, this.formState.PKlist))
          console.timeEnd("sort");
          // console.log("m:", this.str2hex(this.formState.m))

          var i = this.formState.allrpub.indexOf(parafile.ring_pk)
          // console.log("ssssss", i)
          // console.log("ssssss", this.formState.allrpub)
          console.time("sort1");
          this.formState.signature = sign1(parafile.ring_sk, this.formState.allrpub, this.formState.rawballot, i, this.formState.n)
          console.timeEnd("sort1");

          // var ecdsa_pubs = new Object()
          // ecdsa_pubs.x = parafile.ecdsa_pk_x
          // ecdsa_pubs.y = parafile.ecdsa_pk_y
          // this.formStateWe.signature = sign(this.formStateWe.rawballot, parafile.ecdsa_sk, ecdsa_pubs)
          // this.formStateWe.spub = JSON.stringify(ecdsa_pubs)

          // signs[i] = sign(jsonC[i], man[i].ecdsa_sk, ecdsa_pubs[i])
          // this.formState.signature = sign1(man[i].ring_sk, ring_pubs, JSON.stringify(C[i]), i, n)
          console.log("选票和签名", this.formState.rawballot, this.formState.signature)
        }
      };
    },

    setPK() {
      this.$http.post('http://192.168.5.42:8888/voteravc/upload_avcPK', {
        PK: this.formState.PK,
        addr: this.formState.addr,
      }).then((response) => {
        console.log(response)
      })
    },

    nextStep() {
      console.log(this.formState.score)
      // this.$emit('nextStep')
      if (this.formState.m) {
        if (this.formState.signature == '') {
          message.destroy()
          message.warning("请点击并上传本地加密信息文件")
        }
        // console.log(JSON.parse(this.formStateWe.rawballot))
        // this.$emit('nextStep')
        this.addavcballot()
      }
    },
    addavcballot() {
      this.$http.post('http://192.168.5.42:8888/voteravc/add_avc_ballot', {
        name: sessionStorage.getItem('user'),
        password: sessionStorage.getItem('pass'),
        uid: sessionStorage.getItem('uid'),
        ballotstr: this.formState.rawballot,
        // signature: JSON.stringify(this.formStateWe.signature),
        signature: this.formState.signature,
        addr: this.formState.addr,
        PK: this.formState.PK
      }).then((response) => {
        console.log(response)
        if (response.data.result == 'success') {
          emitter.emit('change1', response.data)
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