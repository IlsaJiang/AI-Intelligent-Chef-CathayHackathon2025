import { defineStore } from 'pinia'
import http from '@/api/http'

const ACCESS_TOKEN_KEY = 'cx_access_token'
const REFRESH_TOKEN_KEY = 'cx_refresh_token'
const USER_KEY = 'cx_auth_user'
const STORAGE_MODE_KEY = 'cx_auth_storage_mode'
const STORAGE_LOCAL = 'local'
const STORAGE_SESSION = 'session'

let authStoreInstance = null

const authStoreProxy = {
  get refreshToken() {
    return authStoreInstance?.refreshToken
  },
  async refreshTokens() {
    return authStoreInstance?.refreshTokens()
  },
  logout() {
    authStoreInstance?.logout()
  },
  get accessToken() {
    return authStoreInstance?.accessToken
  }
}

const getEnvironmentStorages = () => {
  if (typeof window === 'undefined') return []
  return [
    { mode: STORAGE_LOCAL, storage: window.localStorage },
    { mode: STORAGE_SESSION, storage: window.sessionStorage }
  ]
}

const applyAuthHeader = (token) => {
  if (token) {
    http.defaults.headers.common.Authorization = `Bearer ${token}`
  } else {
    delete http.defaults.headers.common.Authorization
  }
}

const loadPersistedState = () => {
  const storages = getEnvironmentStorages()
  for (const { mode, storage } of storages) {
    try {
      const accessToken = storage.getItem(ACCESS_TOKEN_KEY)
      const refreshToken = storage.getItem(REFRESH_TOKEN_KEY)
      const userRaw = storage.getItem(USER_KEY)
      if (!accessToken || !refreshToken || !userRaw) continue
      const user = JSON.parse(userRaw)
      applyAuthHeader(accessToken)
      return { accessToken, refreshToken, user, storageMode: mode }
    } catch {
      storage.removeItem(ACCESS_TOKEN_KEY)
      storage.removeItem(REFRESH_TOKEN_KEY)
      storage.removeItem(USER_KEY)
      storage.removeItem(STORAGE_MODE_KEY)
    }
  }
  return {
    accessToken: null,
    refreshToken: null,
    user: null,
    storageMode: null
  }
}

const REWARD_KEY = 'cx_reward'

const clearPersisted = () => {
  for (const { storage } of getEnvironmentStorages()) {
    storage.removeItem(ACCESS_TOKEN_KEY)
    storage.removeItem(REFRESH_TOKEN_KEY)
    storage.removeItem(USER_KEY)
    storage.removeItem(STORAGE_MODE_KEY)
    storage.removeItem(REWARD_KEY)
  }
}

const writePersisted = (mode, accessToken, refreshToken, user) => {
  const storages = getEnvironmentStorages()
  const target = storages.find((item) => item.mode === mode)?.storage
  if (!target) return
  clearPersisted()
  target.setItem(ACCESS_TOKEN_KEY, accessToken)
  target.setItem(REFRESH_TOKEN_KEY, refreshToken)
  target.setItem(USER_KEY, JSON.stringify(user))
  target.setItem(STORAGE_MODE_KEY, mode)
}

let interceptorsBound = false
const bindHttpInterceptors = (store) => {
  if (interceptorsBound) return

  http.interceptors.response.use(
    (response) => response,
    async (error) => {
      const { response, config } = error
      if (!response || !config) {
        return Promise.reject(error)
      }

      const url = config.url || ''

      if (
        response.status === 401 &&
        !config.__isRetryRequest &&
        store.refreshToken &&
        !url.includes('/auth/login/') &&
        !url.includes('/auth/register/') &&
        !url.includes('/auth/refresh/')
      ) {
        try {
          await store.refreshTokens()
          config.__isRetryRequest = true
          config.headers = config.headers || {}
          config.headers.Authorization = `Bearer ${store.accessToken}`
          return http(config)
        } catch (refreshError) {
          store.logout()
          return Promise.reject(refreshError)
        }
      }
      return Promise.reject(error)
    }
  )

  interceptorsBound = true
}

export const useAuthStore = defineStore('auth', {
  state: () => {
    const { accessToken, refreshToken, user, storageMode } = loadPersistedState()
    bindHttpInterceptors(authStoreProxy)
    return {
      accessToken,
      refreshToken,
      user,
      storageMode,
      _isRefreshing: false,
      _refreshPromise: null
    }
  },
  getters: {
    isAuthenticated: (state) => Boolean(state.accessToken),
    displayName: (state) => state.user?.full_name || state.user?.identifier || '',
    identifier: (state) => state.user?.identifier || ''
  },
  actions: {
    async login(identifier, password, remember = true) {
      const payload = { identifier: identifier?.trim?.() ?? identifier, password }
      const { data } = await http.post('/auth/login/', payload)
      this.applySession(data, remember ? STORAGE_LOCAL : STORAGE_SESSION)
      if (data.reward) {
        this.storeReward(data.reward)
      }
      return data
    },
    async register(payload, remember = true, delayApplySession = false) {
      const sanitizedPayload = {
        ...payload,
        email: payload.email?.trim?.() || '',
        phone: payload.phone?.trim?.() || '',
        full_name: payload.full_name?.trim?.() || '',
        otp: payload.otp?.trim?.() || ''
      }
      const { data } = await http.post('/auth/register/', sanitizedPayload)
      if (data.reward) {
        const targetMode = remember ? STORAGE_LOCAL : STORAGE_SESSION
        const storage = targetMode === STORAGE_LOCAL ? localStorage : sessionStorage
        storage.setItem(REWARD_KEY, JSON.stringify(data.reward))
        if (delayApplySession) {
          setTimeout(() => {
            this.applySession(data, remember ? STORAGE_LOCAL : STORAGE_SESSION)
          }, 300)
        } else {
          this.applySession(data, remember ? STORAGE_LOCAL : STORAGE_SESSION)
        }
      } else {
        this.applySession(data, remember ? STORAGE_LOCAL : STORAGE_SESSION)
      }
      return data
    },
    async refreshTokens() {
      if (!this.refreshToken) {
        throw new Error('No refresh token available')
      }
      if (this._refreshPromise) {
        return this._refreshPromise
      }
      this._isRefreshing = true
      this._refreshPromise = http
        .post('/auth/refresh/', { refresh: this.refreshToken })
        .then(({ data }) => {
          this.accessToken = data.access
          applyAuthHeader(this.accessToken)
          if (this.storageMode) {
            writePersisted(this.storageMode, this.accessToken, this.refreshToken, this.user)
          }
          return data.access
        })
        .finally(() => {
          this._isRefreshing = false
          this._refreshPromise = null
        })
      return this._refreshPromise
    },
    logout() {
      this.accessToken = null
      this.refreshToken = null
      this.user = null
      this.storageMode = null
      this._isRefreshing = false
      this._refreshPromise = null
      applyAuthHeader(null)
      clearPersisted()
    },
    async ensureSession() {
      if (this.isAuthenticated) return true
      const persisted = loadPersistedState()
      if (persisted.accessToken || persisted.refreshToken) {
        this.accessToken = persisted.accessToken
        this.refreshToken = persisted.refreshToken
        this.user = persisted.user
        this.storageMode = persisted.storageMode
        applyAuthHeader(this.accessToken)
      }
      if (this.accessToken) return true
      if (this.refreshToken) {
        try {
          await this.refreshTokens()
          return Boolean(this.accessToken)
        } catch {
          this.logout()
        }
      }
      return false
    },
    applySession(data, mode) {
      const { access, refresh, user } = data
      this.accessToken = access
      this.refreshToken = refresh
      this.user = user
      const persistMode = mode || STORAGE_LOCAL
      this.storageMode = persistMode
      applyAuthHeader(access)
      writePersisted(persistMode, access, refresh, user)
    },
    storeReward(reward) {
      if (!reward) return
      const targetMode = this.storageMode || STORAGE_LOCAL
      const storage = targetMode === STORAGE_LOCAL ? localStorage : sessionStorage
      storage.setItem(REWARD_KEY, JSON.stringify(reward))
    },
    consumeReward() {
      const targetMode = this.storageMode || STORAGE_LOCAL
      const storage = targetMode === STORAGE_LOCAL ? localStorage : sessionStorage
      const rewardRaw = storage.getItem(REWARD_KEY)
      if (!rewardRaw) return null
      storage.removeItem(REWARD_KEY)
      try {
        return JSON.parse(rewardRaw)
      } catch {
        return null
      }
    },
    async fetchProfile() {
      if (!this.accessToken) return null
      const { data } = await http.get('/auth/me/')
      this.user = data
      if (this.storageMode) {
        writePersisted(this.storageMode, this.accessToken, this.refreshToken, this.user)
      }
      return data
    }
  }
})

export const registerAuthStoreInstance = (store) => {
  authStoreInstance = store
  bindHttpInterceptors(authStoreProxy)
}

