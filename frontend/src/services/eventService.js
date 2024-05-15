import api, { apiImage } from "./api"

export default {
  async createEvent(event, token) {
    const headers = { Authorization: `Bearer ${token}` }
    const formData = new FormData()
    for (let key in event) {
      formData.append(key, event[key])
    }
    try {
      await apiImage.post("/events/", formData, { headers })
    } catch (err) {
      throw err.response.data
    }
  },

  async fetchEvents() {
    return api.get(`events/`)
  },
  async filterEvents(filters) {
    let url = "/events/?"
    if (filters.name) {
      url += `name=${filters.name}&`
    }
    if (filters.place_name) {
      url += `place_name=${filters.place_name}&`
    }
    if (filters.user) {
      url += `user=${filters.user}`
    }

    try {
      const events = await api.get(url)
      return events.data
    } catch (err) {
      throw err.response.data
    }
  },

  async registerForEvent(id, place, token) {
    const headers = { Authorization: `Bearer ${token}` }
    const formData = new FormData()
    for (let key in place) {
      formData.append(key, place[key])
    }
    try {
      await api.post(`/events/${id}/register/`, formData, { headers })
    } catch (err) {
      throw err.response.data
    }
  },
  async fetchMyevents(token) {
    const headers = { Authorization: `Bearer ${token}` }
    return api.get(`/myevents`, { headers })
  },

  checkUserRegistered(event, userId) {
    for (let participant of event.participants) {
      if (participant.id === userId) {
        return true
      }
    }
    return false
  },
  eventDetail(eventId) {
    return api.get(`/events/${eventId}/`)
  },
  async deleteEvent(id, token) {
    const headers = { Authorization: `Bearer ${token}` }
    try {
      await api.delete(`/events/${id}/`, { headers })
    } catch (err) {
      throw err.response.data
    }
  },
  async unregisterEvent(id, token) {
    const headers = { Authorization: `Bearer ${token}` }
    try {
      await api.delete(`/events/${id}/unregister/`, { headers })
    } catch (err) {
      throw err.response.data
    }
  },
  async isUserOnWaitingList(eventId) {
    try {
      const response = await api.get(`/events/${eventId}/isUserOnWaitingList/`)
      return response.data
    } catch (err) {
      throw err.response.data
    }
  }
}
