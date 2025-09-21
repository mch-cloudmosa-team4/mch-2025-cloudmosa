import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://203.116.30.130:8000'
console.log("API_BASE_URL", API_BASE_URL)

// 取得自己的個人資料 (需要認證)
export async function getMyProfile(token: string) {
    const res = await axios.get(`${API_BASE_URL}/me`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    return res.data
  }
  
  // 部分更新個人資料
  export async function updateMyProfilePartial(token: string, payload: {
    display_name?: string
    birth_date?: string
    gender?: string
    bio?: string
  }) {
    const res = await axios.put(`${API_BASE_URL}/me`, payload, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })
    return res.data
  }
  
  // 完整更新個人資料
  export async function updateMyProfileAll(token: string, payload: {
    display_name: string
    birth_date: string
    gender: string
    bio: string
    primary_language_code: string
  }) {
    const res = await axios.put(`${API_BASE_URL}/me`, payload, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })
    return res.data
  }
  
  // 查詢用戶資料
  export async function getProfiles(token: string, userIds: number[] | string[]) {
    const query = Array.isArray(userIds) ? userIds.join(',') : userIds
    const res = await axios.get(`${API_BASE_URL}?user_ids=${query}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    return res.data
  }