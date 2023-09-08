import { createApi, createCustomServiceCall } from '@thinknimble/tn-models'
import axiosInstance from '../AxiosClient'
import { queryShape, jobDescriptionSearchResultShape, jobDescriptionShape } from './models'

const search = createCustomServiceCall(
  {
    inputShape: queryShape,
    outputShape: jobDescriptionSearchResultShape,
  },
  async ({ client, input, utils }) => {
    const res = await client.post('/job-descriptions/search/', utils.toApi(input))
    return utils.fromApi(res.data)
  },
)

export const jobDescriptionApi = createApi(
  {
    client: axiosInstance,
    baseUri: '/job-descriptions/',
    models: {
      create: jobDescriptionShape,
      entity: jobDescriptionShape,
    },
  },
  { search },
)
