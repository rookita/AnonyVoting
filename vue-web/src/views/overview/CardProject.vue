<template>

	<!-- Project Card -->
	<a-card class="card-project">
		<img
			slot="cover"
			alt="example"
			:src="cover"
		/>
		<div class="card-tag">投票项目 No.{{ id }}</div>
		<h5>{{ title }}</h5>
		<p>
			{{ content }}
		</p>
		<a-row type="flex" :gutter="6" class="card-footer" align="middle">
					
					</a-row>
	</a-card>
	<!-- / Project Card -->

</template>

<script>

	export default ({
		props: {
			id: {
				type: Number,
				required: true,
			},
			title: {
				type: String,
				default: "",
			},
			content: {
				type: String,
				default: "",
			},
			cover: {
				type: String,
				default: "",
			},
			
		},
		data() {
			return {
			}
		},
	})

</script>