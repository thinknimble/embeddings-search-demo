import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import { SET_USER } from './mutation-types'

const STORAGE_HASH = 'WGkzbemqza'
export const STORAGE_KEY = `vector_demonstration-${STORAGE_HASH}`

const state = {
  user: null,
}

const mutations = {
  [SET_USER]: (state, payload) => {
    state.user = payload
  },
}

const actions = {
  setUser({ commit }, user) {
    commit(SET_USER, user)
  },
}

const getters = {
  isLoggedIn: (state) => {
    return !!state.user
  },
  user: (state) => {
    return state.user
  },
  token: (state) => {
    return state.user ? state.user.token : null
  },
}

const store = createStore({
  state,
  mutations,
  actions,
  getters,
  modules: {},
  plugins: [
    createPersistedState({
      key: STORAGE_KEY,
    }),
  ],
})

export default store
