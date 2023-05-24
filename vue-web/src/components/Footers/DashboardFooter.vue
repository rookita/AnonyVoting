<template>

	<!-- Layout Footer -->
	<a-layout-footer>
		<a-row type="flex">
			<a-col :span="24" :md="12">

				<!-- Footer Copyright Notice -->
				<p class="copyright">
					© 2022 <a href="/">AnonyVote</a> for a credible e-voting web.
				</p>
				<!-- / Footer Copyright Notice -->

			</a-col>
			<a-col :span="24" :md="12" class="footer-control">

				<!-- Footer Navigation Menu -->
				<a-menu mode="horizontal" style="float: right;text">
					<a-menu-item key="1">
						<router-link to="/" />主页
					</a-menu-item>
					<a-menu-item key="2">
						<router-link to="/introAvec" />产品介绍
					</a-menu-item>
					<a-menu-item key="3">
						<router-link to="/support" />技术支持
					</a-menu-item>
					<a-menu-item key="4">
						<router-link to="/about" />操作指南
					</a-menu-item>
					<a-menu-item key="5">
						<router-link to="/contact" />联系我们
					</a-menu-item>
				</a-menu>
				<!-- / Footer Navigation Menu -->

			</a-col>
		</a-row>
	</a-layout-footer>
	<!-- / Layout Footer -->

</template>

<script>


</script>
