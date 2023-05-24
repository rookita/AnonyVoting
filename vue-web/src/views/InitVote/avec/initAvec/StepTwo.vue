<template>
  <div style="margin: 60px auto 0;">
    <a-form :model="formState" name="custom-validation" :rules="rules" :labelCol="{ lg: { span: 7 }, sm: { span: 7 } }"
      :wrapperCol="{ lg: { span: 10 }, sm: { span: 20 } }" style="margin: 40px auto 0;" autocomplete="off">

      <a-form-item label="加密参数" :rules="[{ required: true, message: '请选择投票选项' }]">
        <a-button size="large" type="dashed" style="width: 80%" @click="getpara">
          <PlusOutlined />
          获取加密参数
        </a-button>
      </a-form-item>

      <a-form-item label="投票类型" name="pattern" :rules="[{ required: true, message: '请选择投票类型' }]">
        <a-radio-group v-model:value="formState.pattern">
          <a-radio :value="1">单选</a-radio>
          <a-radio :value="2">多选</a-radio>
          <a-radio :value="3">分数</a-radio>
          <!-- <a-radio :value="3">分数</a-radio> -->
        </a-radio-group>
      </a-form-item>

      <a-form-item label="加密参数" v-if="formState.encryption.length">
        <a-descriptions bordered :column="{ xxl: 1, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }">
          <a-descriptions-item label="P">{{ formState.encryption[0] }}</a-descriptions-item>
          <a-descriptions-item label="Q">{{ formState.encryption[1] }}</a-descriptions-item>
          <a-descriptions-item label="G">{{ formState.encryption[2] }}</a-descriptions-item>
        </a-descriptions>
      </a-form-item>


      <a-form-item label="添加投票者" :rules="[{ required: true }]">
        <template v-if="formState.users.length">
          <ul>
            <template v-for="user in formState.users" :key="user.key">
              <li class="user">
                <a-avatar>
                  <template #icon>
                    <UserOutlined />
                  </template>
                </a-avatar>
                {{ user.id }}
              </li>
            </template>
          </ul>
        </template>
        <!-- <template v-else>
          <a-typography-text class="ant-form-text" type="secondary">
            (
            <SmileOutlined />
            请添加合法投票者. )
          </a-typography-text>
        </template>
        <a-button html-type="button" style="margin: 0 8px" @click="visible = true">添加</a-button> -->
        <a-upload :showUploadList="false" :beforeUpload="beforeUpload1" accept=".xlsx" name="file">
          <a-button size="large" html-type="submit">
            <upload-outlined></upload-outlined>
            上传投票者列表信息
          </a-button>
        </a-upload>
      </a-form-item>

      <!-- <a-modal v-model:visible="visible" title="投票者信息" @ok="onOk">
        <a-form ref="modalFormRef" :model="modalFormState" layout="vertical" name="userForm">
          <a-form-item name="id" label="投票者ID" :rules="[{ required: true }]">
            <a-input v-model:value="modalFormState.id" />
          </a-form-item>
        </a-form>
      </a-modal> -->


      <a-form-item label="加密参数" :rules="[{ required: true, message: '请选择投票选项' }]">
        <a-input-number id="inputNumber" v-model:value="formState.k" :min="1" :max="formState.n" @click="number" />
      </a-form-item>

      <a-form-item label="门限参数" v-if="formState.k">
        <a-descriptions bordered :column="{ xxl: 1, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }">
          <a-descriptions-item label="投票者人数">{{ formState.n }}</a-descriptions-item>
          <a-descriptions-item label="门限人数">{{ formState.k }}</a-descriptions-item>
        </a-descriptions>
      </a-form-item>


      <a-form-item :wrapperCol="{ span: 24 }" style="text-align: center">
        <a-button type="primary" @click="prevStep">上一步</a-button>
        <a-button type="primary" html-type="submit" style="margin-left: 8px" @click="nextStep">下一步</a-button>
      </a-form-item>
    </a-form>

    <a-divider />
    <div class="step-form-style-desc">
      <h3>说明</h3>
      <h4>发起匿名权重投票事项</h4>
      <p>本平台的加密部分均在用户本地进行，平台无法得到用户的私钥信息，保证选票和个人信息保密。投票者列表文件支持xlxs表格文件，表头为id和weight，分别填入投票者的uid和对应权重。</p>
    </div>
  </div>
</template>

<script>
import { read, utils } from 'xlsx'
import emitter from '@/utils/bus';
import { message } from 'ant-design-vue';
import { defineComponent, reactive, ref, watch, toRaw } from 'vue';
export default defineComponent({
  setup() {
    const formState = reactive({
      encryption: [],
      users: [],
      n: '',
      k: '',
      pattern: ''
    });

    const formRef = ref();
    const modalFormRef = ref();
    const visible = ref(false);
    const modalFormState = ref({});
    watch(visible, () => {
      modalFormState.value = {};
    }, {
      flush: 'post',
    });

    const onOk = () => {
      modalFormRef.value.validateFields().then(() => {
        formState.users.push({
          ...modalFormState.value,
          key: Date.now(),
        });
        visible.value = false;
      });
    };

    const onFinish = () => {
      console.log('Finish:', toRaw(formState));
    };


    return {
      formState,
      formRef,
      modalFormRef,
      visible,
      modalFormState,
      onOk,
      onFinish
    };
  },


  methods: {
    number() {
      this.formState.n = this.formState.users.length
    },
    getpara() {
      var para = setup1(256)
      console.log(para.P)
      console.log(typeof (para))
      this.formState.encryption = Object.values(para)
      // console.log(Object.values(para))
    },
    prevStep() {
      this.$emit('prevStep')
    },
    nextStep() {

      if (this.formState.encryption != '' && this.formState.users != '' && this.formState.k != '') {
        emitter.emit("Res1", this.formState.encryption)
        var users = []
        for (let i = 0; i < this.formState.users.length; i++) {
          users[i] = this.formState.users[i].id
        }
        console.log(users)
        var res = []
        res.push(users.toString(), this.formState.n, this.formState.k, this.formState.pattern, this.formState.users)
        emitter.emit("Res2", res)
        this.$emit('nextStep')
      }
      else {
        message.destroy()
        message.warning("请生成定制信息")
      }
    },
    beforeUpload1(file) {
      // console.log('上传前校验--文件类型', file)
      // this.fileList = [file]
      // console.log('选择了文件beforeUpload', this.fileList)
      console.log("file", file);
      let files = { 0: file }
      this.read1(files);
      return false
    },
    read1(files) {
      var that = this;
      console.log(files);
      // 此处判断不严谨，思路只是根据传入的参数校验数据的完整性，可根据自己需求修改
      // 如果没有文件名
      if (files.length <= 0) {
        return;
      }
      const fileReader = new FileReader();
      fileReader.onload = (ev) => {
        try {
          const data = ev.target.result;
          const workbook = read(data, {
            type: 'binary'
          });
          // 取第一张表
          const wsname = workbook.SheetNames[0];
          // 生成json表格内容
          const ws = utils.sheet_to_json(workbook.Sheets[wsname]);
          console.log(ws);
          this.formState.users = ws
          // 后续为自己对ws数据的处理
        } catch (e) {
          return false;
        }
      };
      fileReader.readAsBinaryString(files[0]);
      // const reader = new FileReader();
      // reader.readAsText(f, 'UTF-8');
      // // var f = obj.target.files[0]
      // //4.初始化新的文件读取对象，浏览器自带，不用导入
      // //5.绑定FileReader对象读取文件对象时的触发方法
      // reader.onload = fileReader => {
      //   const fileData = fileReader.currentTarget.result;
      //   var parafile = XLSX.read(fileData, { type: 'binary' })
      //   console.log(parafile)
      //   // console.log(para, typeof (para));
      //   // console.log(JSON.parse(reader.result));
      //   // 上面的两个输出相同
      // }
      // reader.onload = function (e) {
      //   //7.获取文件二进制数据流
      //   var data = e.currentTarget.result;
      //   //8.利用XLSX解析二进制文件为xlsx对象
      //   var wb = XLSX.read(data, { type: 'binary' })
      //   //9.利用XLSX把wb第一个sheet转换成JSON对象
      //   //wb.SheetNames[0]是获取Sheets中第一个Sheet的名字
      //   //wb.Sheets[Sheet名]获取第一个Sheet的数据
      //   var j_data = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]])
      //   //10.在终端输出查看结果
      //   console.log(j_data)
      // }
      // //6.使用reader对象以二进制读取文件对象f，
      // reader.readAsBinaryString(f)
    },
  }
});
</script>
<style lang="less" scoped>
.step-form-style-desc {
  padding: 0 56px;
  color: rgba(0, 0, 0, .45);

  h3 {
    margin: 0 0 12px;
    color: rgba(0, 0, 0, .45);
    font-size: 16px;
    line-height: 32px;
  }

  h4 {
    margin: 0 0 4px;
    color: rgba(0, 0, 0, .45);
    font-size: 14px;
    line-height: 22px;
  }

  p {
    margin-top: 0;
    margin-bottom: 12px;
    line-height: 22px;
  }
}

.dynamic-delete-button {
  cursor: pointer;
  position: relative;
  top: 4px;
  font-size: 24px;
  color: #999;
  transition: all 0.3s;
}

.dynamic-delete-button:hover {
  color: #777;
}

.dynamic-delete-button[disabled] {
  cursor: not-allowed;
  opacity: 0.5;
}
</style>
