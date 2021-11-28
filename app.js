import Vue from 'vue';
import App from './App.vue';
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/default.css'
import './css/bulmamods.css';
import '@fortawesome/fontawesome-free/js/all';
// import './css/fontawesome-all.css';
// import { Plugin } from 'vue-fragment'

Vue.config.devtools = true;
Vue.component('VueSlider', VueSlider);
// Vue.use(Plugin);

new Vue({
  el: '#app',
  render: h => h(App),
});
