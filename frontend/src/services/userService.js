import api from "@/services/api"

export default {
  fetchUserByUsername(username) {
    return api.get(`users/?username=${username}`)
  },
  fetchMessages(token, id){
    const headers = { Authorization: `Bearer ${token}` }
    return api.get(`/users/${id}/messages/`, { headers })
  },
  fetchUserDetail(token, id) {
    const headers = { Authorization: `Bearer ${token}` }
    return api.get(`users/?id=${id}/`, { headers })
  }
}
