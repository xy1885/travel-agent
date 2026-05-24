import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 300000, // 2分钟，Agent 规划需要时间
})

export const analyzeRequirements = (userInfo) => {
  return api.post('/analyze', userInfo)
}

export const generatePlan = (userInfo) => {
  return api.post('/plan', userInfo)
}