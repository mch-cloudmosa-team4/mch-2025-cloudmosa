// Applications API service
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://203.116.30.130:8000'

// 取得我的應徵申請
export async function getMyApplications(token: string, options?: { skip?: number, limit?: number, status?: number }) {
  const queryParams = new URLSearchParams()
  
  if (options?.skip) queryParams.append('skip', options.skip.toString())
  if (options?.limit) queryParams.append('limit', options.limit.toString())
  if (options?.status !== undefined) queryParams.append('status', options.status.toString())
  
  const url = `${API_BASE_URL}/api/v1/applications/me${queryParams.toString() ? '?' + queryParams.toString() : ''}`
  
  const res = await fetch(url, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  })
  
  if (!res.ok) {
    throw new Error(`Failed to fetch applications: ${res.status} ${res.statusText}`)
  }
  
  const data = await res.json()
  console.log('✅ Applications fetched successfully:', data)
  return data
}

// 取得單一申請詳情
export async function getApplication(token: string, applicationId: string) {
  const res = await fetch(`${API_BASE_URL}/api/v1/applications/${applicationId}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  })
  
  if (!res.ok) {
    throw new Error(`Failed to fetch application: ${res.status} ${res.statusText}`)
  }
  
  const data = await res.json()
  return data
}

// 狀態對應
export function getStatusText(status: number): string {
  const statusMap: Record<number, string> = {
    0: 'Pending',
    1: 'Under Review', 
    2: 'Interview',
    3: 'Accepted',
    4: 'Rejected'
  }
  return statusMap[status] || 'Unknown'
}

// 日期格式化
export function formatDate(dateString: string): string {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-TW', { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit' 
  })
}
