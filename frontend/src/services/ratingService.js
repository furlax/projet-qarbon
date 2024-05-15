import api from "@/services/api"

export default {
  fetchComments() {
    return api.get(`comments/`).then((response) => response.data)
  },
  async fetchCommentsByPlaceId(placeId) {
    return api.get(`comments/?place=${placeId}`).then((response) => response.data)
  }
}