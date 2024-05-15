<template>
  <div class="box">
    <h2 v-if="hasConversation">{{ conversation.user.username }}</h2>
    <div class="comment-section">
      <div class="oneComment" v-for="message in conversation.messages" :key="message.id">
        <div v-if="message.sender.username == conversation.user.username" class="msgreceiver">
          {{ message.receiver.username }}: {{ message.content }}
        </div>
        <div v-else class="msgsender">Vous: {{ message.content }}</div>
      </div>
    </div>
    <div class="sendmess">
      <input v-model="newMessage" type="text" placeholder="Type your message..." />
      <button @click="emitSendMessage">
        <FontAwesomeIcon icon="fa-paper-plane" />
      </button>
    </div>
  </div>
</template>

<script>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome"
import { library } from "@fortawesome/fontawesome-svg-core"
import { faComment } from "@fortawesome/free-solid-svg-icons"
import { faMessage } from "@fortawesome/free-solid-svg-icons"
import { faPaperPlane } from "@fortawesome/free-solid-svg-icons"
import { faClose } from "@fortawesome/free-solid-svg-icons"
library.add(faComment, faMessage, faPaperPlane, faClose)

export default {
  props: {
    conversation: Object
  },
  data() {
    return {
      newMessage: ""
    }
  },
  methods: {
    emitSendMessage() {
      this.$emit("sendMessage", this.conversation.user, this.newMessage)
      this.newMessage = ""
    },
    emitCloseConversation() {
      this.$emit("closeConversation", this.conversation.user)
    }
  },
  computed: {
    hasConversation() {
      return !!this.conversation
    }
  },
  components: {
    FontAwesomeIcon
  }
}
</script>
<style scoped>
h2 {
  text-align: center;
  margin-top: 10px;
  margin-bottom: 10px;
  color: #000000;
  font-weight: 500;
  color: #000;
  font-size: 20px;
  background-color: transparent;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  font-weight: 100;
}

button {
  background-color: transparent;
  border: none;
  cursor: pointer;
  outline: none;
}

input {
  border-radius: 10px;
  width: 80%;
  margin-right: 10px;
}
.sendmess {
  width: auto;
  margin-top: 20px;
  border-radius: 5px;
}

.box {
  display: block;
  margin-left: 370px;
  margin-right: 370px;
  padding: 10px;
  justify-content: center;
  width: auto;
}

.msgreceiver {
  margin-left: 10px;
  margin-top: 10px;
  margin-bottom: 10px;
  color: #000000;
  text-align: left;
  width: auto;
  font-weight: 500;
  color: #000;
  font-size: 16px;
}

.msgsender {
  font-size: 16px;
  color: #999;
  margin-top: 5px;
  float: right;
  width: auto;
  font-weight: 500;
  color: #000000;
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

.comment-section {
  max-height: 50vh;
  max-width: 100%;
  background-color: #ffffff;
  width: 420px;
  border-radius: 8px;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.5s;
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
  width: 400px;
  height: 50px;
}
</style>
