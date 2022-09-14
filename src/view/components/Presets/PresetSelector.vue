<template>
  <div class="preset-selector-bar">
    <div class="preset-contextmenu">
      <slot name="presetContextMenu" />
      <!-- <ContextMenu ref="crtPresetContextMenu" ctx-menu-id="createPanelPresetContextMenu" 
                   anchor-element-id="presetPopperBtn" placement="top-start"
                   @ctx-menu-open="$emit('ctx-menu-open')"
                   @ctx-option-click="$emit('ctx-option-click')"
                   @ctx-menu-click-outside="$emit('ctx-menu-click-outside')"
      >
        <template #contextMenuItem="ctxItemData">
          <ContextMenuItem>
            <template #contextMenuOptionIcon>
              <ContextMenuItemIcon v-if="ctxItemData.icon">
                <font-awesome-icon :icon="ctxItemData.icon" />
              </ContextMenuItemIcon>
            </template>
            <template #contextMenuOptionLabel>
              {{ ctxItemData.name }}
            </template>
          </ContextMenuItem>
        </template>
      </ContextMenu> -->
    </div>
    <div class="preset-controls-left">
      <slot name="presetControlsLeft" />
      <!-- <a 
        id="presetPopperBtn"
        class="button is-neon-emerald"
        title="Open image loading dialog" @click="$emit('preset-button-click')"
      >
        <span class="icon is-small">
          <font-awesome-icon icon="plus" />
        </span>
        <span>Presets...</span>
      </a> -->
    </div>
    <div class="preset-selection">
      <slot name="presetSelection" />
      <!-- <DropdownField 
        :model-value="presetSelectionValue" 
        :options-list="presetOptionsList" 
        :is-non-interactive="isNonInteractive" 
        :is-fullwidth="true"
        @update:model-value="$emit('update:presetSelectionValue', $event.target.value)"
      /> -->
    </div>
    <div class="preset-controls-right">
      <slot name="presetControlsRight" />
      <!-- <a
        class="button is-neon-emerald"
        title="Open image loading dialog" @click="$emit('apply-preset')"
      >
        <span class="icon is-small">
          <font-awesome-icon icon="plus" />
        </span>
        <span>Apply preset</span>
      </a> -->
    </div>
  </div>
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
      required: true,
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
  emits: ['preset-button-click', 'ctx-menu-open', 'ctx-option-click', 'ctx-menu-click-outside',],
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