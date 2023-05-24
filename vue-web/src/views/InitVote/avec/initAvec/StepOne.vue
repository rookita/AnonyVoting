<template>
  <div style="margin: 60px auto 0;">
    <a-form :model="formState" name="custom-validation" :rules="rules" :labelCol="{ lg: { span: 7 }, sm: { span: 7 } }"
      :wrapperCol="{ lg: { span: 10 }, sm: { span: 12 } }" style="margin: 60px auto 70px;" autocomplete="off">
      <a-form-item has-feedback label="投票主题" name="title">
        <a-input size="large" v-model:value="formState.title" placeholder="输入投票主题" type="text" autocomplete="off" />
      </a-form-item>

      <a-form-item has-feedback label="选择投票时间" name="date">
        <a-range-picker size="large" style="width: 100%;border-radius: 7px;height: 48px;" v-model:value="formState.date"
          :disabled-date="disabledDate" :show-time="{
            hideDisabledOptions: true,
          }" value-format="YYYY-MM-DD HH:mm:ss" />
      </a-form-item>

      <a-form-item v-for="(domain, index) in formState.choices" v-bind="index === 0 ? {} : formItemLayout"
        :key="domain.key" :label="index === 0 ? '投票选项' : ' '" name="choices" has-feedback>
        <a-input size="large" v-model:value="domain.value" placeholder="输入投票选项" style="width: 80%; margin-right: 8px" />
        <MinusCircleOutlined v-if="formState.choices.length > 1" class="dynamic-delete-button"
          :disabled="formState.choices.length === 1" @click="removeDomain(domain)" />
      </a-form-item>
      <a-form-item label=" " :wrapper-col="{ lg: { span: 10 }, sm: { span: 12 }, offset: 0 }">
        <a-button size="large" type="dashed" style="width: 100%" @click="addDomain">
          <PlusOutlined />
          添加投票选项
        </a-button>
      </a-form-item>


      <a-form-item :wrapperCol="{ span: 24 }" style="text-align: center">
        <a-button type="primary" html-type="submit" @click="check">下一步</a-button>
      </a-form-item>
    </a-form>


    <a-divider />
    <div class="step-form-style-desc">
      <h3>说明</h3>
      <h4>发起匿名灵活投票事项</h4>
      <p>如果需要，这里可以放一些关于产品的常见问题说明。如果需要，这里可以放一些关于产品的常见问题说明。如果需要，这里可以放一些关于产品的常见问题说明。</p>
    </div>
  </div>
</template>

<script>
import { message } from 'ant-design-vue';
import dayjs from 'dayjs';
import emitter from '@/utils/bus';
import { defineComponent, reactive } from 'vue';
export default defineComponent({
  setup() {
    const formState = reactive({
      title: '',
      date: undefined,
      choices: [],
    });

    const disabledDate = current => {
      // Can not select days before today and today
      // console.log('zhehsi sha :::',current)
      return current && current < dayjs().endOf('second');
    };

    const removeDomain = item => {
      let index = formState.choices.indexOf(item);

      if (index !== -1) {
        formState.choices.splice(index, 1);
      }
    };

    const addDomain = () => {
      formState.choices.push({
        value: '',
        key: Date.now(),
      });
    };
    const formItemLayout = {
      labelCol: {
        lg: {
          span: 7,
        },
        sm: {
          span: 7,
        },
      },
      wrapperCol: {
        lg: {
          span: 10,
        },
        sm: {
          span: 12,
          // offset: 7,
        },
      },
    };

    let validateID = async (_rule, value) => {
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

    let validateChoice = async (_rule, value) => {
      console.log(value)
      for (var i = 0, len = value.length; i < len; i++) {
        if (value[i].value === '') {
          return Promise.reject('所有选项中存在空输入');
        }
        else if (value[i].value.length != value[i].value.split(" ").join("").length) {
          return Promise.reject('选项中存在空格输入');
        }
      }
    };

    const rules = {
      title: [{
        required: true,
        validator: validateID,
        trigger: 'change',
      }],
      date: [
        {
          required: true,
          message: '请选择投票日期',
        },
      ],
      choices: [
        {
          required: true,
          validator: validateChoice,
          trigger: 'change',
        },
      ]
    };

    return {
      dayjs,
      formState,
      validateID,
      rules,
      disabledDate,
      addDomain,
      removeDomain,
      formItemLayout,
      validateChoice
    };
  },

  methods: {
    nextStep() {
      var choice = [], x
      var flag = 1;
      var res = []
      for (var i = 0, len = this.formState.choices.length; i < len; i++) {
        // console.log(this.formState.choices[i].value)
        // console.log(typeof(this.formState.choices[i].value))
        choice.push(this.formState.choices[i].value)
      }
      if (Object.keys(choice).length === 0) {
        flag = 0;
        message.destroy()
        message.warning('请添加投票选项')
      }
      for (x of choice) {
        if (x == '' || x.length !== x.split(" ").join("").length) {
          flag = 0
        }
      }
      if (flag == 1) {
        // this.check()
        // this.$emit('nextStep')
        res.push({ Title: this.formState.title, startTime: this.formState.date[0], endTime: this.formState.date[1] }, choice.toString())
        // console.log(res,typeof(res))
        // console.log(res[1])
        emitter.emit("Res", res)
        // this.$emit('nextStep',res)
        // this.send(res)
        this.$emit('nextStep')
        console.log('success')
      }
    },

    check() {
      console.log('当前时间：', dayjs().hour())
      console.log('当前时间：', dayjs().minute())
      if (this.formState.title !== '' && this.formState.title.length == this.formState.title.split(" ").join("").length && this.formState.date) {
        this.nextStep()
      }
    },

  }


});
</script>
<style lang="less" >
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

.information {
  line-height: 22px;
  margin-top: 24px;
  // padding: 5px 10px;
  background-color: #fafafa;
  // max-width: 500px;
  margin: 4px auto 10px;

  .ant-row:not(:last-child) {
    margin-bottom: 24px;
  }
}
</style>