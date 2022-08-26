<template>
	<div class="letters">
		<div class="letters__container">
			<div v-for='(lettersContainer, containerIndex) in letters' :key='"c" + containerIndex' class="letters__block letters__block__letter" :data-letters="lettersContainer.length">
				<p v-for='(letter, index) in lettersContainer' :key='"cc" + index' class="letters__description__letter" v-html='letter'></p>
			</div>

			<div class="letters__block letters__block__description">
				<p class="letters__description letters__description__text">
					{{ $t('lettersDescription') }}
				</p>
			</div>

			<div v-for='(symbolContainer, symbolIndex) in symbols' :key='"s" + symbolIndex' class="letters__block letters__block__letter" :data-letters="symbolContainer.length">
				<p v-for='(symbol, index) in symbolContainer' :key='"ss" + index' class="letters__description__letter" v-html='symbol'></p>
			</div>

		</div>
	</div>
</template>


<script>
export default {
	name: 'letters',
	data() {
		return {
			letters: [
				['q', '&gt;', 'w', 'e', 'r', '1', 't', 'y', '6', 'a', 'w'],
				['2', '&gt;', '*', 'e', '$', ':', 'e'],
				['r', '#', 'w', '9', '(', 'r', ')', 'l', 'y', '3', '8', 't', '&gt;'],
				['#', 's', 'w', '5', 'n', '.', 't', 'd', '|', 'a', '+', 'z', '10', 'a'],
				['q', '&gt;', 'w', 'e', 'r', '1', 't', 'y', '6', 'a', 'r'],
				['2', '&gt;', '*', 'e', '$', ':', 'e', '$', ':', 'e'],
				['r', '#', 'w', '9', '(', 'r', ')', 'l', 'y', '3', '8', 't', 'l'],
				['#', 's', 'w', '5', 'n', '.', 't', 'd', '|', 'a', '+', 'z', '10', 'e'],
				['q', '&gt;', 'w', 'e', 'r', '1', 't', 'y', '6', 'a', 's'],
				['2', '&gt;', '*', 'e', '$', ':', 'e', '$', ':', 't'],
				['r', '#', 'w', '9', '(', 'r', ')', 'l', 'y', '3', '8', 't', 'r'],
				['#', 's', 'w', '5', 'n', '.', 't', 'd', '|', 'a', '+', 'z', '10', 'o'],
			],
			symbols: [
				['r', '#', 'w', '9', '(', 'r', ')', 'l', 'y', '3', '8', 't', '&#8765;'],
				['#', 's', 'w', '5', 'n', '.', 't', 'd', '|', 'a', '+', 'z', '10', '&asymp;'],
			]
		}
	},
	mounted(){
		document.querySelectorAll('.letters__block__letter').forEach( element => {
			setTimeout( function() {
				element.classList.add('is_active');
			}, 100)
		})
	}
}
</script>


<style lang="scss">
</style>
