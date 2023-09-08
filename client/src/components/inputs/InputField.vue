<template>
  <div class="mb-2 flex w-full flex-col items-start">
    <label
      v-if="label"
      :for="`${label}-field`"
      v-text="label"
      class="input--label block text-sm font-medium text-primary"
    />
    <input
      :id="`${label}-field`"
      :type="type"
      :placeholder="placeholder"
      spellcheck="false"
      v-model="val"
      @input="$emit('input', $event)"
      @blur="$emit('blur')"
      @focus="$emit('focus', $event)"
      class="input"
    />
    <ul v-if="errors.length">
      <li
        v-for="(error, index) in errors"
        :key="index"
        v-text="error.message"
        class="input--error"
      />
    </ul>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'InputField',
  props: {
    label: {
      type: String,
    },
    type: {
      type: String,
      default: 'text',
    },
    placeholder: {
      type: String,
      default: 'Placeholder...',
    },
    value: {
      type: String,
      required: true,
    },
    errors: {
      type: Array,
      required: true,
    },
  },
  emits: ['blur', 'focus', 'input', 'update:value'],
  setup(props, context) {
    const val = computed({
      get: () => props.value,
      set: (value) => context.emit('update:value', value),
    })

    return { val }
  },
}
</script>

<style scoped lang="css"></style>
