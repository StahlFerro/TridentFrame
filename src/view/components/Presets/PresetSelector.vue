<template>
  <div>
    <ContextMenu ref="crtPresetContextMenu" ctx-menu-id="createPanelPresetContextMenu" 
                 anchor-element-id="presetPopperBtn" placement="top-start"
                 @ctx-menu-click-outside="outsideClickDebug"
                 @ctx-option-click="handleCrtPresetCtxMenuOptionClick"
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
    </ContextMenu>

    
    <div class="preset-selector-bar">
      <div class="preset-controls-left">
        <a 
          id="presetPopperBtn"
          class="button is-neon-emerald"
          title="Open image loading dialog" @click="btnToggleLoadPopper"
        >
          <span class="icon is-small">
            <font-awesome-icon icon="plus" />
          </span>
          <span>Presets...</span>
        </a>
      </div>
      <div class="preset-selection">
        <DropdownField 
          :model-value="presetSelectionValue" 
          :options-list="presetOptionsList" 
          :is-non-interactive="isNonInteractive" 
          @update:model-value="$emit('update:presetSelectionValue', $event.target.value)"
        />
      </div>
      <div class="preset-controls-right">
        <a
          class="button is-neon-emerald"
          title="Open image loading dialog" @click="$emit('apply-preset')"
        >
          <span class="icon is-small">
            <font-awesome-icon icon="plus" />
          </span>
          <span>Apply preset</span>
        </a>
      </div>
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
  emits: ['update:presetSelectionValue', 'add-preset', 'update-preset', 'delete-preset', 'apply-preset'],
  data() {
    return {
      presetCtxMenuOptions: [
        {id: 'preset_new', name: "Create new preset", icon: ['fas', 'plus']},
        {id: 'preset_update', name: "Update to preset", icon: ['fas', 'plus-circle']},
        {id: 'preset_delete', name: "Delete preset", icon: ['fas', 'plus-circle']},
      ],
    }
  },
  methods: {
    handleCrtPresetCtxMenuOptionClick(event, optionId) {

    },
    btnToggleLoadPopper(event) {
      this.$refs.crtPresetContextMenu.openPopper(event, this.presetCtxMenuOptions);
    },
    closeLoadPopper(event) {
      this.$refs.crtPresetContextMenu.closePopper();
    },
    outsideClickDebug(event) {

    },
  }
};
</script>