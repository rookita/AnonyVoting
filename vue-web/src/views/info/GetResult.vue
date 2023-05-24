<template>
<a-card :bordered="false" style="height: auto;">
<h5 style="text-align: center;margin-top: 20px;">投票结果查询</h5>
 <div style="margin: 30px auto 0;">
      <div class="ant-pro-page-header-search">
        <a-input-search  size="large" style="width: 80%; max-width: 500px;" @search="search" v-model:value="value" placeholder="输入投票项目ID">
          <!-- <template #enterButton>
            查询
          </template> -->
        </a-input-search>
      </div>
       
    <a-divider>
    </a-divider>

    <a-form
      :model="formState"
       name="custom-validation"
      :rules="rules"
      :labelCol="{lg: {span: 7}, sm: {span: 7}}"
      :wrapperCol="{lg: {span: 10}, sm: {span: 12}}"
      autocomplete="off"
      
  >
 <a-form-item label=" ">
  <a-table :columns="columns" :data-source="formState.data" :pagination="mypagination" size="middle" v-if="formState.data != ''">
    <template #bodyCell="{ column, text }">
      <template v-if="column.dataIndex === 'name'">
        <a>{{ text }}</a>
      </template>
    </template>
    <template #title>投票项目 <a-typography-text strong>{{formState.ID}}</a-typography-text> 的选票信息</template>
  </a-table>
  
  </a-form-item>
  </a-form>


  <a-divider />
  <div class="step-form-style-desc">
    <h3>说明</h3>
    <h4>获取投票项目所得选票信息注意事项：请根据投票项目唯一ID标识进行输入查询。</h4>
    <p></p>
  </div>
  <a-divider />
  </div>
  </a-card>
</template>

<script>
import { message } from 'ant-design-vue';
import emitter from '@/utils/bus';
import { defineComponent, reactive, ref } from 'vue';
import AddVoting from'@/views/addvoting/AddVoting.vue'

const columns = [{
  title: '选票',
  dataIndex: '0',
},{
  title: '签名',
  dataIndex: '1',
}];
export default defineComponent({
  inject:['reload'],
  setup() {
     const formState = reactive({
      ID:'',
      ballot:'',
      signature:'',
      data:[],
    });

    const value = ref('');

    return {
      formState,
      value,
      columns,
     
      mypagination:{
        defaultPageSize: 6
      }
    };
  },

  components: {
    AddVoting,
  },

  created(){
    emitter.on("search",msg=>{
      this.value = msg
      this.send()
    }
    )
  },

   methods:{
   
  
     search(){
      // var id = this.value
      // this.$router.push({name:'wevoting',params:{id:id}})
       if(this.value =='' || this.value.length !== this.value.split(" ").join("").length){
         message.destroy()
         message.error('请检查输入格式')
       }
       else{
         this.send()
       }
     },
    send(){
      this.$http.post('http://192.168.5.42:8888/voter/get_result', {
        name:sessionStorage.getItem('user'),
        password:sessionStorage.getItem('pass'),
        ID:this.value,
      }).then((response) =>{
        // console.log(response.data.ballot)
        if(response.data.result == 'success'){
          this.formState.ID = response.data.ID
          this.formState.data = response.data.ballot
        }
        if(response.data.result == 'error3'){
          this.formState.ID = response.data.ID
          this.formState.data = response.data.ballot
           message.destroy()
           message.warning('投票项目还没有投票信息')
          //  this.reload()
        }
        if(response.data.result == 'error1'){
           message.destroy()
           message.error('请检查登录')
        }
         if(response.data.result == 'error2'){
           message.destroy()
           message.error('没有找到对应投票项目')
           this.formState.ID = ''
          this.formState.data =[]
        }
      })
    },
  }

});

</script>

<style lang="less">
.ant-pro-page-header-search {
  text-align: center;
  margin-bottom: 16px;
}
.step-form-style-desc {
  padding: 0 56px;
  color: rgba(0,0,0,.45);

  h3 {
    margin: 0 0 12px;
    color: rgba(0,0,0,.45);
    font-size: 17px;
    line-height: 32px;
  }

  h4 {
    margin: 0 0 4px;
    color: rgba(0,0,0,.45);
    font-size: 15px;
    line-height: 22px;
  }

  p {
    margin-top: 0;
    margin-bottom: 12px;
    line-height: 22px;
  }
}
</style>
