<template>
  <div class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <img class="mx-auto h-12 w-auto" src="@/assets/icons/glyph.svg" alt="ThinkNimble" />
      <h2 class="mt-4 text-center text-2xl font-bold leading-9 tracking-tight text-primary">
        Request Password Reset
      </h2>
    </div>
    <div class="mt-6 sm:mx-auto sm:w-full sm:max-w-sm">
      <template v-if="!resetLinkSent">
        <form @submit.prevent="attemptResetRequest()">
          <InputField
            v-model:value="form.email.value"
            :errors="form.email.errors"
            @blur="form.email.validate()"
            type="email"
            label="Email address"
            placeholder="Enter email..."
          />
          <button
            :class="form.isValid ? 'btn--primary bg-primary' : 'btn--disabled bg-gray-200'"
            type="submit"
          >
            Request Password Reset
          </button>
        </form>
      </template>
      <template v-if="resetLinkSent">
        <p class="text-md">
          Your request has been submitted. If there is an account associated with the email
          provided, you should receive an email momentarily with instructions to reset your
          password.
        </p>
        <p class="text-md">
          If you do not see the email in your main folder soon, please make sure to check your spam
          folder.
        </p>
        <div class="pt-6">
          <button type="button" class="btn--primary bg-primary">
            <router-link :to="{ name: 'Login' }" class="" id="login-link">
              Return to Login
            </router-link>
          </button>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import  { userApi,  RequestPasswordResetForm } from '@/services/users/'
import InputField from '@/components/inputs/InputField'

export default {
  name: 'RequestPasswordReset',
  components: {
    InputField,
  },
  setup() {
    const form = ref(new RequestPasswordResetForm())
    const resetLinkSent = ref(false)

    function handleResetRequestSuccess(data) {
      resetLinkSent.value = true
      console.log('success', data)
    }

    function handleResetRequestFailure(error) {
      alert(error)
    }

    function attemptResetRequest() {
      // unwrap form
      const unwrappedForm = form.value
      unwrappedForm.validate()
      if (!unwrappedForm.isValid) return

      userApi.csc.requestPasswordReset({email: unwrappedForm.email.value})
        .then(handleResetRequestSuccess)
        .catch(handleResetRequestFailure)
    }

    return {
      form,
      attemptResetRequest,
      resetLinkSent,
    }
  },
}
</script>
