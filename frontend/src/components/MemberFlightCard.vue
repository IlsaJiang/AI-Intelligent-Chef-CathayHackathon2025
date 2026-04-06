<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'

const STORAGE_PREFIX = 'cx_member_flight_session'
const NOV_START = new Date('2025-11-15T06:00:00')
const NOV_END_SINGLE = new Date('2025-11-16T18:00:00')
const NOV_END_ROUND = new Date('2025-11-16T22:00:00')
const NOV_LAST = new Date('2025-11-16T23:59:00')

const authStore = useAuthStore()
const { user, isAuthenticated } = storeToRefs(authStore)
const { t, locale } = useI18n()

const now = ref(Date.now())
let timerId = null
const arrowAnimated = ref(false)

const memberName = computed(() => {
  return (
    user.value?.full_name ||
    user.value?.identifier ||
    t('home_page.member_card.member_fallback')
  )
})

const cityCatalog = [
  { key: 'beijing', names: { en: 'Beijing', zh: '北京', 'zh-HK': '北京' } },
  { key: 'shanghai', names: { en: 'Shanghai', zh: '上海', 'zh-HK': '上海' } },
  { key: 'guangzhou', names: { en: 'Guangzhou', zh: '广州', 'zh-HK': '廣州' } },
  { key: 'chengdu', names: { en: 'Chengdu', zh: '成都', 'zh-HK': '成都' } },
  { key: 'hangzhou', names: { en: 'Hangzhou', zh: '杭州', 'zh-HK': '杭州' } },
  { key: 'nanjing', names: { en: 'Nanjing', zh: '南京', 'zh-HK': '南京' } },
  { key: 'xian', names: { en: 'Xi’an', zh: '西安', 'zh-HK': '西安' } },
  { key: 'chongqing', names: { en: 'Chongqing', zh: '重庆', 'zh-HK': '重慶' } },
  { key: 'xiamen', names: { en: 'Xiamen', zh: '厦门', 'zh-HK': '廈門' } },
  { key: 'wuhan', names: { en: 'Wuhan', zh: '武汉', 'zh-HK': '武漢' } },
  { key: 'qingdao', names: { en: 'Qingdao', zh: '青岛', 'zh-HK': '青島' } },
  { key: 'changsha', names: { en: 'Changsha', zh: '长沙', 'zh-HK': '長沙' } },
  { key: 'tianjin', names: { en: 'Tianjin', zh: '天津', 'zh-HK': '天津' } }
]

const flightDurationMinutes = {
  beijing: { min: 195, max: 225 },
  shanghai: { min: 155, max: 175 },
  guangzhou: { min: 70, max: 95 },
  chengdu: { min: 165, max: 190 },
  hangzhou: { min: 150, max: 170 },
  nanjing: { min: 165, max: 185 },
  xian: { min: 180, max: 205 },
  chongqing: { min: 145, max: 170 },
  xiamen: { min: 75, max: 95 },
  wuhan: { min: 105, max: 130 },
  qingdao: { min: 180, max: 210 },
  changsha: { min: 110, max: 135 },
  tianjin: { min: 200, max: 230 }
}

const randomItem = (list) => list[Math.floor(Math.random() * list.length)]
const randomInt = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min
const addHours = (date, hours) => new Date(date.getTime() + hours * 60 * 60 * 1000)
const addMinutes = (date, minutes) => new Date(date.getTime() + minutes * 60 * 1000)

const randomDurationForDestination = (key) => {
  const duration = flightDurationMinutes[key]
  const fallback = { min: 150, max: 210 }
  const range = duration ?? fallback
  return randomInt(range.min, range.max)
}

const intlLocale = computed(() => {
  const map = { en: 'en-US', zh: 'zh-CN', 'zh-HK': 'zh-TW' }
  return map[locale.value] ?? 'zh-TW'
})

const formatDate = (date) => {
  const formatter = new Intl.DateTimeFormat(intlLocale.value, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
  return formatter.format(date)
}

const randomDateBetween = (start, end) => {
  const startTime = start.getTime()
  const endTime = end.getTime()
  const randomTime = startTime + Math.random() * (endTime - startTime)
  return new Date(randomTime)
}

const flightRecord = ref(null)
const lastUserKey = ref(null)

const getUserKey = () => {
  if (!user.value) return null
  return (
    user.value.id?.toString?.() ||
    user.value.identifier ||
    user.value.email ||
    user.value.phone ||
    null
  )
}

const storageKeyForUser = (userKey) => `${STORAGE_PREFIX}:${userKey}`

const loadStoredRecord = (userKey) => {
  if (typeof window === 'undefined' || !userKey) return null
  const raw = window.sessionStorage.getItem(storageKeyForUser(userKey))
  if (!raw) return null
  try {
    return JSON.parse(raw)
  } catch (error) {
    return null
  }
}

const persistRecord = (userKey, record) => {
  if (typeof window === 'undefined' || !userKey) return
  window.sessionStorage.setItem(storageKeyForUser(userKey), JSON.stringify(record))
}

const clearRecord = (userKey) => {
  if (typeof window === 'undefined' || !userKey) return
  window.sessionStorage.removeItem(storageKeyForUser(userKey))
}

const createFlightRecord = () => {
  const destinationKey = randomItem(cityCatalog).key
  const tripType = randomItem(['round', 'one_way'])
  const departure = randomDateBetween(
    NOV_START,
    tripType === 'one_way' ? NOV_END_SINGLE : NOV_END_ROUND
  )

  const travelMinutes = randomDurationForDestination(destinationKey)
  const arrivalCandidate = addMinutes(departure, travelMinutes)
  const arrival = tripType === 'one_way' && arrivalCandidate > NOV_LAST ? NOV_LAST : arrivalCandidate
  const returnTime = tripType === 'round'
    ? addHours(departure, 24 * 7 + randomInt(2, 6))
    : null

  return {
    destinationKey,
    tripType,
    departure: departure.toISOString(),
    arrival: arrival.toISOString(),
    returnTime: returnTime ? returnTime.toISOString() : null
  }
}

const triggerArrowAnimation = () => {
  arrowAnimated.value = false
  if (typeof window === 'undefined') {
    arrowAnimated.value = true
    return
  }
  window.requestAnimationFrame(() => {
    window.requestAnimationFrame(() => {
      arrowAnimated.value = true
    })
  })
}

const applyFlightRecord = (record) => {
  flightRecord.value = record
  triggerArrowAnimation()
}

const bootstrapFlightInfo = () => {
  if (!isAuthenticated.value) {
    flightRecord.value = null
    return
  }
  const userKey = getUserKey()
  if (!userKey) return

  let record = loadStoredRecord(userKey)
  if (!record) {
    record = createFlightRecord()
    persistRecord(userKey, record)
  }
  lastUserKey.value = userKey
  applyFlightRecord(record)
}

onMounted(() => {
  bootstrapFlightInfo()
  if (typeof window !== 'undefined') {
    timerId = window.setInterval(() => {
      now.value = Date.now()
    }, 60000)
  }
})

onUnmounted(() => {
  if (timerId) {
    window.clearInterval(timerId)
    timerId = null
  }
})

watch(isAuthenticated, (authed, previous) => {
  if (!authed) {
    if (lastUserKey.value) {
      clearRecord(lastUserKey.value)
      lastUserKey.value = null
    }
    flightRecord.value = null
    return
  }

  if (!previous && authed) {
    bootstrapFlightInfo()
  }
})

watch(
  () => getUserKey(),
  (newKey, oldKey) => {
    if (!isAuthenticated.value) return
    if (newKey && newKey !== oldKey) {
      clearRecord(oldKey)
      lastUserKey.value = newKey
      const record = createFlightRecord()
      persistRecord(newKey, record)
      applyFlightRecord(record)
    }
  }
)

const cityName = (key) => {
  const entry = cityCatalog.find((item) => item.key === key)
  return entry?.names?.[locale.value] || entry?.names?.['zh-HK'] || key
}

const displayFlight = computed(() => {
  if (!flightRecord.value) return null
  const departureDate = new Date(flightRecord.value.departure)
  const arrivalDate = new Date(flightRecord.value.arrival)

  return {
    destination: cityName(flightRecord.value.destinationKey),
    tripTypeLabel: t(`home_page.member_card.trip_types.${flightRecord.value.tripType}`),
    cabinInfo: t('home_page.member_card.cabin_value'),
    departureValue: formatDate(departureDate),
    arrivalValue: formatDate(arrivalDate),
    departureDate,
    arrivalDate
  }
})

const progressPercent = computed(() => {
  if (!flightRecord.value) return 0
  const depart = new Date(flightRecord.value.departure).getTime()
  const arrive = new Date(flightRecord.value.arrival).getTime()
  const duration = arrive - depart
  if (duration <= 0) return 0
  const current = now.value
  if (current <= depart) return 0
  if (current >= arrive) return 1
  return (current - depart) / duration
})

const progressPercentDisplay = computed(() => Math.round(progressPercent.value * 100))

const progressColor = computed(() => {
  const remaining = Math.max(0, 1 - progressPercent.value)
  if (remaining > 0.66) return '#22d3ee'
  if (remaining > 0.33) return '#f59e0b'
  return '#f97316'
})

const progressWidthValue = computed(() => {
  const percent = progressPercentDisplay.value
  const clamped = Math.min(96, Math.max(6, percent))
  return `${clamped}%`
})

const progressFillStyle = computed(() => ({
  width: arrowAnimated.value ? progressWidthValue.value : '0%',
  '--arrow-color': progressColor.value
}))

const planeStyle = computed(() => ({
  left: arrowAnimated.value ? progressWidthValue.value : '0%',
  color: progressColor.value
}))

const timelineAria = computed(() => {
  if (!displayFlight.value) return ''
  return t('home_page.member_card.timeline_aria', {
    from: t('home_page.member_card.from_value'),
    to: displayFlight.value.destination,
    progress: progressPercentDisplay.value
  })
})
</script>
<template>
  <Transition name="banner-fade">
    <section
      v-if="isAuthenticated && displayFlight"
      class="member-flight-banner"
      role="region"
      :aria-label="t('home_page.member_card.greeting', { name: memberName })"
    >
      <div class="member-meta">
        <span class="meta-label">{{ t('home_page.member_card.member_label') }}</span>
        <div class="meta-highlight">
          <span class="meta-name">{{ memberName }}</span>
          <span class="meta-dot" aria-hidden="true">·</span>
          <span class="meta-cabin">{{ displayFlight.cabinInfo }}</span>
        </div>
      </div>

      <div class="member-path">
        <div class="location-block">
          <span class="location-city">{{ t('home_page.member_card.from_value') }}</span>
          <span class="location-time">{{ displayFlight.departureValue }}</span>
        </div>
        <div class="path-visual" :aria-label="timelineAria">
          <div class="progress-track">
            <div class="progress-fill" :style="progressFillStyle"></div>
            <div class="progress-plane" :style="planeStyle">
              <svg viewBox="0 0 32 32" aria-hidden="true" focusable="false">
                <path
                  d="M4 17.5l8.2-1.2-2.3-9.4 3.1-0.9 6.7 8.4 8.3-1.2 0.7 2.7-8 2 2.5 6.6-2.6 0.7-5.8-5.3-5.6 1.4z"
                  fill="currentColor"
                />
              </svg>
            </div>
          </div>
          <div class="progress-labels">
            <span>{{ t('home_page.member_card.departure_time') }}</span>
            <span>{{ t('home_page.member_card.arrival_time') }}</span>
          </div>
        </div>
        <div class="location-block align-right">
          <span class="location-city">{{ displayFlight.destination }}</span>
          <span class="location-time">{{ displayFlight.arrivalValue }}</span>
        </div>
      </div>
    </section>
  </Transition>
</template>

<style scoped>

.member-flight-banner {
  width: min(1200px, 96vw);
  margin: 8px auto 24px;
  padding: 22px 36px;
  border-radius: 0;
  background: linear-gradient(120deg, rgba(255, 255, 255, 0.98), rgba(210, 246, 238, 0.95));
  border: 1px solid rgba(14, 165, 233, 0.2);
  box-shadow: 0 28px 70px rgba(12, 58, 55, 0.22);
  backdrop-filter: blur(18px);
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.member-meta {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  color: #022c22;
  text-align: center;
}

.meta-label {
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.28em;
  color: rgba(4, 120, 87, 0.8);
}

.meta-highlight {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-size: 1.1rem;
  font-weight: 600;
  color: #022c22;
}

.meta-name {
  font-size: 1.2rem;
  font-weight: 700;
}

.meta-dot {
  opacity: 0.4;
}

.meta-cabin {
  color: #0f766e;
  font-weight: 600;
}

.member-path {
  display: flex;
  align-items: center;
  gap: 32px;
}

.location-block {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 160px;
  text-align: center;
}

.location-city {
  font-weight: 700;
  color: #022c22;
  font-size: 1rem;
}

.location-time {
  font-size: 0.9rem;
  color: #475569;
}

.align-right {
  text-align: center;
}

.path-visual {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}


.progress-track {
  position: relative;
  width: 100%;
  height: 12px;
  border-radius: 999px;
  background: rgba(15, 118, 110, 0.12);
  overflow: visible;
}

.progress-fill {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  background: linear-gradient(90deg, var(--arrow-color, #0ea5e9), #14b8a6);
  border-radius: 999px;
  transition: width 0.9s ease, background 0.4s ease;
}

.progress-fill::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(120deg, rgba(255, 255, 255, 0.4), transparent 70%);
  opacity: 0.5;
  animation: sheen 2.8s linear infinite;
}

.progress-plane {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  transition: left 0.9s ease, color 0.4s ease;
  filter: drop-shadow(0 4px 10px rgba(2, 44, 34, 0.3));
}

.progress-plane svg {
  width: 28px;
  height: 28px;
}

.progress-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #64748b;
  letter-spacing: 0.04em;
}

@keyframes sheen {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.banner-fade-enter-active,
.banner-fade-leave-active {
  transition: opacity 0.4s ease, transform 0.4s ease;
}

.banner-fade-enter-from,
.banner-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

@media (max-width: 1024px) {
  .member-flight-banner {
    width: min(1100px, 95vw);
    padding: 18px 26px;
    border-radius: 0;
    gap: 14px;
  }

  .member-path {
    gap: 18px;
  }
}

@media (max-width: 768px) {
  .member-flight-banner {
    border-radius: 0;
    padding: 18px;
  }

  .member-meta {
    flex-direction: column;
    gap: 4px;
  }

  .member-path {
    flex-direction: column;
    align-items: stretch;
  }

  .location-block,
  .align-right {
    text-align: left;
  }
}

@media (max-width: 480px) {
  .member-flight-banner {
    gap: 8px;
  }

  .location-block {
    min-width: auto;
  }
}
</style>
