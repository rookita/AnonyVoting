<template>
    uid : {{formState.uid}} <br>
    username: {{formState.username}} <br>
    address: {{formState.address}} <br>
</template>

<script>
import { defineComponent, reactive } from 'vue';
import emitter from '@/utils/bus';

export default defineComponent({
    setup() {
        const formState = reactive({
            uid: sessionStorage.getItem('uid'),
            username: sessionStorage.getItem('user'),
            address: ''
        });
    
        return {
            formState,
        };
    },

    created(){
        emitter.on("search",msg=>{
        this.value = msg
        this.send()
        })
    },

    send(){
        this.$http.post('http://192.168.5.42:9999/get_userinfo',{})
    }


});


</script>