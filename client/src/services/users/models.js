import { z } from 'zod'
import { readonly } from '@thinknimble/tn-models'
import { baseModelShape } from '../base-model'

export const userShape = {
  ...baseModelShape,
  email: z.string().email(),
  firstName: z.string(),
  lastName: z.string(),
  token: readonly(z.string().nullable()),
}

export const userCreateShape = {
  email: userShape.email,
  firstName: userShape.firstName,
  lastName: userShape.lastName,
  password: z.string(),
}

export const forgotPasswordShape = {
  email: z.string().email(),
}

export const loginShape = {
  email: z.string().email(),
  password: z.string(),
}
