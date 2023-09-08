<template>
  <div class="block text-white">
    <SearchJobDescriptions />
  </div>
</template>

<script>
import SearchJobDescriptions from './SearchJobDescriptions.vue'
export default {
  name: 'Home',
  components: {
    SearchJobDescriptions,
  },
  setup() {},
}
</script>
