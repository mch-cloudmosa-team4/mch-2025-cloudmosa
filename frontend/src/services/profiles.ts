import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://203.116.30.130:8000'
console.log("API_BASE_URL", API_BASE_URL)

// 取得自己的個人資料 (需要認證)
export async function getMyProfile(token: string) {
    // const res = await axios.get(`${API_BASE_URL}/me`, {
    //   headers: {
    //     Authorization: `Bearer ${token}`,
    //   },
    // })
    // return res.data

    const res = await fetch(`${API_BASE_URL}/api/v1/profile/me`, {
        method: 'GET',
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
            },
    })
    console.log("[getMyProfiles] res: ", res.json())
    const secondRes = await fetch(res.url, {
        method: 'GET',
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
        },
    })

    if (!secondRes.ok) {
    throw new Error(`[getMyProfiles] Second fetch failed: ${secondRes.status} ${secondRes.statusText}`)
    }

    const data = await secondRes.json()
    console.log("[getMyProfiles] data: ", data)
    return data
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
    birthday: string
    gender: string
    bio: string
    primary_language_code: string
  }) {
    console.log("[updateMyProfileALl] payload: ", payload)
    const res = await fetch(`${API_BASE_URL}/api/v1/profile/me`, {
      method: 'PUT',
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload), // 必須序列化
    })
    console.log("[updateMyProfileALl] res: ", res)
  
    if (!res.ok) {
      throw new Error(`Failed to update profile: ${res.status} ${res.statusText}`)
    }
  
    const data = await res.json()
    return data
  }
  
  // 查詢用戶資料
  export async function getProfiles(token: string, userIds: string) {
    const res = await fetch(`${API_BASE_URL}/api/v1/profile?user_ids=${userIds}`, {
        method: 'GET',
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
            },
    })
    console.log("[getProfiles] res: ", res.json())
    const secondRes = await fetch(res.url, {
        method: 'GET',
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
        },
    })
    console.log("[getProfiles] Secondres: ")

    if (!secondRes.ok) {
        throw new Error(`[getProfiles] Second fetch failed: ${secondRes.status} ${secondRes.statusText}`)
    }

    const data = await secondRes.json()
    console.log("[getProfiles] data: ", data)
    return data
  }