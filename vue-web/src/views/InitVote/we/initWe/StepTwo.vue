<template>
  <div style="margin: 60px auto 0;">
    <a-form :model="formState" name="custom-validation" :rules="rules" :labelCol="{ lg: { span: 7 }, sm: { span: 7 } }"
      :wrapperCol="{ lg: { span: 10 }, sm: { span: 20 } }" style="margin: 40px auto 0;" autocomplete="off">



      <a-form-item label="加密参数" :rules="[{ required: true }]">
        <a-button size="large" type="dashed" style="width: 80%" @click="getpara">
          <PlusOutlined />
          获取加密参数
        </a-button>
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
                {{ user.id }} - {{ user.weight }}
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
          <a-form-item name="weight" label="投票者权重" :rules="[{ required: true }]">
            <a-input-number v-model:value="modalFormState.weight" :min="1" :max="10" />
          </a-form-item>
        </a-form>
      </a-modal> -->


      <a-form-item :wrapperCol="{ span: 24 }" style="text-align: center">
        <a-button type="primary" @click="prevStep">上一步</a-button>
        <a-button type="primary" html-type="submit" style="margin-left: 8px" @click="nextStep">下一步</a-button>
      </a-form-item>
    </a-form>

    <a-divider />
    <div class="step-form-style-desc">
      <h3>说明</h3>
      <h4>发起匿名权重投票事项</h4>
      <p>本平台的加密部分均在用户本地进行，平台无法得到用户的私钥信息，保证选票和个人信息保密。投票者列表文件支持xlxs表格文件，表头为id，填入所有投票者的uid，不分先后顺序。</p>
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

    let validateEncryption = async (_rule, value) => {
      if (value === '') {
        return Promise.reject('请输入正确格式投票主题');
      }
      else if (value.length != value.split(" ").join("").length) {
        return Promise.reject('输入包含空格');
      }
      else {
        return Promise.resolve();
      }
    };

    const rules = {
      encryption: [
        {
          required: true,
          validator: validateEncryption,
          trigger: 'change',
        },
      ],
    };

    return {
      formState,
      rules,
      validateEncryption,
      formRef,
      modalFormRef,
      visible,
      modalFormState,
      onOk,
      onFinish
    };
  },

  methods: {
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
    },
    getpara() {
      var para = setup(256)
      console.log(para.P)
      console.log(typeof (para))
      this.formState.encryption = Object.values(para)
      // console.log(Object.values(para))
    },
    prevStep() {
      this.$emit('prevStep')
    },
    nextStep() {
      // if(this.formState.encryption == ''){
      //   console.log("KKKK")
      // }
      console.log(this.formState.users)
      if (this.formState.encryption != '' && this.formState.users != '') {
        emitter.emit("Res1", this.formState.encryption)
        emitter.emit("Res2", this.formState.users)
        this.$emit('nextStep')
      }
      else {
        message.destroy()
        message.warning("请生成定制信息")
      }
    }

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