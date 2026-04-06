<script setup>
import { onMounted, ref, computed } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { ArrowLeft, Camera } from '@element-plus/icons-vue'
import ChefChatPanel from '@/components/ChefChatPanel.vue'

// 导入菜品图片
import babaofanImage from '@/assets/babaofan.jpg'
import lianouImage from '@/assets/lianou.jpg'
import tieguanyinImage from '@/assets/tieguanyin.jpg'
import wineImage from '@/assets/wine.jpg'

const route = useRoute()
const id = Number(route.params.id)
const { locale, t } = useI18n()
const dish = ref(null)
const active = ref('overview')

onMounted(async () => {
  const { data } = await axios.get(`/api/dishes/${id}/`)
  dish.value = data
})

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

const nameText = computed(()=> {
  if (!dish.value) return ''
  const dishData = t(`dishes.${dish.value.id}.name`)
  if (dishData && !dishData.includes('dishes')) return dishData
  
  if (locale.value === 'zh-HK') {
    return dish.value.name_zh_hk || dish.value.name_zh || dish.value.name_en
  } else if (locale.value === 'en') {
    return dish.value.name_en || dish.value.name_zh
  } else {
    return dish.value.name_zh || dish.value.name_en
  }
})
const descText = computed(()=> {
  if (!dish.value) return ''
  const dishData = t(`dishes.${dish.value.id}.desc`)
  if (dishData && !dishData.includes('dishes')) return dishData
  
  if (locale.value === 'zh-HK') {
    return dish.value.desc_zh_hk || dish.value.desc_zh || dish.value.desc_en
  } else if (locale.value === 'en') {
    return dish.value.desc_en || dish.value.desc_zh
  } else {
    return dish.value.desc_zh || dish.value.desc_en
  }
})
const emptyTexts = computed(() => ({
  culture: t('dish_detail.empty_culture'),
  nutrition: t('dish_detail.empty_nutrition'),
  ingredients: t('dish_detail.empty_ingredients'),
  steps: t('dish_detail.empty_steps'),
  video: t('dish_detail.empty_video')
}))

// 解析描述文本中的各个部分，支持简体、繁体和英文
const parseDescriptionSection = (text, sectionMarker) => {
  if (!text) return ''
  
  // 定义简体、繁体和英文标记的映射
  const markerMap = {
    '文化故事': { 'zh': '【文化故事】', 'zh-HK': '【文化故事】', 'en': 'Cultural Story' },
    '营养咨询': { 'zh': '【营养咨询】', 'zh-HK': '【營養諮詢】', 'en': 'Nutritional Consultation' },
    '详细配料': { 'zh': '【详细配料】', 'zh-HK': '【詳細配料】', 'en': 'Detailed Ingredients' },
    '具体做法': { 'zh': '【具体做法】', 'zh-HK': '【具體做法】', 'en': 'Cooking Method' },
    '制作工艺': { 'zh': '【制作工艺】', 'zh-HK': '【製作工藝】', 'en': 'Craftsmanship' },
    '冲泡方法': { 'zh': '【冲泡方法】', 'zh-HK': '【沖泡方法】', 'en': 'Brewing Method' },
    '品鉴方法': { 'zh': '【品鉴方法】', 'zh-HK': '【品鑑方法】', 'en': 'Tasting Method' },
    '酿造工艺': { 'zh': '【酿造工艺】', 'zh-HK': '【釀造工藝】', 'en': 'Craftsmanship' }
  }
  
  // 获取当前语言的标记
  const currentLang = locale.value === 'zh-HK' ? 'zh-HK' : (locale.value === 'en' ? 'en' : 'zh')
  const startMarker = markerMap[sectionMarker]?.[currentLang] || `【${sectionMarker}】`
  const allMarkers = locale.value === 'zh-HK'
    ? ['【文化故事】', '【營養諮詢】', '【詳細配料】', '【具體做法】', '【製作工藝】', '【沖泡方法】', '【品鑑方法】', '【釀造工藝】']
    : (locale.value === 'en'
      ? ['Cultural Story', 'Nutritional Consultation', 'Detailed Ingredients', 'Cooking Method', 'Craftsmanship', 'Brewing Method', 'Tasting Method']
      : ['【文化故事】', '【营养咨询】', '【详细配料】', '【具体做法】', '【制作工艺】', '【冲泡方法】', '【品鉴方法】', '【酿造工艺】'])
  
  // 查找标记开始位置
  const startIndex = text.indexOf(startMarker)
  if (startIndex === -1) return ''
  
  // 从标记后开始截取
  const contentStart = startIndex + startMarker.length
  
  // 查找下一个标记的位置
  let nextMarkerIndex = text.length
  for (const marker of allMarkers) {
    // 只查找在当前标记之后的下一个标记
    if (marker !== startMarker) {
      const index = text.indexOf(marker, contentStart)
      if (index !== -1 && index < nextMarkerIndex) {
        nextMarkerIndex = index
      }
    }
  }
  
  // 提取内容并清理
  const content = text.substring(contentStart, nextMarkerIndex).trim()
  return content
}

// 解析新的营养咨询部分（支持加粗标题格式）
const parseNutritionSection = (text) => {
  if (!text) return ''
  
  const nutritionMarker = locale.value === 'zh-HK' ? '【營養諮詢】' : (locale.value === 'en' ? 'Nutritional Consultation' : '【营养咨询】')
  const nutritionStart = text.indexOf(nutritionMarker)
  if (nutritionStart === -1) return ''
  
  // 从营养咨询标记后开始截取
  const contentStart = nutritionStart + nutritionMarker.length
  
  // 查找下一个标记的位置
  const nextMarkers = locale.value === 'zh-HK' 
    ? ['【文化故事】', '【詳細配料】', '【具體做法】', '【製作工藝】', '【沖泡方法】', '【品鑑方法】', '【釀造工藝】']
    : (locale.value === 'en'
      ? ['Cultural Story', 'Detailed Ingredients', 'Cooking Method', 'Craftsmanship', 'Brewing Method', 'Tasting Method']
      : ['【文化故事】', '【详细配料】', '【具体做法】', '【制作工艺】', '【冲泡方法】', '【品鉴方法】', '【酿造工艺】'])
  let nextMarkerIndex = text.length
  for (const marker of nextMarkers) {
    const index = text.indexOf(marker, contentStart)
    if (index !== -1 && index < nextMarkerIndex) {
      nextMarkerIndex = index
    }
  }
  
  // 提取营养咨询内容
  const nutritionContent = text.substring(contentStart, nextMarkerIndex).trim()
  return nutritionContent
}

// 解析新的加粗标题格式部分
const parseBoldTitleSection = (text, title) => {
  if (!text) return ''
  
  // 根据语言适配标题
  const titleMap = {
    '适合人群': { 'zh': '适合人群', 'zh-HK': '適合人群', 'en': 'Suitable for' },
    '搭配食用建议': { 'zh': '搭配食用建议', 'zh-HK': '搭配食用建議', 'en': 'Food Pairing Suggestions' },
    '中药功效': { 'zh': '中药功效', 'zh-HK': '中藥功效', 'en': 'Herbal Benefits' },
    '营养价值分析': { 'zh': '营养价值分析', 'zh-HK': '營養價值分析', 'en': 'Nutritional Value Analysis' },
    '可能的过敏原': { 'zh': '可能的过敏原', 'zh-HK': '可能的過敏原', 'en': 'Potential Allergens' },
    '食用建议': { 'zh': '食用建议', 'zh-HK': '食用建議', 'en': 'Consumption Recommendations' },
    '营养价值': { 'zh': '营养价值', 'zh-HK': '營養價值', 'en': 'Nutritional Value' },
    '制作工艺': { 'zh': '制作工艺', 'zh-HK': '製作工藝', 'en': 'Craftsmanship' },
    '冲泡方法': { 'zh': '冲泡方法', 'zh-HK': '沖泡方法', 'en': 'Brewing Method' },
    '酿造工艺': { 'zh': '酿造工艺', 'zh-HK': '釀造工藝', 'en': 'Craftsmanship' },
    '品鉴方法': { 'zh': '品鉴方法', 'zh-HK': '品鑑方法', 'en': 'Tasting Method' }
  }
  
  // 获取当前语言对应的标题
  const currentLang = locale.value === 'zh-HK' ? 'zh-HK' : (locale.value === 'en' ? 'en' : 'zh')
  const localizedTitle = titleMap[title]?.[currentLang] || title
  
  // 查找加粗标题的位置
  const titleStart = text.indexOf(`**${localizedTitle}**`)
  if (titleStart === -1) return ''
  
  // 从标题后开始截取
  const contentStart = titleStart + `**${localizedTitle}**`.length
  
  // 查找下一个加粗标题或标记的位置，支持简体、繁体和英文
  const nextMarkers = locale.value === 'zh-HK'
    ? ['【文化故事】', '【營養諮詢】', '【詳細配料】', '【具體做法】', '【製作工藝】', '【沖泡方法】', '【品鑑方法】', '【釀造工藝】']
    : (locale.value === 'en' 
      ? ['Cultural Story', 'Nutritional Consultation', 'Detailed Ingredients', 'Cooking Method', 'Craftsmanship', 'Brewing Method', 'Tasting Method']
      : ['【文化故事】', '【营养咨询】', '【详细配料】', '【具体做法】', '【制作工艺】', '【冲泡方法】', '【品鉴方法】', '【酿造工艺】'])
  let nextMarkerIndex = text.length
  
  // 查找下一个加粗标题
  const nextBoldTitle = text.indexOf('**', contentStart)
  if (nextBoldTitle !== -1 && nextBoldTitle < nextMarkerIndex) {
    nextMarkerIndex = nextBoldTitle
  }
  
  // 查找其他标记
  for (const marker of nextMarkers) {
    const index = text.indexOf(marker, contentStart)
    if (index !== -1 && index < nextMarkerIndex) {
      nextMarkerIndex = index
    }
  }
  
  // 提取内容并清理
  const content = text.substring(contentStart, nextMarkerIndex).trim()
  return content
}

// 解析详细配料部分并提取表格数据，支持简体、繁体和英文
const parseIngredientsSection = (text) => {
  if (!text) return ''
  
  const ingredientsMarker = locale.value === 'zh-HK' ? '【詳細配料】' : (locale.value === 'en' ? 'Detailed Ingredients' : '【详细配料】')
  const ingredientsStart = text.indexOf(ingredientsMarker)
  if (ingredientsStart === -1) return ''
  
  // 从详细配料标记后开始截取
  const contentStart = ingredientsStart + ingredientsMarker.length
  
  // 查找下一个标记的位置
  const nextMarkers = locale.value === 'zh-HK'
    ? ['【文化故事】', '【營養諮詢】', '【具體做法】', '【製作工藝】', '【沖泡方法】', '【品鑑方法】', '【釀造工藝】']
    : (locale.value === 'en'
      ? ['Cultural Story', 'Nutritional Consultation', 'Cooking Method', 'Craftsmanship', 'Brewing Method', 'Tasting Method']
      : ['【文化故事】', '【营养咨询】', '【具体做法】', '【制作工艺】', '【冲泡方法】', '【品鉴方法】', '【酿造工艺】'])
  let nextMarkerIndex = text.length
  for (const marker of nextMarkers) {
    const index = text.indexOf(marker, contentStart)
    if (index !== -1 && index < nextMarkerIndex) {
      nextMarkerIndex = index
    }
  }
  
  // 提取详细配料内容
  const ingredientsContent = text.substring(contentStart, nextMarkerIndex).trim()
  return ingredientsContent
}

// 概览内容（基本描述）
const overviewText = computed(() => {
  if (!dish.value) return ''
  const dishData = t(`dishes.${dish.value.id}.desc`)
  const text = dishData && !dishData.includes('dishes') ? dishData : (locale.value==='zh-HK' ? dish.value.desc_zh : dish.value.desc_en)
  if (!text) return ''
  
  // 查找第一个章节标记的位置
  const markers = locale.value === 'zh-HK'
    ? ['【文化故事】', '【營養諮詢】', '【詳細配料】', '【具體做法】', '【製作工藝】', '【沖泡方法】', '【品鑑方法】', '【釀造工藝】', '**適合人群**', '**搭配食用建議**']
    : (locale.value === 'en'
      ? ['Cultural Story', 'Nutritional Consultation', 'Detailed Ingredients', 'Cooking Method', 'Craftsmanship', 'Brewing Method', 'Tasting Method', '**Suitable for**', '**Food Pairing Suggestions**']
      : ['【文化故事】', '【营养咨询】', '【详细配料】', '【具体做法】', '【制作工艺】', '【冲泡方法】', '【品鉴方法】', '【酿造工艺】', '**适合人群**', '**搭配食用建议**'])
  let firstMarkerIndex = text.length
  
  // 找到最近的标记位置
  for (const marker of markers) {
    const index = text.indexOf(marker)
    if (index !== -1 && index < firstMarkerIndex) {
      firstMarkerIndex = index
    }
  }
  
  // 返回第一段作为概览（在第一个标记之前的内容）
  return text.substring(0, firstMarkerIndex).trim()
})

// 适合人群内容
const suitableForText = computed(() => {
  if (!dish.value) return ''
  const dishData = t(`dishes.${dish.value.id}.desc`)
  const text = dishData && !dishData.includes('dishes') ? dishData : (locale.value==='zh-HK' ? dish.value.desc_zh : dish.value.desc_en)
  return parseBoldTitleSection(text, '适合人群') || ''
})

// 搭配食用建议内容
const pairingSuggestionsText = computed(() => {
  if (!dish.value) return ''
  const dishData = t(`dishes.${dish.value.id}.desc`)
  const text = dishData && !dishData.includes('dishes') ? dishData : (locale.value==='zh-HK' ? dish.value.desc_zh : dish.value.desc_en)
  return parseBoldTitleSection(text, '搭配食用建议') || ''
})

// 文化故事内容
const cultureText = computed(() => {
  if (!dish.value) return ''
  const dishData = t(`dishes.${dish.value.id}.desc`)
  const text = dishData && !dishData.includes('dishes') ? dishData : (locale.value==='zh-HK' ? dish.value.desc_zh : dish.value.desc_en)
  return parseDescriptionSection(text, '文化故事') || emptyTexts.value.culture
})

// 营养咨询内容
const nutritionText = computed(() => {
  if (!dish.value) return ''
  const dishData = t(`dishes.${dish.value.id}.desc`)
  const text = dishData && !dishData.includes('dishes') ? dishData : (locale.value==='zh-HK' ? dish.value.desc_zh : dish.value.desc_en)
  // 首先尝试解析新的格式（加粗标题）
  const newFormatContent = parseNutritionSection(text)
  if (newFormatContent) {
    return newFormatContent
  }
  // 如果没有新格式，回退到旧格式
  return parseDescriptionSection(text, '营养咨询') || emptyTexts.value.nutrition
})

// 中药功效内容
const chineseMedicineEffectText = computed(() => {
  if (!dish.value) return ''
  const dishData = t(`dishes.${dish.value.id}.desc`)
  const text = dishData && !dishData.includes('dishes') ? dishData : (locale.value==='zh-HK' ? dish.value.desc_zh : dish.value.desc_en)
  return parseBoldTitleSection(text, '中药功效') || ''
})

// 营养价值分析内容（新格式）
const nutritionalValueText = computed(() => {
  if (!dish.value) return ''
  const dishData = t(`dishes.${dish.value.id}.desc`)
  const text = dishData && !dishData.includes('dishes') ? dishData : (locale.value==='zh-HK' ? dish.value.desc_zh : dish.value.desc_en)
  return parseBoldTitleSection(text, '营养价值分析') || ''
})

// 可能的过敏原内容（新格式）
const allergenText = computed(() => {
  if (!dish.value) return ''
  const dishData = t(`dishes.${dish.value.id}.desc`)
  const text = dishData && !dishData.includes('dishes') 
    ? dishData 
    : (locale.value === 'zh-HK' 
      ? (dish.value.desc_zh_hk || dish.value.desc_zh)
      : (locale.value === 'en' ? dish.value.desc_en : dish.value.desc_zh))
  return parseBoldTitleSection(text, '可能的过敏原') || ''
})

// 食用建议内容（新格式）
const eatingSuggestionText = computed(() => {
  if (!dish.value) return ''
  const dishData = t(`dishes.${dish.value.id}.desc`)
  const text = dishData && !dishData.includes('dishes') 
    ? dishData 
    : (locale.value === 'zh-HK' 
      ? (dish.value.desc_zh_hk || dish.value.desc_zh)
      : (locale.value === 'en' ? dish.value.desc_en : dish.value.desc_zh))
  return parseBoldTitleSection(text, '食用建议') || ''
})

// 配料内容（新格式）
const ingredientsNewText = computed(() => {
  if (!dish.value) return ''
  const dishData = t(`dishes.${dish.value.id}.desc`)
  const text = dishData && !dishData.includes('dishes') ? dishData : (locale.value==='zh-HK' ? dish.value.desc_zh : dish.value.desc_en)
  return parseBoldTitleSection(text, '配料') || ''
})

// 做法内容（新格式）
const productionProcessText = computed(() => {
  if (!dish.value) return ''
  const dishData = t(`dishes.${dish.value.id}.desc`)
  const text = dishData && !dishData.includes('dishes') ? dishData : (locale.value==='zh-HK' ? dish.value.desc_zh : dish.value.desc_en)
  return parseBoldTitleSection(text, '做法') || ''
})

// 详细配料内容（旧格式）
const ingredientsText = computed(() => {
  if (!dish.value) return ''
  const dishData = t(`dishes.${dish.value.id}.desc`)
  const text = dishData && !dishData.includes('dishes') ? dishData : (locale.value==='zh-HK' ? dish.value.desc_zh : dish.value.desc_en)
  return parseDescriptionSection(text, '详细配料') || emptyTexts.value.ingredients
})

// 具体做法内容（旧格式）
const stepsText = computed(() => {
  if (!dish.value) return ''
  const dishData = t(`dishes.${dish.value.id}.desc`)
  const text = dishData && !dishData.includes('dishes') ? dishData : (locale.value==='zh-HK' ? dish.value.desc_zh : dish.value.desc_en)
  return parseDescriptionSection(text, '具体做法') || emptyTexts.value.steps
})

// 解析表格数据
const parseTableData = (text) => {
  if (!text) return null
  
  // 查找表格行
  const lines = text.split('\n')
  const tableLines = lines.filter(line => line.trim().startsWith('|') && line.trim().endsWith('|'))
  
  if (tableLines.length < 2) return null
  
  // 解析表头
  const headers = tableLines[0].split('|').map(cell => cell.trim()).filter(cell => cell !== '')
  
  // 解析数据行
  const rows = []
  for (let i = 2; i < tableLines.length; i++) { // 跳过表头和分隔行
    const cells = tableLines[i].split('|').map(cell => cell.trim()).filter(cell => cell !== '')
    if (cells.length === headers.length) {
      const row = {}
      headers.forEach((header, index) => {
        row[header] = cells[index]
      })
      rows.push(row)
    }
  }
  
  return {
    headers,
    rows
  }
}

// 解析配料信息中的多个表格（主料、辅料、调料）
const parseMultipleIngredientTables = (text) => {
  if (!text) return []
  
  const lines = text.split('\n')
  const tables = [] // 修复：定义tables变量
  
  let currentTitle = ''
  let currentHeaders = []
  let currentRows = []
  let inTable = false
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim()
    
    // 检查是否是加粗标题（主料、辅料、调料）
    if (line.startsWith('**') && line.endsWith('**')) {
      // 如果之前有表格数据，保存它
      if (inTable && currentHeaders.length > 0 && currentRows.length > 0) {
        tables.push({
          title: currentTitle,
          headers: currentHeaders,
          rows: currentRows
        })
      }
      
      // 开始新的表格
      currentTitle = line.replace(/\*\*/g, '')
      currentHeaders = []
      currentRows = []
      inTable = false
      continue
    }
    
    // 检查是否是表格行
    if (line.startsWith('|') && line.endsWith('|')) {
      const cells = line.split('|').map(cell => cell.trim()).filter(cell => cell !== '')
      
      if (cells.length > 0) {
        // 如果是表头
        if (line.includes('---')) {
          inTable = true
          continue
        }
        
        // 如果还没有表头，这是表头
        if (currentHeaders.length === 0) {
          currentHeaders = cells
        } else {
          // 这是数据行
          const row = {}
          currentHeaders.forEach((header, index) => {
            row[header] = cells[index] || ''
          })
          currentRows.push(row)
        }
      }
    } else if (inTable && line === '' && currentHeaders.length > 0 && currentRows.length > 0) {
      // 空行表示表格结束
      tables.push({
        title: currentTitle,
        headers: currentHeaders,
        rows: currentRows
      })
      currentHeaders = []
      currentRows = []
      inTable = false
    }
  }
  
  // 保存最后一个表格
  if (inTable && currentHeaders.length > 0 && currentRows.length > 0) {
    tables.push({
      title: currentTitle,
      headers: currentHeaders,
      rows: currentRows
    })
  }
  
  return tables
}

// 提取营养成分表格数据
const nutritionTableData = computed(() => {
  if (!dish.value) return null
  const dishData = t(`dishes.${dish.value.id}.desc`)
  const text = dishData && !dishData.includes('dishes') ? dishData : (locale.value==='zh-HK' ? dish.value.desc_zh : dish.value.desc_en)
  const nutritionalValue = parseBoldTitleSection(text, '营养价值分析')
  if (!nutritionalValue) return null
  return parseTableData(nutritionalValue)
})

// 提取配料表格数据
const ingredientTablesData = computed(() => {
  if (!dish.value) return []
  const dishData = t(`dishes.${dish.value.id}.desc`)
  const text = dishData && !dishData.includes('dishes') ? dishData : (locale.value==='zh-HK' ? dish.value.desc_zh : dish.value.desc_en)
  const ingredientsSection = parseDescriptionSection(text, '详细配料')
  if (!ingredientsSection) return []
  return parseMultipleIngredientTables(ingredientsSection)
})

// 解析营养咨询中的各个子部分（针对铁观音等饮品格式，支持中英文）
const parseNutritionSubSections = (text) => {
  if (!text) return {}
  
  const result = {}
  const currentLang = locale.value === 'zh-HK' ? 'zh-HK' : (locale.value === 'en' ? 'en' : 'zh')
  
  // 定义多语言标题映射
  const titleVariants = {
    nutritionalValue: {
      'zh': ['**营养价值：**', '**营养价值**'],
      'zh-HK': ['**營養價值：**', '**營養價值**'],
      'en': ['**Nutritional Value:**', '**Nutritional Value**']
    },
    ingredients: {
      'zh': ['**原料：**', '**原料**'],
      'zh-HK': ['**原料：**', '**原料**'],
      'en': ['**Ingredients:**', '**Ingredients**']
    },
    process: {
      'zh': ['**制作工艺：**', '**制作工艺**'],
      'zh-HK': ['**製作工藝：**', '**製作工藝**'],
      'en': ['**Craftsmanship:**', '**Craftsmanship**']
    },
    tasting: {
      'zh': ['**品鉴方法：**', '**品鉴方法**'],
      'zh-HK': ['**品鑑方法：**', '**品鑑方法**'],
      'en': ['**Tasting Method:**', '**Tasting Method**']
    }
  }
  
  // 查找营养价值部分
  const nutritionalValueVariants = titleVariants.nutritionalValue[currentLang]
  let nutritionalValueStart = -1
  let nvMarkerLength = 0
  for (const variant of nutritionalValueVariants) {
    nutritionalValueStart = text.indexOf(variant)
    if (nutritionalValueStart !== -1) {
      nvMarkerLength = variant.length
      break
    }
  }
  if (nutritionalValueStart !== -1) {
    const contentStart = nutritionalValueStart + nvMarkerLength
    let nextSectionStart = text.indexOf('**', contentStart)
    if (nextSectionStart === -1) nextSectionStart = text.length
    result.nutritionalValue = text.substring(contentStart, nextSectionStart).trim()
  }
  
  // 查找原料部分
  const ingredientsVariants = titleVariants.ingredients[currentLang]
  let ingredientsStart = -1
  let ingMarkerLength = 0
  for (const variant of ingredientsVariants) {
    ingredientsStart = text.indexOf(variant)
    if (ingredientsStart !== -1) {
      ingMarkerLength = variant.length
      break
    }
  }
  if (ingredientsStart !== -1) {
    const contentStart = ingredientsStart + ingMarkerLength
    let nextSectionStart = text.indexOf('**', contentStart)
    if (nextSectionStart === -1) nextSectionStart = text.length
    result.ingredients = text.substring(contentStart, nextSectionStart).trim()
  }
  
  // 查找制作工艺部分
  const processVariants = titleVariants.process[currentLang]
  let processStart = -1
  let procMarkerLength = 0
  for (const variant of processVariants) {
    processStart = text.indexOf(variant)
    if (processStart !== -1) {
      procMarkerLength = variant.length
      break
    }
  }
  if (processStart !== -1) {
    const contentStart = processStart + procMarkerLength
    let nextSectionStart = text.indexOf('**', contentStart)
    if (nextSectionStart === -1) nextSectionStart = text.length
    result.process = text.substring(contentStart, nextSectionStart).trim()
  }
  
  // 查找品鉴方法部分
  const tastingVariants = titleVariants.tasting[currentLang]
  let tastingStart = -1
  let tastMarkerLength = 0
  for (const variant of tastingVariants) {
    tastingStart = text.indexOf(variant)
    if (tastingStart !== -1) {
      tastMarkerLength = variant.length
      break
    }
  }
  if (tastingStart !== -1) {
    const contentStart = tastingStart + tastMarkerLength
    result.tasting = text.substring(contentStart).trim()
  }
  
  return result
}

// 提取营养咨询子部分内容
const nutritionSubSections = computed(() => {
  if (!dish.value) return {}
  const dishData = t(`dishes.${dish.value.id}.desc`)
  const text = dishData && !dishData.includes('dishes') ? dishData : (locale.value==='zh-HK' ? dish.value.desc_zh : dish.value.desc_en)
  const nutritionSection = parseDescriptionSection(text, '营养咨询')
  return parseNutritionSubSections(nutritionSection)
})

// 提取制作工艺章节（铁观音等饮品）
const craftingProcessText = computed(() => {
  if (!dish.value) return ''
  const dishData = t(`dishes.${dish.value.id}.desc`)
  const text = dishData && !dishData.includes('dishes') ? dishData : (locale.value==='zh-HK' ? dish.value.desc_zh : dish.value.desc_en)
  const section = parseDescriptionSection(text, '制作工艺')
  return section || ''
})

// 提取冲泡/品鉴方法章节（铁观音等饮品）
const brewingTastingText = computed(() => {
  if (!dish.value) return ''
  const dishData = t(`dishes.${dish.value.id}.desc`)
  const text = dishData && !dishData.includes('dishes') ? dishData : (locale.value==='zh-HK' ? dish.value.desc_zh : dish.value.desc_en)
  // 尝试查找冲泡方法或品鉴方法
  let section = parseDescriptionSection(text, '冲泡方法')
  if (!section) section = parseDescriptionSection(text, '品鉴方法')
  return section || ''
})
</script>

<template>
  <div v-if="dish" class="detail-page">
    <!-- Back Button -->
    <div class="back-btn-container">
      <el-button :icon="ArrowLeft" size="large" @click="$router.back()" class="back-btn">
        {{ t('back') }}
      </el-button>
    </div>

    <div class="detail-grid">
      <div class="main-content">
        <!-- Hero Card -->
        <div class="hero-card">
          <div class="hero-image-wrapper">
            <img :src="getImageForDish(dish.id)" :alt="nameText" class="hero-image" v-if="getImageForDish(dish.id)" />
            <div class="image-badge">
              <Camera class="badge-icon" />
            </div>
          </div>
          <div class="hero-info">
            <h1 class="dish-name">{{ nameText }}</h1>
            <div class="nutrition-badges">
              <span class="nutrition-badge nutrition-badge-calories">
                <span class="badge-label">{{ t('calories') }}</span>
                <span class="badge-value">{{ dish.calories || 0 }}</span>
              </span>
              <span class="nutrition-badge nutrition-badge-protein">
                <span class="badge-label">{{ t('protein') }}</span>
                <span class="badge-value">{{ dish.protein_g || 0 }}g</span>
              </span>
              <span class="nutrition-badge nutrition-badge-fat">
                <span class="badge-label">{{ t('fat') }}</span>
                <span class="badge-value">{{ dish.fat_g || 0 }}g</span>
              </span>
              <span class="nutrition-badge nutrition-badge-carbs">
                <span class="badge-label">{{ t('carbs') }}</span>
                <span class="badge-value">{{ dish.carbs_g || 0 }}g</span>
              </span>
            </div>
          </div>
        </div>

        <!-- Tabs Card -->
        <div class="tabs-card">
          <el-tabs v-model="active" class="detail-tabs">
            <el-tab-pane :label="t('overview')" name="overview">
              <div class="tab-content">
                <p class="overview-desc">{{ overviewText }}</p>
                
                <!-- 适合人群 -->
                <div v-if="suitableForText" class="info-section">
                  <h3 class="section-subtitle">{{ $t('dish_detail.sections.suitable_for') }}</h3>
                  <p class="section-text">{{ suitableForText }}</p>
                </div>
                
                <!-- 搭配食用建议 -->
                <div v-if="pairingSuggestionsText" class="info-section">
                  <h3 class="section-subtitle">{{ $t('dish_detail.sections.pairing_suggestions') }}</h3>
                  <p class="section-text">{{ pairingSuggestionsText }}</p>
                </div>

                <!-- Allergens -->
                <div class="allergen-section">
                  <h3 class="section-subtitle">{{ $t('dish_detail.sections.allergens') || '过敏原' }}</h3>
                  <div class="allergen-tags">
                    <template v-if="dish.allergens?.length">
                      <span v-for="a in dish.allergens" :key="a.id" class="allergen-tag">
                        {{ t(`allergens.${a.id}.name`) || (locale==='zh-HK' ? a.name_zh : (locale==='en' ? a.name_en : a.name_zh)) }}
                      </span>
                    </template>
                    <span v-else class="no-allergen">{{ t('no_allergen_info') }}</span>
                  </div>
                </div>
              </div>
            </el-tab-pane>

            <el-tab-pane :label="t('culture')" name="culture">
              <div class="tab-content">
                <p class="section-text culture-text">{{ cultureText }}</p>
              </div>
            </el-tab-pane>

            <el-tab-pane :label="t('nutrition')" name="nutrition">
              <div class="tab-content">
                <!-- 中药功效 -->
                <div v-if="chineseMedicineEffectText" class="info-section">
                  <h3 class="section-subtitle">{{ $t('dish_detail.sections.herbal_effect') }}</h3>
                  <p class="section-text">{{ chineseMedicineEffectText }}</p>
                </div>
                
                <!-- 营养价值分析 -->
                <div v-if="nutritionalValueText" class="info-section">
                  <h3 class="section-subtitle">{{ $t('dish_detail.sections.nutrition_analysis') }}</h3>
                  <!-- 营养成分表格 -->
                  <div v-if="nutritionTableData" class="nutrition-table-wrapper">
                    <el-table :data="nutritionTableData.rows" style="width: 100%" stripe>
                      <el-table-column
                        v-for="header in nutritionTableData.headers"
                        :key="header"
                        :prop="header"
                        :label="header"
                      />
                    </el-table>
                  </div>
                  <p class="section-text" v-else>{{ nutritionalValueText }}</p>
                </div>
                
                <div v-if="allergenText" class="info-section">
                  <h3 class="section-subtitle">{{ $t('dish_detail.sections.possible_allergens') }}</h3>
                  <p class="section-text">{{ allergenText }}</p>
                </div>
                
                <div v-if="eatingSuggestionText" class="info-section">
                  <h3 class="section-subtitle">{{ $t('dish_detail.sections.eating_suggestion') }}</h3>
                  <p class="section-text">{{ eatingSuggestionText }}</p>
                </div>
                
                <div v-if="ingredientsNewText" class="info-section">
                  <h3 class="section-subtitle">{{ $t('dish_detail.sections.ingredients') }}</h3>
                  <p class="section-text">{{ ingredientsNewText }}</p>
                </div>
                
                <div v-if="productionProcessText" class="info-section">
                  <h3 class="section-subtitle">{{ $t('dish_detail.sections.steps') }}</h3>
                  <p class="section-text">{{ productionProcessText }}</p>
                </div>
                
                <!-- 铁观音等饮品的营养咨询格式 -->
                <div v-if="Object.keys(nutritionSubSections).length > 0">
                  <div v-if="nutritionSubSections.nutritionalValue" class="info-section">
                    <h3 class="section-subtitle">{{ $t('dish_detail.sections.nutritional_value') }}</h3>
                    <p class="section-text">{{ nutritionSubSections.nutritionalValue }}</p>
                  </div>
                  
                  <div v-if="nutritionSubSections.ingredients" class="info-section">
                    <h3 class="section-subtitle">{{ $t('dish_detail.sections.ingredients') }}</h3>
                    <p class="section-text">{{ nutritionSubSections.ingredients }}</p>
                  </div>
                </div>
                
                <!-- 制作工艺章节（铁观音等） -->
                <div v-if="craftingProcessText" class="info-section">
                  <h3 class="section-subtitle">{{ $t('dish_detail.sections.process') }}</h3>
                  <p class="section-text">{{ craftingProcessText }}</p>
                </div>
                
                <!-- 冲泡/品鉴方法章节（铁观音等） -->
                <div v-if="brewingTastingText" class="info-section">
                  <h3 class="section-subtitle">{{ $t('dish_detail.sections.tasting') }}</h3>
                  <p class="section-text">{{ brewingTastingText }}</p>
                </div>
                
                <!-- 配料表格 -->
                <div v-if="ingredientTablesData.length > 0" class="ingredient-tables">
                  <div v-for="(table, index) in ingredientTablesData" :key="index" class="info-section">
                    <h3 class="section-subtitle">{{ table.title }}</h3>
                    <div class="ingredient-table-wrapper">
                      <el-table :data="table.rows" style="width: 100%" stripe>
                        <el-table-column
                          v-for="header in table.headers"
                          :key="header"
                          :prop="header"
                          :label="header"
                        />
                      </el-table>
                    </div>
                  </div>
                </div>
                
                <!-- 旧格式内容（作为备选） -->
                <div v-if="!nutritionalValueText && nutritionText && nutritionText !== emptyTexts.nutrition && Object.keys(nutritionSubSections).length === 0" class="info-section">
                  <p class="section-text">{{ nutritionText }}</p>
                </div>
                <div v-if="!ingredientsNewText && ingredientsText && ingredientsText !== emptyTexts.ingredients && parseMultipleIngredientTables(ingredientsText).length === 0 && !parseTableData(ingredientsText)" class="info-section">
                  <h3 class="section-subtitle">{{ $t('dish_detail.sections.ingredients') }}</h3>
                  <p class="section-text">{{ ingredientsText }}</p>
                </div>
                <div v-if="!productionProcessText && stepsText && stepsText !== emptyTexts.steps" class="info-section">
                  <h3 class="section-subtitle">{{ $t('dish_detail.sections.steps') }}</h3>
                  <p class="section-text">{{ stepsText }}</p>
                </div>
              </div>
            </el-tab-pane>

            <el-tab-pane :label="t('video')" name="video">
              <div class="tab-content">
                <div v-if="dish.video_url" class="video-wrapper">
                  <video :src="dish.video_url" controls class="video-player"/>
                </div>
                <div v-else class="empty-video">
                  <p>{{ $t('dish_detail.empty_video') }}</p>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </div>

      <div class="sidebar">
        <ChefChatPanel :dish-id="id" :lang="locale" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.detail-page {
  min-height: 100vh;
  background: linear-gradient(to bottom, #f8fafc 0%, #ffffff 100%);
  padding: 20px;
}

.back-btn-container {
  max-width: 1400px;
  margin: 0 auto 20px;
}

.back-btn {
  border-radius: 12px;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.detail-grid {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 24px;
}

/* Main Content */
.main-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Hero Card */
.hero-card {
  background: white;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.hero-image-wrapper {
  position: relative;
  width: 100%;
  height: 400px;
  background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #e2e8f0;
}

.hero-image {
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
  object-position: center;
  padding: 20px;
}

.image-badge {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.badge-icon {
  font-size: 24px;
  color: #006564;
}

.hero-info {
  padding: 30px;
}

.dish-name {
  font-size: 32px;
  font-weight: 800;
  color: #1e293b;
  margin: 0 0 24px 0;
  letter-spacing: -0.5px;
}

.nutrition-badges {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 12px;
}

.nutrition-badge {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  transition: all 0.3s ease;
}

/* 热量 - 橙红色 */
.nutrition-badge-calories {
  background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%);
  border-color: #fed7aa;
}

.nutrition-badge-calories:hover {
  border-color: #fb923c;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(251, 146, 60, 0.2);
}

.nutrition-badge-calories .badge-value {
  color: #ea580c;
}

/* 蛋白质 - 蓝色 */
.nutrition-badge-protein {
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border-color: #bfdbfe;
}

.nutrition-badge-protein:hover {
  border-color: #3b82f6;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
}

.nutrition-badge-protein .badge-value {
  color: #2563eb;
}

/* 脂肪 - 紫色 */
.nutrition-badge-fat {
  background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);
  border-color: #e9d5ff;
}

.nutrition-badge-fat:hover {
  border-color: #a855f7;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(168, 85, 247, 0.2);
}

.nutrition-badge-fat .badge-value {
  color: #9333ea;
}

/* 碳水化合物 - 国泰绿色 */
.nutrition-badge-carbs {
  background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
  border-color: #a7f3d0;
}

.nutrition-badge-carbs:hover {
  border-color: #006564;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 101, 100, 0.2);
}

.nutrition-badge-carbs .badge-value {
  color: #006564;
}

.nutrition-badge:hover {
  border-color: #006564;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 101, 100, 0.15);
}

.badge-label {
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-value {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
}

/* Tabs Card */
.tabs-card {
  background: white;
  border-radius: 24px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

:deep(.detail-tabs) {
  --el-tabs-header-height: 50px;
}

:deep(.detail-tabs .el-tabs__nav-wrap::after) {
  display: none;
}

:deep(.detail-tabs .el-tabs__item) {
  font-size: 16px;
  font-weight: 600;
  color: #64748b;
  padding: 0 24px;
  height: 50px;
  line-height: 50px;
}

:deep(.detail-tabs .el-tabs__item.is-active) {
  color: #006564;
}

:deep(.detail-tabs .el-tabs__active-bar) {
  height: 3px;
  background: linear-gradient(90deg, #006564 0%, #00857d 100%);
}

.tab-content {
  padding: 24px 0;
}

.overview-desc {
  font-size: 16px;
  line-height: 1.8;
  color: #475569;
  margin: 0 0 24px 0;
}

.info-section {
  margin-top: 32px;
}

.info-section:first-child {
  margin-top: 0;
}

.section-subtitle {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 12px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-subtitle::before {
  content: '';
  width: 4px;
  height: 20px;
  background: linear-gradient(135deg, #006564 0%, #00857d 100%);
  border-radius: 2px;
}

.section-text {
  font-size: 15px;
  line-height: 1.8;
  color: #475569;
  margin: 0;
  white-space: pre-wrap;
}

.culture-text {
  font-size: 16px;
  line-height: 2;
  color: #334155;
}

/* Allergen Section */
.allergen-section {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 2px dashed #e2e8f0;
}

.allergen-tags {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.allergen-tag {
  padding: 8px 16px;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  border: 2px solid #fbbf24;
}

.no-allergen {
  color: #64748b;
  font-style: italic;
}

/* Table Wrappers */
.nutrition-table-wrapper,
.ingredient-table-wrapper {
  margin: 16px 0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

:deep(.el-table) {
  border-radius: 12px;
}

:deep(.el-table th) {
  background: linear-gradient(135deg, #006564 0%, #00857d 100%);
  color: white;
  font-weight: 600;
}

:deep(.el-table--striped .el-table__body tr.el-table__row--striped td) {
  background: #f8fafc;
}

/* Video */
.video-wrapper {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.video-player {
  width: 100%;
  display: block;
}

.empty-video {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-radius: 16px;
  border: 2px dashed #cbd5e1;
}

.empty-video p {
  color: #64748b;
  font-size: 16px;
  margin: 0;
  font-style: italic;
}

/* Sidebar */
.sidebar {
  position: sticky;
  top: 20px;
  height: fit-content;
}

/* Responsive */
@media (max-width: 1200px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: relative;
    top: 0;
  }
}

@media (max-width: 768px) {
  .detail-page {
    padding: 15px;
  }

  .hero-image-wrapper {
    height: 300px;
  }

  .dish-name {
    font-size: 26px;
  }

  .nutrition-badges {
    grid-template-columns: repeat(2, 1fr);
  }

  .tabs-card {
    padding: 20px;
  }

  :deep(.detail-tabs .el-tabs__item) {
    padding: 0 12px;
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .hero-info {
    padding: 20px;
  }

  .dish-name {
    font-size: 22px;
  }

  .nutrition-badges {
    grid-template-columns: 1fr;
  }

  .back-btn-container {
    margin-bottom: 15px;
  }
}
</style>
