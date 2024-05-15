<template>
  <div class="register">
    <div class="container">
      <div class="card custom-card shadow-lg bg-white rounded">
        <div class="card-body">
          <form class="register-form">
            <h1 style="color: var(--main-color)">Sign up</h1>
            <br />
            <div>
              <div>
                <div class="container col-lg-8">
                  <input
                    type="text"
                    id="firstName"
                    class="form-control"
                    placeholder="Username"
                    aria-label="default input example"
                    v-model="username"
                  />
                </div>
              </div>
              <div class="container col-lg-8">
                <input
                  type="email"
                  id="email"
                  class="form-control"
                  placeholder="Email"
                  aria-label="default input example"
                  v-model="email"
                />
              </div>
              <div>
                <div class="container col-lg-8">
                  <input
                    type="password"
                    id="password"
                    class="form-control"
                    aria-label="default input example"
                    placeholder="Password"
                    v-model="password"
                  />
                </div>
              </div>
              <div>
                <div class="container col-lg-8">
                  <input
                    type="password"
                    id="confirmPassword"
                    class="form-control"
                    aria-label="default input example"
                    placeholder="Confirm password"
                    v-model="confirmPassword"
                  />
                </div>
              </div>

              <div>
                <button
                  class="btn btn-success col-lg-2"
                  v-if="!user"
                  @click="register"
                  :disabled="passwordMismatch"
                >
                  Sign up
                </button>
              </div>
              <p class="error" v-if="passwordMismatch">Password do not match</p>
              <p
                class="error"
                v-if="loginError && loginError.username && loginError.username.length > 0"
              >
                {{ loginError.username[0] }}
              </p>
              <p v-if="!user">
                Already have an account ?
                <router-link to="/login" style="color: var(--main-color)">Sign in</router-link>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import authService from "../services/authService"

export default {
  data() {
    return {
      username: "",
      password: "",
      confirmPassword: "",
      passwordMismatch: false,
      email: "",
      loginError: ""
    }
  },
  methods: {
    validatePassword(password, confirmPassword) {
      this.passwordMismatch = password !== confirmPassword
    },
    register() {
      if (this.password !== this.confirmPassword) {
        this.loginError = "The passwords do not match"
        return
      }

      authService
        .register({
          username: this.username,
          password1: this.password,
          password2: this.password,
          email: this.email
        })
        .then(() => {
          this.$router.push({ name: "home" })
        })
        .catch((err) => {
          this.loginError = err.response.data
        })
    },
    Error() {
      return this.loginError
    }
  },
  watch: {
    password(newPassword) {
      this.validatePassword(newPassword, this.confirmPassword)
    },
    confirmPassword(newConfirmPassword) {
      this.validatePassword(this.password, newConfirmPassword)
    }
  },
  computed: {
    user() {
      return authService.user.value
    }
  }
}
</script>
<style scoped>
.card {
  padding-top: 30px;
  width: 40%;
  margin: auto;
}
.register .btn {
  margin: 1.5rem;
}
.register .form-control {
  margin: 5px;
}
.register {
  padding-top: 70px;
}

.error {
  color: red;
  font-size: 20px;
}
</style>
