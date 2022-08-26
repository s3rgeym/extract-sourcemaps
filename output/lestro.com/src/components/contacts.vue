<template>

  <footer id="myDIV" class="contacts" :class='{is_opened: opened}'>
<iframe src="https://snazzymaps.com/embed/188717" width="100%" height="100%" style="border:none;"></iframe>
<div class="overlay"></div>
		<div class="container">

			<div class="contacts__container">
				<div class="contacts__title-wr">
					<h2 class="contacts__title">{{ $t('contactsTitle') }}<span>— close to you</span></h2>
				</div>
				
				<div class="contacts__adress">
					<p v-html="$t('contactsAddress')">
					</p>
				</div>
				<div class="contacts__contact">
					<p> T:
						<a href="tel:+380674366677">+380 (67) 436 66 77</a>
					</p>
					<p> E:
						<a href="mailto:hi@lestro.com">hi@lestro.com</a>
					</p>
				</div>
			</div>
		</div>
  </footer>
</template>

<script>

import {EventBus} from '../EventBus.js';

export default {
  name: 'contacts',
	components: {
	},
  data() {
		return {
			opened: false
		}
	},
	created() {
		EventBus.$on('contacts-button-event', event => {
			this.opened = event.status;
		});
	}
}


</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
</style>
