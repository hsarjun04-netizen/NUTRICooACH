<template>
  <div class="profile-layout">
    <!-- Dark Sidebar (consistent with Dashboard) -->
    <aside class="sidebar">
      <div class="sidebar-brand">.Diet</div>
      <nav class="sidebar-nav">
        <router-link v-for="item in navItems" :key="item.to" :to="item.to" class="nav-item" :class="{ active: $route.path === item.to }" :title="item.label">
          <span class="nav-icon" v-html="item.icon"></span>
          <span class="nav-label">{{ item.label }}</span>
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <a href="#" class="nav-item" @click.prevent="logout" title="Logout"><span class="nav-icon">&#128682;</span></a>
      </div>
    </aside>

    <main class="main-content">
      <!-- Skeleton Loading -->
      <div v-if="loading" class="skeleton-profile">
        <div class="skeleton-avatar"></div>
        <div class="skeleton-text" style="width:200px;height:28px"></div>
        <div class="skeleton-text" style="width:140px;height:16px"></div>
        <div class="skeleton-cards">
          <div class="skeleton-card"></div>
          <div class="skeleton-card"></div>
          <div class="skeleton-card"></div>
        </div>
      </div>

      <div v-else-if="profile" class="profile-animate">
        <!-- Profile Header -->
        <div class="profile-hero" :style="delayStyle(0)">
          <div class="hero-avatar">
            <span class="avatar-initial">{{ userInitial }}</span>
            <div class="avatar-status"></div>
          </div>
          <div class="hero-info">
            <h1>{{ profile.name || 'User' }}</h1>
            <p>{{ profile.email }}</p>
          </div>
          <div class="hero-actions">
            <button v-if="!editing" class="btn-primary ripple" @click="startEdit">
              <span>&#9998;</span> Edit Profile
            </button>
            <button v-else class="btn-secondary ripple" @click="cancelEdit">
              <span>&#10005;</span> Cancel
            </button>
          </div>
        </div>

        <!-- View Mode -->
        <div v-if="!editing" class="profile-cards">
          <div class="info-card" :style="delayStyle(0.1)">
            <div class="card-header">
              <span class="card-icon">&#128100;</span>
              <h3>Personal Information</h3>
            </div>
            <div class="info-rows">
              <div class="info-row" v-for="(item, i) in personalInfo" :key="i" :style="delayStyle(0.15 + i * 0.05)">
                <span class="info-label">{{ item.label }}</span>
                <span class="info-value">{{ item.value || '-' }}</span>
              </div>
            </div>
          </div>

          <div class="info-card" :style="delayStyle(0.2)">
            <div class="card-header">
              <span class="card-icon">&#127947;</span>
              <h3>Fitness & Diet</h3>
            </div>
            <div class="info-rows">
              <div class="info-row" v-for="(item, i) in fitnessInfo" :key="i" :style="delayStyle(0.25 + i * 0.05)">
                <span class="info-label">{{ item.label }}</span>
                <span class="info-value">{{ item.value || '-' }}</span>
              </div>
            </div>
          </div>

          <div class="info-card" :style="delayStyle(0.3)">
            <div class="card-header">
              <span class="card-icon">&#127973;</span>
              <h3>Health & Medical</h3>
            </div>
            <div class="info-rows">
              <div class="info-row" v-for="(item, i) in healthInfo" :key="i" :style="delayStyle(0.35 + i * 0.05)">
                <span class="info-label">{{ item.label }}</span>
                <span class="info-value">{{ item.value || '-' }}</span>
              </div>
            </div>
          </div>

          <div v-if="healthProfile" class="info-card health-card" :style="delayStyle(0.4)">
            <div class="card-header">
              <span class="card-icon">&#128170;</span>
              <h3>Health Metrics</h3>
            </div>
            <div class="metric-grid">
              <div class="metric" v-for="(m, i) in healthMetrics" :key="i" :style="delayStyle(0.45 + i * 0.08)">
                <span class="metric-value">{{ m.value }}</span>
                <span class="metric-label">{{ m.label }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Edit Mode -->
        <form v-else @submit.prevent="saveProfile" class="edit-form" :style="delayStyle(0.1)">
          <div class="form-card">
            <div class="card-header"><span class="card-icon">&#128100;</span><h3>Personal Information</h3></div>
            <div class="form-grid">
              <div class="form-group"><label>Name</label><input type="text" v-model="editForm.name" /></div>
              <div class="form-group"><label>Age</label><input type="number" v-model.number="editForm.age" min="10" max="120" /></div>
              <div class="form-group"><label>Gender</label>
                <select v-model="editForm.gender">
                  <option value="">Select</option><option value="male">Male</option><option value="female">Female</option>
                </select>
              </div>
              <div class="form-group"><label>Height (cm)</label><input type="number" v-model.number="editForm.height" min="100" max="250" /></div>
              <div class="form-group"><label>Weight (kg)</label><input type="number" v-model.number="editForm.weight" min="30" max="300" step="0.1" /></div>
            </div>
          </div>

          <div class="form-card">
            <div class="card-header"><span class="card-icon">&#127947;</span><h3>Fitness & Diet</h3></div>
            <div class="form-grid">
              <div class="form-group"><label>Goal</label>
                <select v-model="editForm.goals">
                  <option value="">Select</option><option value="weight-loss">Weight Loss</option><option value="muscle-gain">Muscle Gain</option><option value="maintenance">Maintenance</option>
                </select>
              </div>
              <div class="form-group"><label>Activity Level</label>
                <select v-model="editForm.activity_level">
                  <option value="">Select</option><option value="sedentary">Sedentary</option><option value="lightly active">Lightly Active</option><option value="moderately active">Moderately Active</option><option value="very active">Very Active</option><option value="super active">Super Active</option>
                </select>
              </div>
              <div class="form-group"><label>Diet Type</label>
                <select v-model="editForm.diet_type">
                  <option value="">Select</option><option value="veg">Vegetarian</option><option value="non-veg">Non-Vegetarian</option><option value="vegan">Vegan</option>
                </select>
              </div>
              <div class="form-group"><label>Budget</label>
                <select v-model="editForm.budget">
                  <option value="">Select</option><option value="low">Low</option><option value="medium">Medium</option><option value="high">High</option>
                </select>
              </div>
            </div>
          </div>

          <div class="form-card">
            <div class="card-header"><span class="card-icon">&#127973;</span><h3>Health & Medical</h3></div>
            <div class="form-grid">
              <div class="form-group full"><label>Allergies (comma-separated)</label><input type="text" v-model="editForm.allergies" placeholder="e.g., nuts, dairy" /></div>
              <div class="form-group full"><label>Medical Conditions (comma-separated)</label><input type="text" v-model="editForm.medical_conditions" placeholder="e.g., diabetes, high bp" /></div>
            </div>
          </div>

          <div class="form-card">
            <div class="card-header"><span class="card-icon">&#128274;</span><h3>Change Password</h3></div>
            <div class="form-grid">
              <div class="form-group full">
                <label>Current Password</label>
                <input type="password" v-model="passwordForm.currentPassword" placeholder="Enter current password" />
              </div>
              <div class="form-group">
                <label>New Password</label>
                <input type="password" v-model="passwordForm.newPassword" placeholder="Enter new password" />
              </div>
              <div class="form-group">
                <label>Confirm New Password</label>
                <input type="password" v-model="passwordForm.confirmPassword" placeholder="Confirm new password" />
              </div>
            </div>
            <p class="password-hint">&#128161; Password must be at least 6 characters long</p>
          </div>

          <div v-if="error" class="alert alert-error">{{ error }}</div>
          <div v-if="success" class="alert alert-success">{{ success }}</div>

          <div class="form-actions">
            <button type="submit" class="btn-primary ripple" :disabled="saving">
              <span v-if="saving" class="spinner"></span>
              <span v-else>&#10003;</span>
              {{ saving ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>

      <div v-else class="empty-state">
        <div class="empty-icon">&#128533;</div>
        <p>No profile data found.</p>
        <router-link to="/setup" class="btn-primary">Complete Your Profile</router-link>
      </div>
    </main>
  </div>
</template>

<script>
import { useUserStore } from '../src/stores/user'
import { useAuthStore } from '../src/stores/auth'

export default {
  data() {
    return {
      loading: true,
      editing: false,
      saving: false,
      error: '',
      success: '',
      profile: null,
      healthProfile: null,
      editForm: {},
      passwordForm: {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      },
      navItems: [
        { to: '/dashboard', icon: '&#127968;', label: 'Dashboard' },
        { to: '/meal-plan', icon: '&#128197;', label: 'Meal Plan' },
        { to: '/tracker', icon: '&#127860;', label: 'Food Tracker' },
        { to: '/recipes', icon: '&#127859;', label: 'Recipes' },
        { to: '/exercises', icon: '&#127939;', label: 'Exercise Tracker' },
        { to: '/progress', icon: '&#128200;', label: 'Progress' },
        { to: '/profile', icon: '&#9881;', label: 'Profile' }
      ]
    }
  },
  computed: {
    userInitial() {
      return (this.profile?.name || 'U').charAt(0).toUpperCase()
    },
    personalInfo() {
      const p = this.profile || {}
      return [
        { label: 'Name', value: p.name },
        { label: 'Email', value: p.email },
        { label: 'Age', value: p.age ? p.age + ' years' : null },
        { label: 'Gender', value: this.formatValue(p.gender) },
        { label: 'Height', value: p.height ? p.height + ' cm' : null },
        { label: 'Weight', value: p.weight ? p.weight + ' kg' : null }
      ]
    },
    fitnessInfo() {
      const p = this.profile || {}
      return [
        { label: 'Goal', value: this.formatValue(p.goals) },
        { label: 'Activity Level', value: this.formatValue(p.activity_level) },
        { label: 'Diet Type', value: this.formatValue(p.diet_type) },
        { label: 'Budget', value: this.formatValue(p.budget) }
      ]
    },
    healthInfo() {
      const p = this.profile || {}
      return [
        { label: 'Allergies', value: p.allergies || 'None' },
        { label: 'Medical Conditions', value: p.medical_conditions || 'None' }
      ]
    },
    healthMetrics() {
      const h = this.healthProfile || {}
      return [
        { label: 'BMI', value: h.bmi || '-' },
        { label: 'BMR', value: h.bmr ? h.bmr + ' kcal' : '-' },
        { label: 'TDEE', value: h.tdee ? h.tdee + ' kcal' : '-' },
        { label: 'Daily Target', value: h.target_calories ? h.target_calories + ' kcal' : '-' }
      ]
    }
  },
  async mounted() {
    await this.loadProfile()
  },
  methods: {
    async loadProfile() {
      this.loading = true
      try {
        const userStore = useUserStore()
        await userStore.fetchProfile()
        await userStore.fetchHealthProfile()
        this.profile = userStore.profile
        this.healthProfile = userStore.healthProfile
      } catch (e) {
        console.error('Failed to load profile:', e)
      } finally {
        this.loading = false
      }
    },
    startEdit() {
      this.editForm = { ...this.profile }
      this.editing = true
      this.error = ''
      this.success = ''
      this.resetPasswordForm()
    },
    async saveProfile() {
      this.saving = true
      this.error = ''
      this.success = ''
      
      try {
        // Validate password if any password field is filled
        if (this.passwordForm.currentPassword || this.passwordForm.newPassword || this.passwordForm.confirmPassword) {
          // Check if all password fields are filled
          if (!this.passwordForm.currentPassword || !this.passwordForm.newPassword || !this.passwordForm.confirmPassword) {
            this.error = 'Please fill in all password fields'
            this.saving = false
            return
          }
          
          // Check password length
          if (this.passwordForm.newPassword.length < 6) {
            this.error = 'New password must be at least 6 characters long'
            this.saving = false
            return
          }
          
          // Check if passwords match
          if (this.passwordForm.newPassword !== this.passwordForm.confirmPassword) {
            this.error = 'New passwords do not match'
            this.saving = false
            return
          }
          
          // Check if new password is same as current
          if (this.passwordForm.currentPassword === this.passwordForm.newPassword) {
            this.error = 'New password must be different from current password'
            this.saving = false
            return
          }
        }
        
        // Save profile changes
        const userStore = useUserStore()
        await userStore.updateProfile(this.editForm)
        this.profile = { ...this.profile, ...this.editForm }
        this.success = 'Profile saved successfully!'

        const shouldRecalc = ['weight', 'age', 'height', 'gender', 'activity_level'].some(
          key => this.editForm[key] !== this.profile[key]
        )
        if (shouldRecalc) {
          this.healthProfile = await userStore.calculateHealth()
          this.success += ' Health metrics recalculated.'
        }
        
        // Change password if provided
        if (this.passwordForm.currentPassword && this.passwordForm.newPassword) {
          await this.changePassword()
          this.success += ' Password updated.'
        }

        setTimeout(() => { 
          this.editing = false
          this.success = ''
          this.resetPasswordForm()
        }, 2000)
      } catch (e) {
        this.error = e.response?.data?.error || 'Failed to save profile'
      } finally {
        this.saving = false
      }
    },
    formatValue(val) {
      if (!val) return ''
      return val.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
    },
    delayStyle(seconds) {
      return { animationDelay: seconds + 's' }
    },
    logout() {
      const auth = useAuthStore()
      auth.logout()
      this.$router.push('/login')
    },
    async changePassword() {
      const api = (await import('../src/api')).default
      const response = await api.put('/users/change-password', {
        current_password: this.passwordForm.currentPassword,
        new_password: this.passwordForm.newPassword
      })
      return response.data
    },
    resetPasswordForm() {
      this.passwordForm = {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    },
    cancelEdit() {
      this.editing = false
      this.error = ''
      this.success = ''
      this.resetPasswordForm()
    }
  }
}
</script>

<style scoped>
/* ===== LAYOUT ===== */
.profile-layout { display: flex; min-height: 100vh; background: var(--bg-body); transition: background var(--transition-slow); }

/* ===== SIDEBAR ===== */
.sidebar {
  width: 200px; background: var(--bg-sidebar);
  display: flex; flex-direction: column; align-items: stretch;
  padding: 20px 0; flex-shrink: 0;
  border-radius: 0 20px 20px 0; margin: 12px 0 12px 0;
  transition: background var(--transition-slow);
}
.sidebar-brand { color: var(--text-muted); font-size: 0.75rem; font-weight: 700; margin-bottom: 32px; letter-spacing: 1px; }
.sidebar-nav { display: flex; flex-direction: column; gap: 8px; flex: 1; }
.sidebar-footer { margin-top: auto; padding-top: 16px; }
.nav-item {
  height: 44px;
  display: flex; align-items: center; gap: 12px;
  padding: 0 16px;
  border-radius: 12px; color: var(--text-muted);
  text-decoration: none; font-size: 0.9rem;
  transition: all var(--transition-base);
  position: relative;
  margin: 0 8px;
}
.nav-item::before { content: ''; position: absolute; inset: 0; border-radius: 12px; background: var(--accent); opacity: 0; transform: scale(0.8); transition: all var(--transition-base); z-index: 0; }
.nav-item:hover, .nav-item.active { color: #1e293b; transform: scale(1.1); }
.nav-item:hover::before, .nav-item.active::before { opacity: 1; transform: scale(1); }
.nav-item:hover { box-shadow: 0 0 16px rgba(163, 230, 53, 0.4); }
.nav-icon { position: relative; z-index: 1; font-size: 1.2rem; }
.nav-label { position: relative; z-index: 1; font-weight: 500; }

/* ===== MAIN ===== */
.main-content { flex: 1; padding: 32px; max-width: 900px; }

/* ===== SKELETON ===== */
.skeleton-profile { padding: 20px 0; }
.skeleton-avatar { width: 80px; height: 80px; border-radius: 50%; margin-bottom: 16px; }
.skeleton-text, .skeleton-avatar, .skeleton-card {
  background: linear-gradient(90deg, var(--border-color) 25%, var(--bg-hover) 50%, var(--border-color) 75%);
  background-size: 200% 100%; animation: shimmer 1.5s infinite; border-radius: 12px;
}
.skeleton-cards { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 24px; }
.skeleton-card { height: 200px; border-radius: var(--radius-lg); }
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

/* ===== ANIMATIONS ===== */
.profile-animate > * { animation: fadeInUp 0.5s ease-out both; }
@keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

/* ===== PROFILE HERO ===== */
.profile-hero {
  display: flex; align-items: center; gap: 20px;
  margin-bottom: 28px; padding: 24px;
  background: var(--bg-card); border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm); transition: all var(--transition-slow);
}
.profile-hero:hover { box-shadow: var(--shadow-md); }
.hero-avatar { position: relative; width: 72px; height: 72px; flex-shrink: 0; }
.avatar-initial {
  width: 72px; height: 72px; border-radius: 50%;
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.8rem; font-weight: 800; color: white;
  box-shadow: 0 4px 16px rgba(79, 172, 254, 0.3);
  animation: popIn 0.5s ease-out both;
}
.avatar-status { position: absolute; bottom: 4px; right: 4px; width: 16px; height: 16px; background: #22c55e; border-radius: 50%; border: 3px solid var(--bg-card); transition: border-color var(--transition-slow); }
.hero-info { flex: 1; }
.hero-info h1 { margin: 0; font-size: 1.4rem; color: var(--text-primary); font-weight: 700; transition: color var(--transition-slow); }
.hero-info p { margin: 4px 0 0 0; color: var(--text-muted); font-size: 0.85rem; transition: color var(--transition-slow); }
.hero-actions { display: flex; gap: 10px; }

/* ===== BUTTONS ===== */
.btn-primary, .btn-secondary {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 20px; border-radius: var(--radius-sm);
  font-size: 0.9rem; font-weight: 600; cursor: pointer;
  border: none; transition: all var(--transition-base);
}
.btn-primary { background: var(--text-primary); color: var(--bg-card); }
.btn-primary:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }
.btn-primary:active { transform: translateY(0); }
.btn-secondary { background: var(--bg-hover); color: var(--text-primary); border: 1px solid var(--border-color); }
.btn-secondary:hover { background: var(--border-color); }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }

/* ===== CARDS ===== */
.profile-cards { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.info-card {
  background: var(--bg-card); border-radius: var(--radius-lg); padding: 24px;
  box-shadow: var(--shadow-sm); transition: all var(--transition-slow);
  animation: fadeInUp 0.5s ease-out both;
}
.info-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); }
.card-header { display: flex; align-items: center; gap: 10px; margin-bottom: 16px; }
.card-icon { font-size: 1.3rem; }
.card-header h3 { margin: 0; font-size: 1rem; color: var(--text-primary); font-weight: 700; transition: color var(--transition-slow); }
.info-rows { display: flex; flex-direction: column; gap: 10px; }
.info-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 10px 12px; background: var(--bg-hover); border-radius: var(--radius-sm);
  transition: all var(--transition-base);
}
.info-row:hover { transform: translateX(3px); }
.info-label { font-size: 0.8rem; color: var(--text-muted); transition: color var(--transition-slow); }
.info-value { font-size: 0.85rem; color: var(--text-primary); font-weight: 600; transition: color var(--transition-slow); }

/* Health Card */
.health-card { grid-column: 1 / -1; }
.metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.metric {
  text-align: center; padding: 16px;
  background: linear-gradient(135deg, #dcfce7, #bbf7d0);
  border-radius: var(--radius-md); animation: popIn 0.4s ease-out both;
}
.metric-value { display: block; font-size: 1.2rem; font-weight: 800; color: #166534; }
.metric-label { font-size: 0.7rem; color: #15803d; font-weight: 600; margin-top: 4px; display: block; }

/* ===== EDIT FORM ===== */
.edit-form { display: flex; flex-direction: column; gap: 20px; }
.form-card {
  background: var(--bg-card); border-radius: var(--radius-lg); padding: 24px;
  box-shadow: var(--shadow-sm); transition: all var(--transition-slow);
  animation: fadeInUp 0.5s ease-out both;
}
.form-card:hover { box-shadow: var(--shadow-md); }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group.full { grid-column: 1 / -1; }
.form-group label { font-size: 0.8rem; color: var(--text-secondary); font-weight: 500; transition: color var(--transition-slow); }
.form-group input, .form-group select {
  padding: 12px 14px; border: 1px solid var(--border-color); border-radius: var(--radius-sm);
  background: var(--bg-input); color: var(--text-primary); font-size: 0.9rem;
  transition: all var(--transition-base);
}
.form-group input:focus, .form-group select:focus {
  border-color: var(--accent); box-shadow: 0 0 0 3px rgba(163, 230, 53, 0.15);
  outline: none;
}
.form-actions { display: flex; justify-content: flex-end; }

.password-hint {
  margin: 10px 0 0 0;
  font-size: 0.8rem;
  color: var(--text-muted);
  font-style: italic;
  transition: color var(--transition-slow);
}

/* ===== ALERTS ===== */
.alert { padding: 12px 16px; border-radius: var(--radius-sm); font-size: 0.85rem; font-weight: 500; animation: fadeInUp 0.3s ease-out; }
.alert-error { background: #fef2f2; color: #dc2626; }
.alert-success { background: #f0fdf4; color: #16a34a; }

/* ===== SPINNER ===== */
.spinner { display: inline-block; width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* ===== EMPTY ===== */
.empty-state { text-align: center; padding: 80px 20px; color: var(--text-muted); }
.empty-icon { font-size: 3rem; margin-bottom: 12px; }
.empty-state p { margin-bottom: 20px; }

/* Ripple */
.ripple { position: relative; overflow: hidden; }
.ripple::after { content: ''; position: absolute; width: 100%; height: 100%; top: 0; left: 0; pointer-events: none; background-image: radial-gradient(circle, rgba(255,255,255,0.3) 10%, transparent 10.01%); background-repeat: no-repeat; background-position: 50%; transform: scale(10, 10); opacity: 0; transition: transform 0.5s, opacity 1s; }
.ripple:active::after { transform: scale(0, 0); opacity: 0.3; transition: 0s; }

@keyframes popIn { from { opacity: 0; transform: scale(0.5); } to { opacity: 1; transform: scale(1); } }

@media (max-width: 800px) {
  .profile-cards { grid-template-columns: 1fr; }
  .metric-grid { grid-template-columns: repeat(2, 1fr); }
  .form-grid { grid-template-columns: 1fr; }
  .sidebar { width: 52px; }
  .profile-hero { flex-direction: column; text-align: center; }
}
</style>
