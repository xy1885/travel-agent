<template>
    <div class="plan-page" v-if="store.travelPlan">
        <!-- Header -->
        <div class="plan-header">
            <div class="header-inner">
                <button class="back-btn" @click="handleBack">← 重新规划</button>
                <div class="destination-title">
                    <span class="dest-label">目的地</span>
                    <h1>{{ store.travelPlan.destination }}</h1>
                </div>
                <div class="plan-meta">
                    <span class="meta-item">{{ store.travelPlan.duration_days }} 天</span>
                    <span class="meta-dot">·</span>
                    <span class="meta-item">{{ store.userInfo?.person_composition }}</span>
                    <span class="meta-dot">·</span>
                    <span class="meta-item">¥{{ store.travelPlan.practical_info.budget_estimate?.toLocaleString()
                        }}</span>
                </div>
                <p class="plan-summary">{{ store.travelPlan.summary }}</p>
            </div>
        </div>

        <div class="plan-body">
            <!-- Timeline -->
            <section class="section">
                <h2 class="section-title">行程安排</h2>
                <div class="timeline">
                    <div v-for="day in store.travelPlan.days" :key="day.day" class="timeline-item">
                        <div class="timeline-marker">
                            <div class="day-badge">DAY {{ day.day }}</div>
                            <div class="timeline-line"></div>
                        </div>
                        <div class="timeline-content">
                            <div class="day-theme">{{ day.theme }}</div>
                            <div class="attractions">
                                <div v-for="(att, i) in day.attractions" :key="i" class="attraction-card">
                                    <div class="att-header">
                                        <h4>{{ att.name }}</h4>
                                        <span class="att-duration">{{ att.duration_hours }}h</span>
                                    </div>
                                    <p class="att-desc">{{ att.description }}</p>
                                    <div class="att-tips" v-if="att.tips">
                                        <span class="tips-icon">💡</span>{{ att.tips }}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Restaurants -->
            <section class="section">
                <h2 class="section-title">美食推荐</h2>
                <div class="restaurants-grid">
                    <div v-for="(r, i) in store.travelPlan.restaurants" :key="i" class="restaurant-card">
                        <div class="rest-top">
                            <h4>{{ r.name }}</h4>
                            <span class="price-tag">{{ r.price_range }}</span>
                        </div>
                        <span class="cuisine-tag" v-if="r.cuisine">{{ r.cuisine }}</span>
                        <p class="rest-rec">{{ r.recommendation }}</p>
                    </div>
                </div>
            </section>

            <!-- Practical Info -->
            <section class="section">
                <h2 class="section-title">实用信息</h2>
                <div class="practical-grid">
                    <div class="practical-card">
                        <div class="prac-icon">🌸</div>
                        <div class="prac-label">最佳季节</div>
                        <div class="prac-value">
                            {{ Array.isArray(store.travelPlan.practical_info.best_season)
                                ? store.travelPlan.practical_info.best_season.join('、')
                                : store.travelPlan.practical_info.best_season }}
                        </div>
                    </div>
                    <div class="practical-card">
                        <div class="prac-icon">🚄</div>
                        <div class="prac-label">交通建议</div>
                        <div class="prac-value">{{ store.travelPlan.practical_info.transportation }}</div>
                    </div>
                    <div class="practical-card">
                        <div class="prac-icon">💰</div>
                        <div class="prac-label">预算估算</div>
                        <div class="prac-value">¥{{ store.travelPlan.practical_info.budget_estimate?.toLocaleString() }}
                        </div>
                    </div>
                </div>

                <div class="tips-list" v-if="store.travelPlan.practical_info.tips?.length">
                    <h3>出行小贴士</h3>
                    <ul>
                        <li v-for="(tip, i) in store.travelPlan.practical_info.tips" :key="i">
                            <span class="tip-num">{{ String(i + 1).padStart(2, '0') }}</span>
                            {{ tip }}
                        </li>
                    </ul>
                </div>
            </section>
        </div>
    </div>

    <!-- 未找到规划时跳回首页 -->
    <div v-else class="no-plan">
        <p>还没有规划，请先填写表单</p>
        <button class="btn-primary" @click="$router.push('/')">去填写 →</button>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useTravelStore } from '../stores/travelStore'
import { onMounted } from 'vue'

const store = useTravelStore()
const router = useRouter()

onMounted(() => {
    console.log('travelPlan:', store.travelPlan)
    console.log('step:', store.step)
})

function handleBack() {
    store.reset()
    router.push('/')
}
</script>

<style scoped>
.plan-page {
    min-height: 100vh;
    background: var(--paper);
}

.plan-header {
    background: var(--ink);
    color: var(--paper);
    padding: 48px 20px;
}

.header-inner {
    max-width: 800px;
    margin: 0 auto;
}

.back-btn {
    background: transparent;
    color: var(--paper);
    opacity: 0.5;
    font-size: 0.85rem;
    margin-bottom: 24px;
    display: block;
    transition: opacity 0.2s;
}

.back-btn:hover {
    opacity: 1;
}

.dest-label {
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    opacity: 0.5;
    display: block;
    margin-bottom: 6px;
}

.plan-header h1 {
    font-size: 3rem;
    margin-bottom: 12px;
}

.plan-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 16px;
    opacity: 0.7;
    font-size: 0.9rem;
}

.meta-dot {
    opacity: 0.4;
}

.plan-summary {
    opacity: 0.65;
    font-size: 0.95rem;
    max-width: 560px;
    line-height: 1.7;
}

.plan-body {
    max-width: 800px;
    margin: 0 auto;
    padding: 48px 20px;
}

.section {
    margin-bottom: 56px;
}

.section-title {
    font-size: 1.3rem;
    margin-bottom: 28px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--sand);
    color: var(--ink);
}

/* Timeline */
.timeline {
    display: flex;
    flex-direction: column;
    gap: 0;
}

.timeline-item {
    display: flex;
    gap: 24px;
}

.timeline-marker {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-shrink: 0;
}

.day-badge {
    background: var(--terracotta);
    color: white;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    padding: 4px 10px;
    border-radius: 2px;
    white-space: nowrap;
}

.timeline-line {
    width: 1px;
    background: var(--sand);
    flex: 1;
    margin-top: 8px;
    min-height: 20px;
}

.timeline-content {
    padding-bottom: 36px;
    flex: 1;
}

.day-theme {
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--terracotta);
    margin-bottom: 16px;
    margin-top: 4px;
}

.attractions {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.attraction-card {
    background: white;
    border: 1px solid var(--sand);
    border-radius: var(--radius-lg);
    padding: 16px 20px;
    transition: box-shadow 0.2s;
}

.attraction-card:hover {
    box-shadow: 0 4px 16px var(--shadow);
}

.att-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
}

.att-header h4 {
    font-size: 1rem;
}

.att-duration {
    font-size: 0.78rem;
    color: var(--terracotta);
    background: #fef3e2;
    padding: 2px 8px;
    border-radius: 10px;
}

.att-desc {
    font-size: 0.875rem;
    opacity: 0.7;
    line-height: 1.6;
    margin-bottom: 10px;
}

.att-tips {
    font-size: 0.8rem;
    opacity: 0.6;
    display: flex;
    gap: 6px;
    align-items: flex-start;
}

.tips-icon {
    flex-shrink: 0;
}

/* Restaurants */
.restaurants-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 16px;
}

.restaurant-card {
    background: white;
    border: 1px solid var(--sand);
    border-radius: var(--radius-lg);
    padding: 18px;
    transition: box-shadow 0.2s;
}

.restaurant-card:hover {
    box-shadow: 0 4px 16px var(--shadow);
}

.rest-top {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 8px;
}

.rest-top h4 {
    font-size: 0.95rem;
}

.price-tag {
    font-size: 0.8rem;
    color: var(--sage);
    font-weight: 500;
    white-space: nowrap;
}

.cuisine-tag {
    display: inline-block;
    font-size: 0.75rem;
    background: var(--mist);
    border-radius: 10px;
    padding: 2px 10px;
    margin-bottom: 10px;
    opacity: 0.7;
}

.rest-rec {
    font-size: 0.8rem;
    opacity: 0.65;
    line-height: 1.5;
}

/* Practical */
.practical-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 28px;
}

.practical-card {
    background: white;
    border: 1px solid var(--sand);
    border-radius: var(--radius-lg);
    padding: 20px;
    text-align: center;
}

.prac-icon {
    font-size: 1.5rem;
    margin-bottom: 8px;
}

.prac-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    opacity: 0.5;
    margin-bottom: 6px;
}

.prac-value {
    font-size: 0.875rem;
    font-weight: 500;
}

.tips-list h3 {
    font-size: 1rem;
    margin-bottom: 16px;
}

.tips-list ul {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.tips-list li {
    display: flex;
    gap: 14px;
    align-items: flex-start;
    font-size: 0.875rem;
    line-height: 1.6;
}

.tip-num {
    font-family: 'Playfair Display', serif;
    color: var(--terracotta);
    opacity: 0.6;
    flex-shrink: 0;
    font-size: 0.8rem;
    padding-top: 2px;
}

/* No plan */
.no-plan {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    gap: 16px;
}

.btn-primary {
    padding: 12px 32px;
    background: var(--terracotta);
    color: white;
    border-radius: var(--radius);
    font-size: 0.95rem;
    transition: all 0.2s;
}

.btn-primary:hover {
    background: var(--terracotta-light);
}

@media (max-width: 600px) {
    .plan-header h1 {
        font-size: 2rem;
    }

    .practical-grid {
        grid-template-columns: 1fr;
    }

    .restaurants-grid {
        grid-template-columns: 1fr;
    }
}
</style>