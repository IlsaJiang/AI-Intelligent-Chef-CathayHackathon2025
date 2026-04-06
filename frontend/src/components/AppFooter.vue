<template>
  <footer class="cx-footer">
    <div class="cx-container f-row">
      <div class="left">
        <div class="brand">{{ $t('footer.brand') }}</div>
        <div class="muted">{{ $t('footer.disclaimer') }}</div>
      </div>
      <div class="right">
        <router-link to="/preselect" class="link">{{ $t('preselect') }}</router-link>
        <router-link to="/menu" class="link">{{ $t('menu') }}</router-link>
        <router-link to="/survey" class="link">{{ $t('survey_nav') }}</router-link>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.cx-footer {
  margin-top: 40px; background: var(--bg);
  border-top: 1px solid rgba(0,0,0,.06);
}
.cx-container { max-width: 1280px; margin: 0 auto; padding: 18px 16px; }
.f-row { display: flex; justify-content: space-between; gap: 16px; align-items: center; }
.brand { font-weight: 700; color: #0d2f2d; }
.muted { color: #6b7280; font-size: 12px; margin-top: 4px; }
.right { display: flex; gap: 12px; }
.link { color: #0b3f3f; text-decoration: none; }
@media (max-width: 720px){
  .f-row { flex-direction: column; align-items: flex-start; }
}
</style>
