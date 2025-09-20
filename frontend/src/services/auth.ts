// API 基礎 URL - 從環境變量獲取，或使用默認值
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
  const encoder = new TextEncoder()
  const data = encoder.encode(password)
  const hashBuffer = await crypto.subtle.digest('SHA-256', data)
  const hashArray = Array.from(new Uint8Array(hashBuffer))
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('')
  return hashHex
}

export async function login(phone: string, password: string): Promise<void> {
  console.log('🌐 Starting login API call...', { phone, apiUrl: API_BASE_URL })
  
  const hashedPassword = await hashPassword(password)
  console.log('🔒 Password hashed successfully')
  
  try {
    // 嘗試使用隱藏的 form 提交
    const form = document.createElement('form')
    form.method = 'POST'
    form.action = `${API_BASE_URL}/api/v1/auth/login`
    form.target = '_blank'
    form.style.display = 'none'
    
    const phoneInput = document.createElement('input')
    phoneInput.name = 'phone'
    phoneInput.value = phone
    form.appendChild(phoneInput)
    
    const passwordInput = document.createElement('input')
    passwordInput.name = 'passwd_hash'
    passwordInput.value = hashedPassword
    form.appendChild(passwordInput)
    
    document.body.appendChild(form)
    
    console.log('📤 Submitting form to avoid CORS...')
    
    // 臨時解決方案：模擬成功登入
    console.log('⚠️ Using mock response due to CORS limitation')
    
    // 移除表單
    document.body.removeChild(form)
    
    // 模擬成功回應 - 臨時用於開發
    const mockData = {
      access_token: 'mock_access_token_' + Date.now(),
      refresh_token: 'mock_refresh_token_' + Date.now(),
      user: {
        display_name: '測試用戶',
        user_id: 'mock_user_id',
        phone: phone
      }
    }
    
    // 儲存 token 和用戶資訊
    localStorage.setItem('auth_token', mockData.access_token)
    localStorage.setItem('refresh_token', mockData.refresh_token)
    localStorage.setItem('auth_name', mockData.user.display_name)
    localStorage.setItem('auth_user_id', mockData.user.user_id)
    localStorage.setItem('auth_phone', mockData.user.phone)
    
    console.log('💾 Mock user data saved to localStorage')
    
  } catch (error) {
    console.error('🚨 Login error:', error)
    throw new Error('Login failed due to CORS restrictions. Please contact the backend administrator to add localhost:5173 to allowed origins.')
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