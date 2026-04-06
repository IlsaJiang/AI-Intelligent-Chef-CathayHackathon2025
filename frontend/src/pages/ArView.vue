<template>
  <div class="ar-container">
    <div class="header">
      <h1>{{ $t('ar_view_title') }}</h1>
      <p>{{ $t('ar_view_description') }}</p>
    </div>
    
    <!-- AR Viewer with Kivicube integration -->
    <div class="ar-viewer">
      <div v-if="arSupported && !arLoadError" class="ar-content" ref="arContentRef">
        <!-- 悬浮工具栏：重新加载 / 全屏 / 新窗口打开 -->
        <div class="ar-toolbar">
          <el-button size="small" circle @click="reloadAr" :title="$t('ar_toolbar_reload')" :aria-label="$t('ar_toolbar_reload')">⟳</el-button>
          <el-button size="small" circle @click="enterFullscreen" :title="$t('ar_toolbar_fullscreen')" :aria-label="$t('ar_toolbar_fullscreen')">⤢</el-button>
          <el-button size="small" circle @click="openInNewTab" :title="$t('ar_toolbar_open')" :aria-label="$t('ar_toolbar_open')">⇱</el-button>
        </div>
        <iframe 
          id="kivicubeScene"
          :src="kivicubeUrl"
          frameborder="0"
          allowfullscreen
          allow="camera *; microphone *; fullscreen; autoplay"
          title="Kivicube AR Scene"
          class="ar-iframe">
        </iframe>
        <div v-if="loading" class="loading-overlay">
          <div class="spinner"></div>
          <p>{{ $t('ar_loading') }}</p>
          <p class="debug-info" v-if="debugInfo">{{ debugInfo }}</p>
        </div>
      </div>
      
      <div v-else class="ar-unavailable">
        <div class="warning-icon">⚠️</div>
        <h2>{{ $t('ar_unavailable_title') }}</h2>
        <p>{{ arLoadError || $t('ar_unavailable_desc') }}</p>
        
        <div class="debug-section" v-if="debugInfo">
          <h3>{{ $t('ar_debug_info_title') }}</h3>
          <p>{{ debugInfo }}</p>
        </div>
        
        <div class="troubleshooting">
          <h3>{{ $t('ar_troubleshooting_title') }}</h3>
          <ul>
            <li>{{ $t('ar_tip_1') }}</li>
            <li>{{ $t('ar_tip_2') }}</li>
            <li>{{ $t('ar_tip_3') }}</li>
            <li>{{ $t('ar_tip_4') }}</li>
          </ul>
        </div>
        
        <div class="demo-placeholder">
          <div class="placeholder-graphic">
            <div class="cube"></div>
            <div class="plane"></div>
          </div>
          <p>{{ $t('ar_demo_explanation') }}</p>
        </div>
      </div>
      
      <div class="instructions">
        <h2>{{ $t('ar_instructions_title') }}</h2>
        <ul>
          <li>{{ $t('ar_instruction_step_1') }}</li>
          <li>{{ $t('ar_instruction_step_2') }}</li>
          <li>{{ $t('ar_instruction_step_3') }}</li>
        </ul>
      </div>
    </div>
    
    <div class="back-button">
      <el-button type="primary" @click="goBack">{{ $t('back_button') }}</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const arSupported = ref(true)
const loading = ref(true)
const arLoadError = ref('')
const debugInfo = ref('')
const sceneId = ref('l6t3CrZ06gUHXF5hqGa9FT7Fz4hbgP96') // 替换为您的实际场景ID

// 使用直接的Kivicube URL而不是加载JS库
const kivicubeUrl = ref(`https://www.kivicube.com/scenes/${sceneId.value}`)

// 容器引用（用于全屏）
const arContentRef = ref(null)

// 检查环境支持
const checkEnvironment = () => {
  const info = []
  info.push(`协议: ${window.location.protocol}`)
  info.push(`主机名: ${window.location.hostname}`)
  info.push(`端口: ${window.location.port}`)
  
  // 检查是否为安全上下文
  if (window.isSecureContext) {
    info.push('安全上下文: 是')
  } else {
    info.push('安全上下文: 否')
  }
  
  debugInfo.value = info.join(', ')
  return window.isSecureContext
}

// 检查iframe是否正确加载
const checkIframeLoad = () => {
  const iframe = document.getElementById('kivicubeScene')
  if (!iframe) {
    arLoadError.value = '无法找到AR iframe元素'
    loading.value = false
    return
  }
  
  // 监听iframe加载事件
  iframe.onload = () => {
    debugInfo.value += ', iframe加载完成'
    setTimeout(() => {
      loading.value = false
    }, 3000)
  }
  
  iframe.onerror = () => {
    arLoadError.value = 'AR内容加载失败，请检查网络连接和场景ID'
    loading.value = false
    debugInfo.value += ', iframe加载错误'
  }
}

// 初始化AR场景
const initArScene = async () => {
  try {
    // 检查环境
    if (!checkEnvironment()) {
      arLoadError.value = '当前环境不支持AR功能，请确保在HTTPS或localhost环境下运行'
      loading.value = false
      return
    }
    
    // 检查iframe加载
    checkIframeLoad()
    
    // 设置超时
    setTimeout(() => {
      if (loading.value) {
        loading.value = false
        debugInfo.value += ', 加载超时'
      }
    }, 15000)
  } catch (error) {
    console.error('AR初始化失败:', error)
    arLoadError.value = `AR初始化失败: ${error.message}`
    loading.value = false
  }
}

// 工具栏动作：重新加载
const reloadAr = () => {
  const iframe = document.getElementById('kivicubeScene')
  if (iframe) {
    loading.value = true
    arLoadError.value = ''
    try {
      const url = new URL(kivicubeUrl.value)
      url.searchParams.set('_ts', Date.now().toString())
      iframe.src = url.toString()
      debugInfo.value += ', 触发手动重新加载'
    } catch (e) {
      // 兜底：直接赋回原地址
      iframe.src = kivicubeUrl.value
    }
  }
}

// 工具栏动作：全屏/退出全屏
const enterFullscreen = async () => {
  const el = arContentRef.value
  if (!el) return
  try {
    if (document.fullscreenElement) {
      await document.exitFullscreen()
    } else if (el.requestFullscreen) {
      await el.requestFullscreen()
    }
  } catch (error) {
    console.error('全屏切换失败:', error)
  }
}

// 工具栏动作：新窗口打开
const openInNewTab = () => {
  try {
    window.open(kivicubeUrl.value, '_blank', 'noopener,noreferrer')
  } catch (error) {
    console.error('新窗口打开失败:', error)
  }
}

const goBack = () => {
  // 关闭AR场景
  const iframe = document.getElementById('kivicubeScene')
  if (iframe) {
    try {
      // 直接设置为空页面
      iframe.src = 'about:blank'
    } catch (error) {
      console.error('关闭AR场景时出错:', error)
    }
  }
  
  // 返回上一页
  window.history.go(-1)
}

onMounted(() => {
  initArScene()
})

onBeforeUnmount(() => {
  // 组件卸载前关闭AR场景
  const iframe = document.getElementById('kivicubeScene')
  if (iframe) {
    try {
      iframe.src = 'about:blank'
    } catch (error) {
      console.error('关闭AR场景时出错:', error)
    }
  }
})
</script>

<style scoped>
.ar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 2rem;
  color: #0c3342;
  margin-bottom: 15px;
}

.header p {
  font-size: 1.1rem;
  color: #64748b;
  max-width: 800px;
  margin: 0 auto;
}

.ar-viewer {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.ar-content {
  position: relative;
}

.ar-toolbar {
  position: absolute;
  top: 12px;
  right: 12px;
  display: flex;
  gap: 8px;
  z-index: 2;
}

.ar-iframe {
  width: 100%;
  height: clamp(360px, 65vh, 720px);
  border: none;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  display: block;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 12px;
  z-index: 1;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #006564;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.ar-unavailable {
  text-align: center;
  padding: 40px 20px;
  background: #f8f9fa;
  border-radius: 12px;
  border: 2px dashed #dee2e6;
}

.warning-icon {
  font-size: 3rem;
  margin-bottom: 20px;
}

.ar-unavailable h2 {
  color: #0c3342;
  margin-bottom: 15px;
}

.ar-unavailable p {
  color: #495057;
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto 20px;
}

.demo-placeholder {
  margin-top: 30px;
}

.placeholder-graphic {
  position: relative;
  width: 200px;
  height: 200px;
  margin: 0 auto 20px;
}

.cube {
  width: 100px;
  height: 100px;
  background: linear-gradient(45deg, #006564, #00857d);
  position: absolute;
  top: 50px;
  left: 50px;
  transform: rotate(45deg);
  animation: float 3s ease-in-out infinite;
}

.plane {
  width: 150px;
  height: 150px;
  border: 2px solid #64748b;
  position: absolute;
  top: 25px;
  left: 25px;
}

@keyframes float {
  0% { transform: rotate(45deg) translateY(0); }
  50% { transform: rotate(45deg) translateY(-20px); }
  100% { transform: rotate(45deg) translateY(0); }
}

.instructions {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 25px;
}

.instructions h2 {
  color: #0c3342;
  margin-bottom: 15px;
}

.instructions ul {
  padding-left: 20px;
}

.instructions li {
  margin-bottom: 10px;
  line-height: 1.6;
  color: #495057;
}

.back-button {
  margin-top: 30px;
  text-align: center;
}

.debug-section {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 8px;
  padding: 15px;
  margin: 20px 0;
  text-align: left;
}

.debug-section h3 {
  margin-top: 0;
  color: #856404;
}

.troubleshooting {
  background: #d1ecf1;
  border: 1px solid #bee5eb;
  border-radius: 8px;
  padding: 15px;
  margin: 20px 0;
  text-align: left;
}

.troubleshooting h3 {
  margin-top: 0;
  color: #0c5460;
}

.troubleshooting ul {
  padding-left: 20px;
}

.troubleshooting li {
  margin-bottom: 8px;
}

.debug-info {
  font-size: 0.9rem;
  color: #6c757d;
  margin-top: 10px;
}

/* 移动端优化 */
@media (max-width: 768px) {
  .header h1 {
    font-size: 1.6rem;
  }
  .ar-viewer {
    gap: 20px;
  }
  .ar-iframe {
    height: clamp(280px, 55vh, 560px);
  }
}
</style>