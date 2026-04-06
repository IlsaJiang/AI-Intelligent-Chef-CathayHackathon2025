<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { InfoFilled, ArrowRight } from '@element-plus/icons-vue'

const { t } = useI18n()

const shoppingUrl = 'https://lifestyle.asiamiles.com/sc/CN?cxsource=TOP-NAV_SHOPPING_1_1'

const categories = computed(() => [
  {
    title: t('preselectPage.categories.travel.title'),
    desc: t('preselectPage.categories.travel.desc'),
    tag: t('preselectPage.categories.travel.tag')
  },
  {
    title: t('preselectPage.categories.dining.title'),
    desc: t('preselectPage.categories.dining.desc'),
    tag: t('preselectPage.categories.dining.tag')
  },
  {
    title: t('preselectPage.categories.member.title'),
    desc: t('preselectPage.categories.member.desc'),
    tag: t('preselectPage.categories.member.tag')
  }
])

const steps = computed(() => [
  {
    title: t('preselectPage.steps.login.title'),
    desc: t('preselectPage.steps.login.desc')
  },
  {
    title: t('preselectPage.steps.pick.title'),
    desc: t('preselectPage.steps.pick.desc')
  },
  {
    title: t('preselectPage.steps.delivery.title'),
    desc: t('preselectPage.steps.delivery.desc')
  }
])

const openShop = () => {
  if (typeof window !== 'undefined') {
    window.open(shoppingUrl, '_blank', 'noopener')
  }
}
</script>

<template>
  <div class="shop-page">
    <section class="hero">
      <div class="hero-copy">
        <div class="hero-header">
          <span class="eyebrow">{{ $t('preselectPage.hero.eyebrow') }}</span>
          <h1>{{ $t('preselectPage.hero.title') }}</h1>
          <p class="hero-desc">{{ $t('preselectPage.hero.desc') }}</p>
        </div>
        
        <div class="product-highlights">
          <div class="highlight-item new-product">
            <div class="highlight-icon">🆕</div>
            <div class="highlight-content">
              <span class="highlight-label">{{ $t('preselectPage.hero.new_label') }}</span>
              <span class="highlight-text">{{ $t('preselectPage.hero.new_product') }}</span>
            </div>
          </div>
          <div class="highlight-item exclusive">
            <div class="highlight-icon">⭐</div>
            <div class="highlight-content">
              <span class="highlight-label">{{ $t('preselectPage.hero.exclusive_label') }}</span>
              <span class="highlight-text">{{ $t('preselectPage.hero.exclusive_product') }}</span>
            </div>
          </div>
        </div>

        <div class="hero-actions">
          <el-button type="primary" size="large" round @click="openShop">
            {{ $t('preselectPage.hero.primary_cta') }}
          </el-button>
          <el-button round plain size="large" @click="openShop">
            {{ $t('preselectPage.hero.secondary_cta') }}
          </el-button>
        </div>
      </div>
      <div class="hero-card coupon-card">
        <div class="card-head">
          <span class="badge">{{ $t('preselectPage.hero.card.badge') }}</span>
          <h3>{{ $t('preselectPage.hero.card.title') }}</h3>
          <p class="card-subtitle">{{ $t('preselectPage.hero.card.subtitle') }}</p>
        </div>
        <div class="coupon-list">
          <div class="coupon-item">
            <div class="coupon-amount">
              <span class="currency">¥</span>
              <span class="number">10</span>
            </div>
            <div class="coupon-info">
              <div class="coupon-condition">{{ $t('preselectPage.hero.card.coupon_1_condition') }}</div>
              <div class="coupon-validity">{{ $t('preselectPage.hero.card.validity') }}</div>
            </div>
            <el-button class="claim-btn" size="small" round @click="openShop">{{ $t('preselectPage.hero.card.claim_btn') }}</el-button>
          </div>
          <div class="coupon-item">
            <div class="coupon-amount">
              <span class="currency">¥</span>
              <span class="number">20</span>
            </div>
            <div class="coupon-info">
              <div class="coupon-condition">{{ $t('preselectPage.hero.card.coupon_2_condition') }}</div>
              <div class="coupon-validity">{{ $t('preselectPage.hero.card.validity') }}</div>
            </div>
            <el-button class="claim-btn" size="small" round @click="openShop">{{ $t('preselectPage.hero.card.claim_btn') }}</el-button>
          </div>
        </div>
        <div class="coupon-note">
          <el-icon><InfoFilled /></el-icon>
          <span>{{ $t('preselectPage.hero.card.note') }}</span>
        </div>
      </div>
    </section>

    <section class="tiles">
      <div class="section-header">
        <h2>{{ $t('preselectPage.categories.section_title') }}</h2>
        <p class="section-desc">{{ $t('preselectPage.categories.section_desc') }}</p>
      </div>
      <el-row :gutter="20">
        <el-col v-for="item in categories" :key="item.title" :md="8" :sm="24">
          <div class="tile" @click="openShop">
            <div class="tile-header">
              <span class="tile-tag">{{ item.tag }}</span>
              <div class="tile-icon">→</div>
            </div>
            <h4>{{ item.title }}</h4>
            <p>{{ item.desc }}</p>
            <div class="tile-footer">
              <span class="tile-cta">{{ $t('preselectPage.categories.cta') }}</span>
            </div>
          </div>
        </el-col>
      </el-row>
    </section>

    <section class="steps">
      <div class="section-header centered">
        <h2>{{ $t('preselectPage.steps.title') }}</h2>
        <p class="section-desc">{{ $t('preselectPage.steps.subtitle') }}</p>
      </div>
      <el-row :gutter="20">
        <el-col v-for="(step, index) in steps" :key="step.title" :md="8" :sm="24">
          <div class="step-card">
            <div class="step-number">
              <span>{{ index + 1 }}</span>
            </div>
            <h5>{{ step.title }}</h5>
            <p>{{ step.desc }}</p>
          </div>
        </el-col>
      </el-row>
    </section>

    <section class="cta">
      <div class="cta-content">
        <span class="cta-badge">{{ $t('preselectPage.cta.eyebrow') }}</span>
        <h3>{{ $t('preselectPage.cta.title') }}</h3>
        <p>{{ $t('preselectPage.cta.copy') }}</p>
      </div>
      <el-button type="primary" round size="large" @click="openShop">
        {{ $t('preselectPage.cta.button') }}
        <el-icon class="ml-2"><ArrowRight /></el-icon>
      </el-button>
    </section>
  </div>
</template>

<style scoped>
.shop-page {
  max-width: 1080px;
  margin: 0 auto;
  padding: 20px 0 48px;
  display: flex;
  flex-direction: column;
  gap: 28px;
  background: radial-gradient(circle at 20% 20%, rgba(15, 118, 110, 0.08), transparent 45%);
}

.hero {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1.3fr) minmax(0, 0.7fr);
  gap: 24px;
  background: linear-gradient(135deg, #f6fffd, #eef5ff);
  border-radius: 26px;
  padding: 40px;
  border: 1px solid rgba(15, 118, 110, 0.1);
  overflow: hidden;
}

.hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 80% 0, rgba(47, 140, 123, 0.25), transparent 55%);
  pointer-events: none;
}

.hero-copy,
.hero-card {
  position: relative;
  z-index: 1;
}

.hero-copy {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.hero-header h1 {
  font-size: 28px;
  margin: 12px 0 8px;
  color: #0b3f3f;
  line-height: 1.3;
}

.hero-desc {
  color: #4c5f60;
  line-height: 1.7;
  font-size: 15px;
  margin: 0;
}

/* Product Highlights */
.product-highlights {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 8px 0;
}

.highlight-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 14px;
  transition: all 0.3s ease;
  border: 1.5px solid transparent;
}

.highlight-item.new-product {
  background: linear-gradient(135deg, rgba(255, 107, 107, 0.1), rgba(255, 168, 0, 0.08));
  border-color: rgba(255, 107, 107, 0.2);
}

.highlight-item.exclusive {
  background: linear-gradient(135deg, rgba(255, 193, 7, 0.12), rgba(255, 152, 0, 0.08));
  border-color: rgba(255, 193, 7, 0.25);
}

.highlight-item:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(15, 118, 110, 0.1);
}

.highlight-icon {
  font-size: 24px;
  line-height: 1;
  flex-shrink: 0;
}

.highlight-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.highlight-label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  opacity: 0.7;
}

.highlight-item.new-product .highlight-label {
  color: #d32f2f;
}

.highlight-item.exclusive .highlight-label {
  color: #f57c00;
}

.highlight-text {
  font-size: 14px;
  font-weight: 600;
  color: #0b3f3f;
  line-height: 1.4;
}

.hero-actions {
  display: flex;
  gap: 12px;
  margin-top: 18px;
  flex-wrap: wrap;
}

.eyebrow {
  letter-spacing: 0.15em;
  font-size: 12px;
  text-transform: uppercase;
  color: #1f6c6c;
}

.hero-card {
  background: #0f766e;
  color: #f6fffd;
  border-radius: 22px;
  padding: 24px;
  box-shadow: 0 25px 45px rgba(15, 118, 110, 0.15);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}

.hero-card::after {
  content: '';
  position: absolute;
  inset: 12px;
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  pointer-events: none;
}

.card-head h3 {
  margin: 10px 0 4px;
  font-size: 18px;
}

.card-subtitle {
  font-size: 13px;
  opacity: 0.85;
  margin: 0;
  line-height: 1.5;
}

/* Coupon Card Styles */
.coupon-card .card-head {
  margin-bottom: 16px;
}

.coupon-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 16px 0;
}

.coupon-item {
  background: rgba(255, 255, 255, 0.15);
  border: 1px dashed rgba(255, 255, 255, 0.4);
  border-radius: 12px;
  padding: 14px;
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 12px;
  align-items: center;
  transition: all 0.3s ease;
}

.coupon-item:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateX(3px);
}

.coupon-amount {
  display: flex;
  align-items: baseline;
  gap: 2px;
}

.coupon-amount .currency {
  font-size: 16px;
  font-weight: 600;
}

.coupon-amount .number {
  font-size: 28px;
  font-weight: 800;
  line-height: 1;
}

.coupon-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.coupon-condition {
  font-size: 14px;
  font-weight: 600;
}

.coupon-validity {
  font-size: 12px;
  opacity: 0.75;
}

.claim-btn {
  background: rgba(255, 255, 255, 0.95);
  color: #0f766e;
  border: none;
  font-weight: 600;
  padding: 8px 20px;
  transition: all 0.3s ease;
}

.claim-btn:hover {
  background: #ffffff;
  transform: scale(1.05);
}

.coupon-note {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  opacity: 0.8;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.hero-card ul {
  list-style: none;
  padding: 0;
  margin: 18px 0;
  display: grid;
  gap: 12px;
}

.hero-card li {
  display: flex;
  justify-content: space-between;
  border-bottom: 1px dashed rgba(255, 255, 255, 0.35);
  padding-bottom: 6px;
}

.label {
  opacity: 0.8;
}

.value {
  font-weight: 700;
}

.badge {
  display: inline-flex;
  padding: 4px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  font-size: 12px;
  letter-spacing: 0.08em;
}

/* Section Headers */
.section-header {
  margin-bottom: 32px;
}

.section-header.centered {
  text-align: center;
}

.section-header h2 {
  font-size: 28px;
  font-weight: 700;
  color: #0b3f3f;
  margin-bottom: 8px;
}

.section-desc {
  color: #64748b;
  font-size: 15px;
  line-height: 1.6;
  margin: 0;
}

/* Tiles Section */
.tiles {
  position: relative;
  padding: 20px 0;
}

.tiles .tile {
  position: relative;
  border: 2px solid #e1ecec;
  border-radius: 20px;
  padding: 24px;
  background: #fff;
  display: flex;
  flex-direction: column;
  gap: 12px;
  height: 100%;
  box-shadow: 0 4px 12px rgba(9, 54, 54, 0.05);
  z-index: 1;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.tiles .tile::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #0f766e, #14b8a6);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s ease;
}

.tiles .tile:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 32px rgba(15, 118, 110, 0.15);
  border-color: #0f766e;
}

.tiles .tile:hover::before {
  transform: scaleX(1);
}

.tile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.tile-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0f766e, #14b8a6);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
  opacity: 0.8;
  transition: all 0.3s ease;
}

.tiles .tile:hover .tile-icon {
  opacity: 1;
  transform: rotate(-45deg);
}

.tile h4 {
  font-size: 20px;
  font-weight: 700;
  color: #0b3f3f;
  margin: 8px 0;
}

.tile p {
  color: #64748b;
  line-height: 1.6;
  font-size: 14px;
  flex: 1;
  margin: 0;
}

.tile-footer {
  margin-top: 8px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

.tile-cta {
  color: #0f766e;
  font-weight: 600;
  font-size: 15px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: gap 0.3s ease;
}

.tiles .tile:hover .tile-cta {
  gap: 10px;
}

.tile-cta::after {
  content: '→';
  transition: transform 0.3s ease;
}

.tiles .tile:hover .tile-cta::after {
  transform: translateX(4px);
}

.tile-tag {
  font-size: 11px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #0f766e;
  font-weight: 700;
  background: rgba(15, 118, 110, 0.1);
  padding: 4px 12px;
  border-radius: 20px;
}

/* Steps Section */
.steps {
  padding: 40px 0;
}

.step-card {
  border-radius: 20px;
  background: linear-gradient(135deg, #ffffff, #f8fffe);
  padding: 28px 24px;
  height: 100%;
  border: 2px solid #e1ecec;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.step-card:hover {
  border-color: #0f766e;
  box-shadow: 0 8px 24px rgba(15, 118, 110, 0.1);
  transform: translateY(-4px);
}

.step-number {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0f766e, #14b8a6);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(15, 118, 110, 0.3);
}

.step-number span {
  font-size: 24px;
  font-weight: 800;
  color: #ffffff;
}

.step-card h5 {
  font-size: 18px;
  font-weight: 700;
  color: #0b3f3f;
  margin-bottom: 12px;
}

.step-card p {
  color: #64748b;
  line-height: 1.7;
  font-size: 14px;
  margin: 0;
}

.step-card::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #0f766e, #14b8a6);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s ease;
}

.step-card:hover::after {
  transform: scaleX(1);
}

/* CTA Section */
.cta {
  border-radius: 24px;
  background: linear-gradient(135deg, #0b3f3f 0%, #0f766e 50%, #14b8a6 100%);
  color: #f6fffd;
  padding: 48px 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 24px;
  box-shadow: 0 20px 60px rgba(7, 56, 60, 0.25);
  position: relative;
  overflow: hidden;
}

.cta::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.cta-content {
  position: relative;
  z-index: 1;
  flex: 1;
  min-width: 300px;
}

.cta-badge {
  display: inline-block;
  padding: 6px 16px;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: 12px;
}

.cta h3 {
  margin: 12px 0 8px;
  font-size: 26px;
  font-weight: 700;
  line-height: 1.3;
}

.cta p {
  margin: 0;
  opacity: 0.9;
  line-height: 1.6;
  font-size: 15px;
}

.cta .el-button {
  position: relative;
  z-index: 1;
  padding: 16px 32px;
  font-size: 16px;
  font-weight: 600;
  background: white;
  color: #0f766e;
  border: none;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}

.cta .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.ml-2 {
  margin-left: 8px;
}

@media (max-width: 960px) {
  .hero {
    grid-template-columns: 1fr;
  }
  
  .product-highlights {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }
  
  .section-header h2 {
    font-size: 24px;
  }
  
  .cta {
    padding: 36px 28px;
  }
  
  .cta h3 {
    font-size: 22px;
  }
}

@media (max-width: 640px) {
  .hero {
    padding: 24px;
  }
  
  .hero-header h1 {
    font-size: 24px;
  }
  
  .hero-desc {
    font-size: 14px;
  }
  
  .product-highlights {
    grid-template-columns: 1fr;
  }
  
  .highlight-item {
    padding: 12px;
  }
  
  .highlight-icon {
    font-size: 20px;
  }
  
  .section-header h2 {
    font-size: 22px;
  }
  
  .section-desc {
    font-size: 14px;
  }
  
  .tiles .tile {
    margin-bottom: 16px;
  }
  
  .tile h4 {
    font-size: 18px;
  }
  
  .step-number {
    width: 48px;
    height: 48px;
  }
  
  .step-number span {
    font-size: 20px;
  }
  
  .step-card h5 {
    font-size: 16px;
  }
  
  .cta {
    flex-direction: column;
    align-items: flex-start;
    padding: 32px 24px;
  }
  
  .cta h3 {
    font-size: 20px;
  }
  
  .cta .el-button {
    width: 100%;
  }
  
  .hero-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .hero-actions .el-button {
    width: 100%;
  }
  
  .hero-card {
    padding: 20px;
  }
  
  .coupon-item {
    grid-template-columns: auto 1fr;
    gap: 10px;
  }
  
  .claim-btn {
    grid-column: 1 / -1;
    width: 100%;
  }
  
  .coupon-amount .number {
    font-size: 24px;
  }
}
</style>
