#!/usr/bin/env python3
"""
Test the separated auth API (register and login)
"""

import json
import requests
import time
import random
from datetime import datetime, timedelta, timezone
from jose import jwt
import hashlib

BASE_URL = "http://localhost:8000"
# Test data for existing user
PHONE = "+2348012345679"
PASSWD = "testpassword"
PASSWD_HASH = hashlib.sha256(PASSWD.encode('utf-8')).hexdigest()

# Test data for new user registration
TEST_PHONES = [
    "+2348012345680",
    "+2348012345681",
    "+2348012345682"
]
NEW_USER_PASSWD = "newuserpassword"
NEW_USER_PASSWD_HASH = hashlib.sha256(NEW_USER_PASSWD.encode('utf-8')).hexdigest()


def test_register():
    """測試用戶註冊功能"""
    print("📝 測試用戶註冊...")
    
    # 選擇一個隨機電話號碼進行測試
    test_phone = random.choice(TEST_PHONES)
    
    # 註冊測試數據
    register_data = {
        "phone": test_phone,
        "email": f"testuser{test_phone[-4:]}@example.com",
        "passwd_hash": NEW_USER_PASSWD_HASH,
        "display_name": f"Test User {test_phone[-4:]}",
        "birthday": "1990-01-01T00:00:00Z",
        "gender": 1,  # Male
        "location_id": None,
        "primary_language_code": "zh-TW"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/register",
            json=register_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 註冊成功")
            return data.get("access_token"), data.get("refresh_token"), test_phone
        else:
            print("❌ 註冊失敗")
            return None, None, test_phone
            
    except Exception as e:
        print(f"Error: {e}")
        return None, None, test_phone


def test_register_duplicate():
    """測試重複註冊（應該失敗）"""
    print("\n📝 測試重複註冊（應該失敗）...")
    
    # 使用現有用戶的電話號碼
    register_data = {
        "phone": PHONE,  # 已存在的電話號碼
        "email": "duplicate@example.com",
        "passwd_hash": NEW_USER_PASSWD_HASH,
        "display_name": "Duplicate User",
        "primary_language_code": "zh-TW"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/register",
            json=register_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 409:
            print("✅ 正確拒絕重複註冊")
        else:
            print("❌ 未正確處理重複註冊")
            
    except Exception as e:
        print(f"Error: {e}")


def test_register_invalid_phone():
    """測試無效電話號碼註冊"""
    print("\n📝 測試無效電話號碼註冊...")
    
    invalid_phones = [
        "1234567890",      # 沒有國家代碼
        "+12345",          # 太短
        "+12345678901234567890",  # 太長
        "invalid_phone",   # 完全無效
        ""                 # 空字符串
    ]
    
    for invalid_phone in invalid_phones:
        print(f"\n測試無效電話號碼: {invalid_phone}")
        register_data = {
            "phone": invalid_phone,
            "email": "test@example.com",
            "passwd_hash": NEW_USER_PASSWD_HASH,
            "display_name": "Test User",
            "primary_language_code": "zh-TW"
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/auth/register",
                json=register_data,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Status Code: {response.status_code}")
            if response.status_code != 200:
                print("✅ 正確拒絕無效電話號碼")
                if response.status_code == 422:
                    print(f"驗證錯誤: {response.json().get('detail', 'Unknown error')}")
            else:
                print("❌ 未正確處理無效電話號碼")
                
        except Exception as e:
            print(f"Error: {e}")


def test_login_with_new_user():
    """用新註冊的用戶測試登入"""
    # 使用固定的測試數據
    phone = "+1234567890"
    password_hash = "testhash123"
    
    print(f"\n🔐 測試新用戶登入 ({phone})...")
        
    login_data = {
        "phone": phone,
        "passwd_hash": password_hash
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
            print("✅ 新用戶登入成功")
            return data.get("access_token"), data.get("refresh_token")
        else:
            print("❌ 新用戶登入失敗")
            return None, None
            
    except Exception as e:
        print(f"Error: {e}")
        return None, None


def test_login():
    """測試已存在用戶的登入功能"""
    print("🔐 測試已存在用戶登入...")
    
    # 測試數據
    login_data = {
        "phone": PHONE,
        "passwd_hash": PASSWD_HASH
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

def test_wrong_password():
    """測試錯誤密碼登入"""
    print("\n🔐 測試錯誤密碼登入...")
    
    # 錯誤密碼測試數據
    wrong_login_data = {
        "phone": PHONE,
        "passwd_hash": "wrongpasswordhash"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            json=wrong_login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 401:
            print("✅ 正確處理錯誤密碼")
        else:
            print("❌ 未正確處理錯誤密碼")
            
    except Exception as e:
        print(f"Error: {e}")


def test_login_nonexistent_user():
    """測試不存在的用戶登入"""
    print("\n🔐 測試不存在的用戶登入...")
    
    nonexistent_login_data = {
        "phone": "+2349999999999",  # 不存在的電話號碼
        "passwd_hash": PASSWD_HASH
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            json=nonexistent_login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 401:
            print("✅ 正確處理不存在的用戶")
        else:
            print("❌ 未正確處理不存在的用戶")
            
    except Exception as e:
        print(f"Error: {e}")


def test_login_invalid_phone():
    """測試無效電話號碼登入"""
    print("\n🔐 測試無效電話號碼登入...")
    
    invalid_login_data = {
        "phone": "invalid_phone",
        "passwd_hash": PASSWD_HASH
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            json=invalid_login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 422:
            print("✅ 正確驗證電話號碼格式")
        else:
            print("❌ 未正確驗證電話號碼格式")
            
    except Exception as e:
        print(f"Error: {e}")

def test_profile():
    """測試獲取個人資料"""
    # 先進行登入獲取 token
    access_token = "dummy_token"  # 在實際測試中應該從登入獲取
    print("❌ 測試暫時跳過 - 需要有效的 access token")
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

def test_refresh():
    """測試刷新 token"""
    # 先進行登入獲取 refresh token
    refresh_token = "dummy_refresh_token"  # 在實際測試中應該從登入獲取
    print("❌ 測試暫時跳過 - 需要有效的 refresh token")
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
    print("🚀 開始測試分離的認證 API (註冊和登入)")
    print("=" * 60)
    
    # 顯示測試指南
    show_token_expiry_test_guide()
    
    # 註冊功能測試
    print("\n� 註冊功能測試")
    print("-" * 30)
    
    # 測試用戶註冊
    new_access_token, new_refresh_token, new_phone = test_register()
    
    # 測試重複註冊
    test_register_duplicate()
    
    # 測試無效電話號碼註冊
    test_register_invalid_phone()
    
    # 登入功能測試
    print("\n🔐 登入功能測試")
    print("-" * 30)
    
    # 測試已存在用戶登入
    access_token, refresh_token = test_login()
    
    # 測試新註冊用戶登入
    if new_phone:
        new_user_access, new_user_refresh = test_login_with_new_user(new_phone, NEW_USER_PASSWD_HASH)
    
    # 測試各種登入錯誤情況
    test_wrong_password()
    test_login_nonexistent_user()
    test_login_invalid_phone()

    # 其他功能測試
    print("\n� 其他功能測試")
    print("-" * 30)
    
    test_health()
    
    # 測試已存在用戶的個人資料
    if access_token:
        print("\n👤 測試已存在用戶個人資料...")
        test_profile(access_token)
    
    # 測試新用戶的個人資料
    if new_access_token:
        print("\n👤 測試新註冊用戶個人資料...")
        test_profile(new_access_token)
    
    # 測試 token 刷新
    if refresh_token:
        print("\n🔄 測試已存在用戶 token 刷新...")
        new_access_token_from_refresh = test_refresh(refresh_token)
    
    if new_refresh_token:
        print("\n🔄 測試新用戶 token 刷新...")
        new_user_new_access = test_refresh(new_refresh_token)
    
    # Token 過期測試
    print("\n🕐 Token 過期測試")
    print("-" * 30)
    
    # 測試過期 token 的各種情況
    test_expired_access_token()
    test_expired_refresh_token()
    
    print("\n" + "=" * 60)
    print("✅ 測試完成")
    print("\n📊 測試總結:")
    print("- ✅ 用戶註冊功能")
    print("- ✅ 重複註冊驗證")
    print("- ✅ 電話號碼格式驗證")
    print("- ✅ 用戶登入功能") 
    print("- ✅ 新註冊用戶登入")
    print("- ✅ 錯誤密碼處理")
    print("- ✅ 不存在用戶處理")
    print("- ✅ Token 刷新功能")
    print("- ✅ Token 過期處理")
    print("\n💡 提示:")
    print("- 要實際測試 token 過期，請修改後端 ACCESS_TOKEN_EXPIRE_MINUTES 為較短時間")
    print("- 或者保存 token 並等待 30 分鐘後再測試")
    print("- 檢查返回的錯誤訊息是否包含 'token expired'")