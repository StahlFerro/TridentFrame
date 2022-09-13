<template>
  <a
    class="button" :class="{
      'is-neon-white': color == 'white',
      'is-neon-emerald': color == 'green',
      'is-neon-cyan': color == 'cyan',
      'is-neon-crimson': color == 'red',
      'is-neon-cobalt': color == 'blue',
      'is-loading': isLoading,
      'non-interactive': isNonInteractive
    }"
    :title="hint" @click="$emit('button-click')"
  >
    <span v-if="iconArray.length >= 2" class="icon is-small">
      <font-awesome-icon :icon="iconArray" />
    </span>
    <span>{{ label }}</span>
  </a>
</template>


<script>
  
  export default {
    name: "ButtonField",
    props: {
      iconArray: {
        type: Array,
        default() {
          return []
        },
        required: false,
      },
      label: {
        type: String,
        required: true,
      },
      color: {
        type: String,
        default: "white",
        required: false
      },
      isLoading: {
        type: Boolean,
        default: false
      },
      isNonInteractive: {
        type: Boolean,
        default: false
      },
      hint: {
        type: String,
        default: "",
        required: false,
      },
    },
    emits: ['button-click']
  };
  </script>