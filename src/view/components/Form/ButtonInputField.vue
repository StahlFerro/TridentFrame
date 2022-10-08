<template>
  <div class="field is-enhanced textbox">
    <label v-if="label" :title="hint">{{ label }}</label>
    <div class="controls-container">
      <div class="control">
        <slot name="buttonControl" />
        <!-- <a class="button square-button is-neon-cobalt" @click="$emit('control-click', $event)">
          <span class="icon is-small">
            <font-awesome-icon icon="folder-open" />
          </span>
          <span>{{ buttonLabel }}</span>
        </a> -->
      </div>
      <div class="control main">
        <slot name="inputControl" />
        <!-- <input
          :value="modelValue" 
          class="input is-neon-white"
          type="text"
          @change="$emit('update:modelValue', $event.target.value)"
          @blur="$emit('field-blur', $event)"
        /> -->
      </div>
    </div>
    <div v-if="useIcons" class="stat-icon">
      <span v-if="hasError" class="icon is-crimson" :title="errorMessage">
        <font-awesome-icon icon="circle-exclamation" size="lg" />
      </span>
    </div>
  </div>
</template>

<script>
  export default {
    name: "ButtonInputField",
    props: {
      label: {
        type: String,
        default: null,
        required: false,
      },
      hint: {
        type: String,
        default: null,
        required: false
      },
      modelValue: {
        type: String,
        default: null,
        required: false,
      },
      useIcons: {
        type: Boolean
      },
      hasError: {
        type: Boolean
      },
      errorMessage: {
        type: String,
        default: "",
        required: false,
      }
    },
    emits: ['update:modelValue', 'input', 'control-click', 'field-blur']
  }
</script>