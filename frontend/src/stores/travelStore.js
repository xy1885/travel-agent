import { defineStore } from 'pinia'
import { ref } from 'vue'
import { analyzeRequirements, generatePlan } from '../api/agent'

const MOCK = false

const mockPlan = {
  destination: '重庆',
  duration_days: 4,
  summary: '重庆4天3晚深度游，打卡网红景点+地道美食，感受魔幻山城魅力',
  days: [
    {
      day: 1,
      theme: '渝中区经典地标打卡，感受山城魔幻魅力',
      attractions: [
        { name: '解放碑', description: '重庆商业中心地标，周边有八一路好吃街', duration_hours: 1.5, image_url: null, tips: '建议上午到达，先逛解放碑再去好吃街' },
        { name: '洪崖洞', description: '依山而建的吊脚楼群，夜景堪称一绝，对面是绝佳拍照机位', duration_hours: 2.5, image_url: null, tips: '建议傍晚前往，亮灯后夜景最美' },
        { name: '长江索道', description: '横跨长江的空中巴士，俯瞰两岸风光', duration_hours: 1.0, image_url: null, tips: '建议提前在公众号预约购票' },
      ],
    },
    {
      day: 2,
      theme: '南岸文艺之旅，江景与老街的浪漫碰撞',
      attractions: [
        { name: '下浩里', description: '文艺老街，保留了老重庆的市井气息，青石板路非常适合拍照', duration_hours: 2.0, image_url: null, tips: '建议穿复古风格衣服，拍照更出片' },
        { name: '南滨路', description: '一边是美食餐厅，一边是壮丽江景，夜景超浪漫', duration_hours: 2.0, image_url: null, tips: '傍晚时分来最佳' },
      ],
    },
    {
      day: 3,
      theme: '武隆自然奇观一日游',
      attractions: [
        { name: '武隆天生三桥', description: '世界自然遗产，三座天然石桥气势磅礴，《变形金刚4》取景地', duration_hours: 3.0, image_url: null, tips: '建议包车或报一日游团，路程较远需早起' },
        { name: '仙女山', description: '高山草原风光，有东方瑞士之称', duration_hours: 2.5, image_url: null, tips: '山上温度比市区低，记得带外套' },
      ],
    },
    {
      day: 4,
      theme: '美食扫街与自由活动，下午返程',
      attractions: [
        { name: '八一路好吃街', description: '重庆最著名的小吃街，汇集酸辣粉、钵钵鸡、冰粉等地道小吃', duration_hours: 2.0, image_url: null, tips: '空着肚子来！好又来酸辣粉必吃' },
      ],
    },
  ],
  restaurants: [
    { name: '小崖洞街坊老火锅', cuisine: '重庆火锅', price_range: '$$', recommendation: '位于洪崖洞附近，正宗重庆老火锅，人均约¥63-80' },
    { name: '好又来酸辣粉', cuisine: '酸辣粉', price_range: '$', recommendation: '解放碑必吃小吃，人均仅¥10' },
    { name: '1941火锅餐厅', cuisine: '重庆火锅', price_range: '$$', recommendation: '民国风装修+现场表演，适合拍照打卡' },
    { name: '辣得跳毛血旺', cuisine: '川菜', price_range: '$', recommendation: '正宗毛血旺，麻辣鲜香，人均约¥40-60' },
  ],
  practical_info: {
    best_season: ['秋季', '春季'],
    transportation: '南京出发可乘高铁或飞机，市内以地铁+公交为主，重庆地形多山不建议自驾',
    budget_estimate: 6000,
    tips: ['穿舒适的平底鞋，重庆山城地形起伏大', '夏天注意防暑，冬天注意保暖', '洪崖洞、长江索道建议提前预约'],
  },
}

export const useTravelStore = defineStore('travel', () => {
  const userInfo = ref(null)
  const clarificationResponse = ref(null)
  const travelPlan = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const step = ref('form')

  async function submitForm(info) {
    userInfo.value = info

    if (MOCK) {
      await startPlanning()
      return
    }

    loading.value = true
    error.value = null
    try {
      const res = await analyzeRequirements(info)
      clarificationResponse.value = res.data
      if (res.data.needs_clarification) {
        step.value = 'clarification'
      } else {
        await startPlanning()
      }
    } catch (e) {
      error.value = '分析失败，请重试'
    } finally {
      loading.value = false
    }
  }

  async function startPlanning() {
    step.value = 'planning'
    loading.value = true
    error.value = null
    try {
      if (MOCK) {
        await new Promise(r => setTimeout(r, 1500))
        travelPlan.value = mockPlan
      } else {
        const res = await generatePlan(userInfo.value)
        travelPlan.value = res.data
      }
      step.value = 'done'
    } catch (e) {
      error.value = '规划生成失败，请重试'
      step.value = 'form'
    } finally {
      loading.value = false
    }
  }

  function reset() {
    userInfo.value = null
    clarificationResponse.value = null
    travelPlan.value = null
    loading.value = false
    error.value = null
    step.value = 'form'
  }

  return { userInfo, clarificationResponse, travelPlan, loading, error, step, submitForm, startPlanning, reset }
})