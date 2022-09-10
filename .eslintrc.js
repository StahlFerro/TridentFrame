module.exports = {
  extends: [
    // add more generic rulesets here, such as:
    // 'eslint:recommended',
    // "plugin:vue/vue3-essential",
    // "eslint:recommended",
    'plugin:vue/vue3-recommended',
    // 'plugin:vue/recommended' // Use this if you are using Vue.js 2.x.
  ],
  rules: {
    // override/add rules settings here, such as:
    // 'vue/no-unused-vars': 'error'
    "vue/max-attributes-per-line": ["warn", {
      "singleline": {
        "max": 4
      },      
      "multiline": {
        "max": 5
      }
    }],
    "vue/html-self-closing": ["warn", {
      "html": {
        "void": "always",
        "normal": "always",
        "component": "always"
      },
      "svg": "always",
      "math": "always"
    }],
    "vue/no-unused-components": ["warn", {
      "ignoreWhenBindingPresent": true
    }],
    "vue/first-attribute-linebreak": ["warn", {
      "singleline": "ignore",
      "multiline": "ignore"
    }]
  },
  overrides: [
    {
      files: [
        "**/__tests__/*.{j,t}s?(x)",
        "**/tests/unit/**/*.spec.{j,t}s?(x)",
      ],
      env: {
        mocha: true,
      },
    },
  ],
}