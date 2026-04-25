<template>
  <div class="shopping-list">
    <aside class="sidebar">
      <div class="sidebar-brand">.Diet</div>
      <nav class="sidebar-nav">
        <router-link v-for="item in navItems" :key="item.to" :to="item.to" class="nav-item" :class="{ active: $route.path === item.to }" :title="item.label">
          <span class="nav-icon" v-html="item.icon"></span>
          <span class="nav-label">{{ item.label }}</span>
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <a href="#" class="nav-item" @click.prevent="logout" title="Logout">
          <span class="nav-icon">&#128682;</span>
        </a>
      </div>
    </aside>

    <main class="main-content">
      <header class="page-header">
        <h1>&#128722; Shopping List</h1>
        <p class="subtitle">Your grocery essentials for healthy meal prep</p>
      </header>

      <div class="actions-bar">
        <button class="btn-primary" @click="generateList" :disabled="generating">
          {{ generating ? '&#8987; Generating...' : '&#10024; Generate from Meal Plan' }}
        </button>
        <button class="btn-danger" @click="clearList" :disabled="items.length === 0">
          &#128465; Clear List
        </button>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading shopping list...</p>
      </div>

      <div v-else-if="items.length === 0" class="empty-state">
        <div class="empty-icon">&#128722;</div>
        <h3>No items in your shopping list</h3>
        <p>Generate a shopping list from your meal plan or add items manually</p>
        <button class="btn-primary" @click="generateList">Generate Now</button>
      </div>

      <div v-else class="shopping-content">
        <!-- Category Groups -->
        <div v-for="(categoryItems, category) in groupedItems" :key="category" class="category-section">
          <h2 class="category-title">{{ getCategoryIcon(category) }} {{ category }}</h2>
          <div class="items-grid">
            <div v-for="item in categoryItems" :key="item.id" class="item-card" :class="{ purchased: item.is_purchased }">
              <div class="item-checkbox" @click="toggleItem(item)">
                <span v-if="item.is_purchased" class="checkmark">&#10003;</span>
              </div>
              <div class="item-details">
                <h3>{{ item.item_name }}</h3>
                <p class="item-quantity">{{ item.quantity }} {{ item.unit }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Summary -->
        <div class="summary-card">
          <h3>&#128202; Shopping Summary</h3>
          <div class="summary-stats">
            <div class="summary-item">
              <span class="summary-label">Total Items</span>
              <span class="summary-value">{{ items.length }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Purchased</span>
              <span class="summary-value purchased">{{ purchasedCount }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Remaining</span>
              <span class="summary-value remaining">{{ items.length - purchasedCount }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">Progress</span>
              <span class="summary-value">{{ Math.round((purchasedCount / items.length) * 100) }}%</span>
            </div>
          </div>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: `${(purchasedCount / items.length) * 100}%` }"></div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../src/stores/auth'
import { useThemeStore } from '../src/stores/theme'
import { generateShoppingList, getShoppingList, toggleShoppingItem, clearShoppingList as clearListApi } from '../src/api'

const router = useRouter()
const auth = useAuthStore()
const theme = useThemeStore()

const items = ref([])
const loading = ref(false)
const generating = ref(false)

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: '&#127968;' },
  { to: '/meal-plan', label: 'Meal Plan', icon: '&#128197;' },
  { to: '/tracker', label: 'Food Tracker', icon: '&#127859;' },
  { to: '/recipes', label: 'Recipes', icon: '&#128214;' },
  { to: '/shopping-list', label: 'Shopping List', icon: '&#128722;' },
  { to: '/exercises', label: 'Exercise Tracker', icon: '&#127939;' },
  { to: '/progress', label: 'Progress', icon: '&#128200;' },
  { to: '/profile', label: 'Profile', icon: '&#9881;' }
]

const groupedItems = computed(() => {
  const groups = {}
  items.value.forEach(item => {
    const category = item.category || 'Other'
    if (!groups[category]) {
      groups[category] = []
    }
    groups[category].push(item)
  })
  return groups
})

const purchasedCount = computed(() => {
  return items.value.filter(item => item.is_purchased).length
})

const logout = () => {
  auth.logout()
  router.push('/login')
}

const loadList = async () => {
  loading.value = true
  try {
    const response = await getShoppingList()
    items.value = response.data.items
  } catch (error) {
    console.error('Failed to load shopping list:', error)
  } finally {
    loading.value = false
  }
}

const generateList = async () => {
  generating.value = true
  try {
    await generateShoppingList()
    await loadList()
  } catch (error) {
    console.error('Failed to generate shopping list:', error)
    alert('Make sure you have a meal plan generated for today')
  } finally {
    generating.value = false
  }
}

const toggleItem = async (item) => {
  try {
    const response = await toggleShoppingItem(item.id)
    item.is_purchased = response.data.is_purchased
  } catch (error) {
    console.error('Failed to toggle item:', error)
  }
}

const clearList = async () => {
  if (!confirm('Are you sure you want to clear your shopping list?')) {
    return
  }
  
  try {
    await clearListApi()
    items.value = []
  } catch (error) {
    console.error('Failed to clear shopping list:', error)
  }
}

const getCategoryIcon = (category) => {
  const icons = {
    'Protein': '&#129370;',
    'Dairy': '&#129385;',
    'Grains': '&#127838;',
    'Vegetables': '&#129388;',
    'Fruits': '&#127827;',
    'Other': '&#128722;'
  }
  return icons[category] || '&#128722;'
}

onMounted(() => {
  loadList()
})
</script>

<style scoped>
.shopping-list {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 200px;
  background: #1a1a2e;
  color: #fff;
  display: flex;
  flex-direction: column;
  padding: 20px 0;
  position: fixed;
  height: 100vh;
  left: 0;
  top: 0;
}

.sidebar-brand {
  font-size: 24px;
  font-weight: bold;
  padding: 0 20px;
  margin-bottom: 30px;
  color: #16c79a;
}

.sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  color: #8b8b9e;
  text-decoration: none;
  transition: all 0.3s;
  border-left: 3px solid transparent;
}

.nav-item:hover,
.nav-item.active {
  background: #16213e;
  color: #16c79a;
  border-left-color: #16c79a;
}

.nav-icon {
  font-size: 20px;
}

.nav-label {
  font-size: 14px;
  font-weight: 500;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid #16213e;
}

.main-content {
  flex: 1;
  margin-left: 200px;
  padding: 30px;
  background: #f8f9fa;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 32px;
  color: #1a1a2e;
  margin-bottom: 8px;
}

.subtitle {
  color: #8b8b9e;
  font-size: 16px;
}

.actions-bar {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
}

.btn-primary {
  padding: 12px 24px;
  background: #16c79a;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-primary:hover:not(:disabled) {
  background: #13b386;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-danger {
  padding: 12px 24px;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-danger:hover:not(:disabled) {
  background: #c0392b;
}

.btn-danger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.category-section {
  margin-bottom: 30px;
}

.category-title {
  font-size: 24px;
  color: #1a1a2e;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 2px solid #16c79a;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
}

.item-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s;
}

.item-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.item-card.purchased {
  opacity: 0.6;
  background: #f0f0f0;
}

.item-checkbox {
  width: 24px;
  height: 24px;
  border: 2px solid #16c79a;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.checkmark {
  color: #16c79a;
  font-weight: bold;
  font-size: 16px;
}

.item-details {
  flex: 1;
}

.item-details h3 {
  font-size: 16px;
  color: #1a1a2e;
  margin-bottom: 5px;
}

.item-quantity {
  font-size: 14px;
  color: #8b8b9e;
}

.summary-card {
  background: white;
  padding: 30px;
  border-radius: 12px;
  margin-top: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.summary-card h3 {
  font-size: 20px;
  color: #1a1a2e;
  margin-bottom: 20px;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.summary-item {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
}

.summary-label {
  display: block;
  font-size: 12px;
  color: #8b8b9e;
  margin-bottom: 5px;
}

.summary-value {
  display: block;
  font-size: 24px;
  font-weight: bold;
  color: #1a1a2e;
}

.summary-value.purchased {
  color: #16c79a;
}

.summary-value.remaining {
  color: #e74c3c;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #16c79a, #13b386);
  transition: width 0.3s;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f0f0f0;
  border-top-color: #16c79a;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.empty-state h3 {
  font-size: 24px;
  color: #1a1a2e;
  margin-bottom: 10px;
}

.empty-state p {
  color: #8b8b9e;
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .sidebar {
    width: 64px;
  }
  
  .nav-label {
    display: none;
  }
  
  .main-content {
    margin-left: 64px;
    padding: 20px;
  }
  
  .actions-bar {
    flex-direction: column;
  }
  
  .items-grid {
    grid-template-columns: 1fr;
  }
  
  .summary-stats {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
