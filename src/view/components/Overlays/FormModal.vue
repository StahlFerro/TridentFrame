<template>
  <div class="modal" :class="{'is-active': isActive}">
    <div class="modal-background blur" @click="$emit('close-modal-background-clicked')"></div>
    <div class="modal-content neon-modal ">
      <div class="modal-form-container">
        <div class="modal-header">
          <slot name="modalHeader" />
        </div>
        <div v-if="$slots.modalDisplay" class="modal-display">
          <slot name="modalDisplay" />
        </div>
        <div class="modal-form">
          <slot name="modalForm" />
        </div>
        <div class="modal-controls">
          <slot name="modalControls" />
        </div>
      </div>
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
