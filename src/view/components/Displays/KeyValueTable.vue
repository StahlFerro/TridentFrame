<template>
  <table class="kvp-table is-paddingless">
    <tr v-if="useHeader">
      <template v-if="$slots.rowControlsHeaderLeft">
        <slot name="rowControlsHeaderLeft" />
      </template>
      <th v-if="keyHeader" class="kvp-key-column">
        {{ keyHeader }}
      </th>
      <th v-if="valueHeader" class="kvp-value-column">
        {{ valueHeader }}
      </th>
      <template v-if="$slots.rowControlsHeaderRight">
        <slot name="rowControlsHeaderRight" />
      </template>
    </tr>
    <tr v-for="(rowData, index) in rows" :key="index">
      <slot name="rowControlsLeft" v-bind="rowData" />
      <slot name="dataRow" v-bind="rowData" />
      <slot name="rowControlsRight" v-bind="rowData" />
    </tr>
  </table>
</template>

<script>
  export default {
    name: "KeyValueTable",
    props: {
      rows: {
        type: Array,
        default: function() {
          return [];
        },
        required: false,
      },
      keyHeader: {
        type: String,
        default: "",
        required: false,
      },
      valueHeader: {
        type: String,
        default: "",
        required: false,
      },
      useHeader: {
        type: Boolean,
        default: true,
      },
    },
    emits: [],
  }
</script>