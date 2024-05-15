<template>
  <div id="content">
    <div class="container">
      <div class="row align-items-center mt-5">
        <div class="col-lg-6 mb-5">
          <div>
            <h1 style="color: black; text-align: left; font-weight: bold; font-size: 50px">
              Find your favorite student events in
              <span
                style="
                  background: linear-gradient(to right, #42b983, lightgreen);
                  -webkit-background-clip: text;
                  -webkit-text-fill-color: transparent;
                "
                >seconds!</span
              >
              <button
                @click="redirectRegister"
                class="btn btn-success ms-4 mb-2"
                style="font-size: 20px; font-weight: bold"
              >
                Get started
              </button>
            </h1>
            <!-- <p class="lead" style="text-align: left; font-weight: bold; font-size: 25px;">
              We are dedicated to bringing you the latest and greatest events in town. 
            </p> -->
          </div>
        </div>
        <div class="col-lg-5 p-0">
          <div
            id="carouselExampleCaptions"
            class="carousel slide carousel-fade"
            data-bs-ride="carousel"
          >
            <div class="carousel-indicators">
              <button
                v-for="(event, index) in events"
                :key="event.id"
                type="button"
                data-bs-target="#carouselExampleCaptions"
                :data-bs-slide-to="index"
                :class="{ active: index === 0 }"
                :aria-label="'Slide ' + (index + 1)"
              ></button>
            </div>
            <div class="carousel-inner">
              <div
                v-for="(event, index) in events"
                :key="event.id"
                class="carousel-item"
                :class="{ active: index === 0 }"
              >
                <img :src="event.image" class="d-block w-100" :alt="event.name" />
                <div class="carousel-caption d-none d-md-block">
                  <h5>{{ event.name }}</h5>
                  <p>{{ event.description }}</p>
                </div>
              </div>
            </div>
            <button
              class="carousel-control-prev"
              type="button"
              data-bs-target="#carouselExampleCaptions"
              data-bs-slide="prev"
            >
              <span class="carousel-control-prev-icon" aria-hidden="true"></span>
              <span class="visually-hidden">Previous</span>
            </button>
            <button
              class="carousel-control-next"
              type="button"
              data-bs-target="#carouselExampleCaptions"
              data-bs-slide="next"
            >
              <span class="carousel-control-next-icon" aria-hidden="true"></span>
              <span class="visually-hidden">Next</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import axios from "axios"
import eventService from "../services/eventService"
import authService from "../services/authService"

export default {
  data() {
    return {
      events: []
    }
  },
  async created() {
    try {
      const response = await eventService.fetchEvents()
      this.events = response.data
      // const response = await axios.get("http://127.0.0.1:8000/api/events/")
      // this.events = response.data
      console.log(this.events)
    } catch (error) {
      console.error(error)
    }
  },
  computed: {
    user() {
      return authService.user.value ? authService.user.value : null
    }
  },
  methods: {
    redirectRegister() {
      if (this.user) {
        this.$router.push("/event-list")
      } else {
        this.$router.push("/register")
      }
    }
  }
}
</script>

<style scoped>
h1 {
  padding-bottom: 170px !important;
}
.carousel {
  box-shadow: 0 0 13px 2px rgba(0, 0, 0, 0.7);
  border-radius: 10px;
}
.carousel .carousel-item img {
  border-radius: 10px;
}

.carousel-caption {
  background-color: rgba(0, 0, 0, 0.6);
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.carousel-caption h5 {
  font-size: 1.5rem;
}

.carousel-caption p {
  font-size: 1.25rem;
}
</style>
