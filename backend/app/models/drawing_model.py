import tensorflow as tf
import numpy as np
import os
from PIL import Image, ImageDraw
import io
import base64

# Get the absolute path to the model file
# Navigate from backend/app/models/ to project root, then to model_training/model/
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
MODEL_PATH = os.path.join(PROJECT_ROOT, 'model_training', 'model', 'apple_banana_final_model.keras')

# Load your trained Apple vs Banana model
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print(f"✅ Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    # Fallback to .h5 format
    MODEL_PATH_H5 = MODEL_PATH.replace('.keras', '.h5')
    try:
        model = tf.keras.models.load_model(MODEL_PATH_H5)
        print(f"✅ Model loaded successfully from {MODEL_PATH_H5}")
    except Exception as e2:
        print(f"❌ Error loading .h5 model: {e2}")
        model = None

# Class labels for Apple vs Banana model
CLASS_LABELS = ['apple', 'banana']

def predict_drawing(drawing_data):
    """
    Predict if the drawing is an apple or banana
    
    Args:
        drawing_data: List of coordinates [{x: int, y: int}]
    
    Returns:
        dict: Prediction results with confidence scores
    """
    if model is None:
        return {"error": "Model not loaded", "prediction": "unknown", "confidence": 0.0}
    
    try:
        # Convert drawing coordinates to 32x32 image
        processed_image = preprocess_drawing_to_image(drawing_data)
        
        if processed_image is None:
            return {"error": "Failed to process drawing", "prediction": "unknown", "confidence": 0.0}
        
        # Make prediction
        prediction_probs = model.predict(processed_image, verbose=0)
        predicted_class_idx = np.argmax(prediction_probs[0])
        confidence = float(prediction_probs[0][predicted_class_idx])
        predicted_label = CLASS_LABELS[predicted_class_idx]
        
        # Get confidence for both classes
        apple_confidence = float(prediction_probs[0][0])
        banana_confidence = float(prediction_probs[0][1])
        
        return {
            "prediction": predicted_label,
            "confidence": confidence,
            "apple_confidence": apple_confidence,
            "banana_confidence": banana_confidence,
            "all_probabilities": {
                "apple": apple_confidence,
                "banana": banana_confidence
            }
        }
        
    except Exception as e:
        print(f"❌ Error in prediction: {e}")
        return {"error": str(e), "prediction": "unknown", "confidence": 0.0}

def preprocess_drawing_to_image(drawing_data, canvas_size=(600, 400), target_size=(32, 32)):
    """
    Convert drawing coordinates to a 32x32 grayscale image for the model
    
    Args:
        drawing_data: List of coordinate points [{x: int, y: int}]
        canvas_size: Original canvas size (width, height)
        target_size: Target image size for model (32, 32)
    
    Returns:
        np.array: Preprocessed image ready for model prediction
    """
    try:
        if not drawing_data or len(drawing_data) == 0:
            return None
        
        # Create a white image (PIL uses RGB, white = 255)
        img = Image.new('L', canvas_size, color=255)  # 'L' for grayscale, white background
        draw = ImageDraw.Draw(img)
        
        # Draw lines connecting the points (black lines on white background)
        if len(drawing_data) > 1:
            for i in range(len(drawing_data) - 1):
                x1, y1 = int(drawing_data[i]['x']), int(drawing_data[i]['y'])  # Convert to int
                x2, y2 = int(drawing_data[i + 1]['x']), int(drawing_data[i + 1]['y'])  # Convert to int
                
                # Draw line with thickness
                draw.line([(x1, y1), (x2, y2)], fill=0, width=5)  # Black lines (0 = black)
        
        # Draw individual points for single clicks
        for point in drawing_data:
            x, y = int(point['x']), int(point['y'])  # Convert to int
            # Draw a small circle for single points
            draw.ellipse([(x-2, y-2), (x+2, y+2)], fill=0)
        
        # Resize to target size (32x32)
        img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
        
        # Convert to numpy array and normalize
        img_array = np.array(img_resized, dtype=np.float32)
        
        # Normalize pixel values to [0, 1] (model expects this)
        img_array = img_array / 255.0
        
        # Reshape for model input: (1, 32, 32, 1)
        img_array = img_array.reshape(1, target_size[0], target_size[1], 1)
        
        return img_array
        
    except Exception as e:
        print(f"❌ Error preprocessing drawing: {e}")
        return None

def get_random_object():
    """
    Get a random object for the user to draw (Apple or Banana)
    """
    import random
    return random.choice(CLASS_LABELS)

def get_model_info():
    """
    Get information about the loaded model
    """
    if model is None:
        return {"error": "Model not loaded"}
    
    try:
        return {
            "model_loaded": True,
            "input_shape": list(model.input_shape[1:]),
            "output_classes": len(CLASS_LABELS),
            "classes": CLASS_LABELS,
            "total_parameters": model.count_params()
        }
    except Exception as e:
        return {"error": str(e)}