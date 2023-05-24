<template>

	<!-- Main Sidebar -->
	<a-layout-sider collapsible class="sider-primary" breakpoint="lg" collapsed-width="0" width="250px"
		:collapsed="sidebarCollapsed" @collapse="$emit('toggleSidebar', ! sidebarCollapsed)" :trigger="null"
		:class="['ant-layout-sider-' + sidebarColor, 'ant-layout-sider-' + sidebarTheme]" theme="light"
		:style="{ backgroundColor: 'transparent', }">
		<div class="brand"><img alt=""> <span style="font-size: 17px;">
				<router-link to="/overview" style="color: rgba(0, 0, 0, 0.85);">区块链投票AnonyVote</router-link>
			</span></div>
		<hr>


		<!-- Sidebar Navigation Menu -->
		<a-menu theme="light" mode="inline">
			<a-menu-item class="ant-menu-item" key="1">
				<router-link to="/overview">
					<span class="icon">
						<svg width="20" height="20" fill="none" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
							<path
								d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z">
							</path>
						</svg>
					</span>
					<span class="label">使用指南</span>
				</router-link>
			</a-menu-item>

			<a-menu-item class="menu-item-header" key="2">
				投票项目
			</a-menu-item>

			<a-menu-item key="3">
				<router-link to="/avec">
					<span class="icon">
						<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
							<path
								d="M9 2C8.44772 2 8 2.44772 8 3C8 3.55228 8.44772 4 9 4H11C11.5523 4 12 3.55228 12 3C12 2.44772 11.5523 2 11 2H9Z"
								fill="#111827" />
							<path fill-rule="evenodd" clip-rule="evenodd"
								d="M4 5C4 3.89543 4.89543 3 6 3C6 4.65685 7.34315 6 9 6H11C12.6569 6 14 4.65685 14 3C15.1046 3 16 3.89543 16 5V16C16 17.1046 15.1046 18 14 18H6C4.89543 18 4 17.1046 4 16V5ZM7 9C6.44772 9 6 9.44772 6 10C6 10.5523 6.44772 11 7 11H7.01C7.56228 11 8.01 10.5523 8.01 10C8.01 9.44772 7.56228 9 7.01 9H7ZM10 9C9.44772 9 9 9.44772 9 10C9 10.5523 9.44772 11 10 11H13C13.5523 11 14 10.5523 14 10C14 9.44772 13.5523 9 13 9H10ZM7 13C6.44772 13 6 13.4477 6 14C6 14.5523 6.44772 15 7 15H7.01C7.56228 15 8.01 14.5523 8.01 14C8.01 13.4477 7.56228 13 7.01 13H7ZM10 13C9.44772 13 9 13.4477 9 14C9 14.5523 9.44772 15 10 15H13C13.5523 15 14 14.5523 14 14C14 13.4477 13.5523 13 13 13H10Z"
								fill="#111827" />
						</svg>
					</span>
					<span class="label">匿名灵活投票</span>
				</router-link>
			</a-menu-item>



			<a-menu-item key="4">
				<router-link to="/we">
					<span class="icon">
						<svg width="20" height="20" class="w-6 h-6" fill="none" viewBox="0 0 24 24"
							xmlns="http://www.w3.org/2000/svg">
							<path d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4">
							</path>
						</svg>
					</span>
					<span class="label">匿名权重投票</span>
				</router-link>
			</a-menu-item>

			<a-menu-item class="menu-item-header">
				投票信息
			</a-menu-item>

			<a-menu-item>
				<router-link to="/addvoting">
					<span class="icon">
						<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
							<path fill-rule="evenodd" clip-rule="evenodd"
								d="M6 2C5.44772 2 5 2.44772 5 3V4H4C2.89543 4 2 4.89543 2 6V16C2 17.1046 2.89543 18 4 18H16C17.1046 18 18 17.1046 18 16V6C18 4.89543 17.1046 4 16 4H15V3C15 2.44772 14.5523 2 14 2C13.4477 2 13 2.44772 13 3V4H7V3C7 2.44772 6.55228 2 6 2ZM6 7C5.44772 7 5 7.44772 5 8C5 8.55228 5.44772 9 6 9H14C14.5523 9 15 8.55228 15 8C15 7.44772 14.5523 7 14 7H6Z"
								fill="#111827" />
						</svg>
					</span>
					<span class="label">加入投票</span>
				</router-link>
			</a-menu-item>

			<a-menu-item>
				<router-link to="/voting">
					<span class="icon">
						<svg width="14px" height="14px" viewBox="0 0 14 14" version="1.1"
							xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
							<title>duplicate</title>
							<g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
								<g id="Tables" transform="translate(-58.000000, -507.000000)" fill="#BFBFBF"
									fill-rule="nonzero">
									<g id="sidebar" transform="translate(33.000000, 43.000000)">
										<g id="sign-up" transform="translate(16.000000, 455.000000)">
											<g id="duplicate" transform="translate(9.000000, 9.000000)">
												<path
													d="M4,6 C4,4.89543 4.89543,4 6,4 L12,4 C13.1046,4 14,4.89543 14,6 L14,12 C14,13.1046 13.1046,14 12,14 L6,14 C4.89543,14 4,13.1046 4,12 L4,6 Z"
													id="Path"></path>
												<path
													d="M2,0 C0.89543,0 0,0.89543 0,2 L0,8 C0,9.1046 0.89543,10 2,10 L2,4 C2,2.8954305 2.8954305,2 4,2 L10,2 L10,2 C10,0.89543 9.1046,0 8,0 L2,0 Z"
													id="Path"></path>
											</g>
										</g>
									</g>
								</g>
							</g>
						</svg>
					</span>
					<span class="label">开始投票</span>
				</router-link>
			</a-menu-item>

			<a-menu-item>
				<router-link to="/result">
					<span class="icon">
						<svg width="14px" height="14px" viewBox="0 0 14 14" version="1.1"
							xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
							<title>duplicate</title>
							<g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
								<g id="Tables" transform="translate(-58.000000, -507.000000)" fill="#BFBFBF"
									fill-rule="nonzero">
									<g id="sidebar" transform="translate(33.000000, 43.000000)">
										<g id="sign-up" transform="translate(16.000000, 455.000000)">
											<g id="duplicate" transform="translate(9.000000, 9.000000)">
												<path
													d="M4,6 C4,4.89543 4.89543,4 6,4 L12,4 C13.1046,4 14,4.89543 14,6 L14,12 C14,13.1046 13.1046,14 12,14 L6,14 C4.89543,14 4,13.1046 4,12 L4,6 Z"
													id="Path"></path>
												<path
													d="M2,0 C0.89543,0 0,0.89543 0,2 L0,8 C0,9.1046 0.89543,10 2,10 L2,4 C2,2.8954305 2.8954305,2 4,2 L10,2 L10,2 C10,0.89543 9.1046,0 8,0 L2,0 Z"
													id="Path"></path>
											</g>
										</g>
									</g>
								</g>
							</g>
						</svg>
					</span>
					<span class="label">投票结果</span>
				</router-link>
			</a-menu-item>

			<a-menu-item class="menu-item-header">
				个人中心
			</a-menu-item>
			<a-menu-item>
				<router-link to="/userinfo">
					<span class="icon">
						<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
							<path fill-rule="evenodd" clip-rule="evenodd"
								d="M18 10C18 14.4183 14.4183 18 10 18C5.58172 18 2 14.4183 2 10C2 5.58172 5.58172 2 10 2C14.4183 2 18 5.58172 18 10ZM12 7C12 8.10457 11.1046 9 10 9C8.89543 9 8 8.10457 8 7C8 5.89543 8.89543 5 10 5C11.1046 5 12 5.89543 12 7ZM9.99993 11C7.98239 11 6.24394 12.195 5.45374 13.9157C6.55403 15.192 8.18265 16 9.99998 16C11.8173 16 13.4459 15.1921 14.5462 13.9158C13.756 12.195 12.0175 11 9.99993 11Z"
								fill="#111827" />
						</svg>
					</span>
					<span class="label">个人信息</span>
				</router-link>
			</a-menu-item>
		</a-menu>
		<!-- / Sidebar Navigation Menu -->

		<!-- Sidebar Footer -->
		<div class="aside-footer">
			<div class="footer-box">
				<span class="icon">
					<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
						<path
							d="M3 4C3 3.44772 3.44772 3 4 3H16C16.5523 3 17 3.44772 17 4V6C17 6.55228 16.5523 7 16 7H4C3.44772 7 3 6.55228 3 6V4Z"
							fill="#111827" />
						<path
							d="M3 10C3 9.44771 3.44772 9 4 9H10C10.5523 9 11 9.44771 11 10V16C11 16.5523 10.5523 17 10 17H4C3.44772 17 3 16.5523 3 16V10Z"
							fill="#111827" />
						<path
							d="M14 9C13.4477 9 13 9.44771 13 10V16C13 16.5523 13.4477 17 14 17H16C16.5523 17 17 16.5523 17 16V10C17 9.44771 16.5523 9 16 9H14Z"
							fill="#111827" />
					</svg>
				</span>
				<h6>更多信息：</h6>
				<p>loading...</p>

			</div>
		</div>
		<!-- / Sidebar Footer -->

		<a-button type="primary" block target="_blank">
			系统介绍页详情
		</a-button>

	</a-layout-sider>
	<!-- / Main Sidebar -->

</template>

<script>

export default ({
	props: {
		// Sidebar collapsed status.
		sidebarCollapsed: {
			type: Boolean,
			default: false,
		},

		// Main sidebar color.
		sidebarColor: {
			type: String,
			default: "primary",
		},

		// Main sidebar theme : light, white, dark.
		sidebarTheme: {
			type: String,
			default: "light",
		},
	},
	data() {
		return {
			sidebarCollapsedModel: this.sidebarCollapsed,
		}
	},
})

</script>


<style lang="less" scoped>
.ant-collapse-content-box {
	padding: 1px;
}
</style>