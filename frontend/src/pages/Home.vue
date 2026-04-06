<script setup>
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const { t } = useI18n()
const authStore = useAuthStore()
const { user } = storeToRefs(authStore)

const heroMemberName = computed(() => {
  return (
    user.value?.full_name ||
    user.value?.identifier ||
    t('home_page.member_card.member_fallback')
  )
})

const heroWelcomeText = computed(() =>
  t('home_page.hero_member_welcome', { name: heroMemberName.value })
)

const exploreSection = ref(null)

const scrollToExplore = () => {
  const target = exploreSection.value
  if (target) {
    target.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

// Import images
import chefMenu from '@/assets/chef_menu.jpg'
import chefChat from '@/assets/chef_chat.jpg'
import chefSurvey from '@/assets/chef_survey.jpg'
import chefShopping from '@/assets/chef_shopping.jpg'
import chefAr from '@/assets/chef_ar.jpg'
</script>

<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-background">
        <div class="floating-element element-1"></div>
        <div class="floating-element element-2"></div>
        <div class="floating-element element-3"></div>
      </div>
      
      <div class="hero-content">
        <p class="hero-member-welcome">
          {{ heroWelcomeText }}
        </p>
        <div class="hero-badge">
          <el-icon><i-ep-Trophy /></el-icon>
          <span>{{ $t('home_page.hero_badge') }}</span>
        </div>
        
        <h1 class="hero-title">{{ $t('hero_title') }}</h1>
        <p class="hero-subtitle">{{ $t('hero_sub') }}</p>
        
        <div class="hero-features">
          <div class="hero-feature-item">
            <el-icon size="24"><i-ep-MagicStick /></el-icon>
            <span>{{ $t('home_page.hero_feature_1') }}</span>
          </div>
          <div class="hero-feature-item">
            <el-icon size="24"><i-ep-Star /></el-icon>
            <span>{{ $t('home_page.hero_feature_2') }}</span>
          </div>
          <div class="hero-feature-item">
            <el-icon size="24"><i-ep-Present /></el-icon>
            <span>{{ $t('home_page.hero_feature_3') }}</span>
          </div>
        </div>

        <!-- <div class="hero-actions">
          <el-button type="primary" size="large" round @click="router.push('/auth')">
            <el-icon><i-ep-Right /></el-icon>
            {{ $t('cta_start') }}
          </el-button>
        </div> -->
        
        <div class="hero-footer">
          <el-icon size="18"><i-ep-InfoFilled /></el-icon>
          <span>{{ $t('home_page.hero_info') }}</span>
        </div>

        <div class="hero-arrow-cta" @click="scrollToExplore">
          <div class="arrow-icon">
            <el-icon size="40"><i-ep-ArrowDown /></el-icon>
          </div>
          <p class="arrow-text">{{ $t('home_page.scroll_to_explore') }}</p>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section ref="exploreSection" class="features">
      <h2 class="section-title">{{ $t('home_page.features_title') }}</h2>
      <p class="section-subtitle">{{ $t('home_page.features_subtitle') }}</p>
      
      <div class="features-grid">
        <!-- Feature 1: AR Virtual Dish -->
        <div class="feature-card" @click="router.push('/ar')">
          <div class="feature-image">
            <img :src="chefAr" alt="AR Experience" />
            <div class="feature-overlay">
              <el-icon size="48"><i-ep-View /></el-icon>
            </div>
          </div>
          <div class="feature-content">
            <h3>{{ $t('home_page.feature_ar_title') }}</h3>
            <p>{{ $t('home_page.feature_ar_desc') }}</p>
            <div class="feature-steps">
              <div class="step">
                <span class="step-number">1</span>
                <span>{{ $t('home_page.ar_step1') }}</span>
              </div>
              <div class="step">
                <span class="step-number">2</span>
                <span>{{ $t('home_page.ar_step2') }}</span>
              </div>
              <div class="step">
                <span class="step-number">3</span>
                <span>{{ $t('home_page.ar_step3') }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Feature 2: AI Chef Chat -->
        <div class="feature-card" @click="router.push('/chef')">
          <div class="feature-image">
            <img :src="chefChat" alt="AI Chef Chat" />
            <div class="feature-overlay">
              <el-icon size="48"><i-ep-ChatDotRound /></el-icon>
            </div>
          </div>
          <div class="feature-content">
            <h3>{{ $t('home_page.feature_chat_title') }}</h3>
            <p>{{ $t('home_page.feature_chat_desc') }}</p>
            <div class="feature-steps">
              <div class="step">
                <span class="step-number">1</span>
                <span>{{ $t('home_page.chat_step1') }}</span>
              </div>
              <div class="step">
                <span class="step-number">2</span>
                <span>{{ $t('home_page.chat_step2') }}</span>
              </div>
              <div class="step">
                <span class="step-number">3</span>
                <span>{{ $t('home_page.chat_step3') }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Feature 3: Menu & Dish Details -->
        <div class="feature-card" @click="router.push('/menu')">
          <div class="feature-image">
            <img :src="chefMenu" alt="Menu" />
            <div class="feature-overlay">
              <el-icon size="48"><i-ep-Food /></el-icon>
            </div>
          </div>
          <div class="feature-content">
            <h3>{{ $t('home_page.feature_menu_title') }}</h3>
            <p>{{ $t('home_page.feature_menu_desc') }}</p>
            <div class="feature-steps">
              <div class="step">
                <span class="step-number">1</span>
                <span>{{ $t('home_page.menu_step1') }}</span>
              </div>
              <div class="step">
                <span class="step-number">2</span>
                <span>{{ $t('home_page.menu_step2') }}</span>
              </div>
              <div class="step">
                <span class="step-number">3</span>
                <span>{{ $t('home_page.menu_step3') }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Feature 4: Survey & Feedback -->
        <div class="feature-card" @click="router.push('/survey')">
          <div class="feature-image">
            <img :src="chefSurvey" alt="Survey" />
            <div class="feature-overlay">
              <el-icon size="48"><i-ep-EditPen /></el-icon>
            </div>
          </div>
          <div class="feature-content">
            <h3>{{ $t('home_page.feature_survey_title') }}</h3>
            <p>{{ $t('home_page.feature_survey_desc') }}</p>
            <div class="feature-steps">
              <div class="step">
                <span class="step-number">1</span>
                <span>{{ $t('home_page.survey_step1') }}</span>
              </div>
              <div class="step">
                <span class="step-number">2</span>
                <span>{{ $t('home_page.survey_step2') }}</span>
              </div>
              <div class="step">
                <span class="step-number">3</span>
                <span>{{ $t('home_page.survey_step3') }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Feature 5: Shopping -->
        <div class="feature-card" @click="router.push('/preselect')">
          <div class="feature-image">
            <img :src="chefShopping" alt="Shopping" />
            <div class="feature-overlay">
              <el-icon size="48"><i-ep-ShoppingCart /></el-icon>
            </div>
          </div>
          <div class="feature-content">
            <h3>{{ $t('home_page.feature_shopping_title') }}</h3>
            <p>{{ $t('home_page.feature_shopping_desc') }}</p>
            <div class="feature-steps">
              <div class="step">
                <span class="step-number">1</span>
                <span>{{ $t('home_page.shopping_step1') }}</span>
              </div>
              <div class="step">
                <span class="step-number">2</span>
                <span>{{ $t('home_page.shopping_step2') }}</span>
              </div>
              <div class="step">
                <span class="step-number">3</span>
                <span>{{ $t('home_page.shopping_step3') }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
}

/* Hero Section */
.hero {
  background: linear-gradient(135deg, #0c423e 0%, #1a6d70 100%);
  color: white;
  padding: 40px 20px;
  position: relative;
  overflow: hidden;
  min-height: 320px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0;
  width: min(1400px, calc(100% - 60px));
  margin: 18px auto 50px;
  box-shadow: 0 32px 90px rgba(4, 25, 24, 0.4);
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><rect width="100" height="100" fill="none"/><circle cx="50" cy="50" r="1" fill="rgba(255,255,255,0.1)"/></svg>');
  opacity: 0.3;
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  z-index: 0;
}

.floating-element {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  animation: float 20s infinite ease-in-out;
}

.element-1 {
  width: 300px;
  height: 300px;
  top: -100px;
  left: -50px;
  animation-delay: 0s;
}

.element-2 {
  width: 200px;
  height: 200px;
  top: 50%;
  right: -80px;
  animation-delay: 5s;
}

.element-3 {
  width: 150px;
  height: 150px;
  bottom: -50px;
  left: 40%;
  animation-delay: 10s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
    opacity: 0.3;
  }
  50% {
    transform: translateY(-30px) rotate(180deg);
    opacity: 0.6;
  }
}

.hero-content {
  max-width: 900px;
  margin: 0 auto;
  text-align: center;
  position: relative;
  z-index: 1;
  animation: fadeInUp 0.8s ease;
}

.hero-member-welcome {
  font-size: 2rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: #ffeaa7;
  font-weight: 800;
  margin-bottom: 18px;
  line-height: 1.3;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  padding: 10px 24px;
  border-radius: 0;
  margin-bottom: 24px;
  font-size: 0.95rem;
  font-weight: 500;
  border: 1px solid rgba(255, 255, 255, 0.2);
  animation: slideDown 0.6s ease 0.2s both;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 20px;
  line-height: 1.3;
  background: linear-gradient(135deg, #ffffff 0%, #ffd89b 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 2px;
  animation: fadeInUp 0.8s ease 0.3s both;
}

.hero-subtitle {
  font-size: 1.25rem;
  line-height: 1.8;
  margin-bottom: 32px;
  color: rgba(255, 255, 255, 0.95);
  font-weight: 300;
  letter-spacing: 1px;
  animation: fadeInUp 0.8s ease 0.4s both;
}

.hero-features {
  display: flex;
  justify-content: center;
  gap: 32px;
  margin-bottom: 36px;
  flex-wrap: wrap;
  animation: fadeInUp 0.8s ease 0.5s both;
}

.hero-feature-item {
  display: flex;
  align-items: center;
  gap: 10px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.95rem;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0;
  transition: all 0.3s ease;
}

.hero-feature-item:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 48px;
  animation: fadeInUp 0.8s ease 0.6s both;
}

.hero-actions .el-button {
  padding: 16px 48px;
  font-size: 1.1rem;
  font-weight: 500;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.hero-actions .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
}

.hero-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-top: 32px;
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.95rem;
  animation: fadeInUp 0.8s ease 0.7s both;
}

.hero-footer .el-icon {
  font-size: 1.2rem;
}

.hero-arrow-cta {
  margin-top: 36px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.hero-arrow-cta:hover {
  transform: translateY(6px);
}

.arrow-icon {
  color: #ffeaa7;
  animation: bounce 2s infinite;
}

.arrow-text {
  font-size: 1.05rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.95);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(10px);
  }
}

/* Features Section */
.features {
  max-width: 1400px;
  margin: 0 auto;
  padding: 80px 20px;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  color: #0c3342;
  margin-bottom: 16px;
}

.section-subtitle {
  font-size: 1.1rem;
  text-align: center;
  color: #64748b;
  margin-bottom: 60px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  margin-bottom: 60px;
}

/* 让第二行的两个卡片居中 */
.features-grid .feature-card:nth-child(4) {
  grid-column: 1 / 2;
}

.features-grid .feature-card:nth-child(5) {
  grid-column: 2 / 3;
}

.feature-card {
  background: white;
  border-radius: 0;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  cursor: pointer;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.feature-image {
  position: relative;
  width: 100%;
  padding-bottom: 100%; /* 1:1 aspect ratio */
  overflow: hidden;
  background: #f5f5f5;
}

.feature-image img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.feature-card:hover .feature-image img {
  transform: scale(1.1);
}

.feature-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(12, 51, 66, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.feature-card:hover .feature-overlay {
  opacity: 1;
}

.feature-content {
  padding: 24px;
}

.feature-content h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #0c3342;
  margin-bottom: 12px;
}

.feature-content p {
  font-size: 1rem;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 20px;
}

.feature-steps {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.step {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 0.95rem;
  color: #475569;
}

.step-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: linear-gradient(135deg, #1890ff 0%, #0c3342 100%);
  color: white;
  border-radius: 50%;
  font-weight: 600;
  font-size: 0.85rem;
  flex-shrink: 0;
}

/* Animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Responsive */
@media (max-width: 1200px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .features-grid .feature-card:nth-child(4),
  .features-grid .feature-card:nth-child(5) {
    grid-column: auto;
  }
}

@media (max-width: 968px) {
  .hero {
    min-height: 280px;
    padding: 32px 16px;
    width: calc(100% - 40px);
    margin: 30px auto 40px;
    border-radius: 0;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .hero-features {
    gap: 16px;
  }
  
  .hero-stats {
    gap: 24px;
  }
  
  .stat-number {
    font-size: 1.6rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .features-grid .feature-card:nth-child(4),
  .features-grid .feature-card:nth-child(5) {
    grid-column: auto;
  }
  
  .section-title {
    font-size: 2rem;
  }
}

@media (max-width: 640px) {
  .hero {
    min-height: 240px;
    padding: 28px 16px;
    width: calc(100% - 20px);
    margin: 24px auto 32px;
    border-radius: 0;
  }
  
  .hero-badge {
    font-size: 0.85rem;
    padding: 8px 18px;
  }

  .hero-member-welcome {
    font-size: 1rem;
    letter-spacing: 0.12em;
  }
  
  .hero-title {
    font-size: 2rem;
    letter-spacing: 1px;
  }
  
  .hero-subtitle {
    font-size: 1rem;
    margin-bottom: 24px;
  }
  
  .hero-features {
    flex-direction: column;
    gap: 12px;
    align-items: center;
  }
  
  .hero-feature-item {
    font-size: 0.9rem;
  }
  
  .hero-actions .el-button {
    width: 100%;
    padding: 14px 32px;
  }
  
  .hero-stats {
    flex-wrap: wrap;
    gap: 20px;
  }
  
  .stat-divider {
    display: none;
  }
  
  .stat-number {
    font-size: 1.4rem;
  }
  
  .stat-label {
    font-size: 0.85rem;
  }
  
  .floating-element {
    opacity: 0.3;
  }
  
  .element-1 {
    width: 200px;
    height: 200px;
  }
  
  .element-2 {
    width: 150px;
    height: 150px;
  }
  
  .element-3 {
    width: 100px;
    height: 100px;
  }
}
</style>
