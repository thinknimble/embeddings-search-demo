<template>
  <div class="block mx-auto max-w-7xl p-4">
    <div class="md:flex md:space-x-4">
      <div class="md:w-1/3 md:flex-none">
        <h1 class="text-lg text-semibold text-white text-left mb-4">Search Job Descriptions</h1>
        <form @submit.prevent="search">
          <TextArea v-model="searchQuery" />
          <DarkButton label="Search" type="submit" />
        </form>
      </div>

      <div class="md:flex-grow p-4 bg-gray-800 rounded">
        <h2 class="text-lg mb-4">Results</h2>
        <i v-if="!hasResults && !loading"
          >Type a query and hit 'Submit' to find matching job descriptions.</i
        >
        <i v-if="!hasResults && loading">Loading Matches. This takes a few seconds...</i>

        <template v-if="hasResults">
          <Popover
            class="relative text-left"
            v-for="result in searchResults"
            v-bind:key="result.jobDescription.id"
          >
            <div
              class="flex w-full py-2"
              style="align-items: center; justify-content: space-between"
            >
              <div class="w-2/3">
                <p class="text-lg text-semibold">{{ result.jobDescription.title }}</p>
                <p>{{ result.jobDescription.company }}, {{ result.jobDescription.location }}</p>
                <p>(Match Score: {{ result.score.toFixed(3) }})</p>
              </div>
              <div class="flex-none">
                <PopoverButton class="bg-gray-700 px-3 py-1 rounded-md"
                  >See Description</PopoverButton
                >
              </div>
            </div>

            <transition
              enter-active-class="transition duration-200 ease-out"
              enter-from-class="translate-y-1 opacity-0"
              enter-to-class="translate-y-0 opacity-100"
              leave-active-class="transition duration-150 ease-in"
              leave-from-class="translate-y-0 opacity-100"
              leave-to-class="translate-y-1 opacity-0"
            >
              <PopoverPanel
                class="absolute z-10 p-4 max-h-96 overflow-y-auto bg-white rounded text-black"
              >
                <div v-html="result.jobDescription.description"></div>
              </PopoverPanel>
            </transition>
          </Popover>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { jobDescriptionApi } from '@/services/jobDescriptions/'

import { Popover, PopoverButton, PopoverPanel } from '@headlessui/vue'

import TextArea from '@/components/inputs/TextArea'
import DarkButton from '@/components/DarkButton'

export default {
  name: 'SearchJobDescriptions',
  components: {
    DarkButton,
    TextArea,
    Popover,
    PopoverButton,
    PopoverPanel,
  },
  setup() {
    const searchQuery = ref('')
    const searchResults = ref(null)
    const loading = ref(false)

    const handleSearchSuccess = (data) => {
      searchResults.value = data
    }

    const hasResults = computed(() => searchResults.value !== null)

    const search = () => {
      if (!searchQuery.value) return
      searchResults.value = null
      loading.value = true
      jobDescriptionApi.csc
        .search({ query: searchQuery.value })
        .then(handleSearchSuccess)
        .catch(() => console.log('failure'))
        .finally(() => (loading.value = false))
    }

    return {
      searchQuery,
      searchResults,
      search,
      hasResults,
      loading,
    }
  },
}
</script>

<style scoped lang="css"></style>
