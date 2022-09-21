<template>
  <div class="ctxmenu-content">
    <slot name="contextMenuOptionIcon" />
    <div class="ctxmenu-text">
      <slot name="contextMenuOptionLabel" />
    </div>
  </div>
</template>

<script>
export default {
  name: "ContextMenuItem",
  props: {
    color: {
      type: String,
      default: "",
      required: false,
    },
  },
};
</script>
