<template>
  <a-result status="404" title="404" sub-title="错误了！该页面不存在，请返回主页！">
    <template #extra>
      <a-button type="primary"><router-link to='/'>回到主页</router-link></a-button>
    </template>
  </a-result>
</template>