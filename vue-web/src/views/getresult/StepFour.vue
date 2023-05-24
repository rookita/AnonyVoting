<template>
  <div style="margin: 3px auto 0;">
    <a-form :model="formStateWe" name="custom-validation" :rules="rules" :labelCol="{lg: {span: 7}, sm: {span: 7}}"
      :wrapperCol="{lg: {span: 10}, sm: {span: 12}}" style="margin: 40px auto 0;" autocomplete="off">
      <h5 style="text-align: center;margin: 20px;">权重投票活动链上选票信息汇总</h5>
      <a-form-item label="投票信息" :rules="[{ required: true }]">
        <a-descriptions bordered="true" :column="{ xxl: 1, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }">
          <a-descriptions-item label="投票地址">{{formStateWe.addr}}</a-descriptions-item>
        </a-descriptions>

        <!-- <a-descriptions bordered="true" :column="{ xxl: 1, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }"
          style="margin-top: 20px;">
          <a-descriptions-item label="您的投票权重">{{formStateWe.weight}}</a-descriptions-item>
          <a-descriptions-item label="构建的加密公钥">{{formStateWe.PK}}</a-descriptions-item>

        </a-descriptions> -->
        <a-table :columns="columns" :data-source="formStateWe.data" :pagination="mypagination" size="large"
          v-if="formStateWe.data != ''" bordered>
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

      <a-form-item label="统计结果" :rules="[{ required: true }]" v-if="formStateWe.sum">
        <a-descriptions bordered="true" :column="{ xxl: 1, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }">
          <a-descriptions-item label="决议得票">{{formStateWe.sum}}</a-descriptions-item>
        </a-descriptions>
      </a-form-item>

      <a-form-item label="表决结果" :rules="[{ required: true }]" v-if="formStateWe.res">
        <a-descriptions bordered="true" :column="{ xxl: 1, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }">
          <a-descriptions-item label="统计结果">{{formStateWe.res}}</a-descriptions-item>
        </a-descriptions>
      </a-form-item>


      <a-form-item :wrapperCol="{ span: 24 }" style="text-align: center">
        <a-button type="primary" @click="prevStep">上一步</a-button>
        <a-button type="primary" html-type="submit" style="margin-left: 20px" @click="getres">获取结果</a-button>
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
  {
    title: 'ID',
    dataIndex: '0',
    ellipsis: true,
  },
  {
    title: '签名公钥',
    dataIndex: '1',
    ellipsis: true,
  }, {
    title: '权重',
    dataIndex: '2',
  },
  {
    title: '选票',
    dataIndex: '3',
    ellipsis: true,
  },
  {
    title: '签名',
    dataIndex: '4',
    ellipsis: true,
  }];

export default defineComponent({
  inject: ['reload'],
  setup() {

    const formStateWe = reactive({
      addr: '',
      res: '',
      sum:'',
      data: [],
    });

    return {
      formStateWe,
      columns,
      mypagination: {
        defaultPageSize: 3
      }
    };
  },
  created() {
    emitter.on("resballot", msg => {
      // console.log("sdsdsdsdssssss", msg.ballot)
      this.formStateWe.addr = msg.addr,
        this.formStateWe.data = msg.ballot

    })
  },

  methods: {
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
        var index = this.formStateWe.addr.indexOf(parafile.addr)
        console.log("indexshism", index)
        if (index == -1) {
          message.destroy()
          message.warning("文件上传错误，不是当前投票活动参数")
        }

        var para = new Object()
        para.P = parafile.P
        para.Q = parafile.Q
        para.G = parafile.G

        var arr = this.formStateWe.data
        var n = this.formStateWe.data.length
        var C = new Array(n)
        var jsonC = new Array(n)
        var Signs = new Array(n)
        var ecdsa_pubs = new Array(n)
        for (let i = 0; i < n; i++) {
          console.log(arr[i][1])
          C[i] = JSON.parse(arr[i][3])
          jsonC[i] = JSON.stringify(C[i])
          Signs[i] = JSON.parse(arr[i][4])
          ecdsa_pubs[i] = JSON.parse(arr[i][1])
        }
        var countC = count(para, C, Signs, ecdsa_pubs, jsonC, n)

        console.log("CCCCCCCCCC", countC)
        console.log("CCCCCCCCCC", ecdsa_pubs)

        this.formStateWe.share = decrypt0(para, countC.C1, parafile.sk)
        this.formStateWe.C1 = countC.C1
        this.formStateWe.C2 = countC.C2
      };
    },

    prevStep() {
      //  emitter.off('info')
      this.$emit('prevStep')
      this.reload()
    },

    getres() {
      this.$http.post('http://192.168.5.42:8888/voter/get_we_result', {
        name: sessionStorage.getItem('user'),
        password: sessionStorage.getItem('pass'),
        addr: this.formStateWe.addr,
      }).then((response) => {
        console.log(response)
        if (response.data.result == 'success') {
          console.log("jieguo:", response.data)
          // this.$emit('nextStep')
          var para = new Object()
          para.P = response.data.para[0]
          para.Q = response.data.para[1]
          para.G = response.data.para[2]
          var C2 = response.data.C2
          var Cx = response.data.Cx
          var n = Cx.length
          var max = 100 //max为暴力破解上限
          var bsum = decrypt1(para, C2, Cx, n, max)
          console.log("b:", bsum) //sum[m]
          this.formStateWe.sum = bsum
          if(bsum > 0){
            this.formStateWe.res = "通过"
          }
          if(bsum < 0){
            this.formStateWe.res = "未通过"
          }
          if(bsum = 0){
            this.formStateWe.res = "中立"
          }
        }
        if (response.data.result == 'error1') {
          message.destroy()
          message.warning('请检查登录')
        }
        if (response.data.result == 'wait') {
          message.destroy()
          message.warning('请等候所有的参与者共同恢复结果')
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