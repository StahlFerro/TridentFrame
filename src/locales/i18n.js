const { createI18n } = require('vue-i18n');
const messages = require('@intlify/unplugin-vue-i18n/messages');

console.log(`unplugin-vue-i18n/messages on i18n.js`);
console.log(messages);

const localesList = Object.entries(messages.default).map(([langFilename, obj]) => obj);
// console.log(localesList);
const localesObj = localesList.reduce((aggr, loc) => (Object.assign(aggr, loc), aggr) ,{});
// console.log(localesObj);


const i18n = createI18n({
  locale: 'en', // set locale
  fallbackLocale: 'en', // set fallback locale  en: {
  globalInjection: true,
  enableInSFC: true,
  // messages,
  messages: localesObj,
});


module.exports.i18n = i18n;