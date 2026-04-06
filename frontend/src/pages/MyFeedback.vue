<script setup>
import axios from 'axios'
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Check, Clock, Edit } from '@element-plus/icons-vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

const { t, locale } = useI18n()
const authStore = useAuthStore()
const { user } = storeToRefs(authStore)

// 获取会员等级显示文本
const getMembershipTierText = (tier) => {
  if (!tier) return t('my_info.tiers.silver')
  const tierMap = {
    '钻石': t('my_info.tiers.diamond'),
    '金卡': t('my_info.tiers.gold'),
    '银卡': t('my_info.tiers.silver'),
    '普通': t('my_info.tiers.regular'),
    'Diamond': t('my_info.tiers.diamond'),
    'Gold': t('my_info.tiers.gold'),
    'Silver': t('my_info.tiers.silver'),
    'Regular': t('my_info.tiers.regular')
  }
  return tierMap[tier] || t('my_info.tiers.silver')
}

// 计算属性：确保显示固定值（如果值为0或undefined，使用默认值）
const pointsBalance = computed(() => {
  const value = user.value?.points_balance
  return (value !== undefined && value !== null && value !== 0) ? value : 320
})
const milesBalance = computed(() => {
  const value = user.value?.miles_balance
  return (value !== undefined && value !== null && value !== 0) ? value : 3200
})
const membershipTier = computed(() => {
  const value = user.value?.membership_tier
  return value || '银卡'
})

const feedbackList = ref([])
const showEditDialog = ref(false)
const isDeleting = ref(false)  // 删除状态锁
const isSaving = ref(false)    // 保存状态锁
const editForm = ref({
  id: null,
  rating: 5,
  taste_rating: 0,
  texture_rating: 0,
  quantity_rating: 0,
  leftover_level: 1,
  leftover_reason: 0,
  notes: ''
})

// 根据当前语言获取菜品名称
const getDishName = (dish_detail) => {
  if (!dish_detail) return t('feedback.unknown_dish')
  
  if (locale.value === 'en') {
    return dish_detail.name_en || dish_detail.name_zh
  } else if (locale.value === 'zh-HK') {
    // 繁体中文使用 name_zh_hk,如果没有则回退到 name_zh
    return dish_detail.name_zh_hk || dish_detail.name_zh || dish_detail.name_en
  } else {
    // 简体中文使用 name_zh
    return dish_detail.name_zh || dish_detail.name_en
  }
}

// 获取我的反馈列表
const fetchMyFeedback = async () => {
  try {
    const response = await axios.get('/api/survey/')
    // 这里应该根据当前用户筛选，暂时显示所有反馈
    feedbackList.value = response.data
  } catch (error) {
    ElMessage.error(t('feedback.messages.fetch_failed'))
  }
}

const statusMap = computed(() => ({
  0: t('feedback.status.received'),
  1: t('feedback.status.accepted'),
  2: t('feedback.status.rejected')
}))

const getStatusText = (status) => statusMap.value[status] || t('feedback.status.unknown')

const leftoverReasonMap = computed(() => ({
  0: t('survey.leftover_reasons.none'),
  1: t('survey.leftover_reasons.taste'),
  2: t('survey.leftover_reasons.quantity'),
  3: t('survey.leftover_reasons.personal'),
  4: t('survey.leftover_reasons.quality')
}))

const getLeftoverReasonText = (reason) => leftoverReasonMap.value[reason] || t('feedback.reasons.unknown')

// 打开编辑对话框
const openEditDialog = (feedback) => {
  editForm.value = {
    id: feedback.id,
    rating: Number(feedback.rating) || 5,  // 确保是数字类型
    taste_rating: feedback.taste_rating,
    texture_rating: feedback.texture_rating,
    quantity_rating: feedback.quantity_rating,
    leftover_level: feedback.leftover_level,
    leftover_reason: feedback.leftover_reason,
    notes: feedback.notes
  }
  showEditDialog.value = true
}

// 保存编辑
const saveEdit = async () => {
  if (isSaving.value) {
    console.log('正在保存中，请勿重复操作')
    return
  }
  
  try {
    isSaving.value = true
    await axios.put(`/api/survey/${editForm.value.id}/`, editForm.value)
    ElMessage.success(t('feedback.messages.update_success'))
    showEditDialog.value = false
    await fetchMyFeedback() // 重新加载数据
  } catch (error) {
    ElMessage.error(t('feedback.messages.update_failed'))
  } finally {
    isSaving.value = false
  }
}

// 删除反馈
const deleteFeedback = async () => {
  // 防止重复点击
  if (isDeleting.value) {
    console.log('删除操作进行中，请勿重复点击')
    return
  }
  
  try {
    await ElMessageBox.confirm(
      t('feedback.messages.delete_confirm'),
      t('feedback.messages.delete_warning'),
      {
        confirmButtonText: t('feedback.actions.confirm_delete'),
        cancelButtonText: t('common.cancel'),
        type: 'warning',
      }
    )
    
    // 确认后才设置删除锁
    isDeleting.value = true
    const surveyId = editForm.value.id
    
    // 立即从列表中移除（乐观更新）
    const originalList = [...feedbackList.value]
    feedbackList.value = feedbackList.value.filter(item => item.id !== surveyId)
    
    // 立即关闭对话框
    showEditDialog.value = false
    
    try {
      const response = await axios.delete(`/api/survey/${surveyId}/`)
      
      // 检查响应消息
      if (response.data && response.data.message) {
        ElMessage.success(response.data.message)
      } else {
        ElMessage.success(t('feedback.messages.delete_success'))
      }
      
      // 重新加载数据以确保同步
      await fetchMyFeedback()
      
    } catch (apiError) {
      console.error('删除API错误:', apiError)
      
      // 如果是404（已删除），显示警告但不恢复列表
      if (apiError.response && apiError.response.status === 404) {
        ElMessage.warning(t('feedback.messages.already_deleted'))
        await fetchMyFeedback() // 刷新列表
      } 
      // 如果是200（后端返回已删除消息）
      else if (apiError.response && apiError.response.status === 200) {
        const msg = apiError.response.data?.message || t('feedback.messages.already_deleted')
        ElMessage.warning(msg)
        await fetchMyFeedback()
      }
      // 其他错误，恢复列表
      else {
        feedbackList.value = originalList
        
        if (apiError.response && apiError.response.data && apiError.response.data.error) {
          ElMessage.error(apiError.response.data.error)
        } else {
          ElMessage.error(t('feedback.messages.delete_failed'))
        }
      }
    } finally {
      isDeleting.value = false
    }
    
  } catch (error) {
    // 用户取消删除
    if (error !== 'cancel') {
      console.error('删除确认对话框错误:', error)
    }
  }
}

// 页面加载时获取反馈列表和用户信息
onMounted(async () => {
  fetchMyFeedback()
  // 强制获取最新的用户信息（包括积分、里数、会员等级）
  try {
    const userData = await authStore.fetchProfile()
    console.log('用户信息已更新:', userData)
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
})
</script>

<template>
  <!-- 我的信息板块 -->
  <el-card class="card info-card" shadow="never" style="margin-bottom: 24px;">
    <template #header>
      <strong>{{ $t('my_info.title') }}</strong>
    </template>
    <div class="info-content">
      <div class="info-row">
        <span class="info-label">{{ $t('my_info.name') }}：</span>
        <span class="info-value">{{ user?.full_name || '-' }}</span>
      </div>
      <div class="info-row">
        <span class="info-label">{{ $t('my_info.identifier') }}：</span>
        <span class="info-value">{{ user?.identifier || '-' }}</span>
      </div>
      <div class="info-row" v-if="user?.email">
        <span class="info-label">{{ $t('my_info.email') }}：</span>
        <span class="info-value">{{ user.email }}</span>
      </div>
      <div class="info-row" v-if="user?.phone">
        <span class="info-label">{{ $t('my_info.phone') }}：</span>
        <span class="info-value">{{ user.phone }}</span>
      </div>
      <div class="info-row">
        <span class="info-label">{{ $t('my_info.points_balance') }}：</span>
        <span class="info-value highlight">{{ pointsBalance }}</span>
      </div>
      <div class="info-row">
        <span class="info-label">{{ $t('my_info.miles_balance') }}：</span>
        <span class="info-value highlight">{{ milesBalance }}</span>
      </div>
      <div class="info-row">
        <span class="info-label">{{ $t('my_info.membership_tier') }}：</span>
        <span class="info-value highlight">{{ getMembershipTierText(membershipTier) }}</span>
      </div>
    </div>
  </el-card>

  <!-- 菜品反馈板块 -->
  <el-card class="card" shadow="never">
    <template #header>
      <strong>{{ $t('feedback.title') }}</strong>
    </template>

    <el-table :data="feedbackList" style="width: 100%" stripe border :empty-text="' '">
      <!-- 菜品 -->
      <el-table-column prop="dish" :label="$t('feedback.columns.dish')" width="140" show-overflow-tooltip>
        <template #default="scope">
          {{ getDishName(scope.row.dish_detail) }}
        </template>
      </el-table-column>
      
      <!-- 评分 -->
      <el-table-column prop="rating" :label="$t('feedback.columns.rating')" width="140" align="center">
        <template #default="scope">
          <el-rate 
            :model-value="Number(scope.row.rating)" 
            disabled 
            :max="5"
            text-color="#ff9900"
          />
        </template>
      </el-table-column>
      
      <!-- 剩餐 -->
      <el-table-column prop="leftover_level" :label="$t('feedback.columns.leftover_level')" width="90" align="center">
        <template #default="scope">
          <el-tag size="small" :type="scope.row.leftover_level === 0 ? 'success' : scope.row.leftover_level >= 3 ? 'danger' : 'warning'">
            <span v-if="scope.row.leftover_level === 0">0%</span>
            <span v-else-if="scope.row.leftover_level === 1">&lt;25%</span>
            <span v-else-if="scope.row.leftover_level === 2">25-50%</span>
            <span v-else-if="scope.row.leftover_level === 3">50-75%</span>
            <span v-else>&gt;75%</span>
          </el-tag>
        </template>
      </el-table-column>
      
      <!-- 剩餐原因 -->
      <el-table-column prop="leftover_reason" :label="$t('feedback.columns.leftover_reason')" width="100" show-overflow-tooltip>
        <template #default="scope">
          {{ getLeftoverReasonText(scope.row.leftover_reason) }}
        </template>
      </el-table-column>
      
      <!-- 提交时间 -->
      <el-table-column prop="created_at" :label="$t('feedback.columns.submitted_at')" width="110" show-overflow-tooltip>
        <template #default="scope">
          {{ new Date(scope.row.created_at).toLocaleDateString() }}
        </template>
      </el-table-column>
      
      <!-- 状态 -->
      <el-table-column prop="status" :label="$t('feedback.columns.status')" width="90" align="center">
        <template #default="scope">
          <el-tag 
            :type="scope.row.status === 1 ? 'success' : scope.row.status === 2 ? 'danger' : 'info'" 
            size="small"
          >
            {{ getStatusText(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      
      <!-- 里数 -->
      <el-table-column prop="miles_awarded" :label="$t('feedback.columns.miles')" width="90" align="center">
        <template #default="scope">
          <el-icon v-if="scope.row.miles_awarded" color="#67c23a" :size="20">
            <Check />
          </el-icon>
          <el-icon v-else color="#e6a23c" :size="20">
            <Clock />
          </el-icon>
        </template>
      </el-table-column>
      
      <!-- 备注 -->
      <el-table-column prop="notes" :label="$t('notes')" min-width="120" show-overflow-tooltip>
        <template #default="scope">
          <span style="color: #909399;">{{ scope.row.notes || '-' }}</span>
        </template>
      </el-table-column>
      
      <!-- 主厨回复 -->
      <el-table-column prop="chef_response" :label="$t('feedback.columns.chef_response')" min-width="120" show-overflow-tooltip>
        <template #default="scope">
          <span :style="{ color: scope.row.chef_response ? '#303133' : '#c0c4cc' }">
            {{ scope.row.chef_response || $t('feedback.no_reply') }}
          </span>
        </template>
      </el-table-column>
      
      <!-- 操作 -->
      <el-table-column :label="$t('feedback.columns.actions')" width="80" fixed="right" align="center">
        <template #default="scope">
          <el-button 
            size="small" 
            type="primary" 
            circle
            @click="openEditDialog(scope.row)"
          >
            <el-icon><Edit /></el-icon>
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <div v-if="feedbackList.length === 0" class="no-data">
      {{ $t('feedback.no_records') }}
    </div>

    <!-- 编辑对话框 -->
    <el-dialog v-model="showEditDialog" :title="$t('feedback.dialog.title')" width="600px">
      <el-form :model="editForm" label-width="100px">
        <el-form-item label="">
          <el-rate v-model="editForm.rating" :max="5" />
        </el-form-item>
        <el-form-item :label="$t('survey.taste_label')">
          <el-select v-model="editForm.taste_rating" style="width: 100%">
            <el-option :label="$t('survey.common.not_selected')" :value="0" />
            <el-option :label="$t('survey.taste_options.salty')" :value="1" />
            <el-option :label="$t('survey.taste_options.light')" :value="2" />
            <el-option :label="$t('survey.taste_options.balanced')" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item :label="$t('survey.texture_label')">
          <el-select v-model="editForm.texture_rating" style="width: 100%">
            <el-option :label="$t('survey.common.not_selected')" :value="0" />
            <el-option :label="$t('survey.texture_options.overcooked')" :value="1" />
            <el-option :label="$t('survey.texture_options.undercooked')" :value="2" />
            <el-option :label="$t('survey.texture_options.balanced')" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item :label="$t('survey.quantity_label')">
          <el-select v-model="editForm.quantity_rating" style="width: 100%">
            <el-option :label="$t('survey.common.not_selected')" :value="0" />
            <el-option :label="$t('survey.quantity_options.too_much')" :value="1" />
            <el-option :label="$t('survey.quantity_options.just_right')" :value="2" />
            <el-option :label="$t('survey.quantity_options.not_enough')" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item :label="$t('leftover_level')">
          <el-select v-model="editForm.leftover_level" style="width: 100%">
            <el-option label="0%" :value="0" />
            <el-option label="<25%" :value="1" />
            <el-option label="25-50%" :value="2" />
            <el-option label="50-75%" :value="3" />
            <el-option label=">75%" :value="4" />
          </el-select>
        </el-form-item>
        <el-form-item :label="$t('survey.reason_label')">
          <el-select v-model="editForm.leftover_reason" style="width: 100%">
            <el-option :label="$t('survey.leftover_reasons.none')" :value="0" />
            <el-option :label="$t('survey.leftover_reasons.taste')" :value="1" />
            <el-option :label="$t('survey.leftover_reasons.quantity')" :value="2" />
            <el-option :label="$t('survey.leftover_reasons.personal')" :value="3" />
            <el-option :label="$t('survey.leftover_reasons.quality')" :value="4" />
          </el-select>
        </el-form-item>
        <el-form-item :label="$t('notes')">
          <el-input v-model="editForm.notes" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button 
            type="danger" 
            @click="deleteFeedback"
            :loading="isDeleting"
            :disabled="isDeleting || isSaving"
          >
            {{ $t('feedback.actions.delete') }}
          </el-button>
          <div style="flex: 1;"></div>
          <el-button 
            @click="showEditDialog = false"
            :disabled="isDeleting || isSaving"
          >
            {{ $t('common.cancel') }}
          </el-button>
          <el-button 
            type="primary" 
            @click="saveEdit"
            :loading="isSaving"
            :disabled="isDeleting || isSaving"
          >
            {{ $t('common.save') }}
          </el-button>
        </span>
      </template>
    </el-dialog>
  </el-card>
</template>

<style scoped>
.card {
  max-width: 1200px;
  margin: 0 auto;
}

.info-card {
  background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
  border: 1px solid #e5e7eb;
}

.info-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  padding: 8px 0;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.info-label {
  font-weight: 600;
  color: #4b5563;
  min-width: 80px;
}

.info-value {
  color: #1f2937;
  font-size: 15px;
}

.info-value.highlight {
  color: #0f766e;
  font-weight: 600;
  font-size: 16px;
}

.no-data {
  text-align: center;
  color: #909399;
  padding: 40px 0;
}
.dialog-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

@media (max-width: 768px) {
  .info-content {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}
</style>
