// import Vue from 'vue';
import { createApp } from 'vue'
import App from './App.vue';
import VueSlider from 'vue-slider-component'
// import mitt from 'mitt';
import _emitter from './modules/events/emitter';
import 'vue-slider-component/theme/default.css'
// import './css/bulmamods.css';
import { i18n } from './locales/i18n.js';

import "./sass/bulmamods.scss";
import "./assets/imgs/Transparency500.png";
import "./assets/imgs/Generated_Grey_Checker_nl_0.webp";
import "./assets/icons/TridentFrame_logo_256x256.icns";
import "./assets/icons/TridentFrame_logo_256x256.ico";
import "./webfonts/ShareTech-Regular.ttf";
// import "../config/app.toml";

import 'regenerator-runtime/runtime';

import { library } from '@fortawesome/fontawesome-svg-core';
import { faImage } from '@fortawesome/free-solid-svg-icons/faImage';
import { faImages } from '@fortawesome/free-solid-svg-icons/faImages';
import { faImage as farImage } from '@fortawesome/free-regular-svg-icons/faImage';
import { faExchangeAlt } from '@fortawesome/free-solid-svg-icons/faExchangeAlt';
import { faSearch } from '@fortawesome/free-solid-svg-icons/faSearch';
import { faCog } from '@fortawesome/free-solid-svg-icons/faCog';
import { faInfoCircle } from '@fortawesome/free-solid-svg-icons/faInfoCircle';
import { faPlus } from '@fortawesome/free-solid-svg-icons/faPlus';
import { faPlusCircle } from '@fortawesome/free-solid-svg-icons/faPlusCircle';
import { faTimes } from '@fortawesome/free-solid-svg-icons/faTimes';
import { faTimesCircle } from '@fortawesome/free-solid-svg-icons/faTimesCircle';
import { faTriangleExclamation } from "@fortawesome/free-solid-svg-icons/faTriangleExclamation";
import { faCircleExclamation } from '@fortawesome/free-solid-svg-icons/faCircleExclamation';
import { faMinusCircle } from '@fortawesome/free-solid-svg-icons/faMinusCircle';
import { faCheck } from '@fortawesome/free-solid-svg-icons/faCheck';
import { faSpinner } from '@fortawesome/free-solid-svg-icons/faSpinner';
import { faSave } from '@fortawesome/free-solid-svg-icons/faSave';
import { faFolderOpen } from '@fortawesome/free-solid-svg-icons/faFolderOpen';
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
import { faGlobe } from '@fortawesome/free-solid-svg-icons/faGlobe';
import { faSlidersH } from '@fortawesome/free-solid-svg-icons/faSlidersH';
import { faPaintRoller } from '@fortawesome/free-solid-svg-icons/faPaintRoller';
import { faSquarePen } from '@fortawesome/free-solid-svg-icons/faSquarePen';
import { faTrashCan } from '@fortawesome/free-solid-svg-icons/faTrashCan';
import { faLayerGroup } from "@fortawesome/free-solid-svg-icons/faLayerGroup";
import { faFileArrowDown } from "@fortawesome/free-solid-svg-icons/faFileArrowDown";
import { faArrowRotateLeft } from "@fortawesome/free-solid-svg-icons/faArrowRotateLeft";
import { faScaleBalanced } from "@fortawesome/free-solid-svg-icons/faScaleBalanced";
import { faMugHot } from "@fortawesome/free-solid-svg-icons/faMugHot";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

library.add([faImage, farImage, faImages, faExchangeAlt, faSearch, faCog, faInfoCircle, faPlus, faPlusCircle, faTimes, faTimesCircle, faMinusCircle, 
  faTriangleExclamation, faCircleExclamation, faCheck, faSpinner, faSave, faFolderOpen, faChessBoard, faRedoAlt, faBug, faPowerOff, faEye, 
  farCopyright, faFileUpload, farEye, fabGithub, faFlask, faGlobe, faSlidersH, faPaintRoller, faSquarePen, faTrashCan, faLayerGroup,
  faFileArrowDown, faArrowRotateLeft, faScaleBalanced, faMugHot ]);

const app = createApp(App);
// const emitter = mitt();
app.config.globalProperties.emitter = _emitter;


// console.log(`unplugin-vue-i18n/messages on app.js`);
// console.log(i18n);
app.use(i18n);

app.component('font-awesome-icon', FontAwesomeIcon);
app.component('VueSlider', VueSlider);

// app.config.dev
// Vue.component('VueSlider', VueSlider);
// Vue.component('font-awesome-icon', FontAwesomeIcon);

// Vue.config.devtools = true;

// new Vue({
//   el: '#app',
//   render: h => h(App),
// });

app.mount("#app");
