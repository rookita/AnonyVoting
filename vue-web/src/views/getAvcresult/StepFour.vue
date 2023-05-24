<template>
  <a-card :bordered="false">
    <div style="margin: 3px auto 0;">
      <a-form :model="formState" name="custom-validation" :rules="rules"
        :labelCol="{ lg: { span: 7 }, sm: { span: 7 } }" :wrapperCol="{ lg: { span: 10 }, sm: { span: 12 } }"
        style="margin: 40px auto 0;" autocomplete="off">
        <h5 style="text-align: center;margin: 20px;">匿名灵活活动链上选票信息汇总</h5>
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


        <a-form-item label="统计结果" :rules="[{ required: true }]" v-if="formState.type === '分数'">
          <a-descriptions bordered="true" :column="{ xxl: 1, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }" v-if="formState.score"
            v-for="(domain, index) in formState.score" :key="domain.key">
            <a-descriptions-item :label="domain.item">
              {{ domain.value }}
            </a-descriptions-item>
          </a-descriptions>
          <a-spin size="small" v-if="formState.result === '' && formState.click !== ''" />
        </a-form-item>

        <a-form-item label="统计结果" :rules="[{ required: true }]" v-else>
          <a-descriptions bordered="true" :column="{ xxl: 1, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }"
            v-if="formState.result" v-for="domain in formState.result" :key=Date.now()>
            <a-descriptions-item :label="domain[0]">
              {{ domain[1] }}
            </a-descriptions-item>
          </a-descriptions>
          <a-spin size="small" v-if="formState.result === '' && formState.click !== ''" />
        </a-form-item>


        <!-- <a-form-item label="表决结果" :rules="[{ required: true }]" v-if="formState.res">
          <a-descriptions bordered="true" :column="{ xxl: 1, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }">
            <a-descriptions-item label="统计结果">{{ formState.res }}</a-descriptions-item>
          </a-descriptions>
        </a-form-item> -->


        <a-form-item :wrapperCol="{ span: 24 }" style="text-align: center">
          <a-button type="primary" @click="prevStep">上一步</a-button>
          <a-button type="primary" html-type="submit" style="margin-left: 20px" @click="getres"
            :disabled="formState.click !== ''">获取结果</a-button>
        </a-form-item>


        <a-divider />
        <div class="step-form-style-desc">
          <h3>说明</h3>
          <h4>加入匿名权重投票事项：请根据以上项目ID返回投票信息完成投票表决。</h4>
        </div>
      </a-form>
    </div>
  </a-card>
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
  },
];

export default defineComponent({
  inject: ['reload'],
  setup() {

    const formState = reactive({
      addr: '',
      res: '',
      sum: '',
      data: [],
      click: '',
      result: '',
      score: []
    });

    return {
      formState,
      columns,
      mypagination: {
        defaultPageSize: 3
      }
    };
  },
  // created() {
  //   emitter.on("resballot", msg => {
  //     // console.log("sdsdsdsdssssss", msg.ballot)
  //     this.formState.addr = msg.addr,
  //       this.formState.data = msg.ballot

  //   })
  // },
  created() {
    console.log("chancan", this.$route.params.info)
    this.prevStep1(this.$route.params.info)
  },

  methods: {
    prevStep1(msg) {
      //  emitter.off('info')
      msg = JSON.parse(msg)
      this.formState.addr = msg.addr
      this.formState.data = msg.ballot
      this.formState.title = msg.voteinfo[0]
      this.formState.type = msg.voteinfo[2]
      this.formState.endTime = msg.voteinfo[1]
      this.formState.choice = msg.choice
    },
    prevStep() {
      //  emitter.off('info')
      // this.$emit('prevStep')
      // this.reload()
      this.$router.push('/result')
    },

    hex2str(hex) {
      var trimedStr = hex.trim();
      var rawStr = trimedStr.substr(0, 2).toLowerCase() === "0x" ? trimedStr.substr(2) : trimedStr;
      var len = rawStr.length;
      if (len % 2 !== 0) {
        alert("Illegal Format ASCII Code!");
        return "";
      }
      var curCharCode;
      var resultStr = [];
      for (var i = 0; i < len; i = i + 2) {
        curCharCode = parseInt(rawStr.substr(i, 2), 16);
        resultStr.push(String.fromCharCode(curCharCode));
      }
      return resultStr.join("");
    },
    unicode2string(unicode) {
      //console.log('unicode:',unicode)
      if (unicode.length % 4 != 0) {
        unicode = '00' + unicode
      }
      var res = ""
      for (let i = 0; i < unicode.length; i = i + 4) {
        res += String.fromCharCode(parseInt(unicode.substr(i, 4), 16))
      }
      return res
    },

    getres() {
      this.formState.click = 'click'
      this.$http.post('http://192.168.5.42:8888/voteravc/get_avc_result', {
        name: sessionStorage.getItem('user'),
        password: sessionStorage.getItem('pass'),
        addr: this.formState.addr,
      }).then((response) => {
        console.log(response)
        if (response.data.result == 'success') {
          console.log("jieguo:", response.data)
          // this.$emit('nextStep')
          var para = new Object()
          para.P = response.data.para[0]
          para.Q = response.data.para[1]
          para.G = response.data.para[2]
          var arr = this.formState.data
          var k = response.data.para[4]
          console.log("K", k)
          var CE = response.data.PK
          var n = this.formState.data.length
          var C = new Array(n)
          var share = response.data.allshare
          // var ecdsa_pubs = new Array(n)
          for (let i = 0; i < n; i++) {
            // console.log(arr[i][1])
            C[i] = JSON.parse(arr[i][1])
            // jsonC[i] = JSON.stringify(C[i])
            //   ecdsa_pubs[i] = JSON.parse(arr[i][1])
          }

          var m = new Array()
          console.log("dsdsdsdsdsds", JSON.parse(share[0]))
          // var allshare = new Array()
          // for(i in share){
          //   allshare.push(JSON.parse(i))
          // }

          for (let j = 0; j < n; j++) {
            var tmpx = new Array()
            var tmpy = new Array()
            for (let i = 0; i < k; i++) {
              console.log("dsds", share)
              var tmpshare = JSON.parse(share[i])
              tmpx.push(tmpshare.x[j])
              tmpy.push(tmpshare.y[j])
            }
            C[j].x = tmpx
            C[j].y = tmpy
            console.log("PK:", CE[0])
            console.time("sort");
            m[j] = decrypt11(para, C[j], CE[0], k)
            console.timeEnd("sort");
            //console.log(C[j])
            //console.log(decrypt11(para, C[j], CE, k))
          }
          // console.log(hex2str(m))

          // for (var i in response.data.choice) {
          //   this.formState.result.push({
          //     value: 0,
          //     item: response.data.choice[i],
          //     key: Date.now(),
          //   })
          // }
          // console.log(this.formState.result)

          for (let i = 0; i < n; i++) {
            console.log(m[i])
            // m[i] = decodeURIComponent(this.hex2str(m[i]))
            m[i] = this.unicode2string(decodeURIComponent(m[i])).split(',')
            console.log(m[i])
          }
          if (this.formState.type == '单选') {
            var obj = {}
            m.forEach(function (item) {
              obj[item] = obj[item] ? obj[item] + 1 : 1
            })
            console.log(obj);
            this.formState.result = Object.entries(obj)//自身枚举元素
            console.log(Object.entries(this.formState.result))
          }

          if (this.formState.type == '多选') {
            var obj = {}
            for (let i = 0; i < n; i++) {
              m[i].forEach(function (item) {
                obj[item] = obj[item] ? obj[item] + 1 : 1
              })
              console.log(obj)
            }
            this.formState.result = Object.entries(obj)
            console.log(this.formState.result)
          }

          if (this.formState.type == '分数') {


            var res = []
            let result = []
            for (let i = 0; i < n; i++) {
              res.push(m[i])
              console.log(res)
            }
            res = Array.from(res);
            for (let key in res) {
              res[key].forEach((value, index) => {
                if (result[index] == null || result[index] == "") {
                  result[index] = 0;
                }
                console.log(value, index)
                result[index] += parseInt(value);
                // console.log(value, index)
                // result[index] = result[index] + value;
                // console.log(result[index])
              })
            }
            console.log(result)
            for (let i in this.formState.choice.split(',')) {
              console.log(i)
              this.formState.score.push({
                value: result[i],
                item: this.formState.choice.split(',')[i],
                key: Date.now(),
              })
            }
            this.formState.result = 1
          }

          // for (var i in Object.entries(this.formState.result)) {
          //   this.formState.result1.push({
          //     value: 0,
          //     item: response.data.choice[i],
          //     key: Date.now(),
          //   })
          // }
          // console.log(this.formState.result)

        }
        if (response.data.result == 'error1') {
          message.destroy()
          message.warning('请检查登录')
        }
        if (response.data.result == 'wait') {
          message.destroy()
          message.warning('请等候门限数量参与者共同恢复结果')
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