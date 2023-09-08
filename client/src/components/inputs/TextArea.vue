<template>
  <textarea
    rows="12"
    class="block p-2.5 mb-4 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
    placeholder="Describe the job seeker..."
    tabindex="0"
    :value="text"
    @input="onInput"
  ></textarea>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'TextArea',
  props: {
    value: {
      type: String,
      default: '',
    },
  },
  setup(props, { emit }) {
    const text = ref(props.value)

    function onInput(event) {
      text.value = event.target.value
      emit('update:modelValue', text.value)
    }

    return {
      text,
      onInput,
    }
  },
}
</script>
