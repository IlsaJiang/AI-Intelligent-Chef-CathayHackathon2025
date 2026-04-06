<template>
  <header class="cx-header" role="banner">
    <!-- Utility Bar -->
    <div class="util-bar" aria-label="utility">
      <div class="cx-container util-row">
        <div class="util-left">
          <a class="link-muted" href="javascript:void(0)">{{ $t('header.travel_link') }}</a>
        </div>
        <div class="util-right">
          <a class="link-muted" href="javascript:void(0)">
            <el-icon><i-ep-Search /></el-icon><span>{{ $t('search') }}</span>
          </a>
          <a class="link-muted" href="javascript:void(0)">
            <el-icon><i-ep-QuestionFilled /></el-icon><span>{{ $t('help') }}</span>
          </a>
          <a class="link-muted" href="javascript:void(0)">
            <el-icon><i-ep-Bell /></el-icon><span>{{ $t('notices') }}</span>
          </a>

          <!-- 語言切換：简｜繁｜English -->
          <el-dropdown trigger="click" @command="onLang" class="lang-dd">
            <span class="link-muted lang-toggle" aria-haspopup="listbox" :aria-label="$t('header.lang_switch_label')">
              🌐 <span class="sep">｜</span> <span class="lang-text">{{ langPair }}</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="zh">{{ $t('languages.zh_short') }}</el-dropdown-item>
                <el-dropdown-item command="zh-HK">{{ $t('languages.zh_hk') }}</el-dropdown-item>
                <el-dropdown-item command="en">{{ $t('languages.en') }}</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>

          <template v-if="!isAuthenticated">
            <el-button round class="login-btn" @click="goLogin">{{ $t('login') }}</el-button>
          </template>
          <template v-else>
            <div class="user-info">
              <el-avatar :size="28" class="user-avatar">
                {{ userInitial || 'U' }}
              </el-avatar>
              <span class="user-name">{{ displayName || $t('auth.tabs.login') }}</span>
            </div>
            <el-button round class="login-btn" @click="onLogout">{{ $t('logout') }}</el-button>
          </template>
        </div>
      </div>
    </div>

    <!-- Main Navigation -->
    <div class="main-nav" aria-label="primary">
      <div class="cx-container nav-row">
        <!-- Brand: 自動根據語言切換 SVG Logo -->
        <button class="brand" @click="$router.push('/')" aria-label="Go to home">
          <img :src="logoSrc" :alt="logoAlt" class="logo" />
        </button>

        <!-- Desktop Nav -->
        <nav class="nav desktop-only" role="navigation">
          <router-link to="/" active-class="active">{{ $t('home') }}</router-link>
          <router-link to="/menu" active-class="active">{{ $t('menu') }}</router-link>
          <router-link to="/ar" active-class="active">{{ $t('ar_view') }}</router-link>
          <router-link to="/chef" active-class="active">{{ $t('ai_entry') }}</router-link>
          <router-link to="/survey" active-class="active">{{ $t('survey_nav') }}</router-link>
          <router-link to="/my-feedback" active-class="active">{{ $t('my_feedback') }}</router-link>
          <router-link to="/preselect" active-class="active">{{ $t('preselect') }}</router-link>
        </nav>

        <!-- Mobile hamburger -->
        <el-button class="mobile-only" text aria-label="open menu" @click="open = true">
          <el-icon><i-ep-Menu /></el-icon>
        </el-button>
      </div>
    </div>

    <!-- Mobile Drawer -->
    <el-drawer v-model="open" :with-header="false" size="80%" aria-label="mobile menu">
      <div class="drawer-head">
        <div class="brand">
          <img :src="logoSrc" :alt="logoAlt" class="logo" />
        </div>
        <el-button text aria-label="close menu" @click="open = false"><el-icon><i-ep-Close /></el-icon></el-button>
      </div>

      <nav class="drawer-nav" role="navigation">
        <el-menu :default-active="$route.path" router>
          <el-menu-item index="/">{{ $t('home') }}</el-menu-item>
          <el-menu-item index="/menu">{{ $t('menu') }}</el-menu-item>
          <el-menu-item index="/ar">{{ $t('ar_view') }}</el-menu-item>
          <el-menu-item index="/chef">{{ $t('ai_entry') }}</el-menu-item>
          <el-menu-item index="/survey">{{ $t('survey_nav') }}</el-menu-item>
          <el-menu-item index="/my-feedback">{{ $t('my_feedback') }}</el-menu-item>
          <el-menu-item index="/preselect">{{ $t('preselect') }}</el-menu-item>
        </el-menu>
      </nav>

      <div class="drawer-actions">
        <el-dropdown trigger="click" @command="onLang" class="drawer-lang">
          <el-button text>🌐 {{ langPair }}</el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="zh">{{ $t('languages.zh_short') }}</el-dropdown-item>
              <el-dropdown-item command="zh-HK">{{ $t('languages.zh_hk') }}</el-dropdown-item>
              <el-dropdown-item command="en">{{ $t('languages.en') }}</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <el-button
          v-if="!isAuthenticated"
          type="primary"
          round
          block
          @click="goLogin"
        >
          {{ $t('login') }}
        </el-button>
        <el-button
          v-else
          type="primary"
          round
          block
          @click="onLogout"
        >
          {{ $t('logout') }}
        </el-button>
      </div>
    </el-drawer>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import zhLogo from '@/assets/logo-cathay-zh.svg'
import enLogo from '@/assets/logo-cathay-en.svg'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

const open = ref(false)
const { locale, t } = useI18n()
const router = useRouter()
const authStore = useAuthStore()
const { isAuthenticated, displayName } = storeToRefs(authStore)

const userInitial = computed(() => {
  if (!displayName.value) return ''
  return displayName.value.charAt(0).toUpperCase()
})

const logoSrc = computed(() => (locale.value === 'en' ? enLogo : zhLogo))
const logoAlt = computed(() => t('header.logo_alt'))
const langPair = computed(() => t('header.lang_pair'))

const onLang = (value) => {
  locale.value = value
  ElMessage.success(value === 'en' ? t('header.switch_to_en') : t('header.switch_to_zh'))
  open.value = false
}

const goLogin = () => {
  open.value = false
  router.push('/auth')
}

const onLogout = () => {
  open.value = false
  authStore.logout()
  ElMessage.success(t('auth.messages.logout_success'))
  router.push('/auth')
}
</script>

<style scoped>
.cx-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 16px;
}

.util-bar {
  background: #f6f7f4;
  border-bottom: 1px solid #e8eceb;
  font-weight: 400;
  box-shadow: 0 1px 0 rgba(0, 0, 0, 0.01);
}

.util-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 36px;
  font-size: 13px;
  letter-spacing: 0.1px;
}

.util-right,
.util-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.link-muted {
  color: #2b5f5d;
  text-decoration: none;
  display: inline-flex;
  gap: 6px;
  align-items: center;
}

.link-muted span {
  transform: translateY(-0.5px);
}

.lang-toggle {
  cursor: pointer;
}

.sep {
  opacity: 0.5;
  margin: 0 2px;
}

.login-btn {
  border: 1px solid #174c4b;
  color: #174c4b;
  height: 28px;
  line-height: 26px;
  padding: 0 10px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-avatar {
  background: linear-gradient(135deg, #0f766e, #1f8d89);
  color: #fff;
  border: 2px solid rgba(255, 255, 255, 0.3);
  flex-shrink: 0;
  font-weight: 600;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-name {
  font-weight: 600;
  color: #174c4b;
}

.cx-header {
  background: #fff;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
}

.main-nav {
  background: #fff;
  border-bottom: 1px solid #e9efee;
}

.nav-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0;
  margin: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
}

.logo {
  height: 26px;
  width: auto;
  display: block;
}

.nav {
  display: flex;
  gap: 18px;
  font-weight: 500;
}

.nav a {
  text-decoration: none;
  color: #0c3342;
  padding: 8px 10px;
  border-radius: 10px;
  transition: background 0.15s ease, color 0.15s ease;
}

.nav a:hover {
  background: #f1f5f4;
}

.nav a.active {
  background: #e9f2f1;
  color: #0b3f3f;
}

.desktop-only {
  display: flex;
}

.mobile-only {
  display: none;
}

@media (max-width: 960px) {
  .desktop-only {
    display: none;
  }

  .mobile-only {
    display: inline-flex;
  }
}

.drawer-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 6px 14px;
  border-bottom: 1px solid #eef2f3;
}

.drawer-actions {
  margin-top: 12px;
  display: grid;
  gap: 10px;
}

.drawer-lang .el-button {
  font-weight: 600;
}
</style>
