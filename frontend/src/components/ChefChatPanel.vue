<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
import http from '@/api/http'

const props = defineProps({
  dishId: { type: Number, required: true },
  lang: { type: String, default: 'zh' }
})

const { t, locale } = useI18n()

const sessionId = ref(null)
const input = ref('')
const messages = ref([])
const sending = ref(false)

// 欢迎消息 - 根据当前语言动态生成
const welcomeMessage = computed(() => {
  return t('chat.chef_welcome') || '您好!我是AI厨师,很高兴为您介绍这道菜品。请随时向我提问!'
})

// 初始化时添加欢迎消息
onMounted(() => {
  messages.value.push({
    role: 'assistant',
    content: welcomeMessage.value
  })
})

// 监听语言切换 - 重新生成欢迎消息而不是添加系统提示
watch(() => props.lang, (newLang) => {
  // 清空消息并重新添加欢迎语
  messages.value = [{
    role: 'assistant',
    content: welcomeMessage.value
  }]
})

async function send() {
  if (!input.value.trim() || sending.value) return
  const question = input.value
  input.value = ''
  messages.value.push({role: 'user', content: question})
  sending.value = true
  try {
    // 使用AI Chef接口而不是旧的聊天接口
    const {data} = await axios.post('/api/chef/chat/', {
      message: question,
      language: locale.value  // 发送当前语言给后端
    })
    messages.value.push({role: 'assistant', content: data.reply})
  } catch (e) {
    console.error('AI Chef error:', e)
    ElMessage.error(t('chat.send_failed'))
    messages.value.push({role: 'assistant', content: t('chat.generic_error')})
  } finally {
    sending.value = false
  }
}
</script>

<template>
  <el-card class="chef-panel" shadow="never">
    <template #header>
      <div class="panel-header">
        <div class="chef">
          <img class="avatar" src="https://dummyimage.com/40x40/0f5e5e/ffffff&text=👨‍🍳" alt="">
          <div class="meta">
            <div class="name">{{ $t('chat.title') }}</div>
            <div class="sub">Ingredients · History · Techniques</div>
          </div>
        </div>
      </div>
    </template>

    <div class="chat" id="chat-scroll">
      <div v-for="(m, i) in messages" :key="i" class="row" :class="m.role">
        <div class="bubble" v-html="m.content"></div>
      </div>
      <div v-if="sending" class="row assistant">
        <div class="bubble">
          <el-icon class="is-loading" style="margin-right:6px;">
            <i-ep-Refresh />
          </el-icon>
          {{ $t('chat.typing') }}
        </div>
      </div>
    </div>

    <div class="composer">
      <el-input
          v-model="input"
          :placeholder="$t('ask_placeholder')"
          clearable
          @keyup.enter.native="send"
      />
      <el-button type="primary" round :loading="sending" @click="send">{{ $t('send') }}</el-button>
    </div>
    <div class="disclaimer">{{ $t('disclaimer') }}</div>
  </el-card>
</template>

<style scoped>
.chef-panel {
  border-radius: 14px;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.chef {
  display: flex;
  gap: 10px;
  align-items: center;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.meta .name {
  font-weight: 700;
}

.meta .sub {
  font-size: 12px;
  color: #6b7280;
}

.chat {
  max-height: 420px;
  overflow: auto;
  padding: 6px;
  background: #fafbfc;
  border-radius: 10px;
  border: 1px solid #eef2f3;
}

.row {
  display: flex;
  margin: 8px 0;
}

.row.user {
  justify-content: flex-end;
}

.row.system {
  justify-content: center;
}

.bubble {
  max-width: 85%;
  padding: 10px 12px;
  border-radius: 14px;
  background: #e8f3f1;
  color: #0b3f3f;
  box-shadow: 0 2px 8px rgba(0, 0, 0, .04);
}

.row.user .bubble {
  background: var(--brand-primary);
  color: #fff;
}

.row.system .bubble {
  background: #f1f5f9;
  color: #334155;
}

.composer {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-top: 10px;
}

.disclaimer {
  margin-top: 6px;
  font-size: 12px;
  opacity: .7;
}
</style>
