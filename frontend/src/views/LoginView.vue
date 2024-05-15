<template>
  <div class="Login">
    <div class="container text-center col-lg-4">
      <div class="card shadow-lg bg-white rounded">
        <div class="card-body">
          <h1 style="color: var(--main-color)">Welcome back</h1>
          <br />
          <div class="container col-lg-8">
            <div class="container row-1">
              <input
                class="form-control"
                type="text"
                placeholder="Username"
                aria-label="default input example"
                v-model="username"
              />
              <input
                class="form-control"
                type="password"
                placeholder="Password"
                aria-label="default input example"
                v-model="password"
              />
            </div>
          </div>
          <br />
          <button type="button" class="btn btn-success col-lg" @click="login">Sign in</button>
          <div v-if="loginError" class="alert alert-danger" role="alert">
            <p>Wrong username or password</p>
          </div>
        </div>
        <br />
        <p style="padding-bottom: 30px" v-if="!user">
          No account ?
          <router-link style="color: var(--main-color)" to="/register">Sign up</router-link>
        </p>
      </div>
    </div>
  </div>
  <div v-if="user">
    Logged in user data:
    <pre>{{ user }}</pre>
  </div>
</template>

<script>
import authService from "../services/authService"
import { LOCALSTORAGE_TOKEN_KEY } from "../services/authService"

export default {
  data() {
    return {
      username: "",
      password: "",
      loginError: "",
      hasAccount: true
    }
  },
  computed: {
    user() {
      return authService.user.value
    }
  },
  methods: {
    async login() {
      this.loginError = ""
      try {
        await authService.login({
          username: this.username,
          password: this.password
        })
        // if the login is successful, redirect to the event list
        this.$router.push("/event-list")
      } catch (err) {
        this.loginError = err.response.data ? err.response.data : err.message
        console.error(this.loginError)
      }
    }
  },
  async mounted() {
    // authService.getUser()
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

<style scoped>
.card {
  padding-top: 30px;
  /* height: 600px;  */
  overflow: auto;
}
.form-control {
  margin: 5px;
}
.Login {
  padding-top: 70px;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
