<script setup>
import { ref, reactive, computed, watch, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
import heroVisual from '@/assets/aichef.jpg'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'
import http from '@/api/http'

const router = useRouter()
const route = useRoute()
const { t } = useI18n()
const authStore = useAuthStore()
const { isAuthenticated } = storeToRefs(authStore)
const mode = ref('login')
const registerChannel = ref('email')
const otpSending = ref(false)
const loginLoading = ref(false)
const registerLoading = ref(false)
const rewardModalVisible = ref(false)
const rewardInfo = ref(null)

const heroStyle = computed(() => ({
  backgroundImage: `linear-gradient(140deg, rgba(5,32,33,.82), rgba(18,93,94,.55)), url(${heroVisual})`
}))

const redirectTarget = computed(() => {
  const target = route.query.redirect
  return typeof target === 'string' && target ? target : '/'
})

const loginForm = reactive({
  identifier: '',
  password: '',
  remember: true
})

const registerForm = reactive({
  fullName: '',
  countryCode: '+852',
  phone: '',
  email: '',
  otp: '',
  password: '',
  agree: false
})

const parseErrorMessage = (error, fallback) => {
  const detail = error?.response?.data
  if (!detail) return fallback
  if (typeof detail === 'string') return detail
  if (detail.detail) return Array.isArray(detail.detail) ? detail.detail[0] : detail.detail
  const firstKey = Object.keys(detail)[0]
  if (!firstKey) return fallback
  const value = detail[firstKey]
  if (Array.isArray(value)) return value[0]
  if (typeof value === 'string') return value
  return fallback
}

watch(registerChannel, (channel) => {
  registerForm.otp = ''
  if (channel === 'phone') {
    registerForm.email = ''
  } else {
    registerForm.phone = ''
  }
})

const handleLogin = async () => {
  if (!loginForm.identifier || !loginForm.password) {
    ElMessage.warning(t('auth.messages.login_required'))
    return
  }
  try {
    loginLoading.value = true
    const { reward } = await authStore.login(loginForm.identifier, loginForm.password, loginForm.remember)
    ElMessage.success(t('auth.messages.login_success'))
    if (reward) {
      rewardInfo.value = reward
      rewardModalVisible.value = true
    } else {
      setTimeout(() => router.push(redirectTarget.value), 300)
    }
  } catch (error) {
    const message = parseErrorMessage(error, t('auth.messages.login_failed'))
    ElMessage.error(message)
  } finally {
    loginLoading.value = false
  }
}

const handleRegister = async () => {
  if (!registerForm.fullName || !registerForm.password) {
    ElMessage.warning(t('auth.messages.name_password_required'))
    return
  }
  if (registerChannel.value === 'phone' && !registerForm.phone) {
    ElMessage.warning(t('auth.messages.phone_required'))
    return
  }
  if (registerChannel.value === 'email' && !registerForm.email) {
    ElMessage.warning(t('auth.messages.email_required'))
    return
  }
  if (!registerForm.otp) {
    ElMessage.warning(t('auth.messages.otp_required'))
    return
  }
  if (!registerForm.agree) {
    ElMessage.warning(t('auth.messages.agree_required'))
    return
  }

  const payload = {
    channel: registerChannel.value,
    full_name: registerForm.fullName,
    country_code: registerForm.countryCode,
    phone: registerForm.phone,
    email: registerForm.email,
    otp: registerForm.otp,
    password: registerForm.password,
    agree: registerForm.agree
  }

  try {
    registerLoading.value = true
    const result = await authStore.register(payload, true, true)
    console.log('注册返回数据:', result)
    const reward = result?.reward
    console.log('奖励信息:', reward)
    
    if (reward) {
      rewardInfo.value = reward
      console.log('rewardInfo 已设置:', rewardInfo.value)
      await nextTick()
      rewardModalVisible.value = true
      console.log('奖励弹窗已设置为显示, rewardModalVisible:', rewardModalVisible.value)
      console.log('当前路由:', router.currentRoute.value.path)
      console.log('isAuthenticated:', isAuthenticated.value)
      ElMessage.success(t('auth.messages.register_success'))
      
      setTimeout(() => {
        console.log('延迟检查：rewardModalVisible:', rewardModalVisible.value, 'isAuthenticated:', isAuthenticated.value, '弹窗DOM:', document.querySelector('.reward-dialog'))
      }, 500)
    } else {
      console.log('没有奖励信息，准备跳转')
      ElMessage.success(t('auth.messages.register_success'))
      setTimeout(() => router.push(redirectTarget.value), 300)
    }
  } catch (error) {
    console.error('注册错误:', error)
    const message = parseErrorMessage(error, t('auth.messages.register_failed'))
    ElMessage.error(message)
  } finally {
    registerLoading.value = false
  }
}

const sendOtp = async () => {
  if (otpSending.value) return
  const contact = registerChannel.value === 'phone' ? registerForm.phone : registerForm.email
  if (!contact) {
    ElMessage.warning(registerChannel.value === 'phone' ? t('auth.messages.phone_required') : t('auth.messages.email_required'))
    return
  }
  try {
    otpSending.value = true
    await http.post('/auth/send-otp/', {
      channel: registerChannel.value,
      email: registerForm.email,
      phone: registerForm.phone,
      country_code: registerForm.countryCode
    })
    ElMessage.success(t('auth.messages.otp_sent'))
  } catch (error) {
    const message = parseErrorMessage(error, t('auth.messages.otp_send_failed'))
    ElMessage.error(message)
  } finally {
    otpSending.value = false
  }
}

const quickNav = () => router.push('/menu')

onMounted(async () => {
  const pendingReward = authStore.consumeReward?.()
  if (pendingReward) {
    rewardInfo.value = pendingReward
    rewardModalVisible.value = true
    return
  }
  await authStore.ensureSession()
  if (isAuthenticated.value && !rewardModalVisible.value) {
    router.replace(redirectTarget.value)
  }
})

watch(
  () => route.query.redirect,
  () => {
    if (isAuthenticated.value) {
      router.replace(redirectTarget.value)
    }
  }
)

watch(isAuthenticated, (loggedIn) => {
  if (loggedIn && router.currentRoute.value.path === '/auth') {
    console.log('isAuthenticated changed to true, rewardModalVisible:', rewardModalVisible.value, 'rewardInfo:', rewardInfo.value)
    setTimeout(() => {
      const REWARD_KEY = 'cx_reward'
      const hasReward = localStorage.getItem(REWARD_KEY) !== null || sessionStorage.getItem(REWARD_KEY) !== null
      console.log('延迟检查奖励，hasReward:', hasReward, 'rewardModalVisible:', rewardModalVisible.value, 'rewardInfo:', rewardInfo.value)
      if (!rewardModalVisible.value && !rewardInfo.value && !hasReward) {
        console.log('没有奖励，准备跳转')
        router.replace(redirectTarget.value)
      } else {
        console.log('有奖励或弹窗已显示，不跳转')
      }
    }, 100)
  }
})

watch(rewardModalVisible, (visible) => {
  if (!visible && isAuthenticated.value) {
    router.replace(redirectTarget.value)
  }
})
</script>

<template>
  <div class="auth-shell">
    <section class="hero-pane" :style="heroStyle">
      <div class="hero-meta">
        <span class="eyebrow">{{ $t('auth.hero.eyebrow') }}</span>
        <h1>{{ $t('auth.hero.title') }}</h1>
        <p>
          {{ $t('auth.hero.copy') }}
        </p>
        <ul>
          <li>{{ $t('auth.hero.bullet_1') }}</li>
          <li>{{ $t('auth.hero.bullet_2') }}</li>
          <li>{{ $t('auth.hero.bullet_3') }}</li>
        </ul>
        <!-- <el-button plain round class="hero-cta" @click="quickNav">{{ $t('auth.hero.cta') }}</el-button> -->
      </div>
    </section>

    <section class="panel">
      <div class="panel-head">
        <div class="tabs">
          <button
            class="tab"
            :class="{ active: mode === 'login' }"
            @click="mode = 'login'"
          >
            {{ $t('auth.tabs.login') }}
          </button>
          <button
            class="tab"
            :class="{ active: mode === 'register' }"
            @click="mode = 'register'"
          >
            {{ $t('auth.tabs.register') }}
          </button>
        </div>
        <p class="head-copy">
          {{ mode === 'login' ? $t('auth.login_subhead') : $t('auth.register_subhead') }}
        </p>
      </div>

      <div v-if="mode === 'login'" class="card">
        <el-form label-position="top">
          <el-form-item :label="$t('auth.login.identifier_label')">
            <el-input
              v-model="loginForm.identifier"
              :placeholder="$t('auth.login.identifier_placeholder')"
              clearable
            />
          </el-form-item>
          <el-form-item :label="$t('auth.login.password_label')">
            <el-input
              v-model="loginForm.password"
              :placeholder="$t('auth.login.password_placeholder')"
              show-password
            />
          </el-form-item>
          <div class="form-row">
            <el-checkbox v-model="loginForm.remember">{{ $t('auth.login.remember') }}</el-checkbox>
            <a class="link" href="javascript:void(0)">{{ $t('auth.login.forgot') }}</a>
          </div>
          <el-button type="primary" round block size="large" :loading="loginLoading" @click="handleLogin">
            {{ $t('auth.login.submit') }}
          </el-button>
          <p class="switch-copy">
            {{ $t('auth.login.switch_prompt') }}
            <button class="link-btn" @click="mode = 'register'">{{ $t('auth.login.switch_cta') }}</button>
          </p>
        </el-form>
      </div>

      <div v-else class="card">
        <div class="channel-toggle">
          <span>{{ $t('auth.register.channel_label') }}</span>
          <div class="chip-group">
            <button
              class="chip"
              :class="{ active: registerChannel === 'phone' }"
              @click="registerChannel = 'phone'"
            >
              {{ $t('auth.register.channel_phone') }}
            </button>
            <button
              class="chip"
              :class="{ active: registerChannel === 'email' }"
              @click="registerChannel = 'email'"
            >
              {{ $t('auth.register.channel_email') }}
            </button>
          </div>
        </div>

        <el-form label-position="top">
          <el-form-item :label="$t('auth.register.name_label')">
            <el-input v-model="registerForm.fullName" :placeholder="$t('auth.register.name_placeholder')" />
          </el-form-item>

          <el-form-item v-if="registerChannel === 'phone'" :label="$t('auth.register.phone_label')">
            <div class="phone-row">
              <el-select v-model="registerForm.countryCode" class="code-select">
                <el-option :label="$t('auth.region.hk')" value="+852" />
                <el-option :label="$t('auth.region.mo')" value="+853" />
                <el-option :label="$t('auth.region.cn')" value="+86" />
                <el-option :label="$t('auth.region.tw')" value="+886" />
              </el-select>
              <el-input
                v-model="registerForm.phone"
                :placeholder="$t('auth.register.phone_placeholder')"
              />
            </div>
          </el-form-item>

          <el-form-item v-else :label="$t('auth.register.email_label')">
            <el-input
              v-model="registerForm.email"
              :placeholder="$t('auth.register.email_placeholder')"
            />
          </el-form-item>

          <el-form-item :label="$t('auth.register.otp_label')">
            <el-input v-model="registerForm.otp" :placeholder="$t('auth.register.otp_placeholder')">
              <template #append>
                <el-button text type="primary" :loading="otpSending" @click="sendOtp">{{ $t('auth.register.otp_send') }}</el-button>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item :label="$t('auth.register.password_label')">
            <el-input
              v-model="registerForm.password"
              :placeholder="$t('auth.register.password_placeholder')"
              show-password
            />
          </el-form-item>

          <el-checkbox v-model="registerForm.agree" class="agree-box">
            {{ $t('auth.register.agree_prefix') }}
            <a class="link" href="javascript:void(0)">{{ $t('auth.register.terms') }}</a>
            {{ $t('auth.register.and') }}
            <a class="link" href="javascript:void(0)">{{ $t('auth.register.privacy') }}</a>
          </el-checkbox>

          <el-button type="primary" round block size="large" :loading="registerLoading" @click="handleRegister">
            {{ $t('auth.register.submit') }}
          </el-button>

          <p class="switch-copy">
            {{ $t('auth.register.switch_prompt') }}
            <button class="link-btn" @click="mode = 'login'">{{ $t('auth.register.switch_cta') }}</button>
          </p>
        </el-form>
      </div>
    </section>
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
            <h3>{{ $t('auth.reward.title') }}</h3>
            <p>{{ $t('auth.reward.subtitle') }}</p>
          </div>
        </div>
      </template>
      <div class="reward-body">
        <p class="reward-highlight">
          {{ $t('auth.reward.content', { miles: rewardInfo?.miles ?? 0, points: rewardInfo?.points ?? 0 }) }}
        </p>
        <p class="reward-note">
          {{ $t('auth.reward.note') }}
        </p>
      </div>
      <template #footer>
        <el-button type="primary" round block @click="rewardModalVisible = false">
          {{ $t('auth.reward.cta') }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.auth-shell {
  min-height: calc(100vh - 120px);
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(380px, 430px);
  background: #f5f8f7;
  border-radius: 28px;
  overflow: hidden;
  box-shadow: 0 25px 65px rgba(6, 22, 36, 0.08);
}

.hero-pane {
  background-size: cover;
  background-position: center;
  padding: 48px;
  color: #f6fffe;
  display: flex;
  align-items: flex-end;
}

.hero-meta {
  max-width: 460px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.eyebrow {
  letter-spacing: 0.18em;
  font-size: 12px;
  text-transform: uppercase;
  opacity: 0.85;
}

.hero-meta h1 {
  font-size: 32px;
  line-height: 1.3;
  margin: 0;
}

.hero-meta p {
  margin: 0;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.88);
}

.hero-meta ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 4px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.85);
}

.hero-cta {
  align-self: flex-start;
  border-color: rgba(255, 255, 255, 0.8);
  color: #0f766e;
}

.panel {
  background: #ffffff;
  padding: 40px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.panel-head {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tabs {
  display: flex;
  gap: 10px;
}

.tab {
  flex: 1;
  padding: 12px;
  border-radius: 999px;
  border: 1px solid #d1e2e1;
  background: #fff;
  font-weight: 600;
  color: #4a6b6b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab.active {
  background: linear-gradient(130deg, #0f766e, #1f8d89);
  color: #fff;
  border-color: transparent;
  box-shadow: 0 10px 25px rgba(15, 118, 110, 0.22);
}

.head-copy {
  margin: 0;
  color: #6b7f80;
}

.card {
  padding: 24px;
  border: 1px solid #e4eeee;
  border-radius: 20px;
  background: #fbfefe;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.5);
}

.form-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
}

.link {
  color: #0f766e;
  text-decoration: none;
}

.switch-copy {
  text-align: center;
  color: #6b7f80;
  margin-top: 16px;
}

.link-btn {
  background: none;
  border: none;
  color: #0f766e;
  cursor: pointer;
  font-weight: 600;
}

.channel-toggle {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.chip-group {
  display: flex;
  gap: 8px;
}

.chip {
  padding: 8px 14px;
  border-radius: 999px;
  border: 1px solid #d1e2e1;
  background: #fff;
  cursor: pointer;
  color: #4a6b6b;
}

.chip.active {
  background: #0f766e;
  color: #fff;
  border-color: transparent;
  box-shadow: 0 8px 20px rgba(15, 118, 110, 0.2);
}

.phone-row {
  display: flex;
  gap: 10px;
}

.code-select {
  width: 130px;
}

.agree-box {
  margin-bottom: 16px;
}

@media (max-width: 1024px) {
  .auth-shell {
    grid-template-columns: 1fr;
  }

  .hero-pane {
    padding: 32px;
    min-height: 320px;
  }
}

@media (max-width: 640px) {
  .auth-shell {
    border-radius: 0;
  }

  .panel {
    padding: 24px;
  }

  .card {
    padding: 18px;
  }

  .hero-pane {
    padding: 24px;
  }

  .phone-row {
    flex-direction: column;
  }

  .code-select {
    width: 100%;
  }
}

.reward-dialog :deep(.el-dialog__header) {
  margin: 0;
  padding: 24px 24px 0;
}

.reward-dialog :deep(.el-dialog__body) {
  padding: 16px 24px 8px;
}

.reward-dialog :deep(.el-dialog__footer) {
  padding: 0 24px 24px;
}

.reward-header {
  display: flex;
  gap: 12px;
  align-items: center;
}

.reward-icon {
  font-size: 28px;
  color: #f97316;
}

.reward-header h3 {
  margin: 0;
  font-size: 20px;
  color: #0c3342;
}

.reward-header p {
  margin: 2px 0 0;
  color: #4a6b6b;
}

.reward-body {
  display: grid;
  gap: 12px;
}

.reward-highlight {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #0f766e;
}

.reward-note {
  margin: 0;
  font-size: 14px;
  color: #4a6b6b;
}
</style>
