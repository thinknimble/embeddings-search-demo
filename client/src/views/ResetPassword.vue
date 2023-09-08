<template>
  <div class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <img class="mx-auto h-12 w-auto" src="@/assets/icons/glyph.svg" alt="ThinkNimble" />
      <h2 class="mt-4 text-center text-2xl font-bold leading-9 tracking-tight text-primary">
        Password Reset
      </h2>
    </div>
    <div class="mt-6 sm:mx-auto sm:w-full sm:max-w-sm">
      <form @submit.prevent="attemptPasswordReset()">
        <InputField
          v-model:value="form.password.value"
          :errors="form.password.errors"
          @blur="form.password.validate()"
          type="password"
          label="New Password"
          placeholder="New password"
        />

        <InputField
          v-model:value="form.confirmPassword.value"
          :errors="form.confirmPassword.errors"
          @blur="form.confirmPassword.validate()"
          type="password"
          label="Confirm Password"
          placeholder="Confirm Password"
        />

        <button class="btn--primary bg-primary" type="submit">Reset Password</button>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex'
import  { userApi, PasswordResetForm } from '@/services/users/'
import InputField from '@/components/inputs/InputField'

export default {
  name: 'ResetPassword',
  components: {
    InputField,
  },
  setup() {
    const form = ref(new PasswordResetForm())
    const store = useStore()
    const route = useRoute()
    const router = useRouter()

    function handleResetSuccess(data) {
      store.dispatch('setUser', data)
      router.push({ name: 'Dashboard' })
    }

    function handleResetFailure(error) {
      alert(error)
    }

    function attemptPasswordReset() {
      // unwrap form
      const unwrappedForm = form.value
      unwrappedForm.validate()
      if (!unwrappedForm.isValid) return

      const { uid, token } = route.params

      userApi.csc
        .resetPassword({
          uid,
          token,
          password: unwrappedForm.password.value,
        })
        .then(handleResetSuccess)
        .catch(handleResetFailure)
    }

    return {
      form,
      attemptPasswordReset,
    }
  },
}
</script>
