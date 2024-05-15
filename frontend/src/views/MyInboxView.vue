<template>
  <div class="app-container">
    <div class="left-section">
      <div></div>
      <ul v-if="showOptions">
        <li v-for="option in searchOptions" :key="option.id">
          {{ option.username }}<button @click="selectUser(option)">Select</button>
        </li>
      </ul>
      <p>New conversation</p>
      <input
        type="text"
        v-model="username"
        placeholder="Search user..."
        @input="handleSearchInput"
      />
      <!-- liste des convs ici -->
      <div class="listConv">
        <div class="oneComment" v-for="conversation in conversations" :key="conversation.user.id">
          <div class="CommentText">
            <button class="buttonUser" @click="toggleConversation(conversation)">
              {{ conversation.user.username }}
            </button>
            <button class="transparent-button" @click="deleteConversation(conversation.user)">
              <FontAwesomeIcon icon="fa-close" />
            </button>
          </div>
        </div>
      </div>
      <div v-if="errorMessage">
        <h2>Error:</h2>
        <p>{{ errorMessage }}</p>
      </div>
    </div>

    <div class="right-section">
      <div v-for="conversation in conversations" :key="conversation.user.id">
        <ConversationBox
          v-if="conversation.isOpened"
          :conversation="conversation"
          @sendMessage="postMessage"
          @closeConversation="closeConversation(conversation.user)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import userService from "../services/userService"
import authService from "../services/authService"
import ConversationBox from "../components/ConversationBox.vue"
import messagesUsersServices from "../services/messagesUsersServices"

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome"
import { library } from "@fortawesome/fontawesome-svg-core"
import { faClose } from "@fortawesome/free-solid-svg-icons"
library.add(faClose)

export default {
  data() {
    return {
      username: "",
      userId: null,
      errorMessage: "",
      conversations: [],
      searchOptions: [],
      showOptions: false,
      activeConversation: null
    }
  },
  computed: {
    user() {
      return authService.user.value
    }
  },
  methods: {
    async handleSearchInput() {
      // Vérifier si le champ de recherche est vide
      if (this.username.trim() === "") {
        this.showOptions = false
        this.searchOptions = []
      } else {
        try {
          const resp = await userService.fetchUserByUsername(this.username)
          this.searchOptions = resp.data
          this.showOptions = true
        } catch (error) {
          this.errorMessage = error.message
        }
      }
    },
    selectUser(user) {
      // Vérifier si la conversation existe déjà
      const existingConversation = this.conversations.find((c) => c.user.id === user.id)
      // Si elle n'existe pas, l'ajouter
      if (!existingConversation) {
        // unshift ajoute un élément au début du tableau
        this.conversations.unshift({
          user: user,
          messages: [],
          isOpened: true
        })
      } else {
        // Si elle existe, la mettre à jour
        existingConversation.isOpened = true
      }
      this.showOptions = false
      this.searchOptions = []
      this.username = ""
    },
    deleteEmptyMessages() {
      // delete if conv created but no message sent
      const emptyConversationIndex = this.conversations.findIndex((c) => c.messages.length === 0)
      if (emptyConversationIndex !== -1) {
        this.conversations.splice(emptyConversationIndex, 1)
      }
    },
    async postMessage(user, content) {
      const token = localStorage.getItem("access_token")
      const receiver = user.id
      await messagesUsersServices.postMessage(token, receiver, content)
      this.loadMessages()
    },
    async loadMessages() {
      try {
        const token = localStorage.getItem("access_token")
        const resp = await userService.fetchMessages(token, this.user.pk)
        let newConversations = this.groupMessgagesbyUser(resp.data)
        // Keep state of the open conv
        this.conversations.forEach((oldConv) => {
          // Find the new conv
          const newConv = newConversations.find((newConv) => newConv.user.id === oldConv.user.id)
          // If the new conv exists, keep the state of the old conv
          if (newConv) {
            // Keep the state of the old conv
            newConv.isOpened = oldConv.isOpened
          }
        })
        // Update the conversations
        this.conversations = newConversations
      } catch (error) {
        this.errorMessage = error.message
      }
    },
    async fetchUser(id) {
      const token = localStorage.getItem("access_token")
      const resp = await userService.fetchUserDetail(token, id)
      this.user = resp.data
    },
    groupMessgagesbyUser(messages) {
      let groupedMessages = {}
      messages.forEach((msg) => {
        // Trouver l'autre utilisateur de la conversation
        let otherUser = msg.sender.id === this.user.pk ? msg.receiver : msg.sender
        // Ajouter l'autre utilisateur à l'objet groupedMessages
        if (!groupedMessages[otherUser.id]) {
          groupedMessages[otherUser.id] = {
            user: otherUser,
            messages: [],
            isOpened: false
          }
        }
        groupedMessages[otherUser.id].messages.push(msg)
      })
      // Convertir l'objet en tableau
      return Object.values(groupedMessages)
    },
    closeConversation(user) {
      const conversation = this.conversations.find((c) => c.user.id === user.id)
      if (conversation) {
        conversation.isOpened = false
      }
    },
    deleteConversation(user) {
      const conversationIndex = this.conversations.findIndex((c) => c.user.id === user.id)
      if (conversationIndex !== -1) {
        const conversation = this.conversations[conversationIndex]
        this.deleteFromDjango(conversation.user)
        this.conversations.splice(conversationIndex, 1)
      }
    },
    async deleteFromDjango(user) {
      const token = localStorage.getItem("access_token")
      await messagesUsersServices.deleteMessage(token, user.id)
      this.loadMessages()
    },
    toggleConversation(selectedConversation) {
      // if the conversation is already opened, close it
      this.conversations.forEach((conversation) => {
        conversation.isOpened =
          conversation === selectedConversation ? !conversation.isOpened : false
      })
    }
  },
  async mounted() {
    this.loadMessages()
  },
  components: {
    ConversationBox,
    FontAwesomeIcon
  }
}
</script>

<style scoped>
.buttonUser {
  background-color: transparent;
  border: none;
  cursor: pointer;
  outline: none;
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

.transparent-button {
  background-color: transparent;
  border: none;
  cursor: pointer;
  outline: none;
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
  width: 100%;
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

.transparent-button {
  background-color: transparent;
  border: none;
  cursor: pointer;
  outline: none;
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
.app-container {
  width: 100%;
  height: 100%;
}

.left-section {
  width: auto;
  margin-left: 100px;
}

.right-section {
  width: auto;
}

.listConv {
  max-height: 80vh;
  max-width: 90%;
  background-color: #ffffff;
  width: 15%;
  border-radius: 8px;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.5s;
  overflow: hidden;
  margin-top: 60px;
  margin-bottom: 20px;
  margin-left: 35px;
  align-items: center;
  overflow-y: scroll;
  height: 600px;
}

.listConv::-webkit-scrollbar {
  display: none;
}
</style>
