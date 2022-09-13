<template>
  <label class="checkbox" :title="hint">
    <input 
      :value="modelValue" 
      type="checkbox"
      @change="$emit('update:modelValue', $event.target.checked)"
    />
    {{ label }}
  </label>
</template>

<script>

import { ConstraintOption } from "../../../models/componentProps.js";
import { numConstrain } from "../../../modules/events/constraints.js";
  
export default {
  name: "CheckboxField",
  props: {
    label: {
      type: String,
      required: true,
    },
    hint: {
      type: String,
      default: null,
      required: false
    },
    modelValue: {
      type: Boolean,
    },
  },
  emits: ['update:modelValue']
};
</script>