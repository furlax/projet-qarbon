<template>
  <div id="content">
    <div v-if="error">
      <p>Une erreur est survenue: {{ error }}</p>
    </div>
    <div v-else>
      <h1>Events</h1>
      <div class="filterBar">
        <div class="inputFilter">
          <input v-model="searchEvent" @input="filterEventsDebounced" placeholder="Event name" />
          <input v-model="searchPlace" @input="filterEventsDebounced" placeholder="Place name" />
          <input v-model="searchUser" @input="filterEventsDebounced" placeholder="Username" />
          <button class="buttonSee" @click="resetFilters">RESET</button>
        </div>
        <div v-if="user">
          <select class="buttonSee ms-3" v-model="filterStatus" @change="filterEvents">
            <option value="all">All</option>
            <option value="registered">Registered</option>
            <option value="unregistered">Unregistered</option>
          </select>
        </div>

        <!-- <button class="btn btn-success" style="margin-left: 10px" @click="filterEvents">
        FILTER
      </button> -->
      </div>

      <div class="row justify-content-center">
        <div v-for="event in events" :key="event.id" class="col-md-4">
          <div class="card">
            <img :src="event.image" alt="event image" class="card-img-top" />
            <div class="card-body">
              <ul class="list-group list-group-flush">
                <li class="list-group-item">
                  <h5 class="card-title" style="color: var(--main-color)">{{ event.name }}</h5>
                </li>
                <br />
                <li class="list-group-item">
                  <h5 class="card-subtitle">
                    {{ getPlace(event.place).name }}
                  </h5>
                  <p class="subtitle-text">
                    {{ getPlace(event.place).address }}
                    {{ getPlace(event.place).postal_code }}
                    {{ getPlace(event.place).locality }},
                    <br />
                    Number of participants : {{ event.participants.length }}
                  </p>
                  <p style="font-weight: bold;" class="subtitle-text">
                    {{ formatDate(event.date) }} -
                    {{ formatTime(event.date) }}
                  </p>
                </li>
                <li class="list-group-item">
                  <div>
                    <RouterLink :to="'/event-detail/' + event.id">
                      <button class="buttonSee">See more</button>
                    </RouterLink>
                  </div>
                </li>
              </ul>
              <!-- Vous pouvez afficher plus d'informations sur l'événement ici -->
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <br />
</template>

<script>
import authService from "../services/authService"
import eventService from "../services/eventService"
import placeService from "../services/placeService"
import _ from "lodash"
import { library } from "@fortawesome/fontawesome-svg-core"
import { faUserSecret } from "@fortawesome/free-solid-svg-icons"
import { faTwitter } from "@fortawesome/free-brands-svg-icons"
import { faFacebook } from "@fortawesome/free-brands-svg-icons"
import { faWhatsapp } from "@fortawesome/free-brands-svg-icons"
library.add(faUserSecret, faTwitter, faFacebook, faWhatsapp)

export default {
  name: "createEvents",
  data() {
    return {
      searchEvent: "",
      searchPlace: "",
      searchUser: "",
      error: null,
      userFind: null,
      events: [],
      places: [],
      users: [],
      filterStatus: "all"
    }
  },
  async mounted() {
    const response = await placeService.fetchPlaces()
    this.places = response.data
    this.filterEvents()
  },
  computed: {
    user() {
      return authService.user.value ? authService.user.value : null
    }
  },
  methods: {
    filterEventsDebounced: _.debounce(function () {
      this.filterEvents()
    }, 250),

    getPlace(placeId) {
      return this.places.find((place) => place.id === placeId) || {}
    },
    isEventFull(event) {
      return event.participants.length >= event.capacity
    },
    logout() {
      authService.logout()
    },
    async filterEvents() {
      try {
        this.events = await eventService.filterEvents({
          name: this.searchEvent,
          place_name: this.searchPlace,
          user: this.searchUser
        })

        if (this.filterStatus === "registered") {
          this.events = this.events.filter((event) => this.isUserRegistered(event))
        } else if (this.filterStatus === "unregistered") {
          this.events = this.events.filter((event) => !this.isUserRegistered(event))
        }
        this.events.sort((a, b) => new Date(b.date) - new Date(a.date))
      } catch (err) {
        this.error = err
      }
    },
    resetFilters() {
      this.searchEvent = ""
      this.searchPlace = ""
      this.searchUser = ""
      this.filterEvents()
    },
    eventUrl(index) {
      return `http://localhost:5173/#/events/${index}`
    },
    eventUrlTitle(Event) {
      return `Check out ${Event.name} on our plateform !`
    },
    async registerForEvent(id) {
      const token = localStorage.getItem("access_token")
      try {
        await eventService.registerForEvent(id, this.place, token)
        await this.filterEvents()
      } catch (err) {
        this.error = err
      }
    },
    isUserRegistered(event) {
      return event.participants.some((participant) => participant.id === this.user.pk)
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString("fr-CH", {
        year: "numeric",
        month: "long",
        day: "numeric"
      })
    },
    formatTime(date) {
      return new Date(date).toLocaleTimeString("fr-CH", {
        hour: "numeric",
        minute: "numeric"
      })
    }
  },
  components: {}
}
</script>

<style scoped>
h1 {
  font-size: 30px;
  text-transform: uppercase;
  letter-spacing: 2.5px;
  font-weight: 20px;
  color: #000;
  margin-bottom: 30px;
  padding-top: 30px;
  color: var(--main-color);
}

select option {
  color: black;
  background-color: white;
  text-emphasis-color: white;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 2.5px;
  font-weight: 500;
  white-space: pre;
  min-height: 20px;
  border-radius: 20px;
}

input {
  margin-right: 10px;
  height: 34px;
  width: 200px;
  margin-bottom: 30px;
  text-align: center;
  border-radius: 9px;
  text-emphasis-color: white;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 2.5px;
  font-weight: 500;
  color: #000;
}

.inputFilter {
  width: auto;
  height: 40px;
  border-radius: 5px;
  padding-left: 10px;
  font-size: 16px;
}

.filterBar {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
  width: auto;
}

.card:hover .card-img-top {
  transform: scale(1.05);
}

.card-img-top {
  transition: transform 0.2s; /* Animation */
}

.card-img-top {
  max-height: 250px;
  max-width: 100%;
  object-fit: cover;
}

.col-md-4 {
  padding-left: 15px;
  padding-right: 15px;
  margin-bottom: 30px;
}

.col-md-6 {
  padding-left: 15px;
  padding-right: 15px;
  /* margin-bottom: 30px; */
}

.card {
  overflow: hidden;
  justify-content: space-between;
  border-radius: 8px;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
  transition: box-shadow 0.5s;
  width: auto;
}

.card:hover {
  box-shadow: 0 4px 8px grey;
}

.card-body {
  flex-grow: 1;
}

.card-title {
  font-size: 20px;
  font-weight: bold;
  /* margin-bottom: 10px; */
}

.card-subtitle {
  font-size: 17px;
  font-weight: bold;
  /* margin-bottom: 10px; */
  text-align: left;
}

.subtitle-text {
  text-align: left;
}
/* .no-padding {
  padding: 0 !important;
  margin: 0 !important;
} */

.w-100 {
  align-items: end;
  align-content: center;
}

.card-text {
  font-size: 16px;
}
.main-color {
  color: var(--main-color);
}

.icon {
  font-size: 30px;
  margin: 10px;
}
</style>
