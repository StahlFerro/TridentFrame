<template>
  <div class="field">
    <label class="label" :title="hint">{{ label }}</label>
    <div class="control">
      <input 
        :value="modelValue" 
        class="input is-neon-white"
        :type="type"
        :min="minNumber"
        :max="maxNumber"
        @change="$emit('update:modelValue', $event.target.value)"
        @input="$emit('input', $event)"
        @keydown="handleKeyDown($event)" 
      />
    </div>
  </div>
</template>

<script>

import { ConstraintOption } from "../../../models/componentProps.js";
import { numConstrain } from "../../../modules/events/constraints.js";
  
export default {
  name: "InputField",
  props: {
    label: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      required: true
    },
    hint: {
      type: String,
      default: null,
      required: false
    },
    modelValue: {
      type: [String, Number],
      default: null,
      required: false,
    },
    constraintOption: {
      type: ConstraintOption,
      default: null,
      required: false
    },
    minNumber: {
      type: Number,
      default: null,
      required: false,
    },
    maxNumber: {
      type: Number,
      default: null,
      required: false,
    },
  },
  emits: ['update:modelValue', 'input'],
  data() {
    return {
    }
  },
  methods: {
    handleKeyDown(event, args) {
      console.log('constraintOption');
      console.log(this.constraintOption);
      if (this.constraintOption) {
        if (this.constraintOption.handlerName == "numConstraint") {
          const enforceUnsigned = this.constraintOption.options.enforceUnsigned;
          const enforceWhole = this.constraintOption.options.enforceWhole;
          console.log(enforceUnsigned);
          console.log(enforceWhole);
          numConstrain(event, enforceUnsigned, enforceWhole);
        }
      }
    }
  },
};
</script>