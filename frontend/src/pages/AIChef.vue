<script setup>
import { ref, nextTick, computed, watch } from 'vue'
import { ElMessage, ElDialog, ElIcon } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { 
  Star, 
  ChatDotRound, 
  DocumentCopy, 
  MagicStick, 
  ChatLineRound,
  CircleCheckFilled,
  Edit,
  Position,
  InfoFilled
} from '@element-plus/icons-vue'
import http from '@/api/http'
import chefPortrait from '@/assets/aichef.jpg'
import cheflogo from '@/assets/aichef_logo1.jpg'

let counter = 0
const createMessage = (payload) => ({ id: ++counter, ...payload })

const { t, locale } = useI18n()

const messages = ref([
  createMessage({
    role: 'assistant',
    text: t('aichef.chat.welcome')
  })
])
const input = ref('')
const loading = ref(false)
const chatList = ref(null)

// 存储消息的原始问答对，用于语言切换时重新翻译
const messageHistory = ref([
  { question: null, answer: t('aichef.chat.welcome'), language: locale.value }
])

// 监听语言切换
watch(locale, async (newLocale, oldLocale) => {
  if (newLocale === oldLocale) return
  
  // 重新翻译欢迎消息
  messages.value = [
    createMessage({
      role: 'assistant',
      text: t('aichef.chat.welcome')
    })
  ]
  
  // 重新翻译历史消息
  for (let i = 1; i < messageHistory.value.length; i++) {
    const history = messageHistory.value[i]
    
    // 添加用户问题
    if (history.question) {
      messages.value.push(createMessage({
        role: 'user',
        text: history.question
      }))
    }
    
    // 重新请求AI回答（使用新语言）
    if (history.question && !loading.value) {
      loading.value = true
      try {
        const { data } = await http.post('/chef/chat/', {
          message: history.question,
          language: newLocale
        })
        
        // 更新历史记录的答案和语言
        messageHistory.value[i].answer = data.reply
        messageHistory.value[i].language = newLocale
        
        // 添加AI回答
        messages.value.push(createMessage({
          role: 'assistant',
          text: data.reply
        }))
      } catch (error) {
        console.error('AI Chef translation error:', error)
        messages.value.push(createMessage({
          role: 'assistant',
          text: t('aichef.chat.offline_message')
        }))
      }
    }
  }
  
  loading.value = false
  scrollToBottom()
})
// 奖励弹窗相关状态
const rewardModalVisible = ref(false)
const rewardInfo = ref(null)

const heroBackdrop = computed(() => ({
  backgroundImage: `url(${chefPortrait})`
}))

const scrollToBottom = () => {
  nextTick(() => {
    const container = chatList.value
    if (container) {
      container.scrollTo({ top: container.scrollHeight, behavior: 'smooth' })
    }
  })
}

const appendMessage = (message) => {
  messages.value.push(createMessage(message))
  scrollToBottom()
}

const sendMessage = async () => {
  const question = input.value.trim()
  if (!question || loading.value) return

  appendMessage({ role: 'user', text: question })
  input.value = ''
  loading.value = true

  try {
    const { data } = await http.post('/chef/chat/', {
      message: question,
      language: locale.value  // 发送当前语言
    })
    
    // 保存到历史记录
    messageHistory.value.push({
      question: question,
      answer: data.reply,
      language: locale.value
    })
    
    appendMessage({ role: 'assistant', text: data.reply })
    
    // 检查是否有奖励
    if (data.reward) {
      rewardInfo.value = data.reward
      rewardModalVisible.value = true
      console.log('获得奖励:', data.reward)
    }
  } catch (error) {
    console.error('AI Chef error:', error)
    const errorMessage = error.response?.data?.error || error.response?.data?.detail || error.message
    console.error('Error details:', errorMessage)
    
    // 如果是401错误（未授权），提示用户登录
    if (error.response?.status === 401) {
      ElMessage.error('请先登录后再使用AI厨师功能')
      appendMessage({
        role: 'assistant',
        text: '请先登录后再使用AI厨师功能，登录后可以获得对话奖励！'
      })
    } else {
      ElMessage.error(t('chat.send_failed'))
      appendMessage({
        role: 'assistant',
        text: t('aichef.chat.offline_message')
      })
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="ai-chef-page">
    <!-- Hero Section with Enhanced Design -->
    <section class="hero">
      <div class="hero-main">
        <div class="hero-content">
          <span class="hero-badge">
            <el-icon class="badge-icon"><Star /></el-icon>
            {{ $t('aichef.hero.badge') }}
          </span>
          <h1>{{ $t('aichef.hero.title') }}</h1>
          <p class="hero-lead">{{ $t('aichef.hero.lead') }}</p>
          
          <div class="hero-features">
            <div class="feature-item" v-for="(item, index) in 3" :key="index">
              <div class="feature-icon">
                <el-icon v-if="index === 0"><ChatDotRound /></el-icon>
                <el-icon v-else-if="index === 1"><DocumentCopy /></el-icon>
                <el-icon v-else><MagicStick /></el-icon>
              </div>
              <span>{{ $t(`aichef.hero.highlight_${index + 1}`) }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Chat Section with Enhanced UI -->
    <section class="chat-section">
      <div class="chat-intro">
        <div class="intro-header">
          <el-icon class="intro-icon"><ChatLineRound /></el-icon>
          <h2>{{ $t('aichef.chat.section_title') }}</h2>
        </div>
        <p class="intro-desc">{{ $t('aichef.chat.section_desc') }}</p>
        
        <div class="quick-topics">
          <div class="topic-label">{{ $t('aichef.chat.quick_topics') }}</div>
          <el-tag class="topic-tag" @click="input = $t('aichef.chat.topic_1')">
            {{ $t('aichef.chat.topic_1') }}
          </el-tag>
          <el-tag class="topic-tag" @click="input = $t('aichef.chat.topic_2')">
            {{ $t('aichef.chat.topic_2') }}
          </el-tag>
          <el-tag class="topic-tag" @click="input = $t('aichef.chat.topic_3')">
            {{ $t('aichef.chat.topic_3') }}
          </el-tag>
        </div>
      </div>

      <div class="chat-container">
        <div class="chat-card">
          <header class="chat-header">
            <div class="chef-profile">
              <div class="avatar-wrapper">
                <img class="chat-avatar" :src="cheflogo" alt="AI Chef avatar" />
                <span class="online-dot"></span>
              </div>
              <div class="chef-meta">
                <div class="chef-name">{{ $t('aichef.profile.name') }}</div>
                <div class="chef-status">
                  <el-icon class="status-icon"><CircleCheckFilled /></el-icon>
                  {{ $t('aichef.profile.online') }}
                </div>
              </div>
            </div>
            <el-tag type="success" effect="plain" round>{{ $t('aichef.profile.desc') }}</el-tag>
          </header>

          <div class="chat-window" ref="chatList">
            <TransitionGroup name="fade-up" tag="div">
              <div
                v-for="message in messages"
                :key="message.id"
                class="chat-row"
                :class="message.role"
              >
                <div class="message-wrapper">
                  <img v-if="message.role === 'assistant'" class="message-avatar" :src="cheflogo" alt="AI Chef" />
                  <div class="bubble">{{ message.text }}</div>
                </div>
              </div>
            </TransitionGroup>

            <div v-if="loading" class="chat-row assistant typing">
              <div class="message-wrapper">
                <img class="message-avatar" :src="cheflogo" alt="AI Chef" />
                <div class="bubble">
                  <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="composer">
            <el-input
              v-model="input"
              :placeholder="$t('aichef.chat.placeholder')"
              clearable
              size="large"
              @keyup.enter="sendMessage"
            >
              <template #prefix>
                <el-icon><Edit /></el-icon>
              </template>
            </el-input>
            <el-button
              type="primary"
              round
              size="large"
              :loading="loading"
              :disabled="!input.trim()"
              @click="sendMessage"
            >
              <el-icon v-if="!loading"><Position /></el-icon>
              {{ loading ? $t('aichef.chat.sending') : $t('send') }}
            </el-button>
          </div>

          <div class="composer-tips">
            <el-icon><InfoFilled /></el-icon>
            <span>{{ $t('aichef.chat.tip_text') }}</span>
          </div>
        </div>
      </div>
    </section>
    
    <!-- 奖励弹窗 -->
    <el-dialog
      v-model="rewardModalVisible"
      class="reward-dialog"
      width="420px"
      :show-close="false"
      align-center
    >
      <template #header>
        <div class="reward-header">
          <el-icon class="reward-icon"><i-ep-Medal /></el-icon>
          <div>
            <h3>{{ $t('aichef.reward.title') }}</h3>
            <p>{{ $t('aichef.reward.subtitle') }}</p>
          </div>
        </div>
      </template>
      <div class="reward-body">
        <p class="reward-highlight">
          {{ $t('aichef.reward.content', { miles: rewardInfo?.miles ?? 0 }) }}
        </p>
        <p class="reward-note">
          {{ $t('aichef.reward.note') }}
        </p>
      </div>
      <template #footer>
        <el-button type="primary" round block @click="rewardModalVisible = false">
          {{ $t('aichef.reward.cta') }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.ai-chef-page {
  min-height: 100vh;
  padding: 40px 24px 80px;
  background: linear-gradient(180deg, #f0fdfa 0%, #ffffff 40%, #fafafa 100%);
  position: relative;
}

.ai-chef-page::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 600px;
  background: radial-gradient(circle at 30% 20%, rgba(15, 118, 110, 0.05), transparent 60%);
  pointer-events: none;
  z-index: 0;
}

.ai-chef-page::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(20, 184, 166, 0.03), transparent 70%);
  pointer-events: none;
  z-index: 0;
}

/* Hero Section */
.hero {
  max-width: 900px;
  margin: 0 auto 60px;
  position: relative;
  z-index: 1;
}

.hero-main {
  background: linear-gradient(135deg, #ffffff 0%, #f0fdfa 100%);
  border: 1px solid rgba(15, 118, 110, 0.08);
  border-radius: 32px;
  padding: 56px 48px;
  box-shadow: 
    0 4px 24px rgba(15, 118, 110, 0.08),
    0 8px 48px rgba(15, 118, 110, 0.06);
  position: relative;
  overflow: hidden;
  transition: all 0.4s ease;
}

.hero-main:hover {
  box-shadow: 
    0 8px 32px rgba(15, 118, 110, 0.12),
    0 12px 64px rgba(15, 118, 110, 0.08);
  transform: translateY(-4px);
}

.hero-main::before {
  content: '';
  position: absolute;
  top: -60%;
  right: -15%;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(15, 118, 110, 0.04), transparent 70%);
  border-radius: 50%;
  animation: float 8s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(-20px, 20px); }
}

.hero-content {
  position: relative;
  z-index: 1;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 18px;
  border-radius: 30px;
  background: linear-gradient(135deg, #0f766e, #14b8a6);
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  box-shadow: 0 4px 12px rgba(15, 118, 110, 0.3);
}

.badge-icon {
  font-size: 16px;
}

.hero h1 {
  margin: 28px 0 20px;
  font-size: 42px;
  font-weight: 800;
  color: #064e3b;
  line-height: 1.15;
  letter-spacing: -0.03em;
  background: linear-gradient(135deg, #064e3b 0%, #0f766e 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-lead {
  font-size: 17px;
  color: #475569;
  line-height: 1.8;
  margin-bottom: 36px;
  font-weight: 400;
}

.hero-features {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 22px;
  background: linear-gradient(135deg, rgba(240, 253, 250, 0.8), rgba(255, 255, 255, 0.5));
  border: 1px solid rgba(15, 118, 110, 0.1);
  border-radius: 18px;
  color: #064e3b;
  font-size: 15px;
  font-weight: 500;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: default;
  backdrop-filter: blur(10px);
}

.feature-item:hover {
  transform: translateX(8px);
  border-color: rgba(15, 118, 110, 0.3);
  background: linear-gradient(135deg, rgba(15, 118, 110, 0.08), rgba(20, 184, 166, 0.05));
  box-shadow: 0 4px 16px rgba(15, 118, 110, 0.1);
}

.feature-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: linear-gradient(135deg, #0f766e, #14b8a6);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(15, 118, 110, 0.25);
}

/* Chat Section */
.chat-section {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 340px 1fr;
  gap: 32px;
  align-items: start;
  position: relative;
  z-index: 1;
}

.chat-intro {
  position: sticky;
  top: 24px;
  background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
  border-radius: 28px;
  padding: 36px;
  border: 1px solid rgba(15, 118, 110, 0.1);
  box-shadow: 
    0 4px 20px rgba(15, 118, 110, 0.06),
    0 1px 4px rgba(0, 0, 0, 0.02);
  transition: all 0.3s ease;
}

.chat-intro:hover {
  box-shadow: 
    0 8px 28px rgba(15, 118, 110, 0.1),
    0 2px 8px rgba(0, 0, 0, 0.03);
}

.intro-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.intro-icon {
  font-size: 28px;
  color: #0f766e;
}

.chat-intro h2 {
  font-size: 22px;
  font-weight: 700;
  color: #0c3a37;
  margin: 0;
}

.intro-desc {
  color: #4a6363;
  line-height: 1.7;
  font-size: 14px;
  margin: 0 0 24px;
}

.quick-topics {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.topic-label {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 4px;
}

.topic-tag {
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 14px;
  padding: 10px 16px;
  font-size: 13px;
  font-weight: 500;
  background: linear-gradient(135deg, rgba(240, 253, 250, 0.8), rgba(255, 255, 255, 0.5));
  border: 1px solid rgba(15, 118, 110, 0.15);
  color: #0f766e;
}

.topic-tag:hover {
  transform: translateX(6px) scale(1.02);
  background: linear-gradient(135deg, #0f766e, #14b8a6);
  color: white;
  border-color: transparent;
  box-shadow: 0 4px 12px rgba(15, 118, 110, 0.25);
}

/* Chat Container */
.chat-container {
  position: relative;
}

.chat-card {
  background: #ffffff;
  border-radius: 32px;
  border: 1px solid rgba(15, 118, 110, 0.08);
  box-shadow: 
    0 8px 32px rgba(15, 118, 110, 0.08),
    0 2px 8px rgba(0, 0, 0, 0.04);
  padding: 36px;
  display: flex;
  flex-direction: column;
  gap: 28px;
  transition: all 0.3s ease;
}

.chat-card:hover {
  box-shadow: 
    0 12px 48px rgba(15, 118, 110, 0.12),
    0 4px 12px rgba(0, 0, 0, 0.06);
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f0f0f0;
}

.chef-profile {
  display: flex;
  align-items: center;
  gap: 16px;
}

.avatar-wrapper {
  position: relative;
}

.chat-avatar {
  width: 72px;
  height: 72px;
  border-radius: 22px;
  object-fit: cover;
  box-shadow: 
    0 8px 24px rgba(15, 118, 110, 0.2),
    0 2px 8px rgba(0, 0, 0, 0.1);
  border: 4px solid #ffffff;
  transition: all 0.3s ease;
}

.avatar-wrapper:hover .chat-avatar {
  transform: scale(1.05);
  box-shadow: 
    0 12px 32px rgba(15, 118, 110, 0.25),
    0 4px 12px rgba(0, 0, 0, 0.12);
}

.online-dot {
  position: absolute;
  bottom: 4px;
  right: 4px;
  width: 18px;
  height: 18px;
  background: linear-gradient(135deg, #10b981, #059669);
  border: 3px solid white;
  border-radius: 50%;
  box-shadow: 
    0 2px 8px rgba(16, 185, 129, 0.4),
    0 0 0 4px rgba(16, 185, 129, 0.1);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

.chef-meta {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.chef-name {
  font-weight: 700;
  color: #0c3a37;
  font-size: 19px;
}

.chef-status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #10b981;
  font-weight: 500;
}

.status-icon {
  font-size: 14px;
}

.chat-window {
  max-height: 480px;
  overflow-y: auto;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  scroll-behavior: smooth;
}

.chat-window::-webkit-scrollbar {
  width: 6px;
}

.chat-window::-webkit-scrollbar-track {
  background: #f1f5f5;
  border-radius: 10px;
}

.chat-window::-webkit-scrollbar-thumb {
  background: #cbd5d5;
  border-radius: 10px;
}

.chat-window::-webkit-scrollbar-thumb:hover {
  background: #0f766e;
}

:global(.reward-dialog) {
  border-radius: 28px;
  padding: 12px 8px 24px;
  overflow: hidden;
}

:global(.reward-dialog .el-dialog__header) {
  margin: 0;
  padding: 0 24px;
}

:global(.reward-dialog .el-dialog__body) {
  padding: 0 24px 24px;
}

:global(.reward-dialog .el-dialog__footer) {
  padding: 0 24px 24px;
}

.reward-header {
  display: flex;
  gap: 16px;
  align-items: center;
}

.reward-icon {
  width: 56px;
  height: 56px;
  border-radius: 18px;
  background: linear-gradient(135deg, #fde68a, #f97316);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #b45309;
  font-size: 30px;
  box-shadow: 0 8px 20px rgba(249, 115, 22, 0.25);
}

.reward-header h3 {
  margin: 0;
  font-size: 20px;
  color: #92400e;
}

.reward-header p {
  margin: 4px 0 0;
  color: #b45309;
  font-size: 14px;
}

.reward-body {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.reward-highlight {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #92400e;
}

.reward-note {
  margin: 0;
  color: #b45309;
  font-size: 13px;
  opacity: 0.85;
}

.chat-row {
  display: flex;
  width: 100%;
  animation: fadeInUp 0.4s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.chat-row.user {
  justify-content: flex-end;
}

.chat-row.assistant {
  justify-content: flex-start;
}

.message-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  max-width: 75%;
}

.chat-row.user .message-wrapper {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 10px;
  object-fit: cover;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.bubble {
  padding: 14px 18px;
  border-radius: 18px;
  font-size: 15px;
  line-height: 1.6;
  box-shadow: 0 4px 12px rgba(12, 58, 55, 0.08);
  position: relative;
}

.chat-row.assistant .bubble {
  background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
  color: #064e3b;
  border: 1px solid rgba(15, 118, 110, 0.1);
  border-bottom-left-radius: 6px;
  box-shadow: 0 2px 8px rgba(15, 118, 110, 0.06);
}

.chat-row.user .bubble {
  background: linear-gradient(135deg, #0f766e 0%, #14b8a6 100%);
  color: #ffffff;
  border-bottom-right-radius: 6px;
  box-shadow: 
    0 4px 12px rgba(15, 118, 110, 0.25),
    0 2px 6px rgba(0, 0, 0, 0.1);
  font-weight: 500;
}

/* Typing Indicator */
.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 4px 0;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #0f766e;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.4;
  }
  30% {
    transform: translateY(-8px);
    opacity: 1;
  }
}

/* Composer */
.composer {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-top: 20px;
  border-top: 2px solid #f0f0f0;
}

.composer :deep(.el-input__wrapper) {
  border-radius: 24px;
  padding: 14px 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  border: 2px solid rgba(15, 118, 110, 0.12);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: #fafafa;
}

.composer :deep(.el-input__wrapper):hover {
  border-color: rgba(15, 118, 110, 0.3);
  background: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.composer :deep(.el-input__wrapper.is-focus) {
  border-color: #0f766e;
  box-shadow: 
    0 0 0 4px rgba(15, 118, 110, 0.08),
    0 4px 12px rgba(0, 0, 0, 0.06);
  background: #ffffff;
}

.composer .el-button {
  padding: 14px 32px;
  font-weight: 600;
  font-size: 15px;
  background: linear-gradient(135deg, #0f766e 0%, #14b8a6 100%);
  border: none;
  box-shadow: 
    0 4px 12px rgba(15, 118, 110, 0.3),
    0 2px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.composer .el-button:hover:not(.is-disabled) {
  transform: translateY(-2px);
  box-shadow: 
    0 6px 20px rgba(15, 118, 110, 0.4),
    0 4px 10px rgba(0, 0, 0, 0.15);
  background: linear-gradient(135deg, #0d5f58 0%, #12a594 100%);
}

.composer .el-button:active:not(.is-disabled) {
  transform: translateY(0);
}

.composer-tips {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #64748b;
  padding: 12px 16px;
  background: linear-gradient(135deg, rgba(15, 118, 110, 0.04), rgba(20, 184, 166, 0.02));
  border-radius: 12px;
  border: 1px solid rgba(15, 118, 110, 0.08);
}

/* Animations */
.fade-up-enter-active,
.fade-up-leave-active {
  transition: all 0.3s ease;
}

.fade-up-enter-from,
.fade-up-leave-to {
  opacity: 0;
  transform: translateY(12px);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .hero {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .hero-photo {
    min-height: 320px;
  }

  .chat-section {
    grid-template-columns: 1fr;
  }

  .chat-intro {
    position: static;
    margin-bottom: 0;
  }
}

@media (max-width: 768px) {
  .ai-chef-page {
    padding: 40px 16px 60px;
  }

  .hero-main {
    padding: 32px 24px;
  }

  .hero h1 {
    font-size: 32px;
  }

  .hero-features {
    gap: 12px;
  }

  .feature-item {
    padding: 14px 16px;
    font-size: 14px;
  }

  .feature-icon {
    width: 36px;
    height: 36px;
    font-size: 18px;
  }

  .hero-photo {
    min-height: 280px;
  }

  .photo-overlay {
    padding: 28px;
  }

  .photo-overlay h3 {
    font-size: 24px;
  }

  .photo-stats {
    gap: 20px;
  }

  .stat-item strong {
    font-size: 28px;
  }

  .chat-intro {
    padding: 24px;
  }

  .intro-header h2 {
    font-size: 20px;
  }

  .chat-card {
    padding: 24px;
  }

  .chat-avatar {
    width: 56px;
    height: 56px;
  }

  .chef-name {
    font-size: 17px;
  }

  .chat-window {
    max-height: 360px;
  }

  .message-wrapper {
    max-width: 85%;
  }

  .message-avatar {
    width: 28px;
    height: 28px;
  }

  .bubble {
    padding: 12px 16px;
    font-size: 14px;
  }

  .composer {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }

  .composer .el-button {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .hero h1 {
    font-size: 28px;
  }

  .hero-lead {
    font-size: 15px;
  }

  .hero-photo {
    min-height: 240px;
  }

  .photo-overlay {
    padding: 24px;
  }

  .photo-overlay h3 {
    font-size: 22px;
  }

  .photo-copy {
    font-size: 14px;
  }

  .stat-item strong {
    font-size: 24px;
  }

  .stat-item span {
    font-size: 11px;
  }

  .chat-intro {
    padding: 20px;
  }

  .chat-card {
    padding: 20px;
  }

  .chat-window {
    max-height: 320px;
  }

  .bubble {
    font-size: 13px;
  }
}
</style>
