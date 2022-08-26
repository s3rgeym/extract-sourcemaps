<template>
	<header @mouseleave='leaveFromNavigation' class="navigation">
		
		<div class="navigation__wrapper">

			<a @click='closeContacts(); navigationTo(item.rel);' class="navigation__logo" :class='{white: hoveredWorks}' href="#hero">
				<img src="../assets/images/logo.svg" alt="logo" class="svg">
			</a>

			<nav class="navigation__nav" :class='{is_opened: burgerOpen}'>
				<ul class="navigation__nav__list js-navigation__list">

					<li :key='"nav" + 0' :id='0' @click='burgerClicked' @mouseenter='hoverOnNavElement' class="navigation__nav__item">
						<a @click='closeContacts(); navigationTo("hero");' class="active" data-menuanchor='hero' :href='"#hero"'>Lestro</a>
					</li>
					<li :key='"nav" + 1' :id='1' @click='burgerClicked' @mouseenter='hoverOnNavElement' class="navigation__nav__item">
						<a @click='closeContacts(); navigationTo("services");' data-menuanchor='services' :href='"#services"'>{{ $t('servicesTitle') }}</a>
					</li>
					<li :key='"nav" + 2' :id='2' @click='burgerClicked' @mouseenter='hoverOnNavElement' class="navigation__nav__item">
						<a @click='closeContacts(); navigationTo("works");' data-menuanchor='works' :href='"#works"'>{{ $t('worksTitle') }}</a>
					</li>
					<li :key='"nav" + 3' :id='3' @click='burgerClicked' @mouseenter='hoverOnNavElement' class="navigation__nav__item">
						<a @click='closeContacts(); navigationTo("partners");' data-menuanchor='partners' :href='"#partners"'>{{ $t('clientsTitle') }}</a>
					</li>
					
					<li :key='"nav" + 4' :id='4' @click='burgerClicked' @mouseenter='hoverOnNavElement' class="navigation__nav__item navigation__nav__item__contacts">
						<a @click='closeContacts(); navigationTo("contacts");' data-menuanchor='contacts' :href='"#contacts"'>{{ $t('contactsTitle') }}</a>
					</li>
					
				</ul>
			</nav>

			<div class="navigation__line line__yellow"></div>

			<div class="navigation__line line__sharp"></div>


		</div>

		<div @click='burgerClicked' class="navigation__burger" :class='{is_opened: burgerOpen, white: hoveredWorks}'>
			<div class="navigation__burger__line"></div>
			<div class="navigation__burger__line"></div>
			<div class="navigation__burger__line"></div>
		</div>
		

	</header>
</template>


<script>

import {EventBus} from '../EventBus.js';

export default {
	name: 'navigation',
	components: {
	},
	data() {
		return {
			burgerOpen: false,
			siteLink: window.location.origin,
			navList: [
				{
					name: 'Lestro',
					rel: 'hero'
				},
				{
					name: this.$t('servicesTitle'),
					rel: 'services'
				},
				{
					name: this.$t('worksTitle'),
					rel: 'works'
				},
				{
					name: this.$t('clientsTitle'),
					rel: 'partners'
				},
				{
					name: 'contacts',
					rel: 'contacts'
				}
			],
			hoveredWorks: false,
			notMainPage: false,
		}
	},
	methods:{
		navBgOninit() {
			document.querySelector('.line__yellow').style.height = document.querySelector('.navigation__nav__item .active').getBoundingClientRect().bottom + 'px';
		},
		hoverOnNavElement(e) {
			document.querySelector('.line__sharp').style.height = e.target.getBoundingClientRect().bottom + 'px';
		},
		leaveFromNavigation() {
			document.querySelector('.line__sharp').style.height = 0;
		},
		burgerClicked() {
			if(!this.burgerOpen){
				this.burgerOpen = true;
			} else {
				this.burgerOpen = false;
			}
		},
		closeContacts() {
			// on click close-contact button
			EventBus.$emit('contacts-button-event', {status: false});
			// allow scrolling after close contacts
			if(typeof(fullpage_api) != 'undefined') {
				fullpage_api.setAllowScrolling(true);
			}			
		},
		
		navigationTo(e) {
			if(this.notMainPage && e != 'contacts') {
				this.$router.push('/#' + e);
			}

			// logic for contacts button in mob menu
			if(e == 'contacts') {
				EventBus.$emit('contacts-button-event', {status: true});
			}
		}

	},
	created() {
		// hover event on index page on section works
		EventBus.$on('letter-hovered', event => {
			this.hoveredWorks = event.hovered;
		});

		EventBus.$on('on-main-page', event => {
			this.notMainPage = !event.status;
		});
	},
	mounted() {
		this.navBgOninit();
		window.addEventListener('resize', this.navBgOninit);
	},
	beforeDestroy() {
		window.removeEventListener('resize', this.navBgOninit);
	}
}
</script>

<style lang="scss">

</style>
