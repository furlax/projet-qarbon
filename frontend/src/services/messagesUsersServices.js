import api from "@/services/api"

export default {
  fetchMessagesUsers() {
    return api.get(`messagesusers/`).then((response) => response.data)
  },
  async postMessage(token, id, content) {
    const headers = { Authorization: `Bearer ${token}` }
    try {
      await api.post(`/messagesusers/${id}/send_message/`, { content }, { headers })
    } catch (err) {
      throw err.response.data
    }
  },
  fetchMessagesUsersDetail(id) {
    return api.get(`messagesusers/?sender=${id}/`).then((response) => response.data)
  },
  fetchUsersMessages(token) {
    const headers = { Authorization: `Bearer ${token}` }
    return api.get("messagesusers/messages/", { headers })
  },
  async deleteMessage(token, id) {
    const headers = { Authorization: `Bearer ${token}` }
    try {
      await api.put(`messagesusers/${id}/delete_messages/`, { headers })
    } catch (err) {
      throw err.response.data
    }
  }
}
