<template>
  <div class="field is-enhanced textbox">
    <label v-if="label" :title="hint">{{ label }}</label>
    <div class="controls-container">
      <div class="control">
        <a class="button square-button is-neon-cyan" @click="$emit('control-button-click', $event)">
          <span class="icon is-small">
            <font-awesome-icon icon="folder-open" />
          </span>
          <span>{{ buttonLabel }}</span>
        </a>
      </div>
      <div class="control main">
        <input
          :value="modelValue" 
          class="input is-neon-white"
          type="text"
          @change="$emit('update:modelValue', $event.target.value)"
          @blur="$emit('field-blur', $event)"
        />
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
    name: "ExtendedTextField",
    props: {
      label: {
        type: String,
        required: true,
      },
      buttonLabel: {
        type: String,
        required: true,
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
    emits: ['update:modelValue', 'field-input', 'control-button-click', 'field-blur']
  }
</script>