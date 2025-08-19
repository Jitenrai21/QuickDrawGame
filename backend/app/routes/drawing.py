from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.models.drawing_model import predict_drawing, get_random_object, get_model_info
from pydantic import BaseModel
from typing import List, Dict

# Define the drawing data structure
class DrawingData(BaseModel):
    drawing: List[Dict[str, float]]  # List of coordinates [{"x": float, "y": float}] - changed to float
    object: str     # The object that the user was supposed to draw

class CoordinatePoint(BaseModel):
    x: float  # Changed to float to handle decimal coordinates
    y: float  # Changed to float to handle decimal coordinates

router = APIRouter()

# Route to handle the drawing and make predictions
@router.post("/api/recognize-drawing")
async def recognize_drawing(data: DrawingData):
    """
    Recognize if a drawing is an apple or banana
    """
    try:
        drawing = data.drawing
        object_to_draw = data.object
        
        print(f"🔍 Received drawing request:")
        print(f"   Object: {object_to_draw}")
        print(f"   Drawing points: {len(drawing)}")
        print(f"   Sample points: {drawing[:3] if len(drawing) >= 3 else drawing}")
        
        if not drawing:
            print("❌ No drawing data provided")
            return JSONResponse(status_code=400, content={"error": "No drawing data provided"})
        
        # Get the prediction from the model
        prediction_result = predict_drawing(drawing)
        
        print(f"🤖 Prediction result: {prediction_result}")
        
        # Check if there was an error in prediction
        if "error" in prediction_result:
            print(f"❌ Prediction error: {prediction_result['error']}")
            return JSONResponse(
                status_code=500, 
                content={
                    "error": prediction_result["error"],
                    "prediction": "unknown",
                    "expected_object": object_to_draw
                }
            )
        
        # Calculate if the prediction is correct
        predicted_object = prediction_result["prediction"]
        is_correct = predicted_object.lower() == object_to_draw.lower()
        
        print(f"✅ Returning successful prediction: {predicted_object}")
        
        # Return comprehensive prediction results
        return {
            "success": True,
            "prediction": predicted_object,
            "expected_object": object_to_draw,
            "is_correct": is_correct,
            "confidence": prediction_result["confidence"],
            "apple_confidence": prediction_result.get("apple_confidence", 0),
            "banana_confidence": prediction_result.get("banana_confidence", 0),
            "all_probabilities": prediction_result.get("all_probabilities", {}),
            "message": f"I think you drew a {predicted_object}!" if prediction_result["confidence"] > 0.7 else f"I'm not sure, but I think it might be a {predicted_object}."
        }
        
    except Exception as e:
        print(f"❌ Server error in recognize_drawing: {str(e)}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500, 
            content={
                "error": f"Server error: {str(e)}",
                "prediction": "unknown",
                "expected_object": data.object if data else "unknown"
            }
        )

# Route to get a random object to draw
@router.get("/api/random-object")
async def get_random_drawing_object():
    """
    Get a random object for the user to draw (Apple or Banana)
    """
    try:
        random_object = get_random_object()
        return {
            "success": True,
            "object": random_object,
            "emoji": "🍎" if random_object == "apple" else "🍌"
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Server error: {str(e)}", "object": "apple"}
        )

# Route to check model status
@router.get("/api/model-info")
async def model_info():
    """
    Get information about the loaded model
    """
    try:
        info = get_model_info()
        return info
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Server error: {str(e)}"}
        )

# Health check endpoint
@router.get("/api/health")
async def health_check():
    """
    Simple health check for the API
    """
    return {
        "status": "healthy",
        "message": "Apple vs Banana QuickDraw API is running!",
        "version": "1.0.0"
    }
