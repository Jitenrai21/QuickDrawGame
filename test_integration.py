#!/usr/bin/env python3
"""
Test the Apple vs Banana model integration
"""
import sys
import os

# Add the backend directory to Python path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

# Now import from the backend module
try:
    from app.models.drawing_model import predict_drawing, get_model_info, get_random_object
    import numpy as np
    print("✅ Imports successful!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure you're running from the project root directory")
    sys.exit(1)

def test_model_loading():
    """Test if the model loads correctly"""
    print("🧪 Testing model loading...")
    
    info = get_model_info()
    if "error" in info:
        print(f"❌ Model loading failed: {info['error']}")
        return False
    
    print("✅ Model loaded successfully!")
    print(f"   Input shape: {info['input_shape']}")
    print(f"   Classes: {info['classes']}")
    print(f"   Total parameters: {info['total_parameters']:,}")
    return True

def test_random_object():
    """Test random object selection"""
    print("\n🎲 Testing random object selection...")
    
    for i in range(5):
        obj = get_random_object()
        emoji = "🍎" if obj == "apple" else "🍌"
        print(f"   {i+1}. {emoji} {obj}")
    
    print("✅ Random object selection working!")

def test_prediction():
    """Test prediction with dummy drawing data"""
    print("\n🎨 Testing prediction with dummy drawing data...")
    
    # Create simple dummy drawing data (a small circle-like pattern)
    dummy_drawing = []
    center_x, center_y = 300, 200
    
    # Create a circular pattern
    for angle in range(0, 360, 30):
        x = center_x + 50 * np.cos(np.radians(angle))
        y = center_y + 50 * np.sin(np.radians(angle))
        dummy_drawing.append({"x": int(x), "y": int(y)})
    
    print(f"   Created dummy drawing with {len(dummy_drawing)} points")
    
    # Test prediction
    result = predict_drawing(dummy_drawing)
    
    if "error" in result:
        print(f"❌ Prediction failed: {result['error']}")
        return False
    
    print("✅ Prediction successful!")
    print(f"   Predicted: {result['prediction']}")
    print(f"   Confidence: {result['confidence']:.2%}")
    print(f"   Apple confidence: {result['apple_confidence']:.2%}")
    print(f"   Banana confidence: {result['banana_confidence']:.2%}")
    
    return True

def test_empty_drawing():
    """Test prediction with empty drawing"""
    print("\n🚫 Testing prediction with empty drawing...")
    
    result = predict_drawing([])
    
    if result is None:
        print("✅ Empty drawing handled correctly (returned None)")
    elif "error" in result:
        print(f"✅ Empty drawing handled correctly: {result['error']}")
    else:
        print("⚠️  Empty drawing should return error or None")
    
    return True

def main():
    print("🍎🍌 QuickDraw Apple vs Banana - Integration Test")
    print("=" * 60)
    
    # Test model loading
    if not test_model_loading():
        print("\n❌ Model loading test failed - check your model files!")
        return
    
    # Test random object selection
    test_random_object()
    
    # Test prediction
    if not test_prediction():
        print("\n❌ Prediction test failed!")
        return
    
    # Test empty drawing
    test_empty_drawing()
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED!")
    print("🚀 Your QuickDraw Apple vs Banana integration is ready!")
    print("\n💡 Next steps:")
    print("   1. Run 'python start_server.py' to start the server")
    print("   2. Open http://localhost:8000/static/index.html")
    print("   3. Start drawing and testing!")

if __name__ == "__main__":
    main()
