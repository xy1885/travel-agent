<template>
    <div class="home">
        <!-- 背景装饰 -->
        <div class="bg-deco">
            <div class="deco-circle deco-1"></div>
            <div class="deco-circle deco-2"></div>
        </div>

        <div class="container">
            <!-- Header -->
            <header class="header">
                <div class="logo">✦ TravelAgent</div>
                <p class="tagline">由 AI 为你量身定制的旅行攻略</p>
            </header>

            <!-- Step: Form -->
            <transition name="fade" mode="out-in">
                <div v-if="store.step === 'form'" key="form" class="card form-card">
                    <div class="card-title">
                        <span class="step-num">01</span>
                        <h2>告诉我你的旅行计划</h2>
                    </div>

                    <div class="form-grid">
                        <div class="field">
                            <label>出发城市</label>
                            <input v-model="form.location" type="text" placeholder="如：上海" />
                        </div>
                        <div class="field">
                            <label>目的地</label>
                            <input v-model="form.target" type="text" placeholder="如：东京" />
                        </div>
                        <div class="field">
                            <label>旅行天数</label>
                            <input v-model.number="form.day_num" type="number" min="1" placeholder="5" />
                        </div>
                        <div class="field">
                            <label>旅游人数</label>
                            <input v-model.number="form.person_num" type="number" min="1" placeholder="2" />
                        </div>
                        <div class="field">
                            <label>人员构成</label>
                            <select v-model="form.person_composition">
                                <option value="情侣">情侣</option>
                                <option value="家人">家人</option>
                                <option value="朋友">朋友</option>
                                <option value="公司">公司</option>
                            </select>
                        </div>
                        <div class="field">
                            <label>住宿偏好</label>
                            <select v-model="form.accommodation_preference">
                                <option value="繁华市区">繁华市区</option>
                                <option value="景点旁">景点旁</option>
                                <option value="经济型">经济型</option>
                            </select>
                        </div>
                        <div class="field">
                            <label>总预算（人民币）</label>
                            <input v-model.number="form.budget" type="number" min="1" placeholder="20000" />
                        </div>
                        <div class="field field-checks">
                            <label>同行人员</label>
                            <div class="checks">
                                <label class="check-item">
                                    <input type="checkbox" v-model="form.has_old" />
                                    <span>有老人</span>
                                </label>
                                <label class="check-item">
                                    <input type="checkbox" v-model="form.has_child" />
                                    <span>有小孩</span>
                                </label>
                            </div>
                        </div>
                        <div class="field field-full">
                            <label>旅行偏好（可多选）</label>
                            <div class="tags">
                                <label v-for="s in styleOptions" :key="s" class="tag-item">
                                    <input type="checkbox" :value="s" v-model="form.style" />
                                    <span>{{ s }}</span>
                                </label>
                            </div>
                        </div>
                        <div class="field field-full">
                            <label>补充要求 <span class="optional">（选填）</span></label>
                            <textarea v-model="form.extra_info" placeholder="如：想去一些小众地方，不喜欢人多的景点..."
                                rows="3"></textarea>
                        </div>
                    </div>

                    <div v-if="store.error" class="error-msg">{{ store.error }}</div>

                    <button class="btn-primary" @click="handleSubmit" :disabled="store.loading">
                        <span v-if="store.loading">分析中...</span>
                        <span v-else>开始规划 →</span>
                    </button>
                </div>

                <!-- Step: Clarification -->
                <div v-else-if="store.step === 'clarification'" key="clarification" class="card">
                    <div class="card-title">
                        <span class="step-num">02</span>
                        <h2>需要确认一些细节</h2>
                    </div>
                    <p class="subtitle">AI 发现你的补充要求中有一些需要确认的地方，请查看后决定是否修改。</p>

                    <div class="issues">
                        <div v-for="(issue, i) in store.clarificationResponse.issues" :key="i" class="issue-card">
                            <div class="issue-type"
                                :class="issue.issue_type === '模糊描述' ? 'type-vague' : 'type-conflict'">
                                {{ issue.issue_type }}
                            </div>
                            <blockquote class="issue-original">"{{ issue.original_text }}"</blockquote>
                            <p class="issue-explanation">{{ issue.explanation }}</p>
                            <div class="issue-suggestion">
                                <span class="suggestion-label">建议</span>
                                {{ issue.suggestion }}
                            </div>
                        </div>
                    </div>

                    <div class="clarification-actions">
                        <button class="btn-secondary" @click="store.step = 'form'">修改要求</button>
                        <button v-if="!hasConflict" class="btn-primary" @click="store.startPlanning()"
                            :disabled="store.loading">
                            就这样，继续规划 →
                        </button>
                    </div>
                </div>

                <!-- Step: Planning -->
                <div v-else-if="store.step === 'planning'" key="planning" class="card planning-card">
                    <div class="planning-anim">
                        <div class="plane">✈</div>
                    </div>
                    <h2>AI 正在为你规划行程</h2>
                    <p class="subtitle">正在搜索景点、美食、实用信息，请稍候...</p>
                    <div class="planning-steps">
                        <div class="p-step" v-for="(s, i) in planningSteps" :key="i">
                            <span class="p-dot"></span>{{ s }}
                        </div>
                    </div>
                </div>
            </transition>
        </div>
    </div>
</template>

<script setup>
import { reactive, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useTravelStore } from '../stores/travelStore'

const store = useTravelStore()
const router = useRouter()

watch(() => store.step, (val) => {
    if (val === 'done') {
        router.push('/plan')
    }
})

const styleOptions = ['自然景观', '人文景观', '美食']

const form = reactive({
    location: '南京',
    target: '夏威夷',
    day_num: 5,
    person_num: 30,
    person_composition: '公司',
    accommodation_preference: '经济型',
    budget: 100000,
    has_old: false,
    has_child: false,
    style: ['美食', "自然景观"],
    extra_info: '活动内希望有游泳。所有成本控制在2万人民币内',
})

const planningSteps = ['搜索目的地景点信息...', '寻找当地美食推荐...', '整理交通住宿信息...', '生成个性化行程...']

function handleSubmit() {
    if (!form.location || !form.target || !form.day_num || !form.person_num || !form.budget) {
        alert(`请填写必填项：${[
            !form.location && '出发城市',
            !form.target && '目的地',
            !form.day_num && '旅行天数',
            !form.person_num && '旅游人数',
            !form.budget && '总预算',
        ].filter(Boolean).join('、')}`)
        return
    }
    store.submitForm({ ...form })
}

const hasConflict = computed(() =>
    store.clarificationResponse?.issues?.some(i => i.issue_type === '与表单信息冲突')
)
</script>

<style scoped>
.home {
    min-height: 100vh;
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    padding: 40px 20px 80px;
}

.bg-deco {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
}

.deco-circle {
    position: absolute;
    border-radius: 50%;
    opacity: 0.07;
    background: var(--terracotta);
}

.deco-1 {
    width: 600px;
    height: 600px;
    top: -200px;
    right: -200px;
}

.deco-2 {
    width: 400px;
    height: 400px;
    bottom: -100px;
    left: -150px;
    background: var(--sage);
}

.container {
    width: 100%;
    max-width: 680px;
    position: relative;
    z-index: 1;
}

.header {
    text-align: center;
    margin-bottom: 48px;
}

.logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: var(--terracotta);
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}

.tagline {
    color: var(--ink);
    opacity: 0.5;
    font-size: 0.9rem;
    font-weight: 300;
}

.card {
    background: white;
    border-radius: var(--radius-lg);
    padding: 40px;
    box-shadow: 0 2px 24px var(--shadow);
    border: 1px solid var(--sand);
}

.card-title {
    display: flex;
    align-items: baseline;
    gap: 16px;
    margin-bottom: 32px;
}

.step-num {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    color: var(--sand);
    line-height: 1;
}

.card-title h2 {
    font-size: 1.5rem;
}

.form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 24px;
}

.field {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.field-full {
    grid-column: 1 / -1;
}

.field label {
    font-size: 0.8rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    opacity: 0.6;
}

.optional {
    text-transform: none;
    font-weight: 300;
}

.field input,
.field select,
.field textarea {
    background: var(--mist);
    border: 1px solid var(--sand);
    border-radius: var(--radius);
    padding: 10px 14px;
    font-size: 0.95rem;
    color: var(--ink);
    transition: border-color 0.2s;
}

.field input:focus,
.field select:focus,
.field textarea:focus {
    border-color: var(--terracotta);
    background: white;
}

.field textarea {
    resize: vertical;
}

.checks {
    display: flex;
    gap: 20px;
}

.check-item {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    font-size: 0.9rem;
}

.check-item input {
    accent-color: var(--terracotta);
    width: 16px;
    height: 16px;
}

.tags {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.tag-item {
    cursor: pointer;
}

.tag-item input {
    display: none;
}

.tag-item span {
    display: block;
    padding: 6px 16px;
    border: 1px solid var(--sand);
    border-radius: 20px;
    font-size: 0.85rem;
    transition: all 0.2s;
    background: var(--mist);
}

.tag-item input:checked+span {
    background: var(--terracotta);
    color: white;
    border-color: var(--terracotta);
}

.error-msg {
    color: #c0392b;
    font-size: 0.85rem;
    margin-bottom: 16px;
}

.btn-primary {
    width: 100%;
    padding: 14px;
    background: var(--terracotta);
    color: white;
    border-radius: var(--radius);
    font-size: 0.95rem;
    font-weight: 500;
    letter-spacing: 0.04em;
    transition: all 0.2s;
}

.btn-primary:hover:not(:disabled) {
    background: var(--terracotta-light);
    transform: translateY(-1px);
}

.btn-primary:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.subtitle {
    color: var(--ink);
    opacity: 0.6;
    font-size: 0.9rem;
    margin-bottom: 24px;
    margin-top: -16px;
}

.issues {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 28px;
}

.issue-card {
    background: var(--mist);
    border-radius: var(--radius);
    padding: 20px;
    border-left: 3px solid var(--terracotta);
}

.issue-type {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 10px;
}

.type-vague {
    background: #fef3e2;
    color: #d68910;
}

.type-conflict {
    background: #fde8e8;
    color: #c0392b;
}

.issue-original {
    font-style: italic;
    opacity: 0.7;
    margin-bottom: 8px;
    border-left: none;
    padding-left: 0;
    font-size: 0.9rem;
}

.issue-explanation {
    font-size: 0.875rem;
    margin-bottom: 12px;
}

.issue-suggestion {
    background: white;
    border-radius: var(--radius);
    padding: 10px 14px;
    font-size: 0.85rem;
}

.suggestion-label {
    font-weight: 500;
    color: var(--sage);
    margin-right: 8px;
}

.clarification-actions {
    display: flex;
    gap: 12px;
}

.btn-secondary {
    flex: 1;
    padding: 14px;
    background: transparent;
    border: 1px solid var(--sand);
    border-radius: var(--radius);
    font-size: 0.95rem;
    color: var(--ink);
    transition: all 0.2s;
}

.btn-secondary:hover {
    border-color: var(--terracotta);
    color: var(--terracotta);
}

.btn-primary {
    flex: 2;
}

.planning-card {
    text-align: center;
    padding: 60px 40px;
}

.planning-anim {
    margin-bottom: 24px;
}

.plane {
    font-size: 3rem;
    display: inline-block;
    animation: fly 2s ease-in-out infinite;
}

@keyframes fly {

    0%,
    100% {
        transform: translateX(-10px) rotate(-5deg);
    }

    50% {
        transform: translateX(10px) rotate(5deg);
    }
}

.planning-card h2 {
    margin-bottom: 12px;
}

.planning-steps {
    margin-top: 32px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    text-align: left;
}

.p-step {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 0.875rem;
    opacity: 0.6;
}

.p-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--terracotta);
    flex-shrink: 0;
    animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {

    0%,
    100% {
        opacity: 0.3;
    }

    50% {
        opacity: 1;
    }
}

@media (max-width: 600px) {
    .form-grid {
        grid-template-columns: 1fr;
    }

    .card {
        padding: 24px 16px;
    }

    .clarification-actions {
        flex-direction: column;
    }
}
</style>