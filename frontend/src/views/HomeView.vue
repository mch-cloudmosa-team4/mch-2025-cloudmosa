<template>
  <main class="screen">
    <div class="header">
      <h1 class="title">Hi, {{ name }} 👋</h1>
      <div class="logout-container">
        <button class="logout-btn" @click="handleLogout" @mouseenter="showLogoutLabel = true" @mouseleave="showLogoutLabel = false">
          <span class="material-icons-round">logout</span>
        </button>
        <span v-if="showLogoutLabel" class="logout-label">Logout</span>
      </div>
    </div>

    <!-- 登出確認對話框 -->
    <div v-if="showLogoutDialog" class="logout-dialog-overlay" @click="cancelLogout">
      <div class="logout-dialog" @click.stop>
        <h3>Confirm Logout</h3>
        <p>Are you sure you want to logout?</p>
        <div class="dialog-buttons">
          <button class="dialog-btn cancel" @click="cancelLogout">Cancel</button>
          <button class="dialog-btn confirm" @click="confirmLogout">Logout</button>
        </div>
      </div>
    </div>
    
    <!-- 3D 模型容器替換原來的 GIF -->
    <div ref="threeContainer" class="three-model-container">
      <div v-if="loading" class="loading-indicator">
        <div class="spinner"></div>
      </div>
    </div>

    <div class="level-container">
      <span class="level-label">Level {{ level }}</span>
      <div class="level-bar">
        <div class="level-progress" :style="{ width: progress + '%' }"></div>
      </div>
      <span class="level-exp">{{ exp }}/{{ expNeeded }} EXP</span>
      
      <!-- 方向控制按鈕 -->
      <div class="direction-controls">
        <button class="direction-btn up" @click="rotateUp">
          <span class="material-icons-round">keyboard_arrow_up</span>
        </button>
        <button class="direction-btn down" @click="rotateDown">
          <span class="material-icons-round">keyboard_arrow_down</span>
        </button>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { isAuthed, getUserName } from '../services/auth'
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'

const router = useRouter()
const name = getUserName()
const threeContainer = ref<HTMLElement>()
const loading = ref(true)
const showLogoutLabel = ref(false)
const showLogoutDialog = ref(false)

// Mock level
const level = ref(3)
const exp = ref(120)          // 當前經驗
const expNeeded = ref(200)    // 升級所需經驗
const progress = ref((exp.value / expNeeded.value) * 100)

// Three.js variables
let scene: THREE.Scene
let camera: THREE.PerspectiveCamera
let renderer: THREE.WebGLRenderer
let pigModel: THREE.Group
let animationId: number
let cameraRadius = 3.5 // 相機距離中心的固定距離
let cameraAngleY = 0    // 相機的垂直角度（0 = 平視）

const initThreeJS = () => {
  if (!threeContainer.value) return

  // 場景
  scene = new THREE.Scene()
  scene.background = new THREE.Color(0xfdfdfd) // 與背景色一致

  // 相機 - 適合小容器的設置
  const aspect = threeContainer.value.clientWidth / threeContainer.value.clientHeight
  camera = new THREE.PerspectiveCamera(60, aspect, 0.1, 100)
  // 初始設置相機位置
  updateCameraPosition()

  // 渲染器
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
  renderer.setSize(threeContainer.value.clientWidth, threeContainer.value.clientHeight)
  renderer.shadowMap.enabled = true
  renderer.shadowMap.type = THREE.PCFSoftShadowMap
  threeContainer.value.appendChild(renderer.domElement)

  // 光源 - 增強光照設置讓豬更亮
  const ambientLight = new THREE.AmbientLight(0xffffff, 1.0) // 提高環境光強度
  scene.add(ambientLight)

  const directionalLight = new THREE.DirectionalLight(0xffffff, 1.2) // 提高主光源強度
  directionalLight.position.set(5, 5, 5)
  directionalLight.castShadow = true
  scene.add(directionalLight)

  // 增加額外的光源讓豬更亮
  const frontLight = new THREE.DirectionalLight(0xffffff, 0.8)
  frontLight.position.set(0, 0, 10)
  scene.add(frontLight)

  const backLight = new THREE.DirectionalLight(0xffffff, 0.6)
  backLight.position.set(0, 5, -5)
  scene.add(backLight)

  const leftLight = new THREE.PointLight(0xffffff, 0.5, 50)
  leftLight.position.set(-5, 2, 2)
  scene.add(leftLight)

  const rightLight = new THREE.PointLight(0xffffff, 0.5, 50)
  rightLight.position.set(5, 2, 2)
  scene.add(rightLight)
}

const loadPigModel = () => {
  const loader = new GLTFLoader()
  loader.load(
    '/pig.glb',
    (gltf) => {
      pigModel = gltf.scene
      
      // 調整模型大小和位置
      const box = new THREE.Box3().setFromObject(pigModel)
      const center = box.getCenter(new THREE.Vector3())
      const size = box.getSize(new THREE.Vector3())
      
      // 置中模型
      pigModel.position.sub(center)
      pigModel.position.y += 0.3
      
      // 縮放到適合容器大小
      const maxSize = Math.max(size.x, size.y, size.z)
      const scale = 3.0 / maxSize
      pigModel.scale.setScalar(scale)
      
      // 設置陰影
      pigModel.traverse((child) => {
        if (child instanceof THREE.Mesh) {
          child.castShadow = true
          child.receiveShadow = true
        }
      })

      scene.add(pigModel)
      loading.value = false
    },
    undefined,
    (error) => {
      console.error('Error loading pig model:', error)
      loading.value = false
    }
  )
}

const animate = () => {
  animationId = requestAnimationFrame(animate)
  
  // 緩慢自動旋轉
  if (pigModel) {
    pigModel.rotation.y += 0.005
  }
  
  renderer.render(scene, camera)
}

const handleResize = () => {
  if (!threeContainer.value) return
  
  const aspect = threeContainer.value.clientWidth / threeContainer.value.clientHeight
  camera.aspect = aspect
  camera.updateProjectionMatrix()
  renderer.setSize(threeContainer.value.clientWidth, threeContainer.value.clientHeight)
}

// 視角旋轉控制函數
const rotateUp = () => {
  if (camera) {
    // 向上旋轉視角 - 增加仰角（從下往上看）
    cameraAngleY -= 0.15
    // 限制最大仰角，避免轉過頭
    if (cameraAngleY <= -1.2) cameraAngleY = -1.2
    updateCameraPosition()
  }
}

const rotateDown = () => {
  if (camera) {
    // 向下旋轉視角 - 減少仰角（從上往下看）
    cameraAngleY += 0.15
    // 限制最小仰角
    if (cameraAngleY >= 1.35) cameraAngleY = 1.35
    updateCameraPosition()
  }
}

// 更新相機位置的輔助函數
const updateCameraPosition = () => {
  if (camera) {
    // 使用球坐標系統，保持固定距離，只改變角度
    camera.position.x = 0
    camera.position.y = cameraRadius * Math.sin(cameraAngleY)
    camera.position.z = cameraRadius * Math.cos(cameraAngleY)
    
    // 始終看向豬模型中心
    camera.lookAt(0, 0.3, 0) // 稍微向上看一點（豬的中心位置）
  }
}

// 登出處理函數
const handleLogout = () => {
  showLogoutDialog.value = true
}

const confirmLogout = () => {
  // 清除登入狀態
  localStorage.removeItem('auth_token')
  localStorage.removeItem('auth_name')
  // 跳轉到登入頁面
  router.replace('/login')
}

const cancelLogout = () => {
  showLogoutDialog.value = false
}

onMounted(() => {
  initThreeJS()
  loadPigModel()
  animate()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  window.removeEventListener('resize', handleResize)
  if (renderer) {
    renderer.dispose()
  }
})

if (!isAuthed()) router.replace('/login')
</script>

<style scoped>
.screen {
  width: 240px;
  height: 320px;
  background: #fdfdfd;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 8px;
}

.title {
  font-size: 18px;
  padding-top: 16px;
  margin: 0;
  color: #222;
  flex: 1;
  text-align: center;
}

.settings-btn {
  background: none;
  border: none;
  padding: 4px;
  border-radius: 50%;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.settings-btn:hover {
  background: rgba(42, 65, 102, 0.1);
}

.settings-btn .material-icons-round {
  font-size: 20px;
  color: rgb(42, 65, 102);
}

/* 登出按鈕容器 */
.logout-container {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logout-btn {
  background: none;
  border: none;
  padding: 4px;
  border-radius: 50%;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.logout-btn:hover {
  background: rgba(42, 65, 102, 0.1);
}

.logout-btn .material-icons-round {
  font-size: 20px;
  color: rgb(42, 65, 102);
}

.logout-label {
  position: absolute;
  top: 100%;
  margin-top: 4px;
  font-size: 10px;
  color: rgb(42, 65, 102);
  white-space: nowrap;
  background: rgba(255, 255, 255, 0.9);
  padding: 2px 6px;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

/* 登出確認對話框樣式 */
.logout-dialog-overlay {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 240px;
  height: 320px;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.logout-dialog {
  background: white;
  padding: 16px;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  text-align: center;
  width: 180px;
  max-width: 180px;
}

.logout-dialog h3 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 14px;
  font-weight: bold;
}

.logout-dialog p {
  margin: 0 0 16px 0;
  color: #666;
  font-size: 12px;
  line-height: 1.4;
}

.dialog-buttons {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.dialog-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: background-color 0.2s ease;
  flex: 1;
}

.dialog-btn.cancel {
  background: #f5f5f5;
  color: #666;
}

.dialog-btn.cancel:hover {
  background: #e0e0e0;
}

.dialog-btn.confirm {
  background: rgb(42, 65, 102);
  color: white;
}

.dialog-btn.confirm:hover {
  background: rgb(60, 85, 122);
}

.subtitle {
  font-size: 13px;
  color: #555;
  margin-bottom: 16px;
}

.btn {
  width: 80%;
  padding: 8px;
  margin: 6px 0;
  font-size: 14px;
  border: none;
  border-radius: 6px;
  background: rgb(42, 65, 102);
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn:hover,
.btn:focus {
  background: rgb(80, 110, 160);
}

.gif {
  width: 80%;
  max-height: 120px;
  object-fit: contain;
  margin-top: 30px;
}

/* 3D 模型容器樣式 */
.three-model-container {
  width: 90%;
  height: 150px;
  margin-top: 20px;
  position: relative;
  border-radius: 8px;
  overflow: hidden;
}

.loading-indicator {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #666;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #f3f3f3;
  border-top: 2px solid #2a4166;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.video {
  width: 80%;
  max-height: 120px;
  object-fit: contain;
  margin: 8px 0;
}

.level-container {
  width: 100%;
  text-align: center;
  margin-top: 16px;
  align-self: center;
  align-items: center;
  flex-direction: column;
  position: relative;
}

.level-label {
  font-size: 12px;
  font-weight: bold;
  color: #333;
}

.level-bar {
  width: 80%;
  height: 10px;
  background: #ddd;
  border-radius: 6px;
  margin: 6px 0;
  overflow: hidden;
  align-self: center;
  margin-left: 25px;
}

.level-progress {
  height: 100%;
  background: linear-gradient(to right, #2a4166, #5070a0);
  transition: width 0.3s ease;
}

.level-exp {
  font-size: 11px;
  color: #666;
}

/* 方向控制按鈕樣式 */
.direction-controls {
  position: absolute;
  right: 10px;
  top: 0%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0px;
}

.direction-btn {
  width: 18px;
  height: 18px;
  border: none;
  border-radius: 3px;
  background: transparent; /* 移除背景色 */
  color: rgb(42, 65, 102); /* 改為深藍色圖標 */
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.direction-btn:hover {
  background: rgba(42, 65, 102, 0.1); /* 懸停時淡淡的背景 */
  transform: scale(1.1);
}

.direction-btn:active {
  transform: scale(0.95);
  background: rgba(42, 65, 102, 0.2); /* 點擊時稍深的背景 */
}

.direction-btn .material-icons-round {
  font-size: 14px;
}
</style>
