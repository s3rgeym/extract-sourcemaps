import Vue from 'vue'
import App from './App.vue'
import router from './router'

// fullpage include
import 'fullpage.js/vendors/scrolloverflow'
import VueFullPage from 'vue-fullpage.js'
import jsonp from 'jsonp';

Vue.use(VueFullPage);

import VueI18n from 'vue-i18n';

Vue.use(VueI18n);

const I18nPlugin = {
    install (Vue, options) {
      const _$t = Vue.prototype.$t
      Vue.prototype._$t = _$t
  
      Vue.prototype.$t = function () {
        if (this.$i18n) {
          return _$t.apply(this, arguments)
        } else {
          return _$t.apply(this.$root, arguments)
        }
      }
    }
  }

Vue.use(I18nPlugin);

const messages = {
    'en': {
        lettersDescription: 'We create different types of products for our customers. Our solutions include websites, mobile apps, chatbots, and social networks apps.',
        contactsTitle: 'Contacts',
        clientsTitle: 'Our Clients',
        worksTitle: 'Works',
        servicesTitle: 'Services',
        brandsTitle: 'Brands',
        agenciesTitle: 'Agencies',
        presentationTitle: 'Presentation',
        contactsAddress: 'UKRAINE, KYIV<br> Behterevsky lane, 4V',
        close: 'Close',
        back: 'Back',
        down: 'Down',
        subscribe: 'Subscribe',
        services: {
            designTitle: 'Design',
            designSubtitle: '— The best tecnologу',
            designProps: ['Web Design', 'Graphic design', 'UI/UX', '3D modeling', 'Motion design'],

            devTitle: 'Development',
            devSubtitle: '— The best tecnologу',
            devProps: ['Websites', 'Loyalty programs', 'Mobile applications', 'CRM', 'Banners'],

            supportTitle: 'Support',
            supportSubtitle: '— Always close',
            supportProps: ['Consulting', 'Server setup', 'Services setup', 'Support', 'Administration']
        }
    },
    'uk': {
        lettersDescription: 'Ми створюємо різні типи продуктів для наших клієнтів. Наші рішення - це веб-сайти, мобільні додатки, чат-боти, та веб-додатки для соціальних мереж.',
        contactsTitle: 'Контакти',
        clientsTitle: 'Клієнти',
        worksTitle: 'Роботи',
        servicesTitle: 'Послуги',
        brandsTitle: 'Бренди',
        agenciesTitle: 'Агенції',
        presentationTitle: 'Презентація',
        contactsAddress: 'УКРАЇНА, КИЇВ<br>БЕХТЕРЄВСЬКИЙ провулок, 4В<br>ОФІС 101',
        close: 'Закрити',
        back: 'Назад',
        down: 'ВНИЗ',
        subscribe: 'Підписуйтесь',
        services: {
            designTitle: 'Дизайн',
            designSubtitle: '— Завжди унікальний',
            designProps: ['Веб дизайн', 'Графічний дизайн', 'UI/UX', '3D-моделювання', 'Motion design'],

            devTitle: 'Розробка',
            devSubtitle: '— Найкращi технології',
            devProps: ['Сайти', 'Програми лояльності', 'Мобільні додатки', 'CRM', 'Банери'],

            supportTitle: 'Підтримка',
            supportSubtitle: '— Завжди поруч',
            supportProps: ['Консалтинг', 'Налаштування серверу', 'Підключення сервісів', 'Технічна підтримка', 'Адміністрування']
        }
    }
};

const i18n = new VueI18n({
    locale: 'uk', // set locale
    fallbackLocale: 'uk', // set fallback locale
    messages // set locale messages
});

Vue.config.productionTip = false

jsonp( "https://ipinfo.io", {}, (error, data) => {
    if (!error) {
      i18n.locale = data.country.toLowerCase() == 'ua' ? 'uk' : 'en';
    }
});

new Vue({
  i18n,
  router,
  render: h => h(App)
}).$mount('#app')

/* fetch('https://ipapi.co/json/', {
  mode: "no-cors",
  headers: {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    mode: 'no-cors'
  }
}); */



  