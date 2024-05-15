<template>
  <div class="row justify-content-center">
    <div class="col-md-4">
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
            <div v-if="user">
              <button @click="showComments = !showComments" class="buttonSee">
                See comments
                <font-awesome-icon :icon="['fas', showComments ? 'arrow-up' : 'arrow-down']" />
              </button>
              <div v-if="showComments">
                <div class="comment-section">
                  <div class="oneComment" v-for="comment in comments" :key="comment.id">
                    <div class="CommentText">
                      {{ comment.text }}
                    </div>
                    <div class="commentDate">
                      {{ formatDate(comment.created_at) }},
                      {{ formatTime(comment.created_at) }}
                    </div>
                    <div class="postedCommentBy">Posted by {{ comment.user.username }}</div>
                  </div>
                </div>
              </div>
              <div class="card-body">
                <div>
                  <div class="col-6 justify-content-center">
                    <textarea
                      type="text"
                      class="input"
                      placeholder="Write a comment"
                      v-model="newComment"
                      @keyup.enter="postComment()"
                    ></textarea>
                  </div>
                  <!-- col-6 -->
                  <button @click="postComment()" class="buttonSee move" type="submit">
                    Add comment
                  </button>
                </div>
              </div>
            </div>
            <div v-else>
              <p class="text">You need to be logged in to comment. <br /></p>
              <router-link to="/login" class="buttonSee router">Login</router-link>
            </div>
            <div class="d-flex justify-content-evenly">
              
              <ShareNetwork
                network="twitter"
                :title="place.name"
                :url="placeURL(place.id)"
                description="Check out this place!"
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
                :title="place.name"
                :url="placeURL(place.id)"
                description="Check out this place!"
              >
                <button class="transparent-button">
                  <font-awesome-icon icon="fa-brands fa-facebook" class="icon main-color" />
                </button>
              </ShareNetwork>

              <shareNetwork
                network="whatsapp"
                :title="place.name"
                :url="placeURL(place.id)"
                description="Check out this place!"
              >
                <button class="transparent-button">
                  <font-awesome-icon icon="fa-brands fa-whatsapp" class="icon main-color" />
                </button>
              </shareNetwork>
            </div>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import authService from "../services/authService"
import placeService from "../services/placeService"
import commmentService from "../services/commentService"
// import api from "../services/api"
import { ShareNetwork } from "vue-social-sharing"
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome"
import { library } from "@fortawesome/fontawesome-svg-core"
import { faUserSecret } from "@fortawesome/free-solid-svg-icons"
import { faTwitter } from "@fortawesome/free-brands-svg-icons"
import { faFacebook } from "@fortawesome/free-brands-svg-icons"
import { faWhatsapp } from "@fortawesome/free-brands-svg-icons"
library.add(faUserSecret, faTwitter, faFacebook, faWhatsapp)

export default {
  data() {
    return {
      error: null,
      places: [],
      place: "",
      newComment: "",
      placeId: "",
      userId: "",
      token: "",
      comments: [],
      postedby: "",
      rating: "",
      alreadyRated: false,
      showComments: false
    }
  },
  async mounted() {
    this.placeId = this.$route.params.id
    this.fetchPlace(this.placeId)
    this.userId = this.user.pk
    this.token = localStorage.getItem("access_token")
    // this.comments = await commmentService.fetchCommentsByPlaceId(this.placeId)
    await this.filterComments()
  },
  computed: {
    user() {
      return authService.user.value
    }
  },
  methods: {
    logout() {
      authService.logout()
    },
    placeURL(id) {
      return window.location.href + id
    },
    async fetchPlace(id) {
      const response = await placeService.fetchPlaceDetail(id)
      this.place = response.data
    },
    async postComment() {
      await placeService.postCommentOnPlace(this.placeId, this.newComment, this.token)
      this.newComment = ""
      this.comments = await commmentService.fetchCommentsByPlaceId(this.placeId)
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
    async filterComments() {
      this.comments = (await commmentService.fetchCommentsByPlaceId(this.placeId)).sort(
        (a, b) => new Date(b.created_at) - new Date(a.created_at)
      )
    }
  },
  components: {
    FontAwesomeIcon,
    ShareNetwork
  }
}
</script>

<style scoped>
.text {
  font-size: 15px;
  padding-top: 20px;
}
.router {
  text-decoration: none;
  color: #000;
}

.CommentText {
  margin-left: 10px;
  margin-top: 10px;
  margin-bottom: 10px;
  font-size: 15px;
  font-weight: 400;
  color: #000000;
  line-height: 1.5;
  text-align: left;
  width: auto;
  background-color: transparent;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 500;
  color: #000;
  font-size: 12px;
}

.postedCommentBy {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
  float: right;
  width: auto;
}

.commentDate {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
  float: left;
  width: auto;
}

.main-color {
  color: var(--main-color);
}

.icon {
  font-size: 30px;
  margin: 10px;
}

.transparent-button {
  background-color: transparent;
  border: none;
  cursor: pointer;
  outline: none;
}

.comment-section {
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

.comment-section::-webkit-scrollbar {
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

textarea {
  width: 200%;
  border: none;
  background: #e8e8e8;
  height: 40%;
  border-bottom: 4px solid var(--main-color);
  transition: all 0.5s;
  border-radius: 8px;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
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

.d-flex {
  margin-top: 20px;
}
</style>
