#!/usr/bin/env python3
"""
Test the simplified auth API
"""

import json
import requests
import time
from datetime import datetime, timedelta, timezone
from jose import jwt

BASE_URL = "http://localhost:8000"

def test_login():
    """測試登錄功能"""
    print("🔐 測試登錄...")
    
    # 測試數據
    login_data = {
        "phone": "+2348012345678"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token"), data.get("refresh_token")
        else:
            return None, None
            
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def test_profile(access_token):
    """測試獲取個人資料"""
    if not access_token:
        print("❌ 無 access token，跳過測試")
        return
        
    print("\n👤 測試獲取個人資料...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/profile/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
    except Exception as e:
        print(f"Error: {e}")

def test_health():
    """測試健康檢查"""
    print("\n🏥 測試健康檢查...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
    except Exception as e:
        print(f"Error: {e}")

def test_refresh(refresh_token):
    """測試刷新 token"""
    if not refresh_token:
        print("❌ 無 refresh token，跳過測試")
        return
        
    print("\n🔄 測試刷新 token...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            return response.json().get("access_token")
        return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def create_expired_token():
    """創建一個已過期的 access token 用於測試"""
    print("\n⏰ 創建過期 token 進行測試...")
    
    # 使用和後端相同的設定
    SECRET_KEY = "your-secret-key-change-this-in-production"  # 從 app.config 獲取的預設值
    ALGORITHM = "HS256"
    
    # 創建已過期的 payload (過期時間設為 1 秒前)
    expired_payload = {
        "sub": "63f51cf7-140c-4771-b790-d82e6f17cae5",  # 假設的用戶ID (UUID格式)
        "exp": datetime.now(timezone.utc) - timedelta(seconds=1),  # 1秒前過期
        "type": "access"
    }
    
    try:
        expired_token = jwt.encode(expired_payload, SECRET_KEY, algorithm=ALGORITHM)
        print(f"✅ 已創建過期 token: {expired_token[:50]}...")
        return expired_token
    except Exception as e:
        print(f"❌ 創建過期 token 失敗: {e}")
        return None

def test_expired_access_token():
    """測試過期的 access token"""
    print("\n🕐 測試過期的 access token...")
    
    # 方法1: 使用手動創建的過期 token
    expired_token = create_expired_token()
    if expired_token:
        print("使用手動創建的過期 token 測試...")
        test_with_expired_token(expired_token)
    
    # 方法2: 使用實際登錄後等待 token 過期 (如果 token 有效期很短)
    print("\n⏳ 如果要測試真實過期情況，請等待 30 分鐘後使用舊的 access token")

def test_with_expired_token(expired_token):
    """使用過期 token 測試受保護的端點"""
    print(f"測試使用過期 token 訪問 /profile/me...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/profile/me",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        # 檢查是否正確返回 401 和 "token expired" 訊息
        if response.status_code == 401:
            error_detail = response.json().get("detail", "")
            if "expired" in error_detail.lower():
                print("✅ 正確識別出 token 過期")
            else:
                print(f"⚠️  返回了 401 但錯誤訊息不含 'expired': {error_detail}")
        else:
            print(f"❌ 期望返回 401，但實際返回 {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

def test_expired_refresh_token():
    """測試過期的 refresh token"""
    print("\n🕐 測試過期的 refresh token...")
    
    # 創建過期的 refresh token
    SECRET_KEY = "your-secret-key-change-this-in-production"  # 從 app.config 獲取的預設值
    ALGORITHM = "HS256"
    
    expired_refresh_payload = {
        "sub": "550e8400-e29b-41d4-a716-446655440000",  # 假設的用戶ID (UUID格式)
        "exp": datetime.now(timezone.utc) - timedelta(seconds=1),  # 1秒前過期
        "type": "refresh"
    }
    
    try:
        expired_refresh_token = jwt.encode(expired_refresh_payload, SECRET_KEY, algorithm=ALGORITHM)
        print(f"✅ 已創建過期 refresh token")
        
        # 測試使用過期 refresh token
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/refresh",
            json={"refresh_token": expired_refresh_token},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        # 檢查是否正確返回 401 和 "token expired" 訊息
        if response.status_code == 401:
            error_detail = response.json().get("detail", "")
            if "expired" in error_detail.lower():
                print("✅ 正確識別出 refresh token 過期")
            else:
                print(f"⚠️  返回了 401 但錯誤訊息不含 'expired': {error_detail}")
        else:
            print(f"❌ 期望返回 401，但實際返回 {response.status_code}")
            
    except Exception as e:
        print(f"Error creating or testing expired refresh token: {e}")

def test_manual_token_expiry(access_token):
    """手動測試 token 過期 - 需要修改後端 token 有效期為很短的時間"""
    if not access_token:
        print("❌ 無 access token，跳過手動過期測試")
        return
        
    print("\n⏱️  手動測試 token 過期 (需要後端設定短過期時間)")
    print("步驟:")
    print("1. 修改後端 ACCESS_TOKEN_EXPIRE_MINUTES = 0.1 (6秒)")
    print("2. 重啟後端服務")
    print("3. 登錄獲取 token")
    print("4. 等待 6 秒後嘗試訪問受保護端點")
    
    print(f"\n當前 access token: {access_token[:50]}...")
    print("請等待幾秒後再次運行測試...")

def wait_and_test_expiry(access_token, wait_seconds=10):
    """等待指定時間後測試 token 是否過期"""
    if not access_token:
        print("❌ 無 access token，跳過等待測試")
        return
        
    print(f"\n⏰ 等待 {wait_seconds} 秒後測試 token 過期...")
    print("如果後端 token 有效期設為很短，這個測試會有效")
    
    # 先測試當前 token 是否有效
    print("測試當前 token 狀態...")
    test_with_token(access_token, "當前")
    
    # 等待
    print(f"等待 {wait_seconds} 秒...")
    time.sleep(wait_seconds)
    
    # 再次測試
    print("等待後測試 token 狀態...")
    test_with_token(access_token, "等待後")

def test_with_token(token, description=""):
    """測試指定 token 的狀態"""
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/profile/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print(f"{description} - Status Code: {response.status_code}")
        if response.status_code != 200:
            print(f"{description} - Error: {response.json().get('detail', 'Unknown error')}")
        else:
            print(f"{description} - ✅ Token 仍然有效")
            
    except Exception as e:
        print(f"{description} - Error: {e}")

def show_token_expiry_test_guide():
    """顯示 token 過期測試指南"""
    print("\n" + "=" * 60)
    print("🧪 Token 過期測試指南")
    print("=" * 60)
    print()
    print("有以下幾種方法測試 token 過期:")
    print()
    print("方法1: 修改後端 token 有效期 (推薦)")
    print("  1. 編輯 app/utils/auth.py")
    print("  2. 修改 ACCESS_TOKEN_EXPIRE_MINUTES = 0.1  # 6秒過期")
    print("  3. 重啟後端服務")
    print("  4. 登錄後等待 6 秒，然後訪問受保護端點")
    print()
    print("方法2: 手動創建過期 token (需要知道 secret key)")
    print("  1. 獲取後端的 SECRET_KEY")
    print("  2. 使用 jose.jwt 創建過期的 token")
    print("  3. 使用該 token 訪問受保護端點")
    print()
    print("方法3: 等待真實過期 (30分鐘)")
    print("  1. 登錄獲取 token")
    print("  2. 等待 30 分鐘")
    print("  3. 使用舊 token 訪問受保護端點")
    print()
    print("方法4: 使用 Postman/Thunder Client 等工具")
    print("  1. 保存一個舊的 access token")
    print("  2. 等待過期後使用該 token 測試")
    print()
    print("=" * 60)

if __name__ == "__main__":
    print("🚀 開始測試簡化認證 API")
    print("=" * 50)
    
    # 顯示測試指南
    show_token_expiry_test_guide()
    
    # 基礎功能測試
    print("\n📋 基礎功能測試")
    print("-" * 30)
    
    # 測試登錄
    access_token, refresh_token = test_login()
    
    # 測試其他功能
    test_health()
    test_profile(access_token)
    new_access_token = test_refresh(refresh_token)
    
    # Token 過期測試
    print("\n🕐 Token 過期測試")
    print("-" * 30)
    
    # 測試過期 token 的各種情況
    test_expired_access_token()
    test_expired_refresh_token()
    
    # 提供手動測試選項
    # if access_token:
    #     test_manual_token_expiry(access_token)
        
    #     print("\n選擇測試選項:")
    #     print("1. 輸入 'wait' 等待 10 秒測試 (適用於短過期時間)")
    #     print("2. 直接按 Enter 結束測試")
        
    #     user_input = input("\n請選擇 (wait/Enter): ").strip().lower()
    #     if user_input == 'wait':
    #         wait_and_test_expiry(access_token or new_access_token)
    
    print("\n" + "=" * 50)
    print("✅ 測試完成")
    print("\n💡 提示:")
    print("- 要實際測試 token 過期，請修改後端 ACCESS_TOKEN_EXPIRE_MINUTES 為較短時間")
    print("- 或者保存 token 並等待 30 分鐘後再測試")
    print("- 檢查返回的錯誤訊息是否包含 'token expired'")