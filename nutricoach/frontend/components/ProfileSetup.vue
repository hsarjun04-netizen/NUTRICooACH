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
  background: #f5f5f5;
  min-height: 100vh;
  font-family: Arial, sans-serif;
}
.setup-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 600px;
}
h2 { text-align: center; color: #333; }
.subtitle { text-align: center; color: #777; margin-bottom: 24px; font-size: 0.9rem; }
.form-row { display: flex; gap: 16px; }
.form-row .form-group { flex: 1; }
.form-group { margin-bottom: 14px; }
label { display: block; margin-bottom: 4px; color: #555; font-size: 0.9rem; }
input, select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  box-sizing: border-box;
}
button {
  width: 100%;
  padding: 12px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 8px;
}
button:hover { background-color: #45a049; }
button:disabled { background-color: #a5d6a7; cursor: not-allowed; }
.error { color: #e53935; font-size: 0.9rem; margin: 8px 0; }
.success { color: #2e7d32; font-size: 0.9rem; margin: 12px 0; background: #e8f5e9; padding: 12px; border-radius: 6px; }
.checkbox-group { display: flex; flex-direction: column; gap: 8px; }
.checkbox-label { display: flex; align-items: center; gap: 8px; font-size: 0.95rem; color: #444; cursor: pointer; }
.checkbox-label input[type="checkbox"] { width: auto; }
</style>
