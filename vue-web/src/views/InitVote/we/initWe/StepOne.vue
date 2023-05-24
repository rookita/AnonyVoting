<template>
  <div style="margin: 60px auto 0;">
  <a-form
      :model="formState"
       name="custom-validation"
      :rules="rules"
      :labelCol="{lg: {span: 7}, sm: {span: 7}}"
      :wrapperCol="{lg: {span: 10}, sm: {span: 12}}"
      style="margin: 40px auto 0;"
      autocomplete="off" 
  >
    <a-form-item has-feedback label="决策主题" name="title">
      <a-input size="large" v-model:value="formState.title" placeholder="输入投票主题" type="text" autocomplete="off" />
    </a-form-item>

    <a-form-item has-feedback label="决策内容" name="content">
      <a-input size="large" v-model:value="formState.content" placeholder="输入投票主题" type="text" autocomplete="off" />
    </a-form-item>


    <a-form-item has-feedback label="选择投票时间" name="date">
     <a-range-picker
     size="large"
     style="width: 100%;border-radius: 7px;height: 48px;"
      v-model:value="formState.date"
      :disabled-date="disabledDate"
      :show-time="{
        hideDisabledOptions: true,
      }"
      value-format="YYYY-MM-DD HH:mm:ss"
    />
      </a-form-item>

    <a-form-item :wrapperCol="{ span: 24 }"
                 style="text-align: center">
      <a-button type="primary" html-type="submit" @click="nextStep">下一步</a-button>
    </a-form-item>
  </a-form>


  <a-divider />
  <div class="step-form-style-desc">
    <h3>说明</h3>
    <h4>发起匿名权重投票事项</h4>
    <p>如果需要，这里可以放一些关于产品的常见问题说明。如果需要，这里可以放一些关于产品的常见问题说明。如果需要，这里可以放一些关于产品的常见问题说明。</p>
  </div>
</div>
</template>

<script>
// import { message } from 'ant-design-vue';
import dayjs from 'dayjs';
import emitter from '@/utils/bus';
import { defineComponent, reactive} from 'vue';
export default defineComponent({
  setup() {
    const formState = reactive({
      title: '',
      content:'',
      date: undefined,
    });

    const disabledDate = current => {
      // Can not select days before today and today
      // console.log('zhehsi sha :::',current)
      return  current&&current < dayjs().endOf('second');
    };

    let validateTitle = async (_rule, value) => {
      if (value ==='') {
        return Promise.reject('请输入正确格式投票主题');
      } 
      else if(value.length != value.split(" ").join("").length){
        return Promise.reject('输入包含空格');
      }
      else {
        return Promise.resolve();
      }
    };

    let validateContent = async (_rule, value) => {
      if (value ==='') {
        return Promise.reject('请输入正确格式投票主题');
      } 
      else if(value.length != value.split(" ").join("").length){
        return Promise.reject('输入包含空格');
      }
      else {
        return Promise.resolve();
      }
    };

   const rules = {
      title: [{
        required: true,
        validator: validateTitle,
        trigger: 'change',
      }],
      content: [{
        required: true,
        validator: validateContent,
        trigger: 'change',
      }],
       date: [
        {
          required: true,
          message: '请选择投票日期',
        },
      ],
    };

    return {
      dayjs,
      formState,
      validateTitle,
      validateContent,
      rules,
      disabledDate
    };
  },

  methods:{
    nextStep(){
      //  var a = sessionStorage.getItem('uid')
      //  console.log("sdsd",a)
       var res=[]
       if(this.formState.title !== '' && this.formState.title.length == this.formState.title.split(" ").join("").length &&this.formState.date
       &&this.formState.content !==''&&this.formState.content.length == this.formState.content.split(" ").join("").length){
        res.push({Title:this.formState.title,Content:this.formState.content,startTime:this.formState.date[0],endTime:this.formState.date[1]})
        console.log(res)
        emitter.emit("Res",res)
        this.$emit('nextStep')
      }
    },

    }

});
</script>
<style lang="less" scoped>
.step-form-style-desc {
  padding: 0 56px;
  color: rgba(0,0,0,.45);

  h3 {
    margin: 0 0 12px;
    color: rgba(0,0,0,.45);
    font-size: 16px;
    line-height: 32px;
  }

  h4 {
    margin: 0 0 4px;
    color: rgba(0,0,0,.45);
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
    margin: 4px auto 10px ;

    .ant-row:not(:last-child) {
      margin-bottom: 24px;
    }
  }
</style>