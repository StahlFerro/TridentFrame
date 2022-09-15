<template>
  <td>
    <slot name="dataKey" />
  </td>
  <td>
    <slot name="dataValue" />
  </td>
</template>

<script>
  export default {
    name: "KeyValueTableDataRow",
  }
</script>