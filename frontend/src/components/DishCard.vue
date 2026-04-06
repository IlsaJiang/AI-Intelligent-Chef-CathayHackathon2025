<script setup>
const props = defineProps({ dish: Object, locale: String })

// 根据语言获取菜品名称
const getDishName = () => {
  if (props.locale === 'zh-HK') {
    return props.dish.name_zh_hk || props.dish.name_zh || props.dish.name_en
  } else if (props.locale === 'en') {
    return props.dish.name_en || props.dish.name_zh
  } else {
    return props.dish.name_zh || props.dish.name_en
  }
}

// 根据语言获取菜品描述
const getDishDesc = () => {
  if (props.locale === 'zh-HK') {
    return props.dish.desc_zh_hk || props.dish.desc_zh || props.dish.desc_en
  } else if (props.locale === 'en') {
    return props.dish.desc_en || props.dish.desc_zh
  } else {
    return props.dish.desc_zh || props.dish.desc_en
  }
}
</script>

<template>
  <div class="card" style="display:flex; flex-direction:column; gap:8px;">
    <div style="font-weight:600; font-size:18px;">
      {{ getDishName() }}
    </div>
    <div style="opacity:.8;">
      {{ getDishDesc() }}
    </div>
    <router-link class="brand-link" :to="'/dish/' + props.dish.id">{{ $t('view') }}</router-link>
  </div>
</template>
