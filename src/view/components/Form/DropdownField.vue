<template>
  <div class="field">
    <label v-if="label" class="label">{{ label }}</label>
    <div class="control">
      <div class="select is-neon-cyan" :class="{'non-interactive': isNonInteractive, 'is-fullwidth': isFullwidth}">
        <select 
          :value="modelValue"
          @change="$emit('update:modelValue', $event.target.value)"
        >
          <option v-for="(option, index) in optionsList" :key="index" :value="option.name" :title="option.description">
            {{ option.label }}
          </option>
          <!-- <option value="GIF">GIF</option>
          <option value="PNG">APNG</option> -->
        </select>
      </div>
    </div>
  </div>
</template>

<script>
  
import { DropdownOptions } from "../../../models/componentProps.js";
  
export default {
  name: "DropdownField",
  props: {
    modelValue: {
      type: String,
      required: true,
    },
    optionsList: {
      type: Array,
      required: true,
    },
    label: {
      type: String,
      required: true,
    },
    hint: {
      type: String,
      default: null,
      required: false
    },
    isNonInteractive: {
      type: Boolean,
      default: false
    },
    isFullwidth: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['update:modelValue']
};
</script>
