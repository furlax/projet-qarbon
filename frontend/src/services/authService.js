import api from "@/services/api"
import { ref } from "vue"

export const LOCALSTORAGE_TOKEN_KEY = "access_token"
export const LOCALSTORAGE_REFRESH_TOKEN_KEY = "refresh_token"
export const LOCALSTORAGE_TOKEN_TIMESTAMP = "tokenTimestamp"

const MAX_RETRY_COUNT = 3

let access_token = localStorage.getItem(LOCALSTORAGE_TOKEN_KEY)
let refresh_token = localStorage.getItem(LOCALSTORAGE_REFRESH_TOKEN_KEY)
let timestamp_token = localStorage.getItem(LOCALSTORAGE_TOKEN_TIMESTAMP)
let user = ref()

api.interceptors.request.use((config) => {
  if (access_token) {
    config.headers["Authorization"] = `Bearer ${access_token}`
  }
  return config
})

api.interceptors.response.use(null, (error) => {
  if (error.response) {
    const { status } = error.response
    let originalRequest = error.config

    // Initialize retry count if not set
    if (!originalRequest._retryCount) {
      originalRequest._retryCount = 0
    }

    const isRefreshTokenRequest = originalRequest.url === "dj-rest-auth/token/refresh/"

    if (status === 401 && originalRequest._retryCount < MAX_RETRY_COUNT) {
      originalRequest._retryCount++

      // Do not retry if the request that failed was the refresh token request itself
      if (isRefreshTokenRequest) {
        console.error("Refresh token is invalid. Logging out.")
        localStorage.removeItem(LOCALSTORAGE_TOKEN_KEY)
        localStorage.removeItem(LOCALSTORAGE_REFRESH_TOKEN_KEY)
        localStorage.removeItem(LOCALSTORAGE_TOKEN_TIMESTAMP)
        user.value = undefined
        return Promise.reject(error)
      }

      // Try to refresh the token
      return api
        .post("dj-rest-auth/token/refresh/", { refresh: refresh_token })
        .then((response) => {
          if (response.status === 200) {
            access_token = response.data.access
            localStorage.setItem(LOCALSTORAGE_TOKEN_KEY, access_token)

            refresh_token = response.data.refresh
            localStorage.setItem(LOCALSTORAGE_REFRESH_TOKEN_KEY, refresh_token)

            localStorage.setItem(LOCALSTORAGE_TOKEN_TIMESTAMP, Date.now().toString())
            api.defaults.headers.common["Authorization"] = "Bearer " + access_token
            console.log("Token has been successfully refreshed!")
            return api(originalRequest)
          }
        })
        .catch((refreshError) => {
          console.error("Failed to refresh token", refreshError)
          return Promise.reject(refreshError)
        })
    }

    if (status === 403 && !originalRequest._retry) {
      console.error("403 Forbidden Error:", error)
    }

    console.error("API Error:", error)
    return Promise.reject(error)
  }

  console.error("Unexpected Error:", error)
  return Promise.reject(error)
})

export default {
  user,
  login(payload) {
    if (!payload.username || !payload.password) {
      return Promise.reject("Username and password are required.")
    }

    return api.post(`dj-rest-auth/login/`, payload).then((response) => {
      access_token = response.data.access_token
      refresh_token = response.data.refresh_token
      localStorage.setItem(LOCALSTORAGE_TOKEN_KEY, access_token)
      localStorage.setItem(LOCALSTORAGE_REFRESH_TOKEN_KEY, refresh_token)
      localStorage.setItem(LOCALSTORAGE_TOKEN_TIMESTAMP, Date.now().toString())
      user.value = response.data.user
      return response.data.user
    })
  },
  logout() {
    return api.post(`dj-rest-auth/logout/`).then((response) => {
      access_token = undefined
      refresh_token = undefined
      localStorage.removeItem(LOCALSTORAGE_TOKEN_KEY)
      localStorage.removeItem(LOCALSTORAGE_REFRESH_TOKEN_KEY)
      localStorage.removeItem(LOCALSTORAGE_TOKEN_TIMESTAMP)
      user.value = undefined
      return response.data
    })
  },
  register(payload) {
    if (!payload.username || !payload.password1 || !payload.password2 || !payload.email) {
      return Promise.reject("Username, password1, password2, and email are required.")
    }
  
    return api.post(`dj-rest-auth/registration/`, payload)
      .then((response) => {
        if (response.data && response.data.access_token && response.data.refresh_token) {
          access_token = response.data.access_token;
          refresh_token = response.data.refresh_token;
          localStorage.setItem(LOCALSTORAGE_TOKEN_KEY, access_token);
          localStorage.setItem(LOCALSTORAGE_REFRESH_TOKEN_KEY, refresh_token);
          localStorage.setItem(LOCALSTORAGE_TOKEN_TIMESTAMP, Date.now().toString());
  
          if (response.data.user) {
            user.value = response.data.user;
            return response.data.user;
          } else {
            throw new Error("User data is missing in the response");
          }
        } else {
          throw new Error("Access token or refresh token is missing in the response");
        }
      })
      .catch((error) => {
        console.error("Error during registration: ", error);
        throw error; // re-throw the error to be handled in Vue component
      });
  },
  
  // allows to relogin with saved token
  getUser() {
    return api.get(`dj-rest-auth/user/`).then((response) => {
      user.value = response.data
      // console.log(user.value)
      return user.value
    })
  },
  checkTokenExpiry() {
    const tokenTimestamp = parseInt(localStorage.getItem(LOCALSTORAGE_TOKEN_TIMESTAMP))
    const refreshExpiryTime = 24 * 60 * 60 * 1000 // Refresh token lifetime

    if (Date.now() - tokenTimestamp > refreshExpiryTime) {
      // The tokens have expired, clear them
      localStorage.removeItem(LOCALSTORAGE_TOKEN_KEY)
      localStorage.removeItem(LOCALSTORAGE_REFRESH_TOKEN_KEY)
      localStorage.removeItem(LOCALSTORAGE_TOKEN_TIMESTAMP)
      user.value = undefined
    }
  }
}
