import { z } from 'zod'
import { readonly } from '@thinknimble/tn-models'
import { baseModelShape } from '../base-model'

export const jobDescriptionShape = {
  ...baseModelShape,
  title: z.string(),
}

export const jobDescriptionChunkShape = {
  ...baseModelShape,
  jobDescriptionId: z.string(),
  chunk: z.string(),
  token_count: z.number(),
  embedding: z.array(z.number()),
}

export const jobDescriptionSearchResultShape = {
  score: readonly(z.number()),
  jobDescription: jobDescriptionShape,
  chunks: z.array(jobDescriptionChunkShape),
}

export const queryShape = {
  query: z.string(),
}
