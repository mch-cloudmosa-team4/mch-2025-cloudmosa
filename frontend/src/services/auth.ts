// API 基礎 URL - 從環境變量獲取，或使用默認值
import { getLocationWithAddress, type LocationData } from '../utils/location'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

interface LoginResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: {
    user_id: string
    phone: string
    email: string | null
    display_name: string
    is_active: boolean
    created_at: string
    last_login_at: string
  }
}

interface LoginError {
  detail: string
}

// 將密碼轉換為 SHA-256 hash
async function hashPassword(password: string): Promise<string> {
  // 檢查是否有 crypto.subtle 可用（HTTPS 環境）
  if (window.crypto && window.crypto.subtle) {
    try {
      const encoder = new TextEncoder()
      const data = encoder.encode(password)
      const hashBuffer = await crypto.subtle.digest('SHA-256', data)
      const hashArray = Array.from(new Uint8Array(hashBuffer))
      const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('')
      return hashHex
    } catch (error) {
      console.warn('⚠️ crypto.subtle failed, falling back to simple hash:', error)
    }
  }
  
  // 備用方案：簡單的字符串 hash (僅用於開發/測試環境)
  console.warn('⚠️ Using fallback hash function (not secure for production)')
  return btoa(password) // 簡單的 base64 編碼作為備用
}

export async function login(phone: string, password: string): Promise<void> {
  console.log('🌐 Starting login API call...', { phone, apiUrl: API_BASE_URL })
  
  const hashedPassword = await hashPassword(password)
  console.log('🔒 Password hashed successfully')
  
  // 獲取地理位置信息
  let locationData: LocationData | null = null
  try {
    console.log('🌍 Attempting to get location data...')
    locationData = await getLocationWithAddress()
    console.log('📍 Location data obtained successfully:', locationData)
  } catch (locationError) {
    console.warn('⚠️ Could not get location data, continuing without location:', locationError)
    // 繼續登入流程，即使沒有位置信息
    // 不拋出錯誤，讓用戶仍能登入
  }
  
  try {
    // 準備基本的登入資料（暫時不包含地理位置）
    const requestData = {
      phone: phone,
      passwd_hash: hashedPassword
    }
    
    // 地理位置資料先保留在本地，暫時不發送到後端
    if (locationData) {
      console.log('📍 Location data available (not sent to backend yet):', locationData)
      // 儲存到 localStorage 供未來使用
      localStorage.setItem('temp_location_data', JSON.stringify(locationData))
    }
    
    console.log('📤 Sending request to:', `${API_BASE_URL}/api/v1/auth/login`)
    console.log('📤 Request data:', requestData)
    
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData)
    })

    console.log('📥 Response received:', response.status, response.statusText)

    if (!response.ok) {
      let errorMessage = 'Login failed'
      
      // 處理特定的 HTTP 狀態碼
      if (response.status === 401) {
        errorMessage = 'Invalid phone number or password'
      } else {
        try {
          const errorData: LoginError = await response.json()
          console.log('❌ Error response data:', errorData)
          errorMessage = errorData.detail || errorMessage
        } catch {
          errorMessage = `HTTP ${response.status}: ${response.statusText}`
        }
      }
      
      throw new Error(errorMessage)
    }

    const data: LoginResponse = await response.json()
    console.log('✅ Login response data:', data)
    
    // 儲存 token 和用戶資訊
    localStorage.setItem('auth_token', data.access_token)
    localStorage.setItem('refresh_token', data.refresh_token)
    localStorage.setItem('auth_name', data.user.display_name)
    localStorage.setItem('auth_user_id', data.user.user_id)
    localStorage.setItem('auth_phone', data.user.phone)
    
    console.log('💾 User data saved to localStorage')
    
    // 如果之前有獲取到地理位置，也一併儲存（供未來功能使用）
    if (locationData) {
      localStorage.setItem('auth_location', JSON.stringify(locationData))
      console.log('� Location data also saved for future use')
    }
    
  } catch (error) {
    console.error('🚨 Login error:', error)
    if (error instanceof Error) {
      throw new Error(error.message)
    }
    throw new Error('Network error occurred')
  }
}

export function isAuthed(): boolean {
  return !!localStorage.getItem('auth_token')
}

export function logout(): void {
  localStorage.removeItem('auth_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('auth_name')
  localStorage.removeItem('auth_user_id')
  localStorage.removeItem('auth_phone')
}

export function getUserId(): number | null {
  const id = localStorage.getItem('auth_user_id')
  // 為了向後兼容，如果存儲的是數字字符串，返回數字
  // 如果是 UUID，轉換為一個固定的數字（或者你可以保持字符串）
  if (!id) return null
  
  // 檢查是否是純數字
  const numId = parseInt(id)
  if (!isNaN(numId)) return numId
  
  // 如果是 UUID，為了兼容性返回一個 hash 或固定數字
  // 這裡簡單地返回 1，你可以根據需要調整
  return 1
}

export function getUserUUID(): string | null {
  return localStorage.getItem('auth_user_id')
}

export function getAuthToken(): string | null {
  return localStorage.getItem('auth_token')
}

export function getUserName(): string {
  return localStorage.getItem('auth_name') || 'Guest'
}

export function getUserPhone(): string | null {
  return localStorage.getItem('auth_phone')
}

// 用於 API 請求的 Authorization header
export function getAuthHeaders(): Record<string, string> {
  const token = getAuthToken()
  if (!token) {
    throw new Error('No authentication token found')
  }
  return {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
}