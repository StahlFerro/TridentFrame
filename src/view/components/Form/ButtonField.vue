<template>
  <a
    :id="id"
    :v-click-outside="listenToOutsideClicks? emitClickOutside : null"
    class="button" :class="{
      'is-neon-white': color == 'white',
      'is-neon-emerald': color == 'green',
      'is-neon-cyan': color == 'cyan',
      'is-neon-crimson': color == 'red',
      'is-neon-cobalt': color == 'blue',
      'is-neon-purple': color == 'purple',
      'is-loading': isLoading,
      'square-button': isSquare,
      'non-interactive': isNonInteractive,
    }"
    :title="hint" @click="$emit('button-click')"
  >
    <span v-if="icons.length >= 2" class="icon is-small">
      <font-awesome-icon :icon="icons" />
    </span>
    <span>{{ label }}</span>
  </a>
</template>


<script>
  
  export default {
    name: "ButtonField",
    props: {
      id: {
        type: String,
        default: null,
        required: false,
      },
      icons: {
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
      isSquare: {
        type: Boolean,
        default: false,
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
      listenToOutsideClicks: {
        type: Boolean,
        default: false,
      }
    },
    emits: ['button-click', 'click-outside'],
    methods: {
      emitClickOutside(event) {
        console.debug('emitClickOutside');
        this.$emit('click-outside', event);
      }
    }
  };
</script>