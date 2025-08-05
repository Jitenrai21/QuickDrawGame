from fastapi import FastAPI
from app.routes.drawing import router as drawing_router

app = FastAPI()

# Include drawing-related routes
app.include_router(drawing_router)

# uvicorn app.main:app --reload