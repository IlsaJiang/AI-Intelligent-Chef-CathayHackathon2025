<script setup>
import axios from 'axios'
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { Star, Document, Upload, ChatDotRound } from '@element-plus/icons-vue'

// 导入所有语言版本的感谢信图片
import thankYouImageZH from '@/assets/3Q_letter_ZH.jpg'
import thankYouImageHK from '@/assets/3Q_letter_HK.jpg'
import thankYouImageEN from '@/assets/3Q_letter_EN.jpg'

const { t, locale } = useI18n()

const thankYouImageDialogVisible = ref(false) // 感谢信图片弹窗
const isFirstTimeSubmission = ref(false) // 是否首次提交
const form = ref({
  user: null,
  dish: null,
  rating: 5,
  taste_rating: 0,  // 口味评分
  texture_rating: 0,  // 口感评分
  quantity_rating: 0,  // 分量评分
  leftover_level: 1,
  leftover_reason: 0,  // 剩余原因（非必选）
  notes: ''
})

// 根据当前语言获取菜品名称
const getDishName = (dish) => {
  if (!dish) return ''
  
  if (locale.value === 'en') {
    return dish.name_en || dish.name_zh
  } else if (locale.value === 'zh-HK') {
    // 繁体中文使用 name_zh_hk,如果没有则回退到 name_zh
    return dish.name_zh_hk || dish.name_zh || dish.name_en
  } else {
    // 简体中文使用 name_zh
    return dish.name_zh || dish.name_en
  }
}

// 根据当前语言动态选择感谢信图片（默认显示繁体版本）
const currentThankYouImage = computed(() => {
  switch (locale.value) {
    case 'zh': // 简体中文
      return thankYouImageZH
    case 'en':    // 英文
      return thankYouImageEN
    case 'zh-HK': // 繁体中文
    default:      // 默认情况显示繁体版本
      return thankYouImageHK
  }
})

// 周期性反馈表单
const feedbackForm = ref({
  answer: ''
})

const feedbackQuestion = computed(() => t('survey.feedback.question'))

const dishes = ref([])  // 菜品列表
const leftoverPhoto = ref(null)  // 剩餐照片
const milesAwarded = ref(0)
const showmilesMessage = ref(false)
const milesAlertTitle = computed(() => t('survey.messages.miles_awarded', { miles: milesAwarded.value }))

// 口味评分选项
const tasteOptions = computed(() => [
  { label: t('survey.taste_options.salty'), value: 1 },
  { label: t('survey.taste_options.light'), value: 2 },
  { label: t('survey.taste_options.balanced'), value: 3 }
])

// 口感评分选项
const textureOptions = computed(() => [
  { label: t('survey.texture_options.overcooked'), value: 1 },
  { label: t('survey.texture_options.undercooked'), value: 2 },
  { label: t('survey.texture_options.balanced'), value: 3 }
])

// 分量评分选项
const quantityOptions = computed(() => [
  { label: t('survey.quantity_options.too_much'), value: 1 },
  { label: t('survey.quantity_options.just_right'), value: 2 },
  { label: t('survey.quantity_options.not_enough'), value: 3 }
])

// 剩余原因选项
const leftoverReasonOptions = computed(() => [
  { label: t('survey.leftover_reasons.none'), value: 0 },
  { label: t('survey.leftover_reasons.taste'), value: 1 },
  { label: t('survey.leftover_reasons.quantity'), value: 2 },
  { label: t('survey.leftover_reasons.personal'), value: 3 },
  { label: t('survey.leftover_reasons.quality'), value: 4 }
])

// 获取菜品列表
const fetchDishes = async () => {
  try {
    const response = await axios.get('/api/dishes/')
    dishes.value = response.data
  } catch (error) {
    ElMessage.error(t('survey.messages.fetch_failed'))
  }
}

// 提交表单
const submit = async () => {
  // 验证必填字段
  if (!form.value.dish) {
    ElMessage.warning(t('survey.messages.select_dish'))
    return
  }
  
  if (form.value.taste_rating === 0) {
    ElMessage.warning(t('survey.messages.taste_required'))
    return
  }
  
  if (form.value.texture_rating === 0) {
    ElMessage.warning(t('survey.messages.texture_required'))
    return
  }
  
  if (form.value.quantity_rating === 0) {
    ElMessage.warning(t('survey.messages.quantity_required'))
    return
  }
  
  try {
    // 提交问卷
    const response = await axios.post('/api/survey/', form.value)
    
    // 判断是否首次提交(是否获得里数)
    isFirstTimeSubmission.value = response.data.miles_awarded > 0
    
    // 处理里数信息
    if (response.data.miles_awarded > 0) {
      milesAwarded.value = response.data.miles_awarded
      showmilesMessage.value = true
    }

    // 如果上传剩餐照片
    if (leftoverPhoto.value) {
      const fd = new FormData()
      fd.append('user', form.value.user || '')
      fd.append('dish', form.value.dish)
      fd.append('leftover_percent', form.value.leftover_level * 25)
      fd.append('photo', leftoverPhoto.value.raw)

      await axios.post('/api/leftover/', fd, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    }

    // 同时显示感谢消息和感谢信图片弹窗
    // 使用绿色消息提示显示感谢文字
    ElMessage({
      message: thankYouMessage.value,
      type: 'success',
      duration: 5000,
      customClass: 'thank-you-message'
    })
    
    // 同时显示感谢信图片弹窗
    thankYouImageDialogVisible.value = true
  } catch (e) {
    ElMessage.error(t('survey.messages.submit_failed'))
  }
}



// 提交周期性反馈
const submitFeedback = async () => {
  try {
    // 提交周期性反馈（不增加里数）
    await axios.post('/api/periodic-feedback/', {
      question: feedbackQuestion.value,
      answer: feedbackForm.value.answer
    })
    
    ElMessage.success(t('survey.feedback.success'))
  } catch (error) {
    ElMessage.error(t('survey.feedback.error'))
  }
}

// 感谢消息文字
const thankYouMessage = computed(() => {
  return isFirstTimeSubmission.value
    ? t('survey.thank_you.first_time_message', { miles: milesAwarded.value })
    : t('survey.thank_you.repeat_message')
})

// 页面加载时获取菜品列表
onMounted(() => {
  fetchDishes()
})
</script>

<template>
  <div class="survey-page">
    <!-- Hero Section -->
    <div class="survey-hero">
      <div class="hero-content">
        <h1 class="hero-title">{{ $t('survey.hero_title') }}</h1>
        <p class="hero-subtitle">{{ $t('survey.hero_subtitle') }}</p>
      </div>
    </div>

    <div class="survey-container">
      <!-- 里数信息卡片 -->
      <div class="miles-card">
        <div class="miles-icon">✈️</div>
        <div class="miles-content">
          <h3 class="miles-title">{{ $t('survey.miles.title') }}</h3>
          <ul class="miles-list">
            <li>{{ $t('survey.miles.line_1') }}</li>
            <li>{{ $t('survey.miles.line_2') }}</li>
            <li>{{ $t('survey.miles.line_3') }}</li>
          </ul>
        </div>
      </div>

      <!-- 里数奖励提示 -->
      <el-alert 
        v-if="showmilesMessage" 
        :title="milesAlertTitle" 
        type="success" 
        show-icon 
        :closable="false"
        class="miles-alert"
      />

      <!-- 主表单卡片 -->
      <div class="form-card">
        <div class="form-header">
          <h2 class="form-title">{{ $t('survey.form_title') }}</h2>
          <div class="title-decoration"></div>
        </div>

        <el-form :model="form" label-position="top" class="survey-form">
          <div class="form-row two-col">
            <!-- 菜品选择 -->
            <el-form-item :label="$t('dish_id')" required class="form-item-highlight form-col">
              <el-select 
                v-model="form.dish" 
                :placeholder="$t('select_dish')" 
                size="large"
                class="full-width-select"
              >
                <el-option
                  v-for="dish in dishes"
                  :key="dish.id"
                  :label="getDishName(dish)"
                  :value="dish.id"
                />
              </el-select>
            </el-form-item>

            <!-- 整体评分 -->
            <el-form-item :label="$t('rating')" class="rating-item form-col rating-col">
              <div class="rating-wrapper">
                <el-rate v-model="form.rating" :max="5" size="large" />
                <span class="rating-text">{{ form.rating }}/5</span>
              </div>
            </el-form-item>
          </div>

          <!-- 细化评分区域 -->
          <div class="detailed-ratings">
            <h3 class="section-title">{{ $t('survey.detailed_ratings_title') }}</h3>
            
            <!-- 口味评分 -->
            <el-form-item :label="$t('survey.taste_label')" required class="radio-group-item">
              <el-radio-group v-model="form.taste_rating" class="custom-radio-group">
                <el-radio 
                  v-for="option in tasteOptions" 
                  :key="option.value" 
                  :label="option.value"
                  :class="{'is-selected': form.taste_rating === option.value}"
                  border
                >
                  {{ option.label }}
                </el-radio>
              </el-radio-group>
            </el-form-item>

            <!-- 口感评分 -->
            <el-form-item :label="$t('survey.texture_label')" required class="radio-group-item">
              <el-radio-group v-model="form.texture_rating" class="custom-radio-group">
                <el-radio 
                  v-for="option in textureOptions" 
                  :key="option.value" 
                  :label="option.value"
                  :class="{'is-selected': form.texture_rating === option.value}"
                  border
                >
                  {{ option.label }}
                </el-radio>
              </el-radio-group>
            </el-form-item>

            <!-- 分量评分 -->
            <el-form-item :label="$t('survey.quantity_label')" required class="radio-group-item">
              <el-radio-group v-model="form.quantity_rating" class="custom-radio-group">
                <el-radio 
                  v-for="option in quantityOptions" 
                  :key="option.value" 
                  :label="option.value"
                  :class="{'is-selected': form.quantity_rating === option.value}"
                  border
                >
                  {{ option.label }}
                </el-radio>
              </el-radio-group>
            </el-form-item>
          </div>

          <!-- 剩餐信息区域 -->
          <div class="leftover-section">
            <h3 class="section-title">{{ $t('survey.leftover_section_title') }}</h3>
            
            <!-- 剩餐程度 -->
            <el-form-item :label="$t('leftover_level')">
              <el-select v-model="form.leftover_level" size="large" class="full-width-select">
                <el-option label="0%" :value="0" />
                <el-option label="<25%" :value="1" />
                <el-option label="25-50%" :value="2" />
                <el-option label="50-75%" :value="3" />
                <el-option label=">75%" :value="4" />
              </el-select>
            </el-form-item>

            <!-- 剩余原因 -->
            <el-form-item :label="$t('survey.reason_label')">
              <el-select v-model="form.leftover_reason" size="large" class="full-width-select">
                <el-option 
                  v-for="option in leftoverReasonOptions" 
                  :key="option.value" 
                  :label="option.label" 
                  :value="option.value"
                />
              </el-select>
            </el-form-item>
          </div>

          <!-- 备注 -->
          <el-form-item :label="$t('notes')">
            <el-input 
              v-model="form.notes" 
              type="textarea" 
              :rows="4" 
              :placeholder="$t('survey.notes_placeholder')"
              class="custom-textarea"
            />
          </el-form-item>

          <!-- 照片上传区域 -->
          <div class="upload-section">
            <h3 class="section-title">{{ $t('survey.upload_section_title') }}</h3>
            
            <div class="upload-grid single-upload">
              <!-- 剩餐照片 -->
              <el-form-item :label="$t('upload_leftover')" class="upload-item">
                <el-upload
                  :auto-upload="false"
                  :limit="1"
                  :on-change="file => leftoverPhoto = file"
                  accept="image/*"
                  class="custom-upload"
                  drag
                >
                  <div class="upload-content">
                    <Upload class="upload-icon" />
                    <div class="upload-text">{{ $t('survey.actions.drag_or_click') }}</div>
                  </div>
                </el-upload>
              </el-form-item>
            </div>
          </div>

          <!-- 提交按钮 -->
          <el-form-item class="submit-item">
            <el-button type="primary" size="large" @click="submit" class="submit-btn">
              <Document style="margin-right: 8px;" />
              {{ $t('submit') }}
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 周期性反馈卡片 -->
      <div class="feedback-card">
        <div class="feedback-header">
          <h2 class="form-title">{{ $t('survey.feedback.title') }}</h2>
          <div class="title-decoration"></div>
        </div>
        
        <div class="feedback-content">
          <p class="feedback-question">{{ feedbackQuestion }}</p>
          <el-input
            v-model="feedbackForm.answer"
            type="textarea"
            :rows="4"
            :placeholder="$t('survey.feedback.placeholder')"
            class="custom-textarea"
          />
          <el-button type="primary" size="large" @click="submitFeedback" class="feedback-submit-btn">
            {{ $t('survey.feedback.submit') }}
          </el-button>
        </div>
      </div>

      <div class="disclaimer">{{ $t('disclaimer') }}</div>
    </div>

    <!-- 感谢信图片弹窗 -->
    <el-dialog
      v-model="thankYouImageDialogVisible"
      width="60%"
      :show-close="true"
      :close-on-click-modal="true"
      center
      class="thank-you-dialog"
    >
      <img :src="currentThankYouImage" alt="Thank You Letter" class="thank-you-image" />
    </el-dialog>
  </div>
</template>

<style scoped>
.survey-page {
  min-height: 100vh;
  background: linear-gradient(to bottom, #f8fafc 0%, #ffffff 100%);
}

/* Hero Section */
.survey-hero {
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
  font-size: 36px;
  font-weight: 800;
  color: white;
  margin: 0 0 15px 0;
  letter-spacing: -0.5px;
}

.hero-subtitle {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.95);
  margin: 0;
  line-height: 1.6;
}

/* Container */
.survey-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px 40px;
}

/* Miles Card */
.miles-card {
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border: 2px solid #93c5fd;
  border-radius: 20px;
  padding: 24px;
  margin-bottom: 24px;
  display: flex;
  gap: 8px; /* 更靠近文字 */
  align-items: center; /* 垂直居中更协调 */
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
  max-width: 720px;
  margin-left: auto;
  margin-right: auto;
}

.miles-icon {
  font-size: 40px; /* 小飞机更大 */
  flex-shrink: 0;
  line-height: 1; /* 避免额外空隙 */
}

.miles-content {
  flex: 1;
  text-align: center;
}

.miles-title {
  font-size: 20px;
  font-weight: 700;
  color: #1e40af;
  margin: 0 0 12px 0;
}

.miles-list {
  margin: 0;
  padding: 0;
  list-style: none;
  color: #1e40af;
}

.miles-list li {
  margin: 6px 0;
  line-height: 1.6;
}

.miles-alert {
  margin-bottom: 24px;
  border-radius: 12px;
}

/* Form Card */
.form-card {
  background: white;
  border-radius: 24px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.form-header,
.feedback-header {
  position: relative;
  margin-bottom: 16px;
  padding-bottom: 10px;
}

.form-header::after,
.feedback-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #006564 0%, #00857d 100%);
  border-radius: 2px;
}

.title-decoration {
  display: none;
}

.form-title {
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
  position: relative;
  padding-left: 12px;
}

.form-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 24px;
  background: linear-gradient(135deg, #006564 0%, #00857d 100%);
  border-radius: 2px;
}

/* Form */
.survey-form {
  margin-top: 12px;
}

:deep(.el-form-item) {
  margin-bottom: 16px;
}

:deep(.el-form-item__label) {
  font-weight: 600;
  color: #334155;
  font-size: 14px;
  padding-bottom: 6px;
}

.form-item-highlight :deep(.el-form-item__label) {
  color: #006564;
  font-size: 16px;
}

.full-width-select {
  width: 100%;
}

:deep(.full-width-select .el-input__wrapper) {
  border-radius: 12px;
}

/* Rating */
.rating-item {
  margin: 0;
}

.rating-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  background: #f8fafc;
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  transition: all 0.3s ease;
  min-height: 40px; /* 更贴近 large 选择框高度 */
}

.rating-wrapper:hover {
  border-color: #006564;
  background: #f0fdfa;
}

.rating-text {
  font-size: 14px;
  color: #475569;
  font-weight: 600;
}

:deep(.el-rate) {
  height: auto;
}

:deep(.el-rate__icon) {
  font-size: 20px;
  margin-right: 2px;
}

/* Section Title */
.section-title {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin: 20px 0 12px 0;
  padding-left: 10px;
  border-left: 4px solid #006564;
}

/* Detailed Ratings */
.detailed-ratings {
  background: #f8fafc;
  padding: 16px;
  border-radius: 12px;
  margin: 12px 0;
}

.radio-group-item {
  margin-bottom: 14px;
}

.radio-group-item:last-child {
  margin-bottom: 0;
}

.custom-radio-group {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

:deep(.custom-radio-group .el-radio) {
  margin: 0;
  border-radius: 12px;
  padding: 12px 20px;
  transition: all 0.3s ease;
}

:deep(.custom-radio-group .el-radio.is-bordered) {
  border: 2px solid #e2e8f0;
  background: white;
}

:deep(.custom-radio-group .el-radio.is-bordered.is-checked) {
  border-color: #006564;
  background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
}

:deep(.custom-radio-group .el-radio.is-bordered:hover) {
  border-color: #006564;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 101, 100, 0.15);
}

:deep(.custom-radio-group .el-radio__input.is-checked + .el-radio__label) {
  color: #006564;
  font-weight: 600;
}

/* Leftover Section */
.leftover-section {
  background: #f8fafc;
  padding: 16px;
  border-radius: 12px;
  margin: 12px 0;
}

/* Textarea */
.custom-textarea :deep(.el-textarea__inner) {
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  font-size: 14px;
  line-height: 1.6;
}

.custom-textarea :deep(.el-textarea__inner:focus) {
  border-color: #006564;
}

/* Upload Section */
.upload-section {
  margin: 16px 0;
}

.upload-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-top: 10px;
  align-items: stretch;
}

.upload-grid.single-upload {
  grid-template-columns: 1fr;
}

.upload-item {
  margin-bottom: 0;
}

.upload-item :deep(.el-form-item__content) {
  height: 100%;
}

.custom-upload :deep(.el-upload) {
  width: 100%;
  height: 100%;
}

.custom-upload :deep(.el-upload-dragger) {
  padding: 20px;
  border-radius: 10px;
  border: 2px dashed #cbd5e1;
  background: #f8fafc;
  transition: all 0.3s ease;
  min-height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.custom-upload :deep(.el-upload-dragger:hover) {
  border-color: #006564;
  background: #ecfdf5;
}

.upload-content {
  text-align: center;
}

.upload-icon {
  font-size: 32px;
  color: #64748b;
  margin-bottom: 6px;
}

.upload-text {
  color: #64748b;
  font-size: 12px; /* 缩小拖拽提示文字 */
  margin: 0;
}

/* Submit */
.submit-item {
  margin-top: 20px;
}

.submit-btn {
  width: 100%;
  border-radius: 12px;
  background: linear-gradient(135deg, #006564 0%, #00857d 100%);
  border: none;
  transition: all 0.3s ease;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 101, 100, 0.4);
}

/* Two column row for dish + rating */
.form-row.two-col {
  display: flex;
  gap: 16px;
  align-items: center; /* 两列整体中心对齐 */
}

.form-row.two-col .form-col {
  flex: 1;
  min-width: 0;
}

/* 调整两列宽度比例，提升视觉平衡（菜式选择更宽，评分稍窄） */
.form-row.two-col .form-col:first-child {
  flex: 3;
}
.form-row.two-col .form-col:last-child {
  flex: 2;
}

.form-row.two-col :deep(.el-form-item) {
  margin-bottom: 0;
}

.form-row.two-col :deep(.el-form-item__label) {
  font-size: 14px;
  font-weight: 600;
  color: #334155;
}

/* 表单内容常规顶起，不强制贴底，便于整体中心对齐 */
.form-row.two-col :deep(.el-form-item__content) {
  margin-top: 0;
}

/* Keep rating content aligned nicely */
.rating-col .rating-wrapper {
  justify-content: flex-end; /* 与选择框对齐到行尾，更稳重 */
}

/* 选择框占满列宽 */
.full-width-select {
  width: 100%;
}

/* Feedback Card */
.feedback-card {
  background: white;
  border-radius: 24px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.feedback-content {
  margin-top: 12px;
}

.feedback-question {
  font-size: 14px;
  font-weight: 600;
  color: #334155;
  margin-bottom: 12px;
  line-height: 1.6;
}

.feedback-submit-btn {
  margin-top: 12px;
  width: 100%;
  border-radius: 12px;
  background: linear-gradient(135deg, #006564 0%, #00857d 100%);
  border: none;
}

/* Disclaimer */
.disclaimer {
  text-align: center;
  color: #64748b;
  font-size: 13px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 12px;
  margin-top: 24px;
}

/* Dialog */
.thank-you-dialog :deep(.el-dialog) {
  border-radius: 20px;
  overflow: hidden;
}

.thank-you-dialog :deep(.el-dialog__body) {
  padding: 0;
  background-color: #000;
}

.thank-you-image {
  width: 100%;
  height: auto;
  display: block;
}

/* Responsive */
@media (max-width: 768px) {
  .survey-hero {
    padding: 40px 20px;
  }

  .hero-title {
    font-size: 28px;
  }

  .survey-container {
    padding: 20px 16px;
  }

  .miles-card {
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 20px;
    gap: 8px; /* 移动端图标与文字更紧凑 */
  }

  .miles-icon {
    font-size: 32px; /* 移动端略大一些 */
  }

  .miles-title {
    font-size: 17px;
    margin-bottom: 10px;
  }

  .miles-list {
    font-size: 13px;
  }

  .miles-list li {
    margin-bottom: 6px;
    line-height: 1.5;
  }

  .form-card,
  .feedback-card {
    padding: 20px;
    border-radius: 20px;
  }

  .form-header,
  .feedback-header {
    margin-bottom: 14px;
  }

  .form-title {
    font-size: 19px;
  }

  .section-title {
    font-size: 15px;
    margin: 16px 0 10px 0;
  }

  .detailed-ratings,
  .leftover-section {
    padding: 14px;
    margin: 10px 0;
  }

  .radio-group-item {
    margin-bottom: 12px;
  }

  .upload-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .custom-upload :deep(.el-upload-dragger) {
    padding: 16px;
    min-height: 150px;
  }

  .upload-icon {
    font-size: 28px;
  }

  .upload-text {
    font-size: 11px; /* 移动端更小 */
  }

  .custom-radio-group {
    gap: 8px;
  }

  /* 菜式 + 整體評分一行在移动端改为纵向 */
  .form-row.two-col {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }

  :deep(.custom-radio-group .el-radio) {
    padding: 10px 16px;
    font-size: 13px;
  }

  :deep(.el-radio-button__inner) {
    padding: 7px 12px;
    font-size: 12px;
  }

  .submit-btn {
    width: 100%;
    padding: 14px 32px;
    font-size: 15px;
  }

  .feedback-question {
    font-size: 13px;
    margin-bottom: 10px;
  }
}

@media (max-width: 480px) {
  .survey-container {
    padding: 16px 12px;
  }

  .hero-title {
    font-size: 24px;
  }

  .hero-subtitle {
    font-size: 14px;
  }

  .miles-card {
    padding: 16px;
    text-align: center;
    align-items: center;
  }

  .miles-icon {
    font-size: 28px;
    min-width: 36px;
  }

  .miles-title {
    font-size: 16px;
  }

  .miles-list {
    font-size: 12px;
  }

  .form-card,
  .feedback-card {
    padding: 16px;
    border-radius: 16px;
  }

  .form-title {
    font-size: 18px;
  }

  .section-title {
    font-size: 14px;
  }

  :deep(.el-form-item__label) {
    font-size: 13px;
  }

  .rating-wrapper {
    padding: 10px 12px;
    gap: 10px;
  }

  :deep(.el-rate__icon) {
    font-size: 20px;
    margin-right: 2px;
  }

  .custom-radio-group {
    gap: 6px;
  }

  :deep(.custom-radio-group .el-radio) {
    padding: 8px 12px;
    font-size: 12px;
  }

  :deep(.el-radio-button__inner) {
    padding: 6px 10px;
    font-size: 11px;
  }

  .submit-btn {
    padding: 12px 24px;
    font-size: 14px;
  }
  .form-row.two-col {
    gap: 10px;
  }
}
</style>

<style>
/* 感谢消息自定义样式 - 绿色背景，白色文字 */
.thank-you-message {
  background-color: #10b981 !important;
  border-color: #10b981 !important;
}
.thank-you-message .el-message__content {
  color: #ffffff !important;
}
.thank-you-message .el-message__icon {
  color: #ffffff !important;
}
</style>