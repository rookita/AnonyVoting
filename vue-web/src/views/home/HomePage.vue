<template>
  <div class="relative pt-16 pb-32 flex content-center items-center justify-center min-h-screen-75">
    <div class="absolute top-0 w-full h-full bg-center bg-cover" v-bind:style="{ 'background-image': 'url(' + back + ')' }">
      <span id="blackOverlay" class="w-full h-full absolute opacity-75 bg-black"></span>
    </div>
    <div class="container relative mx-auto">
      <div class="items-center flex flex-wrap">
        <div class="w-full lg:w-6/12 px-4 ml-auto mr-auto text-center">
          <div class="pr-">
            <h1 class="text-white font-semibold text-4xl ">
              区块链&电子投票
            </h1>
            <p class="mt-4 text-xl text-blueGray-300">
              围绕区块链技术应用，打造电子投票活动全方位安全保护。
            </p>
            <div class="mt-12">
              <router-link to="/introAvec" type="button" style="background-color:#3498db ;"
                class="get-started text-white font-bold px-7 py-3 rounded outline-none focus:outline-none mr-1 mb-1 bg-emerald-500 active:bg-emerald-600 uppercase text-lg shadow hover:shadow-lg ease-linear transition-all duration-150">
                查看产品
              </router-link>
              <router-link to="/overview" style="background-color:#fafafa ;"
                class="github-star ml-1 text-blue font-bold px-7 py-3 rounded outline-none focus:outline-none mr-1 mb-1 bg-blueGray-700 active:bg-blueGray-600 uppercase text-lg shadow hover:shadow-lg ease-linear transition-all duration-150"
                type="button">
                开始投票
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="top-auto bottom-0 left-0 right-0 w-full absolute pointer-events-none overflow-hidden h-70-px"
      style="transform: translateZ(0);">
      <svg class="absolute bottom-0 overflow-hidden" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none"
        version="1.1" viewBox="0 0 2560 100" x="0" y="0">
        <polygon class="text-blueGray-200 fill-current" points="2560 0 2560 100 0 100"></polygon>
      </svg>
    </div>
  </div>

  <section class="pb-32 bg-blueGray-200 -mt-24">
    <div class="container mx-auto px-4">
      <div class="flex flex-wrap">
        <div class="lg:pt-12 pt-6 w-full md:w-4/12 px-4 text-center">
          <div class="relative flex flex-col min-w-0 break-words bg-white w-full mb-8 shadow-lg rounded-lg">
            <div class="px-4 py-5 flex-auto">
              <div
                class="text-white p-3 text-center inline-flex items-center justify-center w-12 h-12 mb-5 shadow-lg rounded-full bg-emerald-500">
                <i class="far fa-envelope-open"></i>
              </div>
              <h6 class="text-xl font-semibold">透明</h6>
              <p class="mt-4 mb-2 text-blueGray-500 text-lg">
                区块链技术公开透明可访问性使得与投票相关的一切活动均有迹可循，为投票决策过程不断增进信任。
              </p>
            </div>
          </div>
        </div>

        <div class="w-full md:w-4/12 px-4 text-center">
          <div class="relative flex flex-col min-w-0 break-words bg-white w-full mb-8 shadow-lg rounded-lg">
            <div class="px-4 py-5 flex-auto">
              <div
                class="text-white p-3 text-center inline-flex items-center justify-center w-12 h-12 mb-5 shadow-lg rounded-full bg-lightBlue-500">
                <i class="fas fa-shield-alt"></i>
              </div>
              <h6 class="text-xl font-semibold">安全</h6>
              <p class="mt-4 mb-2 text-blueGray-500 text-lg">
                巧妙设计的密码学方案充分保证投票隐私信息的保密。在满足电子投票主要功能的同时，提供强大的安全措施
              </p>
            </div>
          </div>
        </div>

        <div class="pt-6 w-full md:w-4/12 px-4 text-center">
          <div class="relative flex flex-col min-w-0 break-words bg-white w-full mb-8 shadow-lg rounded-lg">
            <div class="px-4 py-5 flex-auto">
              <div
                class="text-white p-3 text-center inline-flex items-center justify-center w-12 h-12 mb-5 shadow-lg rounded-full bg-orange-500">
                <i class="fas fa-project-diagram"></i>
              </div>
              <h6 class="text-xl font-semibold">高效</h6>
              <p class="mt-4 mb-4 text-blueGray-500 text-lg">
                保证投票透明、安全的前提下，从人工计票升级到电子在线投票，支持各种设备访问在线投票平台。
              </p>
            </div>
          </div>
        </div>
      </div>





      <div class="flex flex-wrap items-center mt-48">
        <div class="relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-xl rounded-lg -mt-48">
          <div class="flex flex-wrap justify-center  bg-blueGray-200">
            <div class="w-full lg:w-8/12  lg:order-1">
              <div class="flex justify-center py-4 lg:pt-4 pt-8">
                <div class="mr-4 p-3 text-center md:w-4/12">
                  <span class="text-xl font-bold block uppercase tracking-wide text-blueGray-600">
                    22
                  </span>
                  <span class="text text-blueGray-500">区块高度</span>
                </div>
                <div class="mr-4 p-3 text-center md:w-4/12">
                  <span class="text-xl font-bold  uppercase tracking-wide text-blueGray-600">
                    100
                  </span>
                  <span class="text block text-blueGray-500">选票数量</span>
                </div>
                <div class="lg:mr-4 p-3 text-center md:w-4/12">
                  <span class="text-xl font-bold block uppercase tracking-wide text-blueGray-600">
                    89
                  </span>
                  <span class="text text-blueGray-500">用户量</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="w-full md:w-5/12 px-4  ml-auto">
          <div
            class="text-blueGray-500 p-3 text-center inline-flex items-center justify-center w-12 h-12 mb-6 shadow-lg rounded-full bg-white">
            <i class="fab fa-hive"></i>
          </div>
          <h3 class="text-3xl mb-2 font-semibold leading-normal">
            区块链技术的运用
          </h3>
          <p class="text-lg leading-relaxed mt-4 mb-4 text-blueGray-600">
            区块链作为该在线电子投票平台的底层技术，在实现投票透明及信任方面取得了巨大突破。
          </p>
          <p class="text-lg  leading-relaxed mt-0 mb-4 text-blueGray-600">
            得益于区块链内在的不可篡改存储、分布式信任及公开可验证性质，相较于传统中心化电子投票系统取得强大的信赖。
          </p>
          <router-link to="/support" class="font-bold text-blueGray-700 mt-8">
            了解更多技术细节
          </router-link>
        </div>

        <div class="w-full md:w-4/12 px-4 mr-auto ml-auto">
          <div
            class="relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-lg rounded-lg bg-emerald-500"
            style="background-color:rgba(52, 152, 219,1) ;">
            <img alt="..." :src="blockchain" class="w-full h-full align-middle rounded-t-lg" />
            <blockquote class="relative p-8 mb-4">
              <svg preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 583 95"
                class="absolute left-0 w-full block h-95-px -top-94-px">
                <polygon points="-30,95 583,95 583,65" class="text-emerald-500 fill-current"></polygon>
              </svg>
              <h4 class="text-xl font-bold text-white">
                智能合约
              </h4>
              <p class="text-md font-light mt-2 text-white">
                运行在区块链上的自动化程序，自动化执行投票操作，推动投票进程的可信处理。
              </p>
            </blockquote>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="relative py-24 bg-white">
    <div class="bottom-auto top-0 left-0 right-0 w-full absolute pointer-events-none overflow-hidden -mt-20 h-20"
      style="transform: translateZ(0);">
      <svg class="absolute bottom-0 overflow-hidden" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none"
        version="1.1" viewBox="0 0 2560 100" x="0" y="0">
        <polygon class="text-white fill-current" points="2560 0 2560 100 0 100"></polygon>
      </svg>
    </div>

    <div class="container mx-auto px-4">
      <div class="items-center flex flex-wrap mx-auto px-4 lg:pt-20 lg:pb-48">

        <div class="w-full h-full md:w-5/12 ml-auto mr-auto px-2">
          <img alt="..." class="max-w-full max-h-full rounded-lg shadow-lg" :src="privacy" style="
                transform: scale(1) perspective(1040px) rotateY(11deg)
                  rotateX(-2deg) rotate(2deg);
              " />
        </div>
        <div class="w-full md:w-5/12 ml-auto mr-auto px-4">
          <div class="md:pr-12">
            <div
              class="text-blueGray-500 p-3 text-center inline-flex items-center justify-center w-12 h-12 mb-6 shadow-lg rounded-full bg-lightBlue">
              <i class="fas fa-lock"></i>
            </div>
            <h3 class="text-3xl font-semibold">密码学算法<router-link to="/support"
                class="font-bold text-sm pl-3 text-blueGray-700 mt-8">
                更多信息
              </router-link></h3>
            <p class="mt-4 text-lg leading-relaxed">
              巧妙设计密码学算法，充分保护选民隐私信息，实现安全电子投票平台。
            </p>


            <p class="mt-4 text-lg leading-relaxed">
              针对区块链公开透明所致安全隐私问题，结合不同投票场景提出相对应完整可靠的安全解决方案。经过不断安全分析验证能够满足以下投票安全要求。
            </p>
            <ul class="list-none mt-6">
              <li class="py-2">
                <div class="flex items-center">
                  <div>
                    <span
                      class="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-emerald-600 bg-emerald-200 mr-3">
                      <i class="fas fa-fingerprint"></i>
                    </span>
                  </div>
                  <div>
                    <h5 class="text-blueGray-500">
                      匿名性、完整性
                    </h5>
                  </div>
                </div>
              </li>
              <li class="py-2">
                <div class="flex items-center">
                  <div>
                    <span
                      class="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-emerald-600 bg-emerald-200 mr-3">
                      <i class="fab fa-html5"></i>
                    </span>
                  </div>
                  <div>
                    <h5 class="text-blueGray-500">
                      可验证性、中立性
                    </h5>
                  </div>
                </div>
              </li>
              <li class="py-2">
                <div class="flex items-center">
                  <div>
                    <span
                      class="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-emerald-600 bg-emerald-200 mr-3">
                      <i class="far fa-paper-plane"></i>
                    </span>
                  </div>
                  <div>
                    <h5 class="text-blueGray-500">公平性、正确性</h5>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="pt-20 pb-48 bg-blueGray-100">
    <div class="container mx-auto px-4 pb-20 pt-32">
      <div class="items-center flex flex-wrap">
        <div class="w-full md:w-6/12 ml-auto px-12 md:px-4">
          <div class="md:pr-12">
            <div
              class="text-blueGray-500 p-3 text-center inline-flex items-center justify-center w-12 h-12 mb-6 shadow-lg rounded-full bg-white">
              <i class="fas fa-rocket text-xl"></i>
            </div>
            <h3 class="text-3xl font-semibold">
              自主、高效投票
            </h3>
            <p class="mt-4 text-lg leading-relaxed">
              在线选举平台面向用户提供完全自主设计投票形式，支持各式设备访问并参与投票活动。相较于人工投票得到飞跃式的改进。
            </p>
            <p class="mt-4 text-lg leading-relaxed">
              一切操作均由底层区块链智能合约自动化完成，彻底摒弃第三方参与投票，用户即可自主掌握投票信息。
            </p>
            <p class="mt-4 text-lg leading-relaxed">
              目前版本所提供的的投票产品信息。
            </p>
            <ul class="list-none mt-6">
              <li class="py-2">
                <div class="flex items-center">
                  <div>
                    <span
                      class="text-lg font-semibold inline-block py-1 px-2 uppercase rounded-full text-blueGray-500 bg-blueGray-50 mr-3">
                      <i class="far fa-lightbulb"></i>
                    </span>
                  </div>
                  <div>
                    <h5 class="text-blueGray-500">
                      自主定制投票活动
                      <!-- <router-link to="/introAvec">匿名灵活投票</router-link> -->
                    </h5>
                  </div>
                </div>
              </li>

              <li class="py-2">
                <div class="flex items-center">
                  <div>
                    <span
                      class="text-lg font-semibold inline-block py-1 px-2 uppercase rounded-full text-blueGray-500 bg-blueGray-50 mr-1">
                      <i class="fas fa-balance-scale"></i>
                    </span>
                  </div>
                  <div>
                    <h5 class="text-blueGray-500">
                      即时掌握投票动态
                      <!-- <router-link to="/introWe">匿名权重投票</router-link> -->
                    </h5>
                  </div>
                </div>
              </li>

            </ul>
          </div>
        </div>

        <div class="w-full md:w-5/12 mr-auto px-4 pt-24 md:pt-0">
          <img alt="..." class="max-w-full rounded-lg shadow-xl" style="
                transform: scale(1) perspective(2040px) rotateY(-11deg)
                  rotateX(2deg) rotate(2deg);
              " :src="voting" />
        </div>
      </div>
    </div>
    <div class="justify-center text-center flex flex-wrap mt-48">
      <div class="w-full md:w-6/12 px-12 ">
        <h2 class="font-semibold text-4xl">产品信息</h2>
        <p class="text-xl leading-relaxed mt-6 md-0 text-blueGray-500">
          当前平台版本提供如下所示两款投票产品，分别为匿名灵活投票和匿名权重投票，请依据产品使用说明和应用场景做出合理的选择。
        </p>

      </div>
    </div>
  </section>

  <section class="block relative z-1 bg-blueGray-600 pt-0">
    <div class="container mx-auto">
      <div class="justify-center flex flex-wrap">
        <div class="w-full lg:w-12/12 px-7 -mt-24">
          <div class="flex flex-wrap">
            <div class="w-full lg:w-6/12 px-7">
              <h5 class="text-xl font-semibold pb-4 text-center">
                匿名灵活投票
              </h5>
              <router-link to="/introAvec">
                <div
                  class="hover:-mt-4 relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-lg rounded-lg ease-linear transition-all duration-150">
                  <img alt="..." class="align-middle border-none max-w-full h-auto rounded-lg" :src="avec" />
                </div>
              </router-link>
            </div>



            <div class="w-full lg:w-6/12 px-7">
              <h5 class="text-xl font-semibold pb-4 text-center">
                匿名权重投票
              </h5>
              <router-link to="/introWe">
                <div
                  class="hover:-mt-4 relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-lg rounded-lg ease-linear transition-all duration-150">
                  <img alt="..." class="align-middle border-none max-w-full h-auto rounded-lg" :src="we" />
                </div>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="py-20 bg-blueGray-600 overflow-hidden">
    <div class="container mx-auto pb-48">

    </div>
  </section>

  <section class="pb-16 relative pt-32 bg-blueGray-800">
    <!-- <div
        class="-mt-20 top-0 bottom-auto left-0 right-0 w-full absolute h-20"
        style="transform: translateZ(0);"
      >
        <svg
          class="absolute bottom-0 overflow-hidden"
          xmlns="http://www.w3.org/2000/svg"
          preserveAspectRatio="none"
          version="1.1"
          viewBox="0 0 2560 100"
          x="0"
          y="0"
        >
          <polygon
            class="text-blueGray-800 fill-current"
            points="2560 0 2560 100 0 100"
          ></polygon>
        </svg>
      </div> -->

    <!-- <div class="container mx-auto">
        <div
          class="flex flex-wrap justify-center bg-white shadow-xl rounded-lg -mt-64 py-16 px-7 relative z-10"
        >
          <div class="w-full text-center lg:w-8/12">
            <p class="text-4xl text-center">
              
            </p>
            <h3 class="font-semibold text-2xl">
              投票平台使用须知
            </h3>
            <p class="text-blueGray-500 text-lg leading-relaxed mt-4 mb-4">
              进一步了解投票结合区块链技术，请前往 <span class="text-base text-black font-bold">技术支持</span> 板块！
            </p>

            <p class="text-blueGray-500 text-lg leading-relaxed mt-4 mb-4">
              在此基础上探索更多产品相关介绍信息，请前往 
               <span class="text-base text-black font-bold">产品介绍</span> 板块！
            </p>

             <p class="text-blueGray-500 text-lg leading-relaxed mt-4 mb-4">
               如果您已掌握平台相关信息并着手应用，请浏览平台<span class="text-base text-black font-bold">操作指南</span>后前往投票模块。
            </p>
            
            <div class="sm:block flex flex-col mt-10 pt-6">
              <router-link to="/about"
               type="button"
                class="github-star  text-white font-bold px-7 py-2 rounded outline-none focus:outline-none mr-2 mb-1 bg-blueGray-700 active:bg-blueGray-600 uppercase text-lg shadow hover:shadow-lg ease-linear transition-all duration-150"
              >
                操作指南
              </router-link>

              <router-link to="/overview"
               type="button"
                class="get-started text-white font-bold px-7 py-2 rounded outline-none focus:outline-none mr-1 mb-1 bg-emerald-500 active:bg-emerald-600 uppercase text-lg shadow hover:shadow-lg ease-linear transition-all duration-150"
              >
                开始投票
              </router-link>
            </div>
            <div class="text-center mt-10"></div>
          </div>
        </div>
      </div> -->
  </section>


</template>

<script>

import back from "@/assets/img/back.jpg";
import blockchain from "@/assets/img/blockchain.jpg";
import privacy from "@/assets/img/privacy.jpg";
import voting from "@/assets/img/voting.jpg";
import avec from "@/assets/img/avec.jpg"
import we from "@/assets/img/we.jpg"

export default {
  name: "HomePage",
  data() {
    return {
      blockchain,
      back,
      privacy,
      voting,
      avec,
      we
    };
  },

}
</script>


