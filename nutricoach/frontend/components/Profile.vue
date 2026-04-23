<template>
  <div class="profile-page">
    <div class="profile-card">
      <div class="profile-header">
        <h2>My Profile</h2>
        <button v-if="!editing" class="edit-btn" @click="startEdit">Edit Profile</button>
        <button v-else class="cancel-btn" @click="cancelEdit">Cancel</button>
      </div>

      <div v-if="loading" class="loading">Loading profile...</div>

      <div v-else-if="profile">
        <!-- View Mode -->
        <div v-if="!editing" class="view-mode">
          <div class="info-section">
            <h3>Personal Information</h3>
            <div class="info-grid">
              <div class="info-item"><span class="label">Name</span><span class="value">{{ profile.name || '-' }}</span></div>
              <div class="info-item"><span class="label">Email</span><span class="value">{{ profile.email || '-' }}</span></div>
              <div class="info-item"><span class="label">Age</span><span class="value">{{ profile.age || '-' }}</span></div>
              <div class="info-item"><span class="label">Gender</span><span class="value">{{ profile.gender || '-' }}</span></div>
              <div class="info-item"><span class="label">Height</span><span class="value">{{ profile.height ? profile.height + ' cm' : '-' }}</span></div>
              <div class="info-item"><span class="label">Weight</span><span class="value">{{ profile.weight ? profile.weight + ' kg' : '-' }}</span></div>
            </div>
          </div>

          <div class="info-section">
            <h3>Fitness & Diet Goals</h3>
            <div class="info-grid">
              <div class="info-item"><span class="label">Goal</span><span class="value">{{ formatValue(profile.goals) || '-' }}</span></div>
              <div class="info-item"><span class="label">Activity Level</span><span class="value">{{ formatValue(profile.activity_level) || '-' }}</span></div>
              <div class="info-item"><span class="label">Diet Type</span><span class="value">{{ formatValue(profile.diet_type) || '-' }}</span></div>
              <div class="info-item"><span class="label">Budget</span><span class="value">{{ formatValue(profile.budget) || '-' }}</span></div>
            </div>
          </div>

          <div class="info-section">
            <h3>Health & Medical</h3>
            <div class="info-grid">
              <div class="info-item"><span class="label">Allergies</span><span class="value">{{ profile.allergies || 'None' }}</span></div>
              <div class="info-item"><span class="label">Medical Conditions</span><span class="value">{{ profile.medical_conditions || 'None' }}</span></div>
            </div>
          </div>

          <div v-if="healthProfile" class="info-section health-section">
            <h3>Health Calculations</h3>
            <div class="info-grid">
              <div class="info-item"><span class="label">BMI</span><span class="value highlight">{{ healthProfile.bmi || '-' }}</span></div>
              <div class="info-item"><span class="label">BMR</span><span class="value highlight">{{ healthProfile.bmr ? healthProfile.bmr + ' kcal' : '-' }}</span></div>
              <div class="info-item"><span class="label">TDEE</span><span class="value highlight">{{ healthProfile.tdee ? healthProfile.tdee + ' kcal' : '-' }}</span></div>
              <div class="info-item"><span class="label">Daily Target</span><span class="value highlight">{{ healthProfile.target_calories ? healthProfile.target_calories + ' kcal' : '-' }}</span></div>
            </div>
          </div>
        </div>

        <!-- Edit Mode -->
        <form v-else @submit.prevent="saveProfile" class="edit-mode">
          <div class="form-section">
            <h3>Personal Information</h3>
            <div class="form-row">
              <div class="form-group"><label>Name</label><input type="text" v-model="editForm.name" /></div>
              <div class="form-group"><label>Age</label><input type="number" v-model.number="editForm.age" min="10" max="120" /></div>
            </div>
            <div class="form-row">
              <div class="form-group"><label>Gender</label>
                <select v-model="editForm.gender">
                  <option value="">Select</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                </select>
              </div>
              <div class="form-group"><label>Height (cm)</label><input type="number" v-model.number="editForm.height" min="100" max="250" /></div>
            </div>
            <div class="form-row">
              <div class="form-group"><label>Weight (kg)</label><input type="number" v-model.number="editForm.weight" min="30" max="300" step="0.1" /></div>
            </div>
          </div>

          <div class="form-section">
            <h3>Fitness & Diet Goals</h3>
            <div class="form-row">
              <div class="form-group"><label>Goal</label>
                <select v-model="editForm.goals">
                  <option value="">Select</option>
                  <option value="weight-loss">Weight Loss</option>
                  <option value="muscle-gain">Muscle Gain</option>
                  <option value="maintenance">Maintenance</option>
                </select>
              </div>
              <div class="form-group"><label>Activity Level</label>
                <select v-model="editForm.activity_level">
                  <option value="">Select</option>
                  <option value="sedentary">Sedentary</option>
                  <option value="lightly active">Lightly Active</option>
                  <option value="moderately active">Moderately Active</option>
                  <option value="very active">Very Active</option>
                  <option value="super active">Super Active</option>
                </select>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group"><label>Diet Type</label>
                <select v-model="editForm.diet_type">
                  <option value="">Select</option>
                  <option value="veg">Vegetarian</option>
                  <option value="non-veg">Non-Vegetarian</option>
                  <option value="vegan">Vegan</option>
                </select>
              </div>
              <div class="form-group"><label>Budget</label>
                <select v-model="editForm.budget">
                  <option value="">Select</option>
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
            </div>
          </div>

          <div class="form-section">
            <h3>Health & Medical</h3>
            <div class="form-group"><label>Allergies (comma-separated)</label><input type="text" v-model="editForm.allergies" placeholder="e.g., nuts, dairy" /></div>
            <div class="form-group"><label>Medical Conditions (comma-separated)</label><input type="text" v-model="editForm.medical_conditions" placeholder="e.g., diabetes, high bp" /></div>
          </div>

          <p v-if="error" class="error">{{ error }}</p>
          <p v-if="success" class="success">{{ success }}</p>

          <div class="form-actions">
            <button type="submit" :disabled="saving">{{ saving ? 'Saving...' : 'Save Changes' }}</button>
          </div>
        </form>
      </div>

      <div v-else class="empty">
        <p>No profile data found.</p>
        <router-link to="/setup" class="setup-link">Complete Your Profile</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '../src/stores/user'

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
      editForm: {}
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
    },
    cancelEdit() {
      this.editing = false
      this.error = ''
      this.success = ''
    },
    async saveProfile() {
      this.saving = true
      this.error = ''
      this.success = ''
      try {
        const userStore = useUserStore()
        await userStore.updateProfile(this.editForm)
        this.profile = { ...this.profile, ...this.editForm }
        this.success = 'Profile saved successfully!'

        // Recalculate health if weight/age/height/gender/activity changed
        const shouldRecalc = ['weight', 'age', 'height', 'gender', 'activity_level'].some(
          key => this.editForm[key] !== this.profile[key]
        )
        if (shouldRecalc) {
          this.healthProfile = await userStore.calculateHealth()
          this.success += ' Health metrics recalculated.'
        }

        setTimeout(() => { this.editing = false }, 1500)
      } catch (e) {
        this.error = e.response?.data?.error || 'Failed to save profile'
      } finally {
        this.saving = false
      }
    },
    formatValue(val) {
      if (!val) return ''
      return val.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
    }
  }
}
</script>

<style scoped>
.profile-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 30px 20px;
  font-family: Arial, sans-serif;
}
.profile-card {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}
.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  border-bottom: 1px solid #eee;
  padding-bottom: 16px;
}
h2 { margin: 0; color: #333; }
.edit-btn, .cancel-btn {
  padding: 8px 20px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
}
.edit-btn { background: #4CAF50; color: white; }
.edit-btn:hover { background: #45a049; }
.cancel-btn { background: #e0e0e0; color: #555; }
.cancel-btn:hover { background: #d0d0d0; }

.info-section { margin-bottom: 24px; }
h3 { color: #444; font-size: 1rem; margin: 0 0 12px 0; padding-bottom: 6px; border-bottom: 2px solid #e8f5e9; }
.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.info-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 12px;
  background: #f9f9f9;
  border-radius: 6px;
}
.info-item .label { color: #888; font-size: 0.85rem; }
.info-item .value { color: #333; font-weight: 500; font-size: 0.9rem; }
.info-item .value.highlight { color: #2e7d32; font-weight: bold; }

.health-section h3 { border-bottom-color: #c8e6c9; }

.form-section { margin-bottom: 20px; }
.form-row { display: flex; gap: 16px; }
.form-row .form-group { flex: 1; }
.form-group { margin-bottom: 12px; }
.form-group label { display: block; margin-bottom: 4px; color: #555; font-size: 0.85rem; }
.form-group input, .form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.95rem;
  box-sizing: border-box;
}
.form-actions { margin-top: 16px; }
.form-actions button {
  width: 100%;
  padding: 12px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
}
.form-actions button:hover { background: #45a049; }
.form-actions button:disabled { background: #a5d6a7; cursor: not-allowed; }

.error { color: #e53935; background: #ffebee; padding: 10px; border-radius: 6px; margin: 12px 0; }
.success { color: #2e7d32; background: #e8f5e9; padding: 10px; border-radius: 6px; margin: 12px 0; }

.empty { text-align: center; padding: 40px; color: #999; }
.setup-link {
  display: inline-block;
  margin-top: 12px;
  padding: 10px 24px;
  background: #4CAF50;
  color: white;
  border-radius: 6px;
  text-decoration: none;
}
.loading { text-align: center; padding: 40px; color: #999; }

@media (max-width: 600px) {
  .info-grid { grid-template-columns: 1fr; }
  .form-row { flex-direction: column; gap: 0; }
}
</style>
