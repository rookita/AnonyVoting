<template>
  <div style="margin: 3px auto 0;">
    <a-form :model="formState" name="custom-validation" :rules="rules" :labelCol="{ lg: { span: 7 }, sm: { span: 7 } }"
      :wrapperCol="{ lg: { span: 10 }, sm: { span: 12 } }" style="margin: 40px auto 0;" autocomplete="off">
      <h5 style="text-align: center;margin: 20px;">匿名灵活投票活动链上选票信息</h5>
      <a-form-item label="投票信息" :rules="[{ required: true }]">
        <a-descriptions bordered="true" :column="{ xxl: 1, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }">
          <a-descriptions-item label="投票地址">{{ formState.addr }}</a-descriptions-item>
          <a-descriptions-item label="投票标题">{{ formState.title }}</a-descriptions-item>
          <a-descriptions-item label="投票截止时间">{{ formState.endTime }}</a-descriptions-item>
          <a-descriptions-item label="投票选项">{{ formState.choice }}</a-descriptions-item>
          <a-descriptions-item label="投票类型">{{ formState.type }}</a-descriptions-item>
        </a-descriptions>

        <!-- <a-descriptions bordered="true" :column="{ xxl: 1, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }"
          style="margin-top: 20px;">
          <a-descriptions-item label="您的投票权重">{{formState.weight}}</a-descriptions-item>
          <a-descriptions-item label="构建的加密公钥">{{formState.PK}}</a-descriptions-item>

        </a-descriptions> -->
        <a-table :columns="columns" :data-source="formState.data" :pagination="mypagination" size="large"
          v-if="formState.data != ''" bordered>
          <template #bodyCell="{ column, text }">
            <template v-if="column.dataIndex === 'name'">

              <!-- <a-tooltip #title>{{ text }}</a-tooltip> -->
              <a-tooltip>
                <template #title>{{ text }}</template>
                {{ text }}
              </a-tooltip>

              <!-- <a>{{ text }}</a> -->
            </template>
          </template>
          <template #title>选票信息</template>
          <!-- <template #title>投票项目 <a-typography-text strong>{{formState.ID}}</a-typography-text> 的选票信息</template> -->
        </a-table>
      </a-form-item>



      <a-form-item label="加密选票" has-feedback :rules="[{ required: true }]">
        <a-upload :showUploadList="false" :beforeUpload="beforeUpload1" accept=".txt" name="file">
          <a-button size="large" html-type="submit">
            <upload-outlined></upload-outlined>
            本地生成秘密份额
          </a-button>
        </a-upload>
        <!-- <a-descriptions bordered="true" :column="{ xxl: 1, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }">
          <a-descriptions-item label="计票中间值C1">{{formState.C1}}</a-descriptions-item>
          <a-descriptions-item label="计票中间值C2">{{formState.C2}}</a-descriptions-item>
        </a-descriptions> -->
      </a-form-item>

      <a-form-item label="秘密份额" :rules="[{ required: true }]">
        <a-descriptions bordered="true" :column="{ xxl: 1, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }">
          <a-descriptions-item label="匿名灵活活动秘密份额">{{ formState.share }}</a-descriptions-item>
        </a-descriptions>
      </a-form-item>

      <a-form-item :wrapperCol="{ span: 24 }" style="text-align: center">
        <a-button type="primary" @click="prevStep">上一步</a-button>
        <a-button type="primary" html-type="submit" style="margin-left: 20px" @click="nextStepWe">上传份额</a-button>
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

const columns = [
  // {
  //   title: 'ID',
  //   dataIndex: '0',
  //   ellipsis: true,
  // },
  {
    title: '加密选票',
    dataIndex: '1',
    ellipsis: true,
  }, {
    title: '选票签名',
    dataIndex: '2',
    ellipsis: true,
  }];

export default defineComponent({
  inject: ['reload'],
  setup() {

    const formState = reactive({
      addr: '',
      vote: false,
      share: '',
      C1: '',
      C2: '',
      data: [],
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
      formState,
      columns,
      mypagination: {
        defaultPageSize: 3
      }
    };
  },
  // created() {
  //   emitter.on("ballotshare", msg => {
  //     console.log("sdsdsdsdssssss", msg.ballot)
  //     this.formState.addr = msg.addr,
  //       this.formState.data = msg.ballot

  //     //   this.formState.title = msg.voteinfo[0],
  //     //   this.formState.content = msg.voteinfo[2],
  //     //   this.formState.endTime = msg.voteinfo[1],
  //     //   this.formState.weight = msg.weight,
  //     //   this.formState.PKlist = msg.PK,
  //     //   this.formState.vote = true

  //   })
  // },

  created() {
    console.log("chancan", this.$route.params.info)
    this.weresult(this.$route.params.info)
  },

  methods: {
    weresult(msg) {
      msg = JSON.parse(msg)
      if (msg.result == 'success') {
        emitter.emit('resballot', msg)
        this.$emit('next3Step')
      }
      else {
        this.formState.addr = msg.addr,
          this.formState.data = msg.ballot,
          this.formState.epub = msg.epub
        this.formState.title = msg.voteinfo[0]
        this.formState.type = msg.voteinfo[2]
        this.formState.endTime = msg.voteinfo[1]
        this.formState.choice = msg.choice
      }
      // this.formState.addr = msg.addr,
      //   this.formState.data = msg.ballot
    },

    beforeUpload1(file) {
      // console.log('上传前校验--文件类型', file)
      // this.fileList = [file]
      // console.log('选择了文件beforeUpload', this.fileList)
      this.read1(file);
      return false
    },
    read1(f) {
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

          var arr = this.formState.data
          console.log("arr:", arr)
          var n = this.formState.data.length

          var C = new Array(n)
          var jsonC = new Array(n)
          var Signs = new Array(n)
          // var ecdsa_pubs = new Array(n)
          for (let i = 0; i < n; i++) {
            console.log(arr[i][1])
            C[i] = JSON.parse(arr[i][1])
            jsonC[i] = JSON.stringify(C[i])
            Signs[i] = arr[i][2]
            //   ecdsa_pubs[i] = JSON.parse(arr[i][1])
          }

          var share = new Object()
          var sharex = new Array()
          var sharey = new Array()
          //console.log("n:", n)
          var j = this.formState.epub.indexOf(parafile.elgamal_pk)
          for (let i = 0; i < n; i++) {
            //console.log(C[i].x[j])
            sharex.push(C[i].x[j])
            //console.log(C[i].x[j],C[i].y[j])
            sharey.push(decrypt00(para, C[i].g_r, C[i].y[j], parafile.elgamal_sk))
          }
          share.x = sharex;
          share.y = sharey;
          console.log("share:", share)
          this.formState.share = JSON.stringify(share);


          // var countC = count(para, C, Signs, ecdsa_pubs, jsonC, n)

          // console.log("CCCCCCCCCC", countC)
          // console.log("CCCCCCCCCC", ecdsa_pubs)

          // this.formState.share = decrypt0(para, countC.C1, parafile.sk)
          // this.formState.C1 = countC.C1
          // this.formState.C2 = countC.C2
        }
      };
    },

    prevStep() {
      //  emitter.off('info')
      // this.$emit('prevStep')
      // this.reload()
      this.$router.push('/result')
    },
    nextStepWe() {
      console.log(this.formState.share)
      // this.$emit('nextStep')

      if (this.formState.share == '') {
        message.destroy()
        message.warning("请点击并上传本地加密信息文件")
      }
      // console.log(JSON.parse(this.formState.rawballot))
      // this.$emit('nextStep')
      this.addshare()
    },
    addshare() {
      this.$http.post('http://192.168.5.42:8888/voteravc/upload_share', {
        name: sessionStorage.getItem('user'),
        password: sessionStorage.getItem('pass'),
        uid: sessionStorage.getItem('uid'),
        share: this.formState.share,
        C1: this.formState.C1,
        C2: this.formState.C2,
        addr: this.formState.addr,
      }).then((response) => {
        console.log(response)
        if (response.data.result == 'success') {
          // emitter.emit('change', response.data)
          // console.log("jieguo:", response)
          // emitter.emit('info1', response.data)
          this.$emit('nextStep')
        }
        if (response.data.result == 'error1') {
          message.destroy()
          message.warning('请检查登录')
        }
        if (response.data.result == 'error2') {
          message.destroy()
          message.warning('上链失败！')
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

.multi-ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2; // 超出两行则以...形式隐藏
  -webkit-box-orient: vertical;
  cursor: pointer;
}
</style>