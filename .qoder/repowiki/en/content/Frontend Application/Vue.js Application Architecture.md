# Vue.js Application Architecture

<cite>
**Referenced Files in This Document**
- [main.js](file://nutricoach/frontend/src/main.js)
- [App.vue](file://nutricoach/frontend/src/App.vue)
- [router.js](file://nutricoach/frontend/src/router.js)
- [auth.js](file://nutricoach/frontend/src/stores/auth.js)
- [user.js](file://nutricoach/frontend/src/stores/user.js)
- [api.js](file://nutricoach/frontend/src/api.js)
- [Login.vue](file://nutricoach/frontend/components/Login.vue)
- [Register.vue](file://nutricoach/frontend/components/Register.vue)
- [ProfileSetup.vue](file://nutricoach/frontend/components/ProfileSetup.vue)
- [MealPlan.vue](file://nutricoach/frontend/components/MealPlan.vue)
- [FoodTracker.vue](file://nutricoach/frontend/components/FoodTracker.vue)
- [index.html](file://nutricoach/frontend/index.html)
- [package.json](file://nutricoach/frontend/package.json)
- [vite.config.js](file://nutricoach/frontend/vite.config.js)
</cite>

## Update Summary
**Changes Made**
- Updated main.js to reflect Pinia state management integration
- Enhanced App.vue with navigation bar and computed properties
- Expanded router.js with comprehensive authentication guard system
- Added Pinia store architecture with auth and user management
- Integrated centralized API service with interceptors
- Added new components: Login, Register, ProfileSetup, MealPlan, FoodTracker
- Updated dependency structure to support Vue 3 ecosystem

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Architecture Overview](#architecture-overview)
5. [Detailed Component Analysis](#detailed-component-analysis)
6. [State Management with Pinia](#state-management-with-pinia)
7. [Enhanced Routing System](#enhanced-routing-system)
8. [Component Lifecycle Management](#component-lifecycle-management)
9. [Dependency Analysis](#dependency-analysis)
10. [Performance Considerations](#performance-considerations)
11. [Troubleshooting Guide](#troubleshooting-guide)
12. [Conclusion](#conclusion)

## Introduction
This document describes the Vue.js application architecture for NutriCoach AI, focusing on the major Vue 3 migration with Pinia state management, enhanced routing structure, and comprehensive component ecosystem. The application now features a robust authentication system, centralized state management, and modular component architecture designed for scalability and maintainability.

## Project Structure
The frontend has evolved into a comprehensive Vue 3 application with Pinia state management, featuring five distinct authentication and feature components alongside centralized services for API communication and state persistence.

```mermaid
graph TB
subgraph "Frontend Architecture"
HTML["index.html"]
MAIN["src/main.js<br/>Vue 3 + Pinia + Router"]
APP["src/App.vue<br/>Navigation + Layout"]
ROUTER["src/router.js<br/>Enhanced Routes + Guards"]
AUTHSTORE["src/stores/auth.js<br/>Authentication State"]
USERSTORE["src/stores/user.js<br/>User Profile State"]
API["src/api.js<br/>Centralized API Service"]
end
subgraph "Authentication Components"
LOGIN["components/Login.vue"]
REGISTER["components/Register.vue"]
PROFILE["components/ProfileSetup.vue"]
end
subgraph "Feature Components"
DASHBOARD["components/Dashboard.vue"]
MEALPLAN["components/MealPlan.vue"]
TRACKER["components/FoodTracker.vue"]
end
subgraph "Build & Dependencies"
PKG["package.json<br/>Vue 3 + Pinia + Router"]
VCFG["vite.config.js<br/>Development Server + Proxy"]
end
HTML --> MAIN
MAIN --> APP
MAIN --> ROUTER
MAIN --> AUTHSTORE
MAIN --> USERSTORE
APP --> ROUTER
ROUTER --> LOGIN
ROUTER --> REGISTER
ROUTER --> PROFILE
ROUTER --> DASHBOARD
ROUTER --> MEALPLAN
ROUTER --> TRACKER
AUTHSTORE --> API
USERSTORE --> API
LOGIN --> AUTHSTORE
REGISTER --> AUTHSTORE
PROFILE --> USERSTORE
MEALPLAN --> API
TRACKER --> API
PKG --> VCFG
```

**Diagram sources**
- [main.js:1-10](file://nutricoach/frontend/src/main.js#L1-L10)
- [App.vue:1-83](file://nutricoach/frontend/src/App.vue#L1-L83)
- [router.js:1-35](file://nutricoach/frontend/src/router.js#L1-L35)
- [auth.js:1-59](file://nutricoach/frontend/src/stores/auth.js#L1-L59)
- [user.js:1-40](file://nutricoach/frontend/src/stores/user.js#L1-L40)
- [api.js:1-33](file://nutricoach/frontend/src/api.js#L1-L33)
- [Login.vue:1-92](file://nutricoach/frontend/components/Login.vue#L1-L92)
- [Register.vue:1-96](file://nutricoach/frontend/components/Register.vue#L1-L96)
- [ProfileSetup.vue:1-184](file://nutricoach/frontend/components/ProfileSetup.vue#L1-L184)
- [MealPlan.vue:1-178](file://nutricoach/frontend/components/MealPlan.vue#L1-L178)
- [FoodTracker.vue:1-224](file://nutricoach/frontend/components/FoodTracker.vue#L1-L224)
- [package.json:1-22](file://nutricoach/frontend/package.json#L1-L22)
- [vite.config.js:1-17](file://nutricoach/frontend/vite.config.js#L1-L17)

**Section sources**
- [main.js:1-10](file://nutricoach/frontend/src/main.js#L1-L10)
- [App.vue:1-83](file://nutricoach/frontend/src/App.vue#L1-L83)
- [router.js:1-35](file://nutricoach/frontend/src/router.js#L1-L35)
- [package.json:1-22](file://nutricoach/frontend/package.json#L1-L22)
- [vite.config.js:1-17](file://nutricoach/frontend/vite.config.js#L1-L17)

## Core Components
This section documents the enhanced application bootstrap process, root component with navigation, and comprehensive routing configuration.

### Application Bootstrap and State Management
- **Vue 3 Application Creation**: The application is created using `createApp()` with the root component as the foundation.
- **Pinia Integration**: Pinia state management is initialized globally and provides centralized state management across all components.
- **Plugin Registration**: Both Pinia and Vue Router plugins are registered during application creation.
- **Mount Configuration**: The application mounts to the DOM element with id "app" as defined in the HTML structure.

**Updated** Enhanced with Pinia state management for centralized application state

**Section sources**
- [main.js:1-10](file://nutricoach/frontend/src/main.js#L1-L10)

### Root Component with Enhanced Navigation
- **Dynamic Navigation Bar**: The root component now includes a responsive navigation bar that appears on authenticated routes.
- **Back Navigation**: Implements intelligent back navigation with fallback to home route when history is empty.
- **Route-based Visibility**: Navigation bar visibility is controlled by computed properties based on current route path.
- **Global Styling**: Includes comprehensive CSS styling for responsive design and consistent user experience.

**Updated** Added navigation bar with computed visibility and back navigation functionality

**Section sources**
- [App.vue:1-83](file://nutricoach/frontend/src/App.vue#L1-L83)

### Comprehensive Routing Configuration
- **Enhanced Route Structure**: Expanded from a single route to seven distinct routes covering authentication, setup, and feature pages.
- **Authentication Guards**: Implements route guards using `requiresAuth` meta fields to protect authenticated routes.
- **Navigation Protection**: Prevents access to protected routes without valid authentication tokens.
- **History Mode**: Maintains browser history mode for clean URL structure and proper navigation semantics.

**Updated** Significantly expanded routing structure with authentication guards and comprehensive component coverage

**Section sources**
- [router.js:1-35](file://nutricoach/frontend/src/router.js#L1-L35)

## Architecture Overview
The application now follows a sophisticated client-side routing model with centralized state management and comprehensive authentication flows. The enhanced architecture supports user registration, authentication, profile setup, and feature-rich nutrition tracking capabilities.

```mermaid
sequenceDiagram
participant Browser as "Browser"
participant HTML as "index.html"
participant Main as "main.js"
participant App as "App.vue"
participant Router as "router.js"
participant AuthStore as "auth.js"
participant UserStore as "user.js"
participant API as "api.js"
participant Backend as "Backend API"
Browser->>HTML : Load page
HTML->>Main : Import and execute
Main->>App : Create Vue 3 app with root component
Main->>AuthStore : Initialize Pinia store
Main->>Router : Register router with guards
App->>Router : Render router-view
Router->>Login : Resolve route "/login"
Login->>AuthStore : Call login action
AuthStore->>API : POST /auth/login
API->>Backend : Forward request
Backend-->>API : Authentication response
API-->>AuthStore : Token + user data
AuthStore-->>Login : Success
Login-->>Router : Redirect to "/dashboard"
Router->>Dashboard : Render dashboard component
```

**Diagram sources**
- [index.html:1-14](file://nutricoach/frontend/index.html#L1-L14)
- [main.js:1-10](file://nutricoach/frontend/src/main.js#L1-L10)
- [App.vue:1-83](file://nutricoach/frontend/src/App.vue#L1-L83)
- [router.js:1-35](file://nutricoach/frontend/src/router.js#L1-L35)
- [auth.js:1-59](file://nutricoach/frontend/src/stores/auth.js#L1-L59)
- [api.js:1-33](file://nutricoach/frontend/src/api.js#L1-L33)

## Detailed Component Analysis

### Enhanced Application Bootstrap Process
- **Vue 3 Modern Features**: Utilizes modern Vue 3 features including Composition API patterns and enhanced reactivity.
- **State Management Integration**: Pinia provides reactive state management with persistent storage through localStorage integration.
- **Plugin Ecosystem**: Supports Vue Router for navigation and centralized API service for HTTP communication.
- **Development Workflow**: Vite provides fast development server with hot module replacement and proxy configuration.

**Updated** Migrated to Vue 3 with Pinia state management and enhanced development tooling

**Section sources**
- [main.js:1-10](file://nutricoach/frontend/src/main.js#L1-L10)
- [package.json:10-17](file://nutricoach/frontend/package.json#L10-L17)
- [vite.config.js:1-17](file://nutricoach/frontend/vite.config.js#L1-L17)

### Authentication Component Suite
- **Login Component**: Handles user authentication with form validation, error handling, and automatic redirection to dashboard.
- **Registration Component**: Manages user account creation with validation and automatic login flow.
- **Profile Setup Component**: Comprehensive health profile collection with medical conditions, dietary preferences, and goal setting.
- **Form Validation**: Implements comprehensive form validation with real-time feedback and error handling.

**Updated** Added complete authentication and profile management component suite

**Section sources**
- [Login.vue:1-92](file://nutricoach/frontend/components/Login.vue#L1-L92)
- [Register.vue:1-96](file://nutricoach/frontend/components/Register.vue#L1-L96)
- [ProfileSetup.vue:1-184](file://nutricoach/frontend/components/ProfileSetup.vue#L1-L184)

### Feature-Rich Component Library
- **Meal Plan Component**: Dynamic meal plan generation with safety warnings, medical condition tailoring, and macro nutrition display.
- **Food Tracker Component**: Comprehensive food logging system with daily summaries, calorie tracking, and weight monitoring.
- **Dashboard Component**: Central hub for user progress tracking and quick access to features.
- **Responsive Design**: Mobile-first approach with adaptive layouts and touch-friendly interfaces.

**Updated** Added comprehensive feature components for nutrition tracking and meal planning

**Section sources**
- [MealPlan.vue:1-178](file://nutricoach/frontend/components/MealPlan.vue#L1-L178)
- [FoodTracker.vue:1-224](file://nutricoach/frontend/components/FoodTracker.vue#L1-L224)

### Component Lifecycle Management
- **Mounted Hooks**: Components implement appropriate lifecycle hooks for data fetching and initialization.
- **Computed Properties**: Extensive use of computed properties for derived state and dynamic UI updates.
- **Event Handling**: Comprehensive event handling for user interactions and form submissions.
- **Error Boundaries**: Robust error handling with user-friendly error messages and graceful degradation.

**Updated** Enhanced with computed properties, lifecycle hooks, and comprehensive error handling

**Section sources**
- [Login.vue:25-44](file://nutricoach/frontend/components/Login.vue#L25-L44)
- [ProfileSetup.vue:95-131](file://nutricoach/frontend/components/ProfileSetup.vue#L95-L131)
- [FoodTracker.vue:85-160](file://nutricoach/frontend/components/FoodTracker.vue#L85-L160)

## State Management with Pinia
The application implements a comprehensive state management solution using Pinia, providing centralized control over authentication state, user profiles, and application-wide data.

### Authentication Store Architecture
- **State Persistence**: Authentication state persists across browser sessions using localStorage integration.
- **Token Management**: Automatic JWT token handling with interceptor configuration for secure API communication.
- **User Context**: Comprehensive user context management including profile data and authentication status.
- **Action Methods**: Asynchronous action methods for registration, login, user fetching, and logout operations.

### User Profile Store
- **Profile Management**: Centralized user profile data with update and fetch operations.
- **Health Calculations**: Integration with health calculation endpoints for personalized nutrition recommendations.
- **Dashboard Integration**: Provides dashboard summary data for real-time progress tracking.
- **Data Synchronization**: Automatic data synchronization between local state and backend services.

**Section sources**
- [auth.js:1-59](file://nutricoach/frontend/src/stores/auth.js#L1-L59)
- [user.js:1-40](file://nutricoach/frontend/src/stores/user.js#L1-L40)

## Enhanced Routing System
The routing system has been significantly expanded to support a comprehensive user journey from registration through feature utilization.

### Route Configuration Strategy
- **Authentication Flow**: Sequential routing from landing page through registration, profile setup, to authenticated dashboard.
- **Protected Routes**: Implementation of route guards protecting sensitive features like meal planning and food tracking.
- **Navigation Patterns**: Support for both programmatic navigation and user-driven routing through the interface.
- **Route Meta Fields**: Strategic use of meta fields for authentication requirements and route categorization.

### Navigation Guard Implementation
- **Token Validation**: Real-time token validation using localStorage for authentication state verification.
- **Redirect Logic**: Intelligent redirect logic for unauthenticated users attempting to access protected routes.
- **Guard Execution**: Pre-navigation guard execution ensuring security and proper user flow progression.

**Section sources**
- [router.js:10-35](file://nutricoach/frontend/src/router.js#L10-L35)
- [auth.js:16-56](file://nutricoach/frontend/src/stores/auth.js#L16-L56)

## Dependency Analysis
The application now leverages a modern Vue 3 ecosystem with comprehensive dependencies supporting state management, routing, and development workflows.

```mermaid
graph LR
Vue["vue@^3.4.0"] --> Main["main.js"]
Pinia["pinia@^2.1.0"] --> Main
Router["vue-router@^4.2.0"] --> Main
Axios["axios@^1.6.0"] --> API["api.js"]
ChartJS["chart.js@^4.4.0"] --> MealPlan["MealPlan.vue"]
VueChartJS["vue-chartjs@^5.3.0"] --> MealPlan
Vite["vite@^5.0.0"] --> VCfg["vite.config.js"]
VPlugin["@vitejs/plugin-vue@^4.5.0"] --> VCfg
Main --> App["App.vue"]
Main --> RouterCfg["router.js"]
RouterCfg --> Login["Login.vue"]
RouterCfg --> Register["Register.vue"]
RouterCfg --> Profile["ProfileSetup.vue"]
RouterCfg --> Dashboard["Dashboard.vue"]
RouterCfg --> MealPlan
RouterCfg --> Tracker["FoodTracker.vue"]
Login --> AuthStore["auth.js"]
Register --> AuthStore
Profile --> UserStore["user.js"]
MealPlan --> API
Tracker --> API
AuthStore --> API
UserStore --> API
```

**Diagram sources**
- [package.json:10-17](file://nutricoach/frontend/package.json#L10-L17)
- [main.js:1-10](file://nutricoach/frontend/src/main.js#L1-L10)
- [router.js:1-35](file://nutricoach/frontend/src/router.js#L1-L35)
- [auth.js:1-59](file://nutricoach/frontend/src/stores/auth.js#L1-L59)
- [user.js:1-40](file://nutricoach/frontend/src/stores/user.js#L1-L40)
- [api.js:1-33](file://nutricoach/frontend/src/api.js#L1-L33)
- [MealPlan.vue:1-178](file://nutricoach/frontend/components/MealPlan.vue#L1-L178)
- [vite.config.js:1-17](file://nutricoach/frontend/vite.config.js#L1-L17)

**Section sources**
- [package.json:1-22](file://nutricoach/frontend/package.json#L1-L22)
- [router.js:1-35](file://nutricoach/frontend/src/router.js#L1-L35)
- [auth.js:1-59](file://nutricoach/frontend/src/stores/auth.js#L1-L59)
- [user.js:1-40](file://nutricoach/frontend/src/stores/user.js#L1-L40)

## Performance Considerations
- **State Persistence**: Pinia stores utilize localStorage for state persistence, reducing redundant API calls on page reload.
- **Lazy Loading**: Route-based lazy loading can be implemented for larger components to optimize initial bundle size.
- **Component Optimization**: Individual component optimization through computed properties and efficient rendering strategies.
- **API Caching**: Centralized API service with request/response interceptors for improved network performance.
- **Chart Optimization**: Chart.js integration optimized for performance with selective data updates.

## Troubleshooting Guide
- **Authentication Issues**: Verify token persistence in localStorage and ensure API interceptors are properly configured.
- **Route Protection**: Check authentication guards and ensure token validation logic is functioning correctly.
- **State Management**: Monitor Pinia store state updates and localStorage synchronization for data consistency.
- **API Communication**: Verify baseURL configuration and proxy settings for proper backend communication.
- **Component Rendering**: Ensure proper component imports and route definitions for seamless navigation.

**Section sources**
- [router.js:25-32](file://nutricoach/frontend/src/router.js#L25-L32)
- [auth.js:16-56](file://nutricoach/frontend/src/stores/auth.js#L16-L56)
- [api.js:10-30](file://nutricoach/frontend/src/api.js#L10-L30)
- [vite.config.js:7-14](file://nutricoach/frontend/vite.config.js#L7-L14)

## Conclusion
NutriCoach AI has undergone a comprehensive Vue 3 migration featuring Pinia state management, enhanced routing architecture, and a complete component ecosystem. The application now provides a robust foundation for nutrition tracking, meal planning, and user profile management with centralized authentication and state management. The modern architecture supports scalability, maintainability, and enhanced user experience through responsive design and comprehensive feature coverage.