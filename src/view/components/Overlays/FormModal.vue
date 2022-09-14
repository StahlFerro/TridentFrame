<template>
  <div class="modal" :class="{'is-active': isActive}">
    <div class="modal-background" @click="$emit('close-modal-background-clicked')"></div>
    <div class="modal-content">
      <slot />
    </div>
    <button class="modal-close is-large" aria-label="close" @click="$emit('close-modal-button-clicked')"></button>
  </div>
</template>

<script>
  export default {
    name: "FormModal",
    props: {
      isActive: {
        type: Boolean,
        default: false,
      }
    },
    emits: ['close-modal-background-clicked', 'close-modal-button-clicked'],
    data() {
      return {
        
      }
    }
  };
</script>
