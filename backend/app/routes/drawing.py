from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.models.drawing_model import predict_drawing
from pydantic import BaseModel

# Define the drawing data structure
class DrawingData(BaseModel):
    drawing: list  # List of coordinates as a list of dictionaries [{x: int, y: int}]
    object: str     # The object that the user was supposed to draw

router = APIRouter()

# Route to handle the drawing and make predictions
@router.post("/api/recognize-drawing")
async def recognize_drawing(data: DrawingData):
    drawing = data.drawing
    object_to_draw = data.object
    
    if not drawing:
        return JSONResponse(status_code=400, content={"error": "No drawing data provided"})
    
    # Preprocess the drawing data (you can add your own preprocessing logic)
    processed_drawing = preprocess_drawing(drawing)
    
    # Get the prediction from the model
    prediction = predict_drawing(processed_drawing)
    
    # Return the prediction to the frontend
    return {"prediction": prediction, "expected_object": object_to_draw}

def preprocess_drawing(drawing):
    # Placeholder function: Preprocess the drawing (e.g., convert coordinates to image)
    # In a real case, this would include your image creation or normalization process
    return drawing
