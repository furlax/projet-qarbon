<template>
  <div id="content">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="card shadow-lg p-3 mb-5 bg-white rounded">
            <div class="card-body">
              <form @submit.prevent="submitForm" class="event-form">
                <h2 class="mb-4 text-center" style="color: var(--main-color)">
                  Create a new event
                </h2>
                <div class="mb-3">
                  <input
                    type="text"
                    id="name"
                    v-model="event.name"
                    class="form-control"
                    placeholder="Enter event name"
                  />
                </div>
                <div class="mb-3">
                  <textarea
                    id="description"
                    v-model="event.description"
                    class="form-control"
                    rows="3"
                    placeholder="Describe the event"
                  ></textarea>
                </div>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="price" class="form-label">Price</label>
                    <input
                      type="number"
                      id="price"
                      v-model="event.price"
                      class="form-control"
                      placeholder="0.00"
                    />
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="date" class="form-label">Date</label>
                    <input
                      type="datetime-local"
                      id="date"
                      v-model="event.date"
                      class="form-control"
                    />
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="capacity" class="form-label">Capacity</label>
                    <input
                      type="number"
                      id="capacity"
                      v-model="event.capacity"
                      class="form-control"
                      placeholder="0"
                    />
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="place" class="form-label">Place</label>
                    <select
                      id="place"
                      v-model="event.place"
                      @change="checkPlace"
                      class="form-select"
                    >
                      <option value="new">Add a new place</option>
                      <option v-for="place in places" :key="place.id" :value="place.id">
                        {{ place.name }}
                      </option>
                    </select>
                  </div>
                </div>
                <div class="mb-3">
                  <label for="image" class="form-label">Image for the event</label>
                  <picture-input
                    v-model="form.picture"
                    @src="this.src = $event"
                    @change="handleFileUpload($event)"
                  ></picture-input>
                </div>
                <button type="submit" id="CreateButton" class="btn btn-success btn-lg btn-block">
                  Create Event
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import eventService from "../services/eventService"
import placeService from "../services/placeService"
import PictureInput from "../components/PictureInput.vue"

export default {
  components: {
    "picture-input": PictureInput
  },
  data() {
    return {
      form: {
        picture: null
      },
      src: "",
      event: {
        name: "",
        description: "",
        price: 0,
        date: "",
        place: 0,
        capacity: 0
      },
      places: [],
      newPlace: {
        name: ""
        // Add other fields for the new place here
      },
      newPlaceForm: false
    }
  },
  methods: {
    checkPlace() {
      if (this.event.place === "new") {
        this.$router.push("/create-place")
      }
    },
    handleFileUpload(event) {
      this.event.image = event.target.files[0]
    },
    async submitForm() {
      try {
        const token = localStorage.getItem("access_token")
        // const headers = { Authorization: `Bearer ${token}` }

        await eventService.createEvent(this.event, token)

        this.event = {
          name: "",
          description: "",
          price: 0,
          date: "",
          image: null,
          place: 0,
          capacity: 0
        }
      } catch (error) {
        console.error(error)
      }
      this.$router.push({ name: "event-list" })
    }
  },
  async created() {
    try {
      const response = await placeService.fetchPlaces()
      this.places = response.data
    } catch (error) {
      console.error(error)
    }
  }
}
</script>
<style scoped>

#CreateButton {
  padding: 1.3em 3em;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 2.5px;
  font-weight: 500;
  color: #000;
  background-color: #fff;
  border: none;
  border-radius: 45px;
  box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease 0s;
  cursor: pointer;
  outline: none;
  margin: 15px;
}

#CreateButton:hover {
  background-color: #23c483;
  box-shadow: 0px 15px 20px rgba(46, 229, 157, 0.4);
  color: #fff;
  transform: translateY(-7px);
}

#CreateButton:active {
  transform: translateY(-1px);
}

h2 {
  color: #050d15;
  font-weight:500;
}

.event-form .form-label {
  color: #34495e;
  font-weight: 500;
}

.event-form .form-control {
  border-color: #34495e;
  border-radius: 10px;
  transition: all 0.3s ease-in-out;
}

.event-form .form-control:focus {
  border-color: #3498db;
  box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
}

.card {
  border-radius: 10px;
}

.card-body {
  padding: 20px;
}
</style>
