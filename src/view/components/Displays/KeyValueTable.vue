<template>
  <table class="kvp-table is-paddingless">
    <tr>
      <template v-if="$slots.rowControlsHeaderLeft">
        <slot name="rowControlsHeaderLeft" />
      </template>
      <th class="kvp-key-column">
        {{ keyHeader }}
      </th>
      <th class="kvp-value-column">
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
        default: "Attribute",
        required: false,
      },
      valueHeader: {
        type: String,
        default: "Value",
        required: false,
      },
    },
    emits: [],
  }
</script>