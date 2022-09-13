<template>
  <div class="preset-selector-bar">
    <div class="preset-controls-left">
      <a
        class="button is-neon-emerald"
        title="Open image loading dialog" @click="$emit('add-preset')"
      >
        <span class="icon is-small">
          <font-awesome-icon icon="plus" />
        </span>
        <span>New preset</span>
      </a>

      <a
        class="button is-neon-emerald"
        title="Open image loading dialog" @click="$emit('update-preset')"
      >
        <span class="icon is-small">
          <font-awesome-icon icon="plus" />
        </span>
        <span>Update preset</span>
      </a>
      
      <a
        class="button is-neon-emerald"
        title="Open image loading dialog" @click="$emit('delete-preset')"
      >
        <span class="icon is-small">
          <font-awesome-icon icon="plus" />
        </span>
        <span>Delete preset</span>
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
</template>

<script>
import { DropdownOptions } from '../../../models/componentProps';
import DropdownField from '../Form/DropdownField.vue';
  
export default {
  name: "PresetSelector",
  components: {
    DropdownField,
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
  emits: ['update:presetSelectionValue', 'add-preset', 'update-preset', 'delete-preset', 'apply-preset']
};
</script>