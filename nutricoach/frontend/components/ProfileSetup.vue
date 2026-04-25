<template>
  <div class="setup-page">
    <div class="setup-card">
      <h2>Set Up Your Profile</h2>
      <p class="subtitle">Tell us about yourself so we can personalize your plan</p>
      <form @submit.prevent="handleSubmit">
        <div class="form-row">
          <div class="form-group">
            <label>Age</label>
            <input type="number" v-model.number="form.age" required placeholder="25" min="10" max="120" />
          </div>
          <div class="form-group">
            <label>Gender</label>
            <select v-model="form.gender" required>
              <option value="">Select</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Height (cm)</label>
            <input type="number" v-model.number="form.height" required placeholder="170" min="100" max="250" />
          </div>
          <div class="form-group">
            <label>Weight (kg)</label>
            <input type="number" v-model.number="form.weight" required placeholder="70" min="30" max="300" />
          </div>
        </div>
        <div class="form-group">
          <label>Goal</label>
          <select v-model="form.goals" required>
            <option value="">Select your goal</option>
            <option value="weight-loss">Weight Loss</option>
            <option value="muscle-gain">Muscle Gain</option>
            <option value="maintenance">Maintenance</option>
          </select>
        </div>
        <div class="form-group">
          <label>Activity Level</label>
          <select v-model="form.activity_level" required>
            <option value="">Select</option>
            <option value="sedentary">Sedentary (little or no exercise)</option>
            <option value="lightly active">Lightly Active (1-3 days/week)</option>
            <option value="moderately active">Moderately Active (3-5 days/week)</option>
            <option value="very active">Very Active (6-7 days/week)</option>
            <option value="super active">Super Active (athlete level)</option>
          </select>
        </div>
        <div class="form-group">
          <label>Diet Type</label>
          <select v-model="form.diet_type" required>
            <option value="">Select</option>
            <option value="veg">Vegetarian</option>
            <option value="non-veg">Non-Vegetarian</option>
            <option value="vegan">Vegan</option>
          </select>
        </div>
        <div class="form-group">
          <label>Allergies (comma-separated)</label>
          <input type="text" v-model="form.allergies" placeholder="e.g., nuts, dairy, gluten" />
        </div>
        <div class="form-group">
          <label>Medical Conditions (check all that apply)</label>
          <div class="checkbox-group">
            <label class="checkbox-label"><input type="checkbox" value="diabetes" v-model="form.medical_conditions" /> Diabetes</label>
            <label class="checkbox-label"><input type="checkbox" value="high bp" v-model="form.medical_conditions" /> High Blood Pressure</label>
            <label class="checkbox-label"><input type="checkbox" value="high cholesterol" v-model="form.medical_conditions" /> High Cholesterol</label>
            <label class="checkbox-label"><input type="checkbox" value="pcos" v-model="form.medical_conditions" /> PCOS</label>
            <label class="checkbox-label"><input type="checkbox" value="thyroid" v-model="form.medical_conditions" /> Thyroid Issues</label>
            <label class="checkbox-label"><input type="checkbox" value="obesity" v-model="form.medical_conditions" /> Obesity</label>
            <label class="checkbox-label"><input type="checkbox" value="acid reflux" v-model="form.medical_conditions" /> Acid Reflux / GERD</label>
          </div>
        </div>
        <div class="form-group">
          <label>Budget Preference</label>
          <select v-model="form.budget">
            <option value="">Select</option>
            <option value="low">Low Budget</option>
            <option value="medium">Medium Budget</option>
            <option value="high">High Budget</option>
          </select>
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <p v-if="healthResult" class="success">
          BMI: {{ healthResult.bmi }} | BMR: {{ healthResult.bmr }} kcal | Target: {{ healthResult.target_calories }} kcal/day
        </p>
        <button type="submit" :disabled="loading">{{ loading ? 'Saving...' : 'Save Profile & Calculate' }}</button>
      </form>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '../src/stores/user'

export default {
  data() {
    return {
      form: {
        age: null, gender: '', height: null, weight: null,
        goals: '', activity_level: '', diet_type: 'veg',
        allergies: '', medical_conditions: [], budget: ''
      },
      healthResult: null,
      error: '',
      loading: false
    }
  },
  methods: {
    async handleSubmit() {
      this.loading = true
      this.error = ''
      try {
        const userStore = useUserStore()
        const payload = {
          ...this.form,
          medical_conditions: this.form.medical_conditions.join(', ')
        }
        await userStore.updateProfile(payload)
        this.healthResult = await userStore.calculateHealth()
        setTimeout(() => { this.$router.push('/dashboard') }, 2000)
      } catch (e) {
        this.error = e.response?.data?.error || 'Failed to save profile'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.setup-page {
  display: flex;
  justify-content: center;
  padding: 40px 20px;
  background: var(--bg-body);
  min-height: 100vh;
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  transition: background var(--transition-slow);
}
.setup-card {
  background: var(--bg-card);
  padding: 40px;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  width: 100%;
  max-width: 600px;
  border: 1px solid var(--border-color);
  transition: background var(--transition-slow), border-color var(--transition-slow), box-shadow var(--transition-slow);
  animation: cardSlideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) both;
}
@keyframes cardSlideUp {
  from { opacity: 0; transform: translateY(24px) scale(0.97); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
h2 { text-align: center; color: var(--text-primary); margin-bottom: 4px; }
.subtitle { text-align: center; color: var(--text-secondary); margin-bottom: 24px; font-size: 0.95rem; }
.form-row { display: flex; gap: 16px; }
.form-row .form-group { flex: 1; }
.form-group { margin-bottom: 16px; }
label { display: block; margin-bottom: 6px; color: var(--text-secondary); font-size: 0.9rem; font-weight: 500; }
input, select {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  font-size: 1rem;
  box-sizing: border-box;
  background: var(--bg-input);
  color: var(--text-primary);
  transition: all var(--transition-base);
}
input:focus, select:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(163, 230, 53, 0.15);
  transform: translateY(-1px);
}
input::placeholder { color: var(--text-muted); }
button {
  width: 100%;
  padding: 14px;
  background: var(--accent);
  color: #1e293b;
  border: none;
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 12px;
  transition: all var(--transition-base);
  position: relative;
  overflow: hidden;
}
button:hover:not(:disabled) {
  background: var(--accent-hover);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(163, 230, 53, 0.3);
}
button:active:not(:disabled) { transform: translateY(0) scale(0.98); }
button:disabled { background: var(--border-color); color: var(--text-muted); cursor: not-allowed; }
.error { color: #ef4444; font-size: 0.9rem; margin: 10px 0; }
.success {
  color: #22c55e;
  font-size: 0.9rem;
  margin: 14px 0;
  background: rgba(34, 197, 94, 0.1);
  padding: 14px;
  border-radius: var(--radius-md);
  border: 1px solid rgba(34, 197, 94, 0.2);
  animation: successPop 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
@keyframes successPop {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
.checkbox-group { display: flex; flex-direction: column; gap: 10px; }
.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.95rem;
  color: var(--text-primary);
  cursor: pointer;
  padding: 8px 10px;
  border-radius: var(--radius-sm);
  transition: background var(--transition-fast);
}
.checkbox-label:hover { background: var(--bg-hover); }
.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: var(--accent);
  cursor: pointer;
}
@media (max-width: 600px) {
  .setup-card { padding: 24px; }
  .form-row { flex-direction: column; gap: 0; }
}
</style>
