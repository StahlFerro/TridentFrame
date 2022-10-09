<template>
  <!-- <div class="preset-selector-bar"> -->
    <!-- <div class="preset-contextmenu"> -->
      <slot name="presetContextMenu" />
    <!-- </div> -->
    <!-- <div class="preset-controls-left"> -->
      <slot name="presetControlsLeft" />
    <!-- </div> -->
    <!-- <div class="preset-selection"> -->
      <slot name="presetSelection" />
    <!-- </div> -->
    <!-- <div class="preset-controls-right"> -->
      <slot name="presetControlsRight" />
    <!-- </div> -->
  <!-- </div> -->
</template>

<script>
import { DropdownOptions } from '../../../models/componentProps';
import ContextMenu from '../ContextMenu/ContextMenu.vue';
import ContextMenuItem from '../ContextMenu/ContextMenuItem.vue';
import ContextMenuItemIcon from '../ContextMenu/ContextMenuItemIcon.vue';
import DropdownField from '../Form/DropdownField.vue';
  
export default {
  name: "PresetSelector",
  components: {
    DropdownField,
    ContextMenu,
    ContextMenuItem,
    ContextMenuItemIcon
  },
  props: {
    presetSelectionValue: {
      type: String,
      required: false,
    },
    presetOptionsList: {
      type: DropdownOptions,
      required: true,
    },
    isNonInteractive: {
      type: Boolean,
      default: false
    },
  },
  emits: ['preset-click', 'ctx-menu-open', 'ctx-option-click', 'ctx-menu-click-outside',],
  data() {
    return {
    }
  },
  methods: {
    handleCrtPresetCtxMenuOptionClick(event, optionId) {

    },
    // btnToggleLoadPopper(event) {
    //   this.$refs.crtPresetContextMenu.openPopper(event, this.presetCtxMenuOptions);
    // },
    // closeLoadPopper(event) {
    //   this.$refs.crtPresetContextMenu.closePopper();
    // },
    outsideClickDebug(event) {

    },
  }
};
</script>