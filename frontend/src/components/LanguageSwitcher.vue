<script setup>
import { useI18n } from 'vue-i18n'
const { locale } = useI18n()
const setLang = (l) => {
  locale.value = l
}
</script>

<template>
  <div style="display:flex; gap:8px;">
    <button class="brand-btn" @click="setLang('zh')">{{ $t('languages.zh_short') }}</button>
    <button class="brand-btn" @click="setLang('zh-HK')">{{ $t('languages.zh_hk') }}</button>
    <button class="brand-btn" @click="setLang('en')">{{ $t('languages.en_short') }}</button>
  </div>
</template>
