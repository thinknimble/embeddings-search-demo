/**
 * This function accepts any type of value and reduces it to a single
 * string. This is particularly useful for translating objects with
 * nested values into a string.
 **/
function toMessageString(data) {
  if (typeof data === 'string' || typeof data === 'number') {
    return `<h2>${String(data)}</h2>`
  } else if (data instanceof Array) {
    return '<h2>' + data.map((i) => String(i)).join(', ') + '</h2>'
  } else if (data instanceof Object) {
    let message = ''
    for (var key in data) {
      message += '<h2>' + toMessageString(data[key]) + '</h2>'
    }
    return message
  }
}

/**
 * A generic handler for API Errors.
 *
 * Shows an alert-alert notification for response error codes.
 **/
export function apiErrorHandler({
  apiName = '',
  enable400Alert = false,
  enable500Alert = false,
  rethrowErrors = true,
} = {}) {
  return (error) => {
    const { response } = error
    // Console log for dev debug
    // eslint-disable-next-line no-console
    console.log(`${apiName} Error:`, error)

    let message = '<h2>Error...</h2>'
    // Show error to user
    if (response.status >= 400 && response.status < 500) {
      // Handle 4xx errors (probably bad user input)
      const { data } = response
      let message = '<h2>Error...</h2>'
      // Handle common error structures
      if (data.detail) {
        message += `<h2>${data.detail}</h2>`
      } else if (data.non_field_errors) {
        message += `<h2>${data.non_field_errors}</h2>`
      } else {
        message = toMessageString(data)
      }
      if (enable400Alert) {
        return message
      }
      // Optionally re-raise for further optional error handling
      if (rethrowErrors) {
        throw error
      }

      return
    }

    if (enable500Alert) {
      // Generic handling for other errors (ex: 500 errors)
      return message
    }
    // Optionally re-raise for further optional error handling
    if (rethrowErrors) {
      throw error
    }
  }
}

/**
 * API FILTERS
 *
 * Utility classes for prepping filter parameters for the API
 */
export function isNotBlank(value) {
  return value !== ''
}

export function isNotNull(value) {
  return value !== null
}

export function isDefined(value) {
  return typeof value !== 'undefined'
}

export function isNotEmpty(value) {
  return value && value.length > 0
}

export function isDefinedAndNotNull(value) {
  return isNotNull(value) && isDefined(value)
}

export class ApiFilter {
  static validators = {
    isNotNull,
    isDefined,
    isNotEmpty,
    isDefinedAndNotNull,
  }

  /**
   * @param {string} key - The key to use for the query parameter in the query string.
   * @param {array[function]} validators - List of functions to use to check that the
   *                                       filter has a valid value. If not, it should
   *                                       not be included in query params.
   * @param {function} extractor - How to extract the filters value. Usually, this is
   *                               one-to-one, but sometimes (as in the case of arrays)
   *                               the value needs to be transformed.
   */
  constructor(key, validators = [isDefinedAndNotNull, isNotBlank], extractor = (i) => i) {
    this.key = key
    this.validators = validators
    this.extractor = extractor
  }

  static create({ key, validators, extractor }) {
    return new ApiFilter(key, validators, extractor)
  }

  static buildParams(filtersMap, filters) {
    const result = {}

    Object.keys(filters).forEach((key) => {
      const value = filters[key]
      const filter = filtersMap[key]
      if (!filter) return
      if (filter.isValid(value)) {
        result[filter.key] = filter.extractor(value)
      }
    })
    return result
  }

  isValid(value) {
    let valid = true
    this.validators.forEach((v) => {
      if (!v(value)) {
        valid = false
      }
    })
    return valid
  }
}
