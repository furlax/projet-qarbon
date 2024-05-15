<template>
  <div id="content">
    <div v-if="error">
      <p>Une erreur est survenue: {{ error }}</p>
    </div>
    <div v-else>
      <h1>Places</h1>
      <input v-model="searchByName" @input="filterPlacesDebounced" placeholder="name" />
      <input v-model="searchByStreet" @input="filterPlacesDebounced" placeholder="Street" />
      <input v-model="searchByLocality" @input="filterPlacesDebounced" placeholder="Locality" />

      <button class="buttonSee" @click="resetFilters">RESET</button>

      <div class="row justify-content-center">
        <div v-for="place in places" :key="place.id" class="col-md-4">
          <div class="card">
            <img :src="place.image" alt="place image" class="card-img-top" />
            <div class="card-body">
              <ul class="list-group list-group-flush">
                <li class="list-group-item">
                  <h5 class="card-title" style="color: var(--main-color)">{{ place.name }}</h5>
                </li>
                <br />
                <li class="list-group-item">
                  <h5 class="card-subtitle">{{ place.street }} {{ place.number }}</h5>
                  <p class="subtitle-text">{{ place.postal_code }} {{ place.locality }}</p>
                </li>
                <li class="list-group-item">
                  <div>
                    <RouterLink :to="'/place-detail/' + place.id">
                      <button class="buttonSee">See more</button>
                    </RouterLink>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import authService from "../services/authService"
import placeService from "../services/placeService"
import _ from "lodash"

export default {
  data() {
    return {
      error: null,
      places: [],
      searchByName: "",
      searchByLocality: "",
      searchByStreet: ""
    }
  },
  async mounted() {
    try {
      const response = await placeService.fetchPlaces()
      this.places = response.data
    } catch (err) {
      this.error = err.response.data
    }
  },
  computed: {
    user() {
      return authService.user.value
    }
  },
  methods: {
    filterPlacesDebounced: _.debounce(function () {
      this.filterPlaces()
    }, 250),
    logout() {
      authService.logout()
    },
    storeEvent(event) {
      sessionStorage.setItem("place", JSON.stringify(event))
    },
    async filterPlaces() {
      try {
        this.places = await placeService.filterPlaces({
          name: this.searchByName,
          locality: this.searchByLocality,
          street: this.searchByStreet
        })
      } catch (error) {
        this.error = error.response.data
      }
    },
    resetFilters() {
      this.searchByName = ""
      this.searchByLocality = ""
      this.searchByStreet = ""
      this.filterPlaces()
    },
    components: {}
  }
}
</script>

<style scoped>
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
.transparent-button {
  background-color: transparent;
  border: none;
  cursor: pointer;
  outline: none;
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

.card {
  overflow: hidden;
  justify-content: space-between;
  border-radius: 8px;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
  transition: box-shadow 0.5s;
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
  padding-left: 10px;
  padding-right: 10px;
  margin-bottom: 20px;
}
.card-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
}
.card-display {
  display: flex;
  flex-wrap: wrap;
  align-content: center;
  gap: 25px;
}
.PlaceView {
  padding-top: 120px;
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
