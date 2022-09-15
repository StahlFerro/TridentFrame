<template>
  <li class="context-menu-option">
    <div class="ctxmenu-content">
      <slot name="contextMenuOptionIcon" />
      <div class="ctxmenu-text">
        <slot name="contextMenuOptionLabel" />
      </div>
    </div>
  </li>
</template>

<script>
export default {
  name: "ContextMenuItem",
}
</script>

