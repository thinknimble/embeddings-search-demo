<template>
  <div class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <img class="mx-auto h-12 w-auto" src="@/assets/icons/glyph.svg" alt="ThinkNimble" />
      <h2 class="mt-4 text-center text-2xl font-bold leading-9 tracking-tight text-primary">
        Log in
      </h2>
    </div>

    <div class="mt-6 sm:mx-auto sm:w-full sm:max-w-sm">
      <form @submit.prevent="attemptLogin()">
        <InputField
          v-model:value="form.email.value"
          :errors="form.email.errors"
          @blur="form.email.validate()"
          type="email"
          data-cy="email"
          label="Email address"
          placeholder="Enter email..."
        />
        <div>
          <div class="flex items-center justify-between">
            <label for="password" class="block text-sm font-medium leading-6 text-primary"
              >Password</label
            >
            <div class="text-sm hover:underline">
              <router-link :to="{ name: 'RequestPasswordReset' }" class="font-semibold text-accent"
                >Forgot password?</router-link
              >
            </div>
          </div>
          <div class="mt-2">
            <InputField
              v-model:value="form.password.value"
              :errors="form.password.errors"
              @blur="form.password.validate()"
              type="password"
              data-cy="password"
              placeholder="Enter password..."
            />
          </div>
        </div>

        <div>
          <button type="submit" data-cy="submit" class="btn--primary bg-primary">Log in</button>
        </div>
      </form>
    </div>
    <div class="m-4 flex self-center text-sm">
      <p class="mr-2">Don't have an account?</p>
      <router-link :to="{ name: 'Signup' }" class="font-bold text-primary hover:underline">
        Sign up.
      </router-link>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import  { LoginForm, userApi } from '@/services/users/'
import InputField from '@/components/inputs/InputField'

export default {
  name: 'Login',
  components: {
    InputField,
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    const form = ref(new LoginForm())

    async function handleLoginSuccess(user) {
      await store.dispatch('setUser', user)
      const redirectPath = router.currentRoute.value.query.redirect
      if (redirectPath) {
        router.push({ path: redirectPath })
      } else {
        router.push({ name: 'Dashboard' })
      }
    }

    function handleLoginFailure(error) {
      alert(error)
    }

    function attemptLogin() {
      // unwrap form
      const unwrappedForm = form.value
      unwrappedForm.validate()
      if (!unwrappedForm.isValid) return
      userApi.csc
        .login({ email: unwrappedForm.email.value, password: unwrappedForm.password.value })
        .then(handleLoginSuccess)
        .catch(handleLoginFailure)
    }

    return {
      form,
      attemptLogin,
    }
  },
}
</script>

<style scoped lang="css"></style>
