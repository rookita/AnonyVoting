import { createRouter, createWebHistory } from "vue-router";
import Layout from "@/layout/HomeNav.vue";
import HomeLayout from "@/layout/HomeLayout";
import UserLayout from "@/layout/UserLayout";
import { message } from "ant-design-vue";

const routes = [
    {
        path: '/',
        component: HomeLayout,
        redirect: '/home',
        children: [
            {
                path: '/home',
                component: () => import('@/views/home/HomePage.vue'),
                name: 'home',
                meta: {
                    title: '主页'
                }
            },
            {
                path: '/introAvec',
                component: () => import('@/views/home/IntroAvec.vue'),
                name: 'introAvec',
                meta: {
                    title: '介绍'
                }
            },

            {
                path: '/introWe',
                component: () => import('@/views/home/IntroWe.vue'),
                name: 'introWe',
                meta: {
                    title: '介绍'
                }
            },
            {
                path: '/support',
                component: () => import('@/views/home/supportPage.vue'),
                name: 'support',
                meta: {
                    title: '技术支持'
                }
            },
            {
                path: '/about',
                component: () => import('@/views/home/AboutPage.vue'),
                name: 'about',
                meta: {
                    title: '操作指南'
                }
            },
            {
                path: '/contact',
                component: () => import('@/views/home/ContactPage.vue'),
                name: 'contact',
                meta: {
                    title: '操作指南'
                }
            }
        ]
    },

    {
        path: '/login',
        component: UserLayout,
        children: [{
            path: '/login',
            component: () => import('@/views/user/LoginUser.vue'),
            name: 'login',
            meta: {
                title: '登录',
            }
        },

        {
            path: '/register',
            component: () => import('@/views/user/RegisterUser.vue'),
            name: 'register',
            meta: {
                title: '登录'
            }
        },
        ]
    },





    {
        path: '/init-voting',
        component: Layout,
        children: [
            {
                path: '/avec',
                component: () => import('@/views/InitVote/avec/initAvec/AVEC.vue'),
                name: 'avec',
                meta: {
                    title: '匿名灵活投票',
                    requiredLogin: true
                }
            },

            {
                path: '/we',
                component: () => import('@/views/InitVote/we/initWe/WE.vue'),
                name: 'we',
                meta: {
                    title: '匿名权重投票',
                    requiredLogin: true
                }
            },
        ]

    },

    {
        path: '/addvoting',
        component: Layout,
        children: [{
            path: '/addvoting',
            component: () => import('@/views/addvoting/AddVoting.vue'),
            name: 'addvoting',
            meta: {
                title: '加入投票',
                requiredLogin: true
            }
        },
        {
            path: '/addvotingwe',
            component: () => import('@/views/addwe/AddVoting.vue'),
            name: 'addvotingwe',
            meta: {
                title: '加入匿名权重投票',
                requiredLogin: true
            },
            beforeEnter: (to, from, next) => {
                //to是当用户点击进入当前页面的时候,我们可以进行一些拦截设置
                //from当来自其他页面进入当前页面的时候，我们也可以进行拦截提示用户

                if (from.name == 'addvoting') {
                    next()
                }
                else {
                    alert('我是匿名权重投票路由独享守卫！清先加入投票！')
                    router.push('/addvoting')
                }
            }
        },
        {
            path: '/addvotingavec',
            component: () => import('@/views/addavec/AddVoting.vue'),
            name: 'addvotingavec',
            meta: {
                title: '加入匿名灵活投票',
                requiredLogin: true
            },
            beforeEnter: (to, from, next) => {
                //to是当用户点击进入当前页面的时候,我们可以进行一些拦截设置
                //from当来自其他页面进入当前页面的时候，我们也可以进行拦截提示用户

                if (from.name == 'addvoting') {
                    next()
                }
                else {
                    alert('我是匿名灵活投票路由独享守卫！清先加入投票！')
                    router.push('/addvoting')
                }
            }
        },
        ]
    },

    {
        path: '/voting',
        component: Layout,
        children: [{
            path: '/voting',
            component: () => import('@/views/voting/AddVoting.vue'),
            name: 'voting',
            meta: {
                title: '开始投票',
                requiredLogin: true
            }
        },
        {
            path: '/votingwe',
            component: () => import('@/views/wevoting/AddVoting.vue'),
            name: 'votingwe',
            meta: {
                title: '开始匿名权重投票',
                requiredLogin: true
            },
            beforeEnter: (to, from, next) => {
                //to是当用户点击进入当前页面的时候,我们可以进行一些拦截设置
                //from当来自其他页面进入当前页面的时候，我们也可以进行拦截提示用户

                if (from.name == 'voting') {
                    next()
                }
                else {
                    alert('我是匿名权重投票路由独享守卫！清返回点击开始投票！')
                    router.push('/voting')
                }
            }
        },
        {
            path: '/votingavec',
            component: () => import('@/views/avecvoting/AddVoting.vue'),
            name: 'votingavec',
            meta: {
                title: '开始匿名灵活投票',
                requiredLogin: true
            },
            beforeEnter: (to, from, next) => {
                //to是当用户点击进入当前页面的时候,我们可以进行一些拦截设置
                //from当来自其他页面进入当前页面的时候，我们也可以进行拦截提示用户

                if (from.name == 'voting') {
                    next()
                }
                else {
                    alert('我是匿名灵活投票路由独享守卫！清返回点击开始投票！')
                    router.push('/voting')
                }
            }
        }
        ]
    },

    {
        path: '/overview',
        component: Layout,
        children: [{
            path: '/overview',
            component: () => import('@/views/overview/OverView.vue'),
            name: 'overview',
            meta: {
                title: '概览',
                requiredLogin: true
            }
        }
        ]
    },
    {
        path: '/result',
        component: Layout,
        children: [
            {
                path: '/result',
                component: () => import('@/views/getresult/GetResult.vue'),
                name: 'result',
                meta: {
                    title: '投票结果',
                    requiredLogin: true
                }
            },
            {
                path: '/resultwe',
                component: () => import('@/views/getWeresult/GetResult.vue'),
                name: 'resultwe',
                meta: {
                    title: '匿名权重投票结果',
                    requiredLogin: true
                },
                beforeEnter: (to, from, next) => {
                    //to是当用户点击进入当前页面的时候,我们可以进行一些拦截设置
                    //from当来自其他页面进入当前页面的时候，我们也可以进行拦截提示用户

                    if (from.name == 'result') {
                        next()
                    }
                    else {
                        alert('我是匿名灵活投票路由独享守卫！清返回点击投票结果！')
                        router.push('/result')
                    }
                }
            },
            {
                path: '/resultavec',
                component: () => import('@/views/getAvcresult/GetResult.vue'),
                name: 'resultavec',
                meta: {
                    title: '匿名灵活投票结果',
                    requiredLogin: true
                },
                beforeEnter: (to, from, next) => {
                    //to是当用户点击进入当前页面的时候,我们可以进行一些拦截设置
                    //from当来自其他页面进入当前页面的时候，我们也可以进行拦截提示用户

                    if (from.name == 'result') {
                        next()
                    }
                    else {
                        alert('我是匿名灵活投票路由独享守卫！清返回点击投票结果！')
                        router.push('/result')
                    }
                }
            },

            {
                path: '/avecresult',
                component: () => import('@/views/getAvcresult/StepFour.vue'),
                name: 'avecresult',
                meta: {
                    title: '匿名灵活投票结果',
                    requiredLogin: true
                },
                beforeEnter: (to, from, next) => {
                    //to是当用户点击进入当前页面的时候,我们可以进行一些拦截设置
                    //from当来自其他页面进入当前页面的时候，我们也可以进行拦截提示用户

                    if (from.name == 'result') {
                        next()
                    }
                    else {
                        alert('我是匿名灵活投票路由独享守卫！清返回点击投票结果！')
                        router.push('/result')
                    }
                }
            },

            {
                path: '/weresult',
                component: () => import('@/views/getWeresult/StepFour.vue'),
                name: 'weresult',
                meta: {
                    title: '匿名权重投票结果',
                    requiredLogin: true
                },
                beforeEnter: (to, from, next) => {
                    //to是当用户点击进入当前页面的时候,我们可以进行一些拦截设置
                    //from当来自其他页面进入当前页面的时候，我们也可以进行拦截提示用户

                    if (from.name == 'result') {
                        next()
                    }
                    else {
                        alert('我是匿名权重路由独享守卫！清返回点击投票结果！')
                        router.push('/result')
                    }
                }
            },


            // {
            //     path: '/voting-info',
            //     component: () => import('@/views/info/GetInfo.vue'),
            //     name: 'voting-info',
            //     meta: {
            //         title: '投票详情',
            //         requiredLogin: true
            //     }
            // }
        ]
    },

    {
        path: '/userinfo',
        component: Layout,
        children: [{
            path: '/userinfo',
            component: () => import('@/views/info/GetUserInfo.vue'),
            name: 'userinfo',
            meta: {
                title: '个人信息',
                requiredLogin: true
            }
        }
        ]
    },


    {
        path: '/404',
        name: 'NotFoundPage',
        component: () => import('@/views/PageNot.vue'),
    },
    {
        // will match everything
        path: '/:catchAll(.*)',
        redirect: '/404',
    },

]


const router = createRouter(
    {
        history: createWebHistory(),
        routes
    }
)


router.beforeEach((to, from, next) => {
    const requiredLogin = to.meta.requiredLogin
    // console.log(requiredLogin)
    let token = sessionStorage.getItem("token");

    if (requiredLogin) {
        if (token) {
            next();
        }
        else {
            message.warning("请完成登录！")
            next('/login')
        }
    }
    else {
        next()
    }
});
export default router