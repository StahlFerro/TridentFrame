import Vue from 'vue';
import App from './App.vue';
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/default.css'
// import './css/bulmamods.css';
import "./sass/bulmamods.scss";
import "./assets/imgs/Transparency500.png";
import "./assets/icons/TridentFrame_logo_256x256.icns";
import "./assets/icons/TridentFrame_logo_256x256.ico";
import "./webfonts/ShareTech-Regular.ttf";
// import "../config/app.toml";

import 'regenerator-runtime/runtime';

import { library } from '@fortawesome/fontawesome-svg-core';
import { faImage } from '@fortawesome/free-solid-svg-icons/faImage';
import { faImages } from '@fortawesome/free-solid-svg-icons/faImages';
import { faExchangeAlt } from '@fortawesome/free-solid-svg-icons/faExchangeAlt';
import { faSearch } from '@fortawesome/free-solid-svg-icons/faSearch';
import { faCog } from '@fortawesome/free-solid-svg-icons/faCog';
import { faInfoCircle } from '@fortawesome/free-solid-svg-icons/faInfoCircle';
import { faPlus } from '@fortawesome/free-solid-svg-icons/faPlus';
import { faPlusCircle } from '@fortawesome/free-solid-svg-icons/faPlusCircle';
import { faTimes } from '@fortawesome/free-solid-svg-icons/faTimes';
import { faTimesCircle } from '@fortawesome/free-solid-svg-icons/faTimesCircle';
import { faMinusCircle } from '@fortawesome/free-solid-svg-icons/faMinusCircle';
import { faCheck } from '@fortawesome/free-solid-svg-icons/faCheck';
import { faSpinner } from '@fortawesome/free-solid-svg-icons/faSpinner';
import { faSave } from '@fortawesome/free-solid-svg-icons/faSave';
import { faChessBoard } from '@fortawesome/free-solid-svg-icons/faChessBoard';
import { faEye } from '@fortawesome/free-solid-svg-icons/faEye';
import { faFileUpload } from '@fortawesome/free-solid-svg-icons/faFileUpload';
import { faRedoAlt } from '@fortawesome/free-solid-svg-icons/faRedoAlt';
import { faBug } from '@fortawesome/free-solid-svg-icons/faBug';
import { faPowerOff } from '@fortawesome/free-solid-svg-icons/faPowerOff';
import { faEye as farEye } from '@fortawesome/free-regular-svg-icons/faEye';
import { faCopyright as farCopyright } from '@fortawesome/free-regular-svg-icons/faCopyright';
import { faGithub as fabGithub } from '@fortawesome/free-brands-svg-icons/faGithub';
import { faFlask } from '@fortawesome/free-solid-svg-icons/faFlask';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

library.add([faImage, faImages, faExchangeAlt, faSearch, faCog, faInfoCircle, faPlus, faPlusCircle, faTimes, faTimesCircle, faMinusCircle, faCheck, faSpinner,
  faSave, faChessBoard, faRedoAlt, faBug, faPowerOff, faEye, farCopyright, faFileUpload, farEye, fabGithub, faFlask]);

Vue.component('font-awesome-icon', FontAwesomeIcon);

Vue.config.devtools = true;
Vue.component('VueSlider', VueSlider);

new Vue({
  el: '#app',
  render: h => h(App),
});
