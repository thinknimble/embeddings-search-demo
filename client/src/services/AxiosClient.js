import axios from 'axios'
import store from '@/store'
import CSRF from '@/services/csrf'

/**
 *   Get the axios API client.
 *   This conveniently sets the `baseURL` and `headers` for the API client,
 *   so that we don't have to do this in every function that needs to call
 *   the API.
 *   This will automaticaly proxy requrests to /api/
 *   if the /api/ route is already included the vue.config.js will overwrite it
 *
 *
 *   @returns {object} - An instance of the axios API client.
 */

class ApiService {
  static session
  static init
  constructor() {
    let baseURL = `${window.location.protocol}//${window.location.host}/api`

    console.debug(`API Service for ${baseURL}`)

    ApiService.session = axios.create({
      baseURL,
      headers: {
        ...CSRF.getHeaders(),
      },
    })
    ApiService.session.interceptors.request.use(
      async (config) => {
        if (store.getters.isLoggedIn) {
          config.headers['Authorization'] = `Token ${store.getters.token}`
        }
        return config
      },
      (error) => {
        Promise.reject(error)
      },
    )
  }

  static get instance() {
    if (!ApiService.init) {
      new ApiService()
      ApiService.init = true
    }
    return ApiService.session
  }
}

export default ApiService.instance
// extend and use
export { ApiService }
