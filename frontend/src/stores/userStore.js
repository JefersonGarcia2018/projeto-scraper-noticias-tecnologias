import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: null,
    user: null,
    roles: []
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.roles.includes('admin')
  },
  actions: {
    setToken(token) {
      this.token = token
    },
    setUser(user) {
      this.user = user
    },
    logout() {
      this.token = null
      this.user = null
      this.roles = []
    }
  }
})
