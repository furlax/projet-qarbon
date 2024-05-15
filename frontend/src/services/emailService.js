import api from "@/services/api"

export default {
  async sendNotification(eventId, subject, message) {
    const token = localStorage.getItem("access_token")
    try {
      await api.post(
        `/events/${eventId}/send_notification/`,
        {
          subject: subject,
          message: message
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )
    } catch (error) {
      console.error(error)
    }
  }
}
