<template>

  <a-row :gutter="24" type="flex">
    <!-- Table -->
    <a-col :span="24" :lg="24" class="mb-24">

      <!-- Projects Table Card -->
      <a-card :bordered="false" class="h-full">
        <a-steps class="steps" :current="currentTab">
          <template #progressDot="{ index, status, prefixCls }">
            <a-popover>
              <template #content>
                <span>step {{ index }} status: {{ status }}</span>
              </template>
              <span :class="`${prefixCls}-icon-dot`" />
            </a-popover>
          </template>
          <a-step title="投票基本信息" />
          <a-step title="投票定制信息" />
          <a-step title="投票项目上链" />
          <a-step title="完成" />
        </a-steps>

        <div class="content">
          <StepOne v-show="currentTab === 0" @nextStep="nextStep" />
          <StepTwo v-show="currentTab === 1" @nextStep="nextStep" @prevStep="prevStep" />
          <StepThree v-show="currentTab === 2" @prevStep="prevStep" @nextStep="nextStep" />
          <StepFour v-show='currentTab === 3' @finish="finish" />
        </div>
      </a-card>
      <!-- / Projects Table Card -->

    </a-col>
    <!-- / Table -->

    <!-- Timeline -->
    <!-- <a-col :span="24" :lg="5" class="mb-24">

      <LogHistory></LogHistory>

			</a-col> -->
    <!-- / Timeline -->
  </a-row>
  <!-- / Table & Timeline -->

</template>

<script>
import StepOne from './StepOne'
import StepTwo from './StepTwo'
import StepThree from './StepThree'
import StepFour from './StepFour.vue'
import LogHistory from './LogHistory.vue'


export default {
  name: 'StepForm',
  components: {
    StepOne,
    StepTwo,
    StepThree,
    StepFour,
    LogHistory
  },
  data() {
    return {
      currentTab: 0,
      // form
      form: null,
      title: ''
    }
  },
  methods: {
    nextStep() {
      if (this.currentTab < 3) {
        this.currentTab += 1
      }
    },
    prevStep() {
      if (this.currentTab > 0) {
        this.currentTab -= 1
      }
    },
    finish() {
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