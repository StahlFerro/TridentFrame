<template>
    <div class="status-bar">
        <input
            :value="modelValue"
            type="text"
            class="status-textbox"
            readonly="readonly"
        />
    </div>
</template>

<script>
export default {
    props: {
        modelValue: String,
    }
}
</script>
