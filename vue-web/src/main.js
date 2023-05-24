import {createApp} from 'vue'
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';
import App from './App.vue'
import router from "./router";
import * as Icons from '@ant-design/icons-vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import './scss/app.scss';

// styles
import "@fortawesome/fontawesome-free/css/all.min.css";
// import "@/assets/styles/tailwind.css";

const app= createApp(App)
app.use(router).use(VueAxios, axios).use(Antd)
    .mount('#app')


for (const i in Icons) {
    app.component(i, Icons[i])
}