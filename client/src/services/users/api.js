import { createApi, createCustomServiceCall } from '@thinknimble/tn-models'
import { z } from 'zod'
import axiosInstance from '../AxiosClient'
import { userShape, forgotPasswordShape, userCreateShape, loginShape } from './models'

const login = createCustomServiceCall(
  {
    inputShape: loginShape,
    outputShape: userShape,
  },
  async ({ client, input, utils }) => {
    const res = await client.post('/login/', utils.toApi(input))
    return utils.fromApi(res.data)
  },
)

const requestPasswordReset = createCustomServiceCall(
  {
    inputShape: forgotPasswordShape,
  },
  async ({ client, input }) => {
    await client.get(`/password/reset/${input.email}/`)
  },
)
const resetPassword = createCustomServiceCall(
  {
    inputShape: { uid: z.string().email(), token: z.string(), password: z.string() },
    outputShape: userShape,
  },
  async ({ client, input, utils }) => {
    const { email, ...rest } = utils.toApi(input)
    const res = await client.post(`/password/reset/code/confirm/${input.email}/`, rest)
    return utils.fromApi(res.data)
  },
)

export const userApi = createApi(
  {
    client: axiosInstance,
    baseUri: '/users/',
    models: {
      create: userCreateShape,
      entity: userShape,
    },
  },
  { login, requestPasswordReset, resetPassword },
)
