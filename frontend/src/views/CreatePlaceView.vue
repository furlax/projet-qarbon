<template>
  <div id="content">
    <div class="create-place">
      <div class="card shadow-lg bg-white rounded">
        <div class="card-body">
          <form @submit.prevent="submitForm" class="event-form">
            <h2 class="mb-4 text-center" style="color: var(--main-color)">Create a new place</h2>
            <div class="col-lg-6">
              <input
                class="form-control"
                type="text"
                placeholder="Place name"
                v-model="place.name"
              />
              <span class="input-group">
                <input
                  class="form-control"
                  type="text"
                  placeholder="Street"
                  v-model="place.street"
                />
                <input
                  class="form-control"
                  type="number"
                  placeholder="Street number"
                  v-model="place.number"
                />
              </span>
              <input
                class="form-control"
                type="number"
                placeholder="Zip code"
                v-model="place.postal_code"
              />
              <input
                class="form-control"
                type="text"
                placeholder="Locality"
                v-model="place.locality"
              />
            </div>
            <div class="col-lg-8">
              <picture-input
                v-model="form.picture"
                @src="this.src = $event"
                @change="handleFileUpload($event)"
              ></picture-input>
            </div>
            <button type="submit" id="CreateButton">Create</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import "../services/placeService"
// import { useRouter } from "vue-router"
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
      place: {
        name: "",
        street: "",
        number: "",
        postal_code: "",
        locality: ""
      },
      places: []
    }
  },
  methods: {
    handleFileUpload(event) {
      this.place.image = event.target.files[0]
    },
    async submitForm() {
      try {
        const token = localStorage.getItem("access_token")
        // const headers = { Authorization: `Bearer ${token}` }

        // const formData = new FormData()
        // for (let key in this.place) {
        //   formData.append(key, this.place[key])
        // }

        console.log(this.place)
        await placeService.createPlace(this.place, token)
        // await axios.post("http://127.0.0.1:8000/api/places/", formData, { headers })
        this.place = {
          name: "",
          street: "",
          number: 0,
          postal_code: 0,
          locality: "",
          image: null
        }
        // await this.fetchPlaces()

        // Navigate to PlaceView
        this.$router.push({ name: "place-list" })
      } catch (error) {
        console.error(error.response)
      }
    }
  },
  async mounted() {
    await placeService.fetchPlaces()
  }
}
</script>

<style scoped>
.card {
  width: 70%;
  margin: auto;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
}

h1 {
  font-size: 24px;
  margin-bottom: 20px;
}

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
  font-weight: 500;
}
.form-control {
  margin: 5px;
}
.create-place {
  padding-top: 55px;
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
</style>
