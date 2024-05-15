<template>
  <div id="content">
    <nav class="navbar navbar-expand-lg navbar-light">
      <div id="nav" class="container-fluid">
        <router-link class="navbar-brand ms-3 fs-2 p-0" to="/">Qarbon</router-link>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'event-list' }">See events</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'place-list' }">See places</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'create-place' }"
                >Create a place</router-link
              >
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'event-create' }"
                >Create an event</router-link
              >
            </li>
          </ul>
          <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
            <li class="nav-item" v-if="!user">
              <router-link class="nav-link" :to="{ name: 'login' }">Sign in</router-link>
            </li>
            <li class="nav-item" v-else>
              <div class="nav-item dropdown">
                <a
                  class="nav-link dropdown-toggle"
                  role="button"
                  data-bs-toggle="dropdown"
                  aria-haspopup="true"
                  aria-expanded="false"
                >
                  <span class="me-2">Signed in as {{ capitalizeFirstLetter(user.username) }}</span>
                </a>
                <div class="dropdown-menu dropdown-menu-end">
                  <a class="dropdown-item" @click="$router.push('/my-events')">My Events</a>
                  <a class="dropdown-item">Edit Profile</a>
                  <a class="dropdown-item" @click="$router.push('/myinbox')">My Inbox</a>
                  <div class="dropdown-divder"></div>
                  <a class="dropdown-item" @click="logout">Sign out</a>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
  <router-view />
</template>


<script>
import authService from "../src/services/authService"
import { LOCALSTORAGE_TOKEN_KEY } from "../src/services/authService"

export default {
  data() {
    return {}
  },
  computed: {
    user() {
      return authService.user.value
    }
  },
  methods: {
    capitalizeFirstLetter(string) {
      return string.charAt(0).toUpperCase() + string.slice(1)
  },
    async logout() {
      console.log("Logging out...")
      try {
        await authService.logout()
        console.log("Logged out")
        this.$router.push("/")
      } catch (err) {
        console.error("Logout failed:", err)
      }
    }
  },
  async mounted() {
    // authService
    authService.checkTokenExpiry()
    if (localStorage.getItem(LOCALSTORAGE_TOKEN_KEY)) {
      try {
        await authService.getUser()
        // this.messages = await messageService.fetchMessages()
      } catch (error) {
        console.log("Error fetching user", error)
      }
    }
  }
}
</script>
<style>
.dropdown-item:hover,
.dropdown-item:focus {
  background-color: #42b983 !important;
  color: #fff !important;
}

.dropdown-divider {
  border-top-color: #42b983;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#background {
  position: fixed;
  z-index: -1;
  width: 100vw;
  height: 100vh;
}

#content {
  margin-left: 10%;
  margin-right: 10%;
}

#nav {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.nav-link {
  transition: transform 0.3s ease;
}

.nav-link:hover {
  transform: scale(1.1);
  color: #42b983;
}

#nav a {
  font-weight: bold;
  color: #2c3e50; 
}

#nav a.router-link-exact-active {
  color: #42b983;
}

.buttonSee {
  margin-top: 10px;
  padding: 0.9em 1em;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 2.5px;
  font-weight: 500;
  color: #000;
  background-color: #fff;
  border: 0.5px solid gray;
  border-radius: 45px;
  /* box-shadow: 0px 8px 5px rgba(0, 0, 0, 0.1); */
  transition: all 0.3s ease 0s;
  cursor: pointer;
  outline: none;
}

.buttonSee:hover {
  background-color: var(--main-color);
  box-shadow: 0px 15px 20px rgba(46, 229, 157, 0.4);
  color: #fff;
  transform: translateY(-2px);
}

.buttonSee:active {
  transform: translateY(-1px);
}
</style>
