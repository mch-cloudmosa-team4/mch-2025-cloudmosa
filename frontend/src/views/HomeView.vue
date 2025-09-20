<template>
  <main class="screen">
    <div class="header">
      <h1 class="title">Hi, {{ name }} 👋</h1>
      <button class="settings-btn" @click="$router.push('/menu')">
        <span class="material-icons-round">settings</span>
      </button>
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
    </div>
  </main>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { isAuthed } from '../services/auth'
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'

const router = useRouter()
const name = localStorage.getItem('auth_name') || 'Guest'
const threeContainer = ref<HTMLElement>()
const loading = ref(true)

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

const initThreeJS = () => {
  if (!threeContainer.value) return

  // 場景
  scene = new THREE.Scene()
  scene.background = new THREE.Color(0xfdfdfd) // 與背景色一致

  // 相機 - 適合小容器的設置
  const aspect = threeContainer.value.clientWidth / threeContainer.value.clientHeight
  camera = new THREE.PerspectiveCamera(60, aspect, 0.1, 100)
  camera.position.set(0, 0.8, 3.5)

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
      pigModel.position.y += 0.7
      
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
  width: 80%;
  height: 120px;
  margin-top: 30px;
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
</style>
