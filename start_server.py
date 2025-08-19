#!/usr/bin/env python3
"""
QuickDraw Apple vs Banana Server Startup Script
"""
import os
import sys
import subprocess
import time
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import tensorflow
        import PIL
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Please install dependencies with: pip install -r requirements.txt")
        return False

def check_model():
    """Check if the trained model exists"""
    model_path = Path("model_training/model/apple_banana_balanced_final.keras")
    model_path_h5 = Path("model_training/model/balanced_apple_banana_model.h5")
    
    if model_path.exists():
        print(f"✅ Model found: {model_path}")
        return True
    elif model_path_h5.exists():
        print(f"✅ Model found: {model_path_h5}")
        return True
    else:
        print("❌ Trained model not found!")
        print("🏗️  Please train the model first using the Jupyter notebook")
        return False

def start_server():
    """Start the FastAPI server"""
    print("\n🚀 Starting QuickDraw Apple vs Banana Server...")
    print("=" * 50)
    
    try:
        # Change to backend directory
        os.chdir("backend")
        
        # Start the server
        cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
        print(f"💻 Running command: {' '.join(cmd)}")
        print("\n🌐 Server will be available at:")
        print("   • Backend API: http://localhost:8000")
        print("   • API Docs: http://localhost:8000/docs")
        print("   • Frontend: http://localhost:8000/static/index.html")
        print("\n⏹️  Press Ctrl+C to stop the server")
        print("=" * 50)
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Make sure you're in the project root directory")
        print("   2. Check that all dependencies are installed")
        print("   3. Verify the model files exist")

def main():
    print("🍎🍌 QuickDraw Apple vs Banana - Server Startup")
    print("=" * 50)
    
    # Check current directory
    if not Path("backend").exists() or not Path("frontend").exists():
        print("❌ Please run this script from the project root directory")
        print("📁 Expected structure: backend/, frontend/, model_training/")
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check model
    if not check_model():
        return
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
