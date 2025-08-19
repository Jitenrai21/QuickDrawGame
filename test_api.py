#!/usr/bin/env python3
"""
Quick API test for the recognize-drawing endpoint
"""
import requests
import json

# Test data
test_data = {
    "drawing": [
        {"x": 100.0, "y": 100.0},
        {"x": 150.0, "y": 120.0},
        {"x": 200.0, "y": 100.0},
        {"x": 250.0, "y": 150.0},
        {"x": 200.0, "y": 200.0},
        {"x": 150.0, "y": 180.0},
        {"x": 100.0, "y": 200.0}
    ],
    "object": "apple"
}

def test_api():
    url = "http://127.0.0.1:8000/api/recognize-drawing"
    
    print("🧪 Testing API endpoint...")
    print(f"📡 URL: {url}")
    print(f"📊 Test data: {len(test_data['drawing'])} points")
    
    try:
        response = requests.post(url, json=test_data, timeout=10)
        
        print(f"📡 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API request successful!")
            print(f"🍎 Prediction: {result.get('prediction', 'N/A')}")
            print(f"📊 Confidence: {result.get('confidence', 0):.2%}")
            print(f"🎯 Expected: {result.get('expected_object', 'N/A')}")
            print(f"✅ Correct: {result.get('is_correct', False)}")
            return True
        else:
            print(f"❌ API request failed with status {response.status_code}")
            try:
                error_data = response.json()
                print(f"📄 Error response: {json.dumps(error_data, indent=2)}")
            except:
                print(f"📄 Raw response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🍎🍌 QuickDraw API Test")
    print("=" * 40)
    
    success = test_api()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 API test passed! The endpoint is working correctly.")
    else:
        print("❌ API test failed. Check the server logs for details.")
