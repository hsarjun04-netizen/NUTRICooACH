<template>
  <div class="chat-page">
    <div class="chat-container">
      <div class="chat-header">
        <h1>AI Nutrition Coach</h1>
        <p class="subtitle">Ask me anything about nutrition, fitness, and your health goals</p>
      </div>

      <div class="chat-box" ref="chatBox">
        <div v-if="messages.length === 0" class="chat-welcome">
          <div class="welcome-icon">&#129302;</div>
          <h3>Hi! I'm your NutriCoach AI</h3>
          <p>I can help you with:</p>
          <ul>
            <li>Personalized nutrition advice</li>
            <li>Meal suggestions based on your profile</li>
            <li>Calorie and macro calculations</li>
            <li>Fitness and health tips</li>
          </ul>
        </div>
        <div
          v-for="(msg, idx) in messages"
          :key="idx"
          class="message"
          :class="msg.role"
        >
          <div class="message-avatar">{{ msg.role === 'user' ? '&#128100;' : '&#129302;' }}</div>
          <div class="message-bubble">
            <div class="message-text">{{ msg.message }}</div>
            <div v-if="msg.created_at" class="message-time">{{ formatTime(msg.created_at) }}</div>
          </div>
        </div>
        <div v-if="typing" class="message assistant typing">
          <div class="message-avatar">&#129302;</div>
          <div class="message-bubble">
            <div class="typing-dots"><span></span><span></span><span></span></div>
          </div>
        </div>
      </div>

      <div class="chat-input-area">
        <form @submit.prevent="sendMessage" class="chat-form">
          <input
            v-model="newMessage"
            type="text"
            placeholder="Ask me about nutrition, meals, or your health..."
            :disabled="sending"
            autocomplete="off"
          />
          <button type="submit" :disabled="sending || !newMessage.trim()">
            <span v-if="!sending">&#10148;</span>
            <span v-else>...</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../src/api'

export default {
  data() {
    return {
      messages: [],
      newMessage: '',
      sending: false,
      typing: false
    }
  },
  mounted() {
    this.loadHistory()
  },
  updated() {
    this.scrollToBottom()
  },
  methods: {
    async loadHistory() {
      try {
        const res = await api.get('/chat/history')
        this.messages = res.data.messages || []
      } catch (e) {
        console.error('Failed to load chat history:', e)
      }
    },
    async sendMessage() {
      const text = this.newMessage.trim()
      if (!text || this.sending) return

      this.messages.push({ role: 'user', message: text })
      this.newMessage = ''
      this.sending = true
      this.typing = true

      try {
        const res = await api.post('/chat', { message: text })
        this.messages.push({ role: 'assistant', message: res.data.response })
      } catch (e) {
        console.error('Chat error:', e)
        this.messages.push({ role: 'assistant', message: 'Sorry, I had trouble processing that. Please try again.' })
      } finally {
        this.sending = false
        this.typing = false
        this.scrollToBottom()
      }
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const box = this.$refs.chatBox
        if (box) box.scrollTop = box.scrollHeight
      })
    },
    formatTime(ts) {
      const d = new Date(ts)
      return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  }
}
</script>

<style scoped>
.chat-page { max-width: 800px; margin: 0 auto; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background: var(--bg-body); min-height: 100vh; display: flex; flex-direction: column; transition: background var(--transition-slow); }
.chat-container { flex: 1; display: flex; flex-direction: column; height: 100vh; max-height: 100vh; }
.chat-header { padding: 24px 24px 12px; background: var(--bg-card); border-bottom: 1px solid var(--border-color); transition: all var(--transition-slow); }
.chat-header h1 { margin: 0; font-size: 1.3rem; color: var(--text-primary); transition: color var(--transition-slow); }
.subtitle { margin: 4px 0 0 0; color: var(--text-muted); font-size: 0.85rem; transition: color var(--transition-slow); }

.chat-box { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 16px; }

.chat-welcome { text-align: center; padding: 40px 20px; color: var(--text-secondary); transition: color var(--transition-slow); }
.welcome-icon { font-size: 3rem; margin-bottom: 12px; }
.chat-welcome h3 { margin: 0 0 8px 0; color: var(--text-primary); transition: color var(--transition-slow); }
.chat-welcome p { margin: 0 0 8px 0; }
.chat-welcome ul { text-align: left; display: inline-block; margin: 0; color: var(--text-muted); font-size: 0.9rem; transition: color var(--transition-slow); }

.message { display: flex; gap: 10px; align-items: flex-start; max-width: 85%; }
.message.user { align-self: flex-end; flex-direction: row-reverse; }
.message.assistant { align-self: flex-start; }

.message-avatar { font-size: 1.4rem; flex-shrink: 0; margin-top: 2px; }
.message-bubble {
  padding: 12px 16px;
  border-radius: 16px;
  font-size: 0.95rem;
  line-height: 1.5;
  word-wrap: break-word;
}
.message.user .message-bubble { background: linear-gradient(135deg, #22c55e, #16a34a); color: white; border-bottom-right-radius: 4px; }
.message.assistant .message-bubble { background: var(--bg-card); color: var(--text-primary); border-bottom-left-radius: 4px; box-shadow: var(--shadow-sm); transition: all var(--transition-slow); }

.message-time { font-size: 0.7rem; color: rgba(255,255,255,0.7); margin-top: 4px; text-align: right; }
.message.assistant .message-time { color: var(--text-muted); }

.typing-dots { display: flex; gap: 4px; padding: 4px 0; }
.typing-dots span { width: 8px; height: 8px; background: #bbb; border-radius: 50%; animation: bounce 1.4s infinite ease-in-out both; }
.typing-dots span:nth-child(1) { animation-delay: -0.32s; }
.typing-dots span:nth-child(2) { animation-delay: -0.16s; }
@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.chat-input-area { padding: 14px 20px 20px; background: var(--bg-card); border-top: 1px solid var(--border-color); transition: all var(--transition-slow); }
.chat-form { display: flex; gap: 10px; }
.chat-form input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: 24px;
  font-size: 0.95rem;
  background: var(--bg-input);
  color: var(--text-primary);
  outline: none;
  transition: all var(--transition-base);
}
.chat-form input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(163, 230, 53, 0.15); }
.chat-form button {
  width: 44px; height: 44px;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  transition: all var(--transition-base);
}
.chat-form button:hover { transform: scale(1.1); box-shadow: var(--shadow-md); }
.chat-form button:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

@media (max-width: 600px) {
  .chat-header { padding: 16px 16px 8px; }
  .chat-box { padding: 14px; }
  .chat-input-area { padding: 10px 14px 14px; }
  .message { max-width: 92%; }
}
</style>
