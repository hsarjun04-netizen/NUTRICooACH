import axios from 'axios'

// Simple demo mode - use localStorage for auth when backend is unavailable
const useDemo = () => {
  const token = localStorage.getItem('token');
  return token && token.startsWith('demo_');
};

const demoApi = {
  // Demo user database
  getUsers: () => JSON.parse(localStorage.getItem('nutricoach_users') || '[]'),
  saveUsers: (users) => localStorage.setItem('nutricoach_users', JSON.stringify(users)),
  getSessions: () => JSON.parse(localStorage.getItem('nutricoach_sessions') || '{}'),
  saveSessions: (sessions) => localStorage.setItem('nutricoach_sessions', JSON.stringify(sessions)),
  
  generateToken: () => 'demo_' + Math.random().toString(36).substr(2) + Date.now(),
  delay: (ms = 300) => new Promise(r => setTimeout(r, ms)),

  async register(name, email, password) {
    await this.delay();
    const users = this.getUsers();
    if (users.find(u => u.email === email)) {
      throw { response: { data: { error: 'Email already registered' }, status: 409 } };
    }
    const newUser = {
      id: users.length + 1,
      name,
      email,
      password,
      created_at: new Date().toISOString()
    };
    users.push(newUser);
    this.saveUsers(users);
    
    const token = this.generateToken();
    const sessions = this.getSessions();
    sessions[token] = newUser.id;
    this.saveSessions(sessions);
    localStorage.setItem('token', token);
    localStorage.setItem('user_id', newUser.id);
    localStorage.setItem('user_name', newUser.name);
    
    return { data: { token, user_id: newUser.id } };
  },

  async login(email, password) {
    await this.delay();
    const users = this.getUsers();
    const user = users.find(u => u.email === email && u.password === password);
    if (!user) {
      throw { response: { data: { error: 'Invalid credentials' }, status: 401 } };
    }
    
    const token = this.generateToken();
    const sessions = this.getSessions();
    sessions[token] = user.id;
    this.saveSessions(sessions);
    localStorage.setItem('token', token);
    localStorage.setItem('user_id', user.id);
    localStorage.setItem('user_name', user.name);
    
    return { data: { token, user_id: user.id, name: user.name } };
  },

  async getMe() {
    await this.delay();
    const sessions = this.getSessions();
    const token = localStorage.getItem('token');
    const userId = sessions[token];
    const users = this.getUsers();
    const user = users.find(u => u.id === userId);
    if (!user) throw { response: { data: { error: 'Unauthorized' }, status: 401 } };
    return { data: user };
  },

  async getSummary() {
    await this.delay();
    return { 
      data: { 
        name: localStorage.getItem('user_name') || 'User',
        goal: 'Weight Loss',
        bmi: 24.5,
        bmr: 1650,
        target_calories: 2000,
        consumed_calories: 1450,
        remaining_calories: 550,
        latest_weight: 72.5,
        goal_progress_percent: 35,
        water_intake: 1500
      } 
    };
  },

  async getTodayMeals() {
    await this.delay();
    return { 
      data: { 
        meals: [
          { id: 1, name: 'Oatmeal with Berries', calories: 350, protein: 12, carbs: 58, fats: 8, meal_type: 'breakfast' },
          { id: 2, name: 'Grilled Chicken Salad', calories: 420, protein: 35, carbs: 18, fats: 22, meal_type: 'lunch' },
          { id: 3, name: 'Greek Yogurt', calories: 180, protein: 15, carbs: 22, fats: 3, meal_type: 'snack' }
        ], 
        total_calories: 1450 
      } 
    };
  },

  async getWater() {
    await this.delay();
    return { data: { total_ml: 1500, entries: 6 } };
  },

  async chat(message) {
    await this.delay();
    const msg = message.toLowerCase();
    let response = "I'm your NutriCoach AI assistant. I can help with nutrition advice, meal suggestions, calorie calculations, and health tips based on your profile.";
    
    if (msg.includes('hi') || msg.includes('hello')) response = `Hello! I'm your NutriCoach AI. How can I help you today?`;
    if (msg.includes('calorie')) response = `Your daily calorie target is approximately 2000 kcal based on your profile.`;
    if (msg.includes('protein')) response = `For your weight, aim for about 80g of protein daily. Good sources: eggs, chicken, lentils, and Greek yogurt.`;
    if (msg.includes('water')) response = `You should drink about 2500ml (10 glasses) of water daily. Stay hydrated!`;
    if (msg.includes('weight loss')) response = `For weight loss, aim for a 300-500 kcal deficit. Focus on high-protein, high-fiber foods.`;
    
    return { data: { response } };
  },

  async getChatHistory() {
    await this.delay();
    return { data: { messages: [] } };
  },

  async getCurrentMealPlan() {
    await this.delay();
    return { 
      data: { 
        meals: [
          { id: 1, name: 'Idli (2 pcs)', calories: 130, protein: 4, carbs: 26, fats: 0.5, meal_type: 'breakfast' },
          { id: 2, name: 'Rice and Dal', calories: 350, protein: 12, carbs: 60, fats: 6, meal_type: 'lunch' },
          { id: 3, name: 'Grilled Chicken with Salad', calories: 320, protein: 35, carbs: 10, fats: 16, meal_type: 'dinner' },
          { id: 4, name: 'Handful of Nuts', calories: 170, protein: 5, carbs: 6, fats: 15, meal_type: 'snack' }
        ], 
        total_calories: 970 
      } 
    };
  },

  async getWeightHistory() {
    await this.delay();
    return { 
      data: { 
        history: [
          { weight: 78, date: '2024-01-01' },
          { weight: 76, date: '2024-01-15' },
          { weight: 74, date: '2024-02-01' },
          { weight: 72.5, date: '2024-02-15' }
        ] 
      } 
    };
  },

  async post(url, data) {
    await this.delay();
    if (url.includes('/meals/log') || url.includes('/water/log') || url.includes('/weight/log')) {
      return { data: { success: true, message: 'Logged successfully' } };
    }
    return { data: { success: true } };
  },

  async put(url, data) {
    await this.delay();
    return { data: { message: 'Updated successfully' } };
  },

  isDemo: true
};

// Real API instance
const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add JWT token to requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token && !token.startsWith('demo_')) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle 401 errors
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user_id')
      localStorage.removeItem('user_name')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// ========== NEW API HELPERS ==========

// Recipes
export const getRecipes = (filters = {}) => {
  const params = new URLSearchParams()
  if (filters.diet_type) params.append('diet_type', filters.diet_type)
  if (filters.meal_type) params.append('meal_type', filters.meal_type)
  if (filters.max_calories) params.append('max_calories', filters.max_calories)
  
  return api.get(`/recipes?${params.toString()}`)
}

export const getRecipe = (id) => api.get(`/recipes/${id}`)

export const getRecipeSuggestions = () => api.get('/recipes/suggestions')

export const toggleRecipeFavorite = (id) => api.post(`/recipes/${id}/favorite`)

// Body Measurements
export const logMeasurement = (data) => api.post('/measurements/log', data)

export const getMeasurementsHistory = () => api.get('/measurements/history')

// Exercise
export const logExercise = (data) => api.post('/exercise/log', data)

export const getExerciseHistory = () => api.get('/exercise/history')

export const getTodayExercise = () => api.get('/exercise/today')

// Custom Goals
export const updateGoals = (data) => api.put('/users/goals', data)

export const getGoals = () => api.get('/users/goals')

// Export both - app will use demoApi when backend fails
export default api
export { demoApi }
