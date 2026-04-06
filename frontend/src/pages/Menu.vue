<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useI18n } from 'vue-i18n'
import { Search, Filter } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

// 导入菜品图片
import babaofanImage from '@/assets/babaofan.jpg'
import lianouImage from '@/assets/lianou.jpg'
import tieguanyinImage from '@/assets/tieguanyin.jpg'
import wineImage from '@/assets/wine.jpg'

const { locale, t } = useI18n()
const authStore = useAuthStore()
const { user, displayName } = storeToRefs(authStore)

const dishes = ref([])
const allergens = ref([])
const q = ref('')
const allergen = ref('')
const filterPeanut = ref(false) // 是否筛选掉花生过敏原

onMounted(async () => {
  const d = await axios.get('/api/dishes/')
  dishes.value = d.data
  const a = await axios.get('/api/allergens/')
  allergens.value = a.data
})

const nameOf = (d) => {
  const dishData = t(`dishes.${d.id}.name`)
  if (dishData && !dishData.includes('dishes')) return dishData
  
  if (locale.value === 'zh-HK') {
    return d.name_zh_hk || d.name_zh || d.name_en
  } else if (locale.value === 'en') {
    return d.name_en || d.name_zh
  } else {
    return d.name_zh || d.name_en
  }
}
const descOf = (d) => {
  const dishData = t(`dishes.${d.id}.desc`)
  if (dishData && !dishData.includes('dishes')) return dishData
  
  if (locale.value === 'zh-HK') {
    return d.desc_zh_hk || d.desc_zh || d.desc_en
  } else if (locale.value === 'en') {
    return d.desc_en || d.desc_zh
  } else {
    return d.desc_zh || d.desc_en
  }
}

// 根据菜品ID获取对应的图片
const getImageForDish = (dishId) => {
  switch (dishId) {
    case 1: // 八宝红鲟饭
      return babaofanImage
    case 2: // 枸杞百合伴藕带
      return lianouImage
    case 3: // 铁观音
      return tieguanyinImage
    case 4: // 怡园德熙珍藏霞多丽干白葡萄酒
      return wineImage
    default:
      return null
  }
}

const filtered = computed(() => {
  return dishes.value.filter(d=>{
    const hitQ = q.value ? (nameOf(d)?.includes(q.value) || descOf(d)?.includes(q.value)) : true
    const hitA = allergen.value ? (d.allergens || []).some(a => String(a.id) === String(allergen.value)) : true
    // 如果启用了花生筛选，过滤掉包含花生过敏原（ID为2）的菜品
    const hitPeanut = filterPeanut.value ? !(d.allergens || []).some(a => String(a.id) === '2') : true
    return hitQ && hitA && hitPeanut
  })
})

// 将菜品分为餐食和佐饮两类
// 餐食: 八宝红鲟饭(1) 和 枸杞百合伴藕带(2)
// 佐饮: 铁观音(3) 和 怡园德熙珍藏霞多丽干白葡萄酒(4)
const foodDishes = computed(() => {
  return filtered.value.filter(d => d.id === 1 || d.id === 2)
})

const drinkDishes = computed(() => {
  return filtered.value.filter(d => d.id === 3 || d.id === 4)
})
</script>

<template>
  <div class="menu-page">
    <!-- Hero Section -->
    <div class="menu-hero">
      <div class="hero-content">
        <h1 class="hero-title">{{ t('menu_title') }}</h1>
        <p class="hero-subtitle">{{ t('menu_subtitle') }}</p>
        <div 
          class="hero-member-notice" 
          v-if="displayName"
          :class="{ 'filtered': filterPeanut }"
          @click="filterPeanut = !filterPeanut"
        >
          <div class="notice-content">
            <span class="notice-icon">{{ filterPeanut ? '✓' : '⚙' }}</span>
            <span class="notice-text">
              {{ filterPeanut 
                ? t('menu_page.member_notice_filtered', { name: displayName })
                : t('menu_page.member_notice_all', { name: displayName })
              }}
            </span>
            <span class="notice-hint">{{ t('menu_page.click_to_toggle') }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Filter Section -->
    <div class="filter-section">
      <div class="filter-container">
        <el-input 
          v-model="q" 
          :placeholder="t('filter_keyword')" 
          :prefix-icon="Search"
          clearable 
          size="large"
          class="search-input"
        />
        <el-select 
          v-model="allergen" 
          :placeholder="t('filter_allergen')" 
          :prefix-icon="Filter"
          clearable 
          size="large"
          class="filter-select"
        >
          <el-option :label="t('no_allergen')" value="" />
          <el-option v-for="a in allergens" :key="a.id" :label="t(`allergens.${a.id}.name`) || (locale==='zh-HK'?a.name_zh:a.name_en)" :value="String(a.id)" />
        </el-select>
      </div>
    </div>

    <!-- 餐食板块 -->
    <div class="section">
      <div class="section-header">
        <div class="section-badge">🍽</div>
        <h2 class="section-title">{{ t('food_section') }}</h2>
        <div class="section-line"></div>
      </div>
      <div class="grid">
        <div v-for="d in foodDishes" :key="d.id" class="dish-card" @click="$router.push('/dish/' + d.id)">
          <div class="card-image-wrapper">
            <img :src="getImageForDish(d.id)" :alt="nameOf(d)" class="card-image" />
            <div class="card-overlay">
              <span class="view-detail">{{ t('view_detail') }}</span>
            </div>
          </div>
          <div class="card-content">
            <h3 class="card-title">{{ nameOf(d) }}</h3>
            <p class="card-desc" :title="descOf(d)">{{ descOf(d) || '-' }}</p>
            <div class="card-meta">
              <span class="calorie-badge">
                <span class="calorie-icon">🔥</span>
                {{ d.calories || '-' }} {{ t('kcal') }}
              </span>
            </div>
            <div class="card-tags">
              <span v-for="a in d.allergens" :key="a.id" class="allergen-tag">
                {{ t(`allergens.${a.id}.name`) || (locale==='zh-HK'?a.name_zh:a.name_en) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 佐饮板块 -->
    <div class="section">
      <div class="section-header">
        <div class="section-badge">🍵</div>
        <h2 class="section-title">{{ t('drink_section') }}</h2>
        <div class="section-line"></div>
      </div>
      <div class="grid" v-if="drinkDishes.length > 0">
        <div v-for="d in drinkDishes" :key="d.id" class="dish-card" @click="$router.push('/dish/' + d.id)">
          <div class="card-image-wrapper">
            <img :src="getImageForDish(d.id)" :alt="nameOf(d)" class="card-image" />
            <div class="card-overlay">
              <span class="view-detail">{{ t('view_detail') }}</span>
            </div>
          </div>
          <div class="card-content">
            <h3 class="card-title">{{ nameOf(d) }}</h3>
            <p class="card-desc" :title="descOf(d)">{{ descOf(d) || '-' }}</p>
            <div class="card-meta">
              <span class="calorie-badge">
                <span class="calorie-icon">🔥</span>
                {{ d.calories || '-' }} {{ t('kcal') }}
              </span>
            </div>
            <div class="card-tags">
              <span v-for="a in d.allergens" :key="a.id" class="allergen-tag">
                {{ t(`allergens.${a.id}.name`) || (locale==='zh-HK'?a.name_zh:a.name_en) }}
              </span>
            </div>
          </div>
        </div>
      </div>
      <div class="empty-section" v-else>
        <p>{{ t('no_drinks_available') }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.menu-page {
  min-height: 100vh;
  background: linear-gradient(to bottom, #f8fafc 0%, #ffffff 100%);
}

/* Hero Section */
.menu-hero {
  background: linear-gradient(135deg, #006564 0%, #00857d 100%);
  padding: 60px 20px;
  text-align: center;
  border-radius: 0 0 30px 30px;
  margin-bottom: 40px;
  box-shadow: 0 10px 40px rgba(0, 101, 100, 0.2);
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 42px;
  font-weight: 800;
  color: white;
  margin: 0 0 15px 0;
  letter-spacing: -0.5px;
  text-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
}

.hero-subtitle {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.95);
  margin: 0 0 16px 0;
  font-weight: 400;
  line-height: 1.6;
}

.hero-member-notice {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.9);
  margin: 16px 0 0 0;
  font-weight: 500;
  line-height: 1.6;
  padding: 16px 24px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  user-select: none;
}

.hero-member-notice:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.hero-member-notice.filtered {
  background: rgba(76, 175, 80, 0.25);
  border-color: rgba(76, 175, 80, 0.4);
}

.notice-content {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.notice-icon {
  font-size: 20px;
  font-weight: bold;
  min-width: 24px;
  text-align: center;
}

.notice-text {
  flex: 1;
  min-width: 200px;
}

.notice-hint {
  font-size: 13px;
  opacity: 0.8;
  font-style: italic;
}

/* Filter Section */
.filter-section {
  padding: 0 20px 40px;
}

.filter-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.search-input {
  flex: 1;
  min-width: 260px;
}

.filter-select {
  width: 240px;
}

:deep(.search-input .el-input__wrapper) {
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

:deep(.search-input .el-input__wrapper:hover) {
  box-shadow: 0 4px 20px rgba(0, 101, 100, 0.15);
}

:deep(.filter-select .el-input__wrapper) {
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

/* Section */
.section {
  margin-bottom: 60px;
  padding: 0 20px;
}

.section-header {
  max-width: 1200px;
  margin: 0 auto 30px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.section-badge {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #006564 0%, #00857d 100%);
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  box-shadow: 0 4px 15px rgba(0, 101, 100, 0.3);
}

.section-title {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
  letter-spacing: -0.3px;
}

.section-line {
  flex: 1;
  height: 2px;
  background: linear-gradient(to right, #e2e8f0, transparent);
}

/* Grid */
.grid {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  gap: 24px;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
}

/* Dish Card */
.dish-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.dish-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 30px rgba(0, 101, 100, 0.2);
}

.card-image-wrapper {
  position: relative;
  width: 100%;
  padding-top: 75%; /* 4:3 aspect ratio */
  overflow: hidden;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.card-image {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center;
  transition: transform 0.4s ease;
  padding: 10px;
}

.dish-card:hover .card-image {
  transform: translate(-50%, -50%) scale(1.05);
}

.card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to top, rgba(0, 101, 100, 0.9), transparent);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding: 20px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.dish-card:hover .card-overlay {
  opacity: 1;
}

.view-detail {
  color: white;
  font-weight: 600;
  font-size: 16px;
  padding: 10px 24px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.card-content {
  padding: 20px;
}

.card-title {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 10px 0;
  line-height: 1.4;
}

.card-desc {
  color: #64748b;
  font-size: 14px;
  line-height: 1.6;
  height: 42px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  margin: 0 0 12px 0;
}

.card-meta {
  margin-bottom: 12px;
}

.calorie-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  color: #92400e;
}

.calorie-icon {
  font-size: 14px;
}

.card-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.allergen-tag {
  padding: 5px 12px;
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  color: #065f46;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.empty-section {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-radius: 20px;
  border: 2px dashed #cbd5e1;
}

.empty-section p {
  color: #64748b;
  font-size: 16px;
  margin: 0;
  font-style: italic;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-title {
    font-size: 32px;
  }

  .hero-subtitle {
    font-size: 16px;
  }

  .filter-container {
    flex-direction: column;
  }

  .filter-select {
    width: 100%;
  }

  .section-title {
    font-size: 24px;
  }

  .grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}

@media (max-width: 480px) {
  .menu-hero {
    padding: 40px 20px;
  }

  .hero-title {
    font-size: 28px;
  }

  .section-badge {
    width: 40px;
    height: 40px;
    font-size: 20px;
  }
}
</style>