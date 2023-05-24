<template>
    <a-card :bordered="false" >
      <a-steps class="steps" :current="currentTab">
      <template #progressDot="{ index, status, prefixCls }">
        <a-popover>
          <template #content>
            <span>step {{ index }} status: {{ status }}</span>
          </template>
          <span :class="`${prefixCls}-icon-dot`" />
        </a-popover>
      </template>
      <a-step title="投票基本信息"  />
      <a-step title="投票定制信息"  />
      <a-step title="投票项目上链"  />
      <a-step title="完成" description="投票项目上链" />
    </a-steps>

      <div class="content">
        <StepOne v-show="currentTab === 0" @nextStep="nextStep"/>
        <StepTwo v-show="currentTab === 1" @nextStep="nextStep" @prevStep="prevStep"/>
        <StepThree v-show="currentTab === 2" @prevStep="prevStep" @nextStep="nextStep"/>
        <StepFour v-show = 'currentTab === 3'  @finish="finish"/>
      </div>
    </a-card>
    
  
</template>

<script>
import StepOne from './StepOne'
import StepTwo from './StepTwo'
import StepThree from './StepThree'
import StepFour from './StepFour.vue'


export default {
  name: 'StepForm',
  components: {
    StepOne,
    StepTwo,
    StepThree,
    StepFour
},
  data () {
    return {
      currentTab: 0,
    }
  },
  methods: {
    nextStep () {
      if (this.currentTab < 3) {
        this.currentTab += 1
      }
    },
    prevStep () {
      if (this.currentTab > 0) {
        this.currentTab -= 1
      }
    },
    finish () {
      this.currentTab = 0
    }
  }
}
</script>

<style lang="less" scoped>
.steps {
  max-width: 82%;
  margin: 16px auto;
}
</style>