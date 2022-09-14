<template>
  <div class="modal" :class="{'is-active': isActive}">
    <div class="modal-background blur" @click="$emit('close-modal-background-clicked')"></div>
    <div class="modal-content neon-modal ">
      <slot name="modalForm" />
      <slot name="modalControls" />
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
