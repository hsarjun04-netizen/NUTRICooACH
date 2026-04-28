#!/usr/bin/env python3
"""
Unified NutriCoach starter script
Handles frontend build and backend initialization in one command
"""
import os
import sys
import subprocess
import platform

def run_command(cmd, description):
    """Run a shell command and report status"""
    print(f"\n{'='*60}")
    print(f"▶ {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        print(f"✓ {description} - SUCCESS\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} - FAILED")
        print(f"Error: {e}\n")
        return False

def main():
    """Main execution flow"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("\n" + "="*60)
    print("🥗 NutriCoach AI - Unified Setup")
    print("="*60)
    
    # 1. Build frontend
    print("\n[1/4] Building Frontend...")
    if not run_command("npm run build", "Frontend Build"):
        print("⚠ Frontend build failed. Continuing with backend setup...")
    
    # 2. Setup backend environment
    print("\n[2/4] Setting up Backend...")
    if not run_command(
        f"{sys.executable} backend/init_db.py",
        "Initialize Database"
    ):
        print("⚠ Database initialization had issues")
    
    # 3. Seed recipes
    print("\n[3/4] Seeding Recipe Database...")
    if not run_command(
        f"{sys.executable} backend/seed_recipes.py",
        "Seed Recipes"
    ):
        print("⚠ Recipe seeding had issues")
    
    # 4. Start backend
    print("\n[4/4] Starting Backend Server...")
    print("="*60)
    print("✓ Setup Complete!")
    print("="*60)
    print("\n🚀 Starting NutriCoach on http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    
    run_command(
        f"{sys.executable} backend/wsgi.py",
        "Backend Server"
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 NutriCoach stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
