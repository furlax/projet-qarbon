<template>
  <div class="row justify-content-center">
    <div class="col-md-4">
      <div class="card">
        <img :src="event.image" alt="event image" class="card-img-top" />
        <div class="card-body">
          <ul class="list-group list-group-flush">
            <li class="list-group-item">
              <h5 class="card-title" style="color: var(--main-color)">
                {{ event.name }}
              </h5>
            </li>
            <br />
            <li class="list-group-item">
              <h5 class="card-subtitle">
                {{ event.description }}
              </h5>
              <br />
              <p class="subtitle-text"></p>
            </li>
            <li class="list-group-item" style="margin-top: 10px">
              <h5 class="card-subtitle">
                {{ getPlace(event.place).name }}
              </h5>
              <p class="subtitle-text">
                {{ getPlace(event.place).street }}, {{ getPlace(event.place).number }}
              </p>
              <p class="subtitle-text" style="margin-top: -15px">
                {{ getPlace(event.place).postal_code }}
                {{ getPlace(event.place).locality }}
              </p>
              <p class="subtitle-text" style="margin-top: 0px">
                {{ formatDate(event.date) }} -
                {{ formatTime(event.date) }}
              </p>
            </li>
            <li class="list-group-item" style="margin-top: 10px">
              <div class="card-subtitle">
                Number of participants :
                {{ participants.length }} /
                {{ event.capacity }}
              </div>
            </li>
            <li class="list-group-item" style="margin-top: 10px">
              <div class="test">
                <button @click="showParticipants = !showParticipants" class="buttonSee">
                  participants
                </button>
              </div>
              <div v-if="showParticipants">
                <div class="participants-section">
                  <div class="oneComment" v-for="p in participants" :key="p.id">
                    <div class="CommentText">
                      {{ p.username }}
                    </div>
                  </div>
                </div>
              </div>
            </li>
            <div v-if="user">
              <li class="list-group-item" style="margin-top: 10px">
                <button
                  v-if="!isUserRegistered(participants) && !isEventFull(event, participants)"
                  @click="registerForEvent(event.id)"
                  class="buttonSee test2"
                >
                  Register
                </button>
                <p v-else-if="isUserRegistered(participants)" class="text">
                  <button class="buttonSee" @click="unregisterForEvent(event.id)">
                    Unregistered
                  </button>
                  <br />
                  <br />
                  You are already registered
                </p>
                <p v-else-if="isUserOnWaitingList" class="text">You are on the waiting list</p>
                <p v-else class="text">
                  <button class="buttonSee" @click="registerForEvent(event.id)">WaitingList</button>
                  <br />
                  <br />
                  The event is full
                </p>
              </li>
            </div>
            <div v-else class="text">
              <p>You need to be logged in to register</p>
            </div>
            <li class="list-group-item" style="margin-top: 10px">
              <div class="d-flex justify-content-evenly">
                <ShareNetwork
                  network="twitter"
                  :url="eventUrl(event.id)"
                  :title="eventUrlTitle(event)"
                  :description="eventDesc(event)"
                  twitter-user="qarbon"
                >
                  <button class="transparent-button">
                    <span
                      ><font-awesome-icon icon="fa-brands fa-twitter" class="icon main-color"
                    /></span>
                  </button>
                </ShareNetwork>

                <ShareNetwork
                  network="facebook"
                  :url="eventUrl(event.id)"
                  :title="eventUrlTitle(event)"
                  :description="eventDesc(event)"
                >
                  <button class="transparent-button">
                    <font-awesome-icon icon="fa-brands fa-facebook" class="icon main-color" />
                  </button>
                </ShareNetwork>

                <ShareNetwork
                  network="whatsapp"
                  :url="eventUrl(event.id)"
                  :title="eventUrlTitle(event)"
                  :description="eventDesc(event)"
                >
                  <button class="transparent-button">
                    <font-awesome-icon icon="fa-brands fa-whatsapp" class="icon main-color" />
                  </button>
                </ShareNetwork>
              </div>
            </li>
          </ul>
          <!-- Vous pouvez afficher plus d'informations sur l'événement ici -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import authService from "../services/authService"
import eventService from "../services/eventService"
import placeService from "../services/placeService"
// import api from "../services/api"
import { ShareNetwork } from "vue-social-sharing"
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome"
import { library } from "@fortawesome/fontawesome-svg-core"
import { faUserSecret } from "@fortawesome/free-solid-svg-icons"
import { faTwitter } from "@fortawesome/free-brands-svg-icons"
import { faFacebook } from "@fortawesome/free-brands-svg-icons"
import { faWhatsapp } from "@fortawesome/free-brands-svg-icons"
import { faUser } from "@fortawesome/free-solid-svg-icons"
library.add(faUserSecret, faTwitter, faFacebook, faWhatsapp, faUser)

export default {
  data() {
    return {
      error: null,
      event: [],
      //place: [],
      places: [],
      userPublisher: "",
      userCo: "",
      participants: [],
      isUserOnWaitingList: false,
      showParticipants: false
    }
  },
  async mounted() {
    const eventId = this.$route.params.id
    this.fetchEvent(eventId)
    const resp = await placeService.fetchPlaces()
    this.places = resp.data
    this.checkUserIsOnWaitList(eventId)
  },
  computed: {
    user() {
      return authService.user.value ? authService.user.value : null
    }
  },
  methods: {
    async checkUserIsOnWaitList(eventId) {
      const resp = await eventService.isUserOnWaitingList(eventId)
      this.isUserOnWaitingList = resp.status
    },

    logout() {
      authService.logout()
    },
    eventUrl(id) {
      return window.location.href + id
    },
    eventUrlTitle(event) {
      return "Event : " + event.name
    },
    eventDesc(event) {
      return "Description : " + event.description
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
    },
    isUserRegistered(participants) {
      for (let participant of participants) {
        if (participant.id === this.user.pk) {
          return true
        }
      }
      return false
    },
    async registerForEvent(id) {
      const token = localStorage.getItem("access_token")
      try {
        await eventService.registerForEvent(id, this.place, token)
        await this.fetchEvent(id)
        await this.checkUserIsOnWaitList(id)
      } catch (err) {
        this.error = err
      }
    },
    isEventFull(event, participants) {
      return participants.length >= event.capacity
    },
    async fetchEvent(eventId) {
      const response = await eventService.eventDetail(eventId)
      this.event = response.data
      //this.place = response.data.place
      this.userPublisher = response.data.user.username
      this.participants = response.data.participants
    },
    getPlace(placeId) {
      return this.places.find((place) => place.id === placeId) || {}
    },
    shareOnWhatsapp() {
      let message = `Check out this awesome place: ${this.event.name} - ${this.eventUrl(
        this.event.id
      )}`
      let whatsappUrl = `https://wa.me/?text=${encodeURIComponent(message)}`
      window.location.href = whatsappUrl
    },
    shareOnFacebook() {
      let url = this.eventUrl(this.event.id)
      let facebookUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`
      window.location.href = facebookUrl
    },
    shareOnTwitter() {
      let url = this.eventUrl(this.event.id)
      let text = `${this.event.name} - Check out this place!`
      let twitterUrl = `https://twitter.com/intent/tweet?url=${encodeURIComponent(
        url
      )}&text=${encodeURIComponent(text)}&via=qarbon`
      window.location.href = twitterUrl
    },
    async unregisterForEvent(id) {
      const token = localStorage.getItem("access_token")
      try {
        await eventService.unregisterEvent(id, token)
        await this.fetchEvent(id)
      } catch (err) {
        this.error = err
      }
    }
  },
  components: {
    FontAwesomeIcon,
    ShareNetwork
  }
}
</script>

<style scoped>
.test2{
  margin-top: 20px;
  margin-bottom: 20px;
}
.test{
  margin-bottom: 20px;
}

.participants-section {
  max-height: 25vh;
  max-width: 90%;
  background-color: #ffffff;
  width: auto;
  border-radius: 8px;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.5s;
  overflow: hidden;
  margin-top: 20px;
  margin-bottom: 20px;
  margin-left: 35px;
  align-items: center;
  overflow-y: scroll;
}

.participants-section::-webkit-scrollbar {
  display: none;
}
.oneComment {
  margin: 10px;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.5s;
  overflow: hidden;
  margin-top: 20px;
  margin-bottom: 20px;
  align-items: center;
}

.CommentText {
  margin-left: 10px;
  margin-top: 10px;
  margin-bottom: 10px;
  font-size: 15px;
  font-weight: 400;
  color: #000000;
  line-height: 1.5;
  text-align: center;
  width: auto;
  background-color: transparent;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 500;
  color: #000;
  font-size: 12px;
}

.text {
  margin-top: 10px;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 2.5px;
  font-weight: 500;
  color: #000;
  background-color: #fff;
}

.transparent-button {
  background-color: transparent;
  border: none;
  cursor: pointer;
  outline: none;
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
  font-size: 20px;
  margin: 10px;
}

.buttonSee {
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
