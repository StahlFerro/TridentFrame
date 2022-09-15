<template>
  <table class="kvp-table is-paddingless">
    <tr>
      <template v-if="$slots.rowControlsLeftLabel">
        <slot name="rowControlsLeftLabel" />
      </template>
      <th class="kvp-key-column">Attribute</th>
      <th class="kvp-value-column">Value</th>
      <template v-if="$slots.rowControlsRightlabel">
        <th>
          <slot name="rowControlsRightlabel" />
        </th>
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
    },
    emits: [],
  }
</script>