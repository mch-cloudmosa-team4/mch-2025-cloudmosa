// 地理位置和地址反查工具
export interface LocationData {
  latitude: number
  longitude: number
  address?: string
  city?: string
  country?: string
  state?: string
  formatted_address?: string
}

// 獲取用戶當前位置
export async function getCurrentLocation(): Promise<{ latitude: number; longitude: number }> {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('Geolocation is not supported by this browser'))
      return
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        resolve({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude
        })
      },
      (error) => {
        let errorMessage = 'Unknown geolocation error'
        
        switch (error.code) {
          case error.PERMISSION_DENIED:
            errorMessage = 'User denied the request for Geolocation'
            break
          case error.POSITION_UNAVAILABLE:
            errorMessage = 'Location information is unavailable'
            break
          case error.TIMEOUT:
            errorMessage = 'The request to get user location timed out'
            break
          default:
            errorMessage = 'An unknown error occurred while retrieving location'
            break
        }
        
        console.error('Geolocation error details:', {
          code: error.code,
          message: error.message,
          description: errorMessage
        })
        
        reject(new Error(errorMessage))
      },
      {
        enableHighAccuracy: false, // 改為 false，減少對精確位置的要求
        timeout: 15000, // 增加超時時間到 15 秒
        maximumAge: 300000 // 允許使用 5 分鐘內的快取位置
      }
    )
  })
}

// 使用 OpenStreetMap Nominatim API 反查地址（免費，無需 API Key）
export async function reverseGeocode(latitude: number, longitude: number): Promise<any> {
  try {
    console.log(`🗺️ Requesting address from Nominatim for ${latitude}, ${longitude}`)
    
    const response = await fetch(
      `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&accept-language=zh-TW,zh,en`,
      {
        headers: {
          'User-Agent': 'MCH-2025-CloudMosa-Frontend/1.0' // Nominatim 要求提供 User-Agent
        }
      }
    )
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    console.log('🗺️ Nominatim raw response:', data)
    
    if (data && data.address) {
      const address = data.address
      
      // 從回應中提取地址資訊
      const city = address.city || address.town || address.village || address.hamlet || '未知城市'
      const country = address.country || '未知國家'
      const state = address.state || address.province || ''
      
      // 組合完整地址
      const formatted_address = data.display_name || `${latitude}, ${longitude}`
      
      const result = {
        formatted_address: formatted_address,
        city: city,
        country: country,
        state: state,
        full_result: data
      }
      
      console.log('🏠 Parsed address info:', result)
      return result
      
    } else {
      throw new Error('No address data found in response')
    }
  } catch (error) {
    console.error('🚨 Nominatim geocoding error:', error)
    
    // 如果反查失敗，返回基本的座標資訊
    return {
      formatted_address: `${latitude}, ${longitude}`,
      city: '位置未知',
      country: '未知',
      state: '',
      error: error instanceof Error ? error.message : String(error)
    }
  }
}

// 獲取完整的位置信息（位置 + 地址）
export async function getLocationWithAddress(): Promise<LocationData> {
  try {
    console.log('🌍 Getting current location...')
    const coords = await getCurrentLocation()
    console.log('📍 Location coordinates:', coords)
    
    const locationData: LocationData = {
      latitude: coords.latitude,
      longitude: coords.longitude
    }
    
    // 嘗試獲取地址信息
    try {
      console.log('🏠 Reverse geocoding address...')
      const addressInfo = await reverseGeocode(coords.latitude, coords.longitude)
      console.log('🏠 Address info:', addressInfo)
      
      locationData.address = addressInfo.formatted_address
      locationData.city = addressInfo.city
      locationData.country = addressInfo.country
      locationData.state = addressInfo.state
      locationData.formatted_address = addressInfo.formatted_address
      
    } catch (geocodeError) {
      console.warn('⚠️ Failed to get address info:', geocodeError)
      // 即使地址反查失敗，我們仍然可以使用坐標
    }
    
    return locationData
  } catch (error) {
    console.error('❌ Failed to get location:', error)
    throw error
  }
}