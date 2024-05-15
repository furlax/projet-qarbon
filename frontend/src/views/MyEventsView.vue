<template>
  <div id="content">
    <div v-if="error">
      <p>An error occurred: {{ error }}</p>
    </div>
    <div v-if="!events || events.length === 0">
      <h2>You didn't create any events</h2>
    </div>
    <div v-else>
      <h1>My Events</h1>
      <div class="row justify-content-center">
        <div v-for="event in events" :key="event.id" class="col-md-4">
          <div class="card mb-3 position-relative">
            <div class="position-relative">
              <img :src="event.image" alt="event image" class="card-img-top" />
              <button
                class="btn btn-success position-absolute top-50 start-50 translate-middle"
                @click="openModal(event.id)"
              >
                Notify Participants
              </button>
            </div>
            <button
              class="btn btn-danger position-absolute top-0 start-0"
              @click="deleteEvent(event.id)"
            >
              Delete
            </button>
            <div class="card-body">
              <ul class="list-group list-group-flush">
                <li class="list-group-item">
                  <h5 class="card-title">{{ event.name }}</h5>
                </li>
                <li class="list-group-item">
                  <h6 class="card-subtitle">
                    {{ getPlace(event.place).name }}
                  </h6>
                  <p class="card-text">
                    {{ getPlace(event.place).address }}
                    {{ getPlace(event.place).postal_code }}
                    {{ getPlace(event.place).locality }},
                    <br />
                    Number of participants: {{ event.participants.length }}
                  </p>
                  <p class="card-text">
                    {{ formatDate(event.date) }} -
                    {{ formatTime(event.date) }}
                  </p>
                </li>
                <li class="list-group-item">
                  <div>
                    <router-link :to="'/event-detail/' + event.id">
                      <button class="buttonSee">See more</button>
                    </router-link>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-if="showModal" class="modal d-block" style="background-color: rgba(0, 0, 0, 0.5)">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" style="color: var(--main-color); font-weight: bold">
            Let them know how great your event will be !
          </h5>
          <button type="button" class="btn-close" @click="closeModal"></button>
        </div>
        <div class="modal-body">
          <form>
            <div class="mb-3">
              <label for="subjectInput" class="form-label" style="font-weight: bold">Subject</label>
              <input type="text" class="form-control" id="subjectInput" v-model="subject" />
            </div>
            <div class="mb-3">
              <label for="messageInput" class="form-label" style="font-weight: bold">Message</label>
              <textarea class="form-control" id="messageInput" v-model="message"></textarea>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closeModal">Close</button>
          <button type="button" class="btn btn-success" @click="sendNotification">Send</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import eventService from "../services/eventService"
import placeService from "../services/placeService"
import emailService from "../services/emailService"

export default {
  name: "MyEvents",
  data() {
    return {
      error: null,
      events: [],
      places: [],
      showModal: false,
      subject: "",
      message: "",
      currentEventId: null
    }
  },

  async mounted() {
    const token = localStorage.getItem("access_token")
    try {
      const response_events = await eventService.fetchMyevents(token)
      this.events = response_events.data
      console.log(this.events)
      const response_places = await placeService.fetchPlaces()
      this.places = response_places.data
    } catch (error) {
      this.error = error.message
    }
  },
  methods: {
    async sendNotification() {
      try {
        await emailService.sendNotification(this.currentEventId, this.subject, this.message)
        this.closeModal()
      } catch (error) {
        console.error(error)
      }
    },
    openModal(eventId) {
      this.currentEventId = eventId
      this.showModal = true
    },
    closeModal() {
      this.currentEventId = null
      this.showModal = false
    },
    toggleModal(eventId) {
      this.currentEventId = eventId
      this.showModal = !this.showModal
    },
    async deleteEvent(id) {
      const token = localStorage.getItem("access_token")
      try {
        await eventService.deleteEvent(id, token)
        this.events = this.events.filter((event) => event.id !== id)
      } catch (error) {
        this.error = error.message
      }
    },

    getPlace(placeId) {
      return this.places.find((place) => place.id === placeId) || {}
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
  }
}
</script>

<style scoped>
h1 {
  font-size: 30px;
  text-transform: uppercase;
  letter-spacing: 2.5px;
  font-weight: bold;
  margin-bottom: 30px;
  color: var(--main-color);
}

h2 {
  font-size: 30px;
  text-transform: uppercase;
  letter-spacing: 2.5px;
  font-weight: bold;
  margin-bottom: 30px;
  color: var(--main-color);
}

.card {
  border-radius: 8px;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
  transition: box-shadow 0.5s;
}

.card:hover {
  box-shadow: 0 4px 8px grey;
}

.card-img-top {
  max-height: 250px;
  object-fit: cover;
}

.card-body {
  flex-grow: 1;
}

.card-title {
  font-size: 20px;
  font-weight: bold;
}

.card-subtitle {
  font-size: 17px;
  font-weight: bold;
}

.card-text {
  font-size: 16px;
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
