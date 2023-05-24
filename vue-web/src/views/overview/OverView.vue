<template>
	<div style="margin:0 0 20px;">
		<!-- Counter Widgets -->
		<a-row :gutter="24" justify="space-around" align="middle">
			<a-col :span="24" :lg="12" :xl="6" class="mb-24" v-for="(stat, index) in stats" :key="index">
				<!-- Widget 1 Card -->
				<WidgetCounter :title="stat.title" :value="stat.value" :prefix="stat.prefix" :suffix="stat.suffix"
					:icon="stat.icon" :status="stat.status"></WidgetCounter>
				<!-- / Widget 1 Card -->
			</a-col>
			<a-col :span="24" :lg="12" :xl="6" class="mb-24">
				<a-card :bordered="false" class="widget-3">
					<a-statistic title="投票合约地址" :value=address>
					</a-statistic>
					<div class="icon" v-html="icon"></div>
				</a-card>
			</a-col>
		</a-row>
		<!-- / Counter Widgets -->

		<a-row :gutter="24" type="flex" justify="space-around" align="stretch">
			<a-col :span="24" :xl="14" class="mb-24">

				<!-- Information Card 1 -->
				<a-card :bordered="false" class="card-info">
					<a-row type="flex">
						<a-col class="col-content" :span="24" :xl="15">
							<div class="card-content">
								<h6>区块链可信投票平台</h6>
								<h5>为投票活动提供公开透明环境</h5>
								<p>智能合约自动化执行投票流程</p>
								<p>链上可靠公开存储选票</p>
								<p>链上信息不可篡改、自主访问可验证</p>
								<p>去中心化、分布式投票信任</p>
							</div>
							<div class="card-footer">
								<a href="#" size="small">
									<span>
										<router-link to="/support">了解更多</router-link>
									</span>
									<svg width="16" height="16" viewBox="0 0 20 20" fill="none"
										xmlns="http://www.w3.org/2000/svg">
										<path fill-rule="evenodd" clip-rule="evenodd"
											d="M7.29289 14.7071C6.90237 14.3166 6.90237 13.6834 7.29289 13.2929L10.5858 10L7.29289 6.70711C6.90237 6.31658 6.90237 5.68342 7.29289 5.29289C7.68342 4.90237 8.31658 4.90237 8.70711 5.29289L12.7071 9.29289C13.0976 9.68342 13.0976 10.3166 12.7071 10.7071L8.70711 14.7071C8.31658 15.0976 7.68342 15.0976 7.29289 14.7071Z"
											fill="#111827" />
									</svg>
								</a>
							</div>
						</a-col>
						<a-col class="col-img" :span="24" :xl="1">
							<div class="card-img-bg">
								<img src="images/info-card-1.jpg" alt="">
							</div>
						</a-col>
					</a-row>
				</a-card>
				<!-- / Information Card 1 -->

			</a-col>
			<a-col :span="24" :xl="10" class="mb-24">

				<!-- Information Card 2 -->
				<a-card :bordered="false" class="card-info-2 h-full">
					<div class="col-content h-full" style="background-image: url('images/info-card-2.jpg')">
						<div class="card-content">
							<h5>投票隐私保护</h5>
							<h6>结合投票场景，特别设计密码学方案实现安全电子投票</h6>
							<p>支持投票匿名性、完整性和可验证性</p>
							<p>提供投票流程中立性、公平性和正确性</p>
						</div>
						<div class="card-footer">
							<a href="#" size="small">
								<span>
									<router-link to="/support">了解更多</router-link>
								</span>
								<svg width="16" height="16" viewBox="0 0 20 20" fill="none"
									xmlns="http://www.w3.org/2000/svg">
									<path fill-rule="evenodd" clip-rule="evenodd"
										d="M7.29289 14.7071C6.90237 14.3166 6.90237 13.6834 7.29289 13.2929L10.5858 10L7.29289 6.70711C6.90237 6.31658 6.90237 5.68342 7.29289 5.29289C7.68342 4.90237 8.31658 4.90237 8.70711 5.29289L12.7071 9.29289C13.0976 9.68342 13.0976 10.3166 12.7071 10.7071L8.70711 14.7071C8.31658 15.0976 7.68342 15.0976 7.29289 14.7071Z"
										fill="#111827" />
								</svg>
							</a>
						</div>
					</div>
				</a-card>
				<!-- / Information Card 2 -->

			</a-col>
		</a-row>

		<a-card :bordered="false" class="header-solid h-full mb-24" :bodyStyle="{ paddingTop: '14px' }">
			<template #title>
				<h6 class="font-semibold">安全的投票项目</h6>
				<p>支持不同场景下的投票活动</p>
			</template>

			<a-row type="flex" :gutter="[24, 24]" align="stretch">

				<!-- Project Column -->
				<a-col :span="24" :lg="12" :xl="8" v-for="(project, index) in projects" :key="index">
					<CardProject :id="project.id" :title="project.title" :content="project.content"
						:cover="project.cover" :team="project.team"></CardProject>
					<a-col :span="12">
						<a-button size="small" v-if="index == 0">
							<router-link to="/avec">发起项目投票</router-link>
						</a-button>
						<a-button size="small" v-else>
							<router-link to="/we">发起项目投票</router-link>
						</a-button>
					</a-col>
				</a-col>
				<!-- / Project Column -->

				<!-- Project Column -->
				<a-col :span="24" :lg="12" :xl="8">

					<!-- Project Upload Component -->
					<a-upload name="avatar" list-type="picture-card" class="projects-uploader" :show-upload-list="false"
						:disabled="true">
						<img v-if="false" src="" alt="avatar" />
						<div v-else>
							<a-icon v-if="false" type="loading" />
							<svg v-else width="20" height="20" viewBox="0 0 20 20" fill="none"
								xmlns="http://www.w3.org/2000/svg">
								<path fill-rule="evenodd" clip-rule="evenodd"
									d="M3 17C3 16.4477 3.44772 16 4 16H16C16.5523 16 17 16.4477 17 17C17 17.5523 16.5523 18 16 18H4C3.44772 18 3 17.5523 3 17ZM6.29289 6.70711C5.90237 6.31658 5.90237 5.68342 6.29289 5.29289L9.29289 2.29289C9.48043 2.10536 9.73478 2 10 2C10.2652 2 10.5196 2.10536 10.7071 2.29289L13.7071 5.29289C14.0976 5.68342 14.0976 6.31658 13.7071 6.70711C13.3166 7.09763 12.6834 7.09763 12.2929 6.70711L11 5.41421L11 13C11 13.5523 10.5523 14 10 14C9.44771 14 9 13.5523 9 13L9 5.41421L7.70711 6.70711C7.31658 7.09763 6.68342 7.09763 6.29289 6.70711Z"
									fill="#111827" />
							</svg>

							<div class="ant-upload-text font-semibold text-dark">
								更多投票项目待推出 ...
							</div>
						</div>
					</a-upload>
					<!-- / Project Upload Component -->

				</a-col>
				<!-- / Project Column -->

			</a-row>
		</a-card>

	</div>
</template>

<script>
// Counter Widgets
import WidgetCounter from './WidgetCounter.vue';
import CardProject from './CardProject.vue'

// Counter Widgets stats
const stats = [
	{
		title: "区块高度",
		value: 53,
		// prefix: "$",
		suffix: "+10%",
		icon: `
						<svg width="22" height="22" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
							<path d="M8.43338 7.41784C8.58818 7.31464 8.77939 7.2224 9 7.15101L9.00001 8.84899C8.77939 8.7776 8.58818 8.68536 8.43338 8.58216C8.06927 8.33942 8 8.1139 8 8C8 7.8861 8.06927 7.66058 8.43338 7.41784Z" fill="#111827"/>
							<path d="M11 12.849L11 11.151C11.2206 11.2224 11.4118 11.3146 11.5666 11.4178C11.9308 11.6606 12 11.8861 12 12C12 12.1139 11.9308 12.3394 11.5666 12.5822C11.4118 12.6854 11.2206 12.7776 11 12.849Z" fill="#111827"/>
							<path fill-rule="evenodd" clip-rule="evenodd" d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18ZM11 5C11 4.44772 10.5523 4 10 4C9.44772 4 9 4.44772 9 5V5.09199C8.3784 5.20873 7.80348 5.43407 7.32398 5.75374C6.6023 6.23485 6 7.00933 6 8C6 8.99067 6.6023 9.76515 7.32398 10.2463C7.80348 10.5659 8.37841 10.7913 9.00001 10.908L9.00002 12.8492C8.60902 12.7223 8.31917 12.5319 8.15667 12.3446C7.79471 11.9275 7.16313 11.8827 6.74599 12.2447C6.32885 12.6067 6.28411 13.2382 6.64607 13.6554C7.20855 14.3036 8.05956 14.7308 9 14.9076L9 15C8.99999 15.5523 9.44769 16 9.99998 16C10.5523 16 11 15.5523 11 15L11 14.908C11.6216 14.7913 12.1965 14.5659 12.676 14.2463C13.3977 13.7651 14 12.9907 14 12C14 11.0093 13.3977 10.2348 12.676 9.75373C12.1965 9.43407 11.6216 9.20873 11 9.09199L11 7.15075C11.391 7.27771 11.6808 7.4681 11.8434 7.65538C12.2053 8.07252 12.8369 8.11726 13.254 7.7553C13.6712 7.39335 13.7159 6.76176 13.354 6.34462C12.7915 5.69637 11.9405 5.26915 11 5.09236V5Z" fill="#111827"/>
						</svg>`,
	},
	{
		title: "链上投票活动",
		value: 120,
		prefix: "+",
		// status: "danger
		suffix: "+20%",
		icon: `
						<svg width="22" height="22" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
							<path fill-rule="evenodd" clip-rule="evenodd" d="M3.17157 5.17157C4.73367 3.60948 7.26633 3.60948 8.82843 5.17157L10 6.34315L11.1716 5.17157C12.7337 3.60948 15.2663 3.60948 16.8284 5.17157C18.3905 6.73367 18.3905 9.26633 16.8284 10.8284L10 17.6569L3.17157 10.8284C1.60948 9.26633 1.60948 6.73367 3.17157 5.17157Z" fill="#111827"/>
						</svg>`,
	},
	{
		title: "活跃用户数量",
		value: 32,
		suffix: "+20%",
		icon: `
						<svg width="22" height="22" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
							<path d="M9 6C9 7.65685 7.65685 9 6 9C4.34315 9 3 7.65685 3 6C3 4.34315 4.34315 3 6 3C7.65685 3 9 4.34315 9 6Z" fill="#111827"/>
							<path d="M17 6C17 7.65685 15.6569 9 14 9C12.3431 9 11 7.65685 11 6C11 4.34315 12.3431 3 14 3C15.6569 3 17 4.34315 17 6Z" fill="#111827"/>
							<path d="M12.9291 17C12.9758 16.6734 13 16.3395 13 16C13 14.3648 12.4393 12.8606 11.4998 11.6691C12.2352 11.2435 13.0892 11 14 11C16.7614 11 19 13.2386 19 16V17H12.9291Z" fill="#111827"/>
							<path d="M6 11C8.76142 11 11 13.2386 11 16V17H1V16C1 13.2386 3.23858 11 6 11Z" fill="#111827"/>
						</svg>`,
	},
];
const address = "0xdca85f5f7a4fc8742495cd263ee12b8122e2dd1c"

const projects = [
	{
		id: 1,
		title: "匿名灵活投票",
		content: "提供定制安全投票活动，满足一般性投票场景需求。",
		cover: "images/avec.jpg",

	},
	{
		id: 2,
		title: "匿名权重投票",
		content: "支持不同决策权重场景下的投票活动",
		cover: "images/we.jpg",
	},
];
export default ({
	components: {
		WidgetCounter,
		CardProject
	},
	data() {
		return {
			stats,
			address,
			projects
		}
	},
})

</script>

<style lang="scss">

</style>