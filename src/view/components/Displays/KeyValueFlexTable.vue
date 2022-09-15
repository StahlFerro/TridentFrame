<template>
  <div class="table-kvp">
    <template v-for="(dval, dkey, index) in dictionary" :key="index">
      <div class="cell-k">
        {{ dkey }}
      </div>
      <div class="cell-v">
        {{ dval }}
      </div>
    </template>
  </div>
</template>

<script>
  export default {
    name: "KeyValueFlexTable",
    props: {
      dictionary: {
        type: Object,
        default: function() {
          return {};
        },
        required: false,
      },
    },
    emits: []
  }
</script>