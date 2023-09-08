<template>
  <main class="grid h-full flex-auto place-items-center bg-white px-6 py-24 sm:py-32 lg:px-8">
    <div class="text-center">
      <p class="font-semibold text-accent">404</p>
      <h1 class="mt-4 text-3xl font-bold tracking-tight sm:text-5xl">
        Page not found
      </h1>
      <p class="mt-6 leading-7">
        Sorry, we couldn't find the page you're looking for.
      </p>
      <div class="mt-10 gap-x-6">
        <router-link
          to="/"
          class="rounded-md bg-accent px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-primary focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
          >Go back home</router-link
        >
      </div>
    </div>
  </main>
</template>

<script>
export default {
  name: 'PageNotFound',
}
</script>
