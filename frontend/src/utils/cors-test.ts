// CORS 測試工具
export async function testCors(apiUrl: string): Promise<void> {
  console.log('Testing CORS with API:', apiUrl)
  
  // 1. 測試簡單的 GET 請求
  try {
    const getResponse = await fetch(`${apiUrl}/api/v1/health`, {
      method: 'GET',
      mode: 'cors'
    })
    console.log('✅ Simple GET request successful:', getResponse.status)
  } catch (error) {
    console.error('❌ Simple GET request failed:', error)
  }
  
  // 2. 測試 OPTIONS 請求（手動預檢）
  try {
    const optionsResponse = await fetch(`${apiUrl}/api/v1/auth/login`, {
      method: 'OPTIONS',
      headers: {
        'Origin': window.location.origin,
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Content-Type'
      },
      mode: 'cors'
    })
    console.log('✅ OPTIONS request successful:', optionsResponse.status)
    console.log('CORS headers:', optionsResponse.headers)
  } catch (error) {
    console.error('❌ OPTIONS request failed:', error)
  }
  
  // 3. 測試簡單的 POST 請求（不觸發預檢）
  try {
    const formData = new URLSearchParams()
    formData.append('test', 'value')
    
    const simplePostResponse = await fetch(`${apiUrl}/api/v1/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: formData,
      mode: 'cors'
    })
    console.log('✅ Simple POST request completed:', simplePostResponse.status)
  } catch (error) {
    console.error('❌ Simple POST request failed:', error)
  }
}

// 在瀏覽器 console 中調用此函數進行測試
(window as any).testCors = testCors