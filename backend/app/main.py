from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes.drawing import router as drawing_router
import os

# Create FastAPI app
app = FastAPI(
    title="QuickDraw Apple vs Banana API",
    description="AI-powered drawing recognition for apples and bananas",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include drawing-related routes
app.include_router(drawing_router)

# Serve static files (frontend)
# Navigate from backend/app/ up to project root, then to frontend/
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
frontend_path = os.path.join(PROJECT_ROOT, "frontend")

print(f"🔍 Checking frontend path: {frontend_path}")
print(f"📁 Frontend path exists: {os.path.exists(frontend_path)}")

if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")
    print(f"✅ Static files mounted from: {frontend_path}")
else:
    print(f"❌ Frontend directory not found at: {frontend_path}")
    # List available directories for debugging
    parent_dir = os.path.dirname(frontend_path)
    if os.path.exists(parent_dir):
        print(f"📋 Available directories in {parent_dir}:")
        for item in os.listdir(parent_dir):
            if os.path.isdir(os.path.join(parent_dir, item)):
                print(f"   📂 {item}")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to QuickDraw Apple vs Banana API!",
        "docs": "/docs", 
        "frontend": "/static/index.html",
        "game": "Open /static/index.html to play the game!"
    }

# Serve the game directly
@app.get("/game")
async def serve_game():
    """Redirect to the game"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/static/index.html")

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy", "service": "QuickDraw API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# To run: uvicorn app.main:app --reload