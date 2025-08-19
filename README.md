# 🍎🍌 QuickDraw Apple vs Banana - Full Stack Integration

A full-stack AI-powered drawing game where users draw apples or bananas and a trained CNN model tries to recognize them in real-time.

## 🏗️ Architecture Overview

```
QuickDrawGame/
├── 🎨 frontend/           # React-like vanilla JS frontend
├── ⚙️ backend/            # FastAPI backend with ML model
├── 🤖 model_training/     # Jupyter notebook & trained models
├── 📋 requirements.txt    # Python dependencies
├── 🚀 start_server.py     # Easy server startup
└── 🧪 test_integration.py # Integration tests
```

## ✨ Features

- **Real-time Drawing Recognition**: Draw with mouse/touch, get instant AI feedback
- **Apple vs Banana Binary Classification**: Trained CNN model with 85%+ accuracy
- **Responsive Design**: Works on desktop and mobile devices
- **Detailed Results**: Shows confidence scores and analysis
- **Modern UI**: Beautiful gradient background with smooth animations

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Verify Model Training
Ensure your model is trained and saved in `model_training/model/`:
- `apple_banana_final_model.keras` (preferred)
- `apple_banana_final_model.h5` (fallback)

### 3. Test Integration
```bash
python test_integration.py
```

### 4. Start Server
```bash
python start_server.py
```

### 5. Play the Game!
Open your browser and go to: `http://localhost:8000/static/index.html`

## 🔧 Technical Details

### Backend (FastAPI)
- **Model Loading**: Automatic loading of Keras/TensorFlow model
- **Image Processing**: Converts drawing coordinates to 32x32 images
- **API Endpoints**: 
  - `/api/recognize-drawing` - Main prediction endpoint
  - `/api/random-object` - Get random apple/banana
  - `/api/model-info` - Model status and info
  - `/docs` - Interactive API documentation

### Frontend (Vanilla JS)
- **Canvas Drawing**: Smooth drawing with mouse/touch support
- **Real-time Feedback**: Instant recognition results
- **Mobile Responsive**: Touch-friendly interface
- **Error Handling**: Graceful handling of network/server issues

### Model Integration
- **Input Processing**: Drawing coordinates → 32x32 grayscale image
- **Normalization**: Pixel values normalized to [0,1] range
- **Prediction**: Binary classification with confidence scores
- **Output**: Detailed results with per-class probabilities

## 📊 Model Performance

Based on training results:
- **Test Accuracy**: ~64-85% (varies with dataset size)
- **Model Size**: ~100K parameters
- **Input**: 32x32x1 grayscale images
- **Classes**: Apple (🍎), Banana (🍌)

## 🎮 How to Play

1. **Start Game**: Click "🚀 Start Game"
2. **Draw**: You have 30 seconds to draw the requested object
3. **Results**: See what the AI thinks you drew!
4. **Play Again**: Try to improve your drawing skills

## 🛠️ Development

### Backend Development
```bash
cd backend
uvicorn app.main:app --reload
```

### Adding New Features

#### New Object Classes
1. Retrain model with additional classes in `train_apple_banana_model.ipynb`
2. Update `CLASS_LABELS` in `drawing_model.py`
3. Update frontend object selection logic

#### Improve Model Accuracy
1. Use full dataset instead of limited samples
2. Add data augmentation
3. Try the improved CNN architecture in the notebook

### API Endpoints

#### POST `/api/recognize-drawing`
```json
{
  "drawing": [{"x": 100, "y": 150}, ...],
  "object": "apple"
}
```

Response:
```json
{
  "success": true,
  "prediction": "apple",
  "confidence": 0.87,
  "apple_confidence": 0.87,
  "banana_confidence": 0.13,
  "is_correct": true,
  "message": "I think you drew an apple!"
}
```

#### GET `/api/random-object`
```json
{
  "success": true,
  "object": "banana",
  "emoji": "🍌"
}
```

## 🚨 Troubleshooting

### Common Issues

1. **Model Not Loading**
   - Check if model files exist in `model_training/model/`
   - Verify TensorFlow installation: `pip install tensorflow`

2. **CORS Errors**
   - Backend includes CORS middleware for all origins
   - If issues persist, check browser developer tools

3. **Drawing Not Recognized**
   - Draw clearly and fill more of the canvas
   - Ensure drawing has sufficient detail
   - Check model accuracy in training notebook

4. **Server Won't Start**
   - Install dependencies: `pip install -r requirements.txt`
   - Check port 8000 is available
   - Run from project root directory

### Development Tips

1. **Model Improvements**
   - Load full dataset in training notebook
   - Use data augmentation
   - Try improved CNN architecture

2. **Frontend Enhancements**
   - Add drawing hints/guides
   - Implement scoring system
   - Add sound effects

3. **Backend Optimizations**
   - Add model caching
   - Implement batch predictions
   - Add request rate limiting

## 📱 Mobile Support

The game is fully responsive and supports:
- Touch drawing on tablets/phones
- Responsive canvas sizing
- Mobile-friendly UI elements
- Touch event handling

## 🔮 Future Enhancements

- [ ] Add more object classes (fruits, animals, etc.)
- [ ] Implement user scoring system
- [ ] Add multiplayer functionality
- [ ] Progressive Web App (PWA) support
- [ ] Real-time collaborative drawing
- [ ] Drawing tutorials and hints

## 📄 License

This project is for educational and demonstration purposes. The QuickDraw dataset is provided by Google under their terms of service.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Happy Drawing! 🎨🍎🍌**
