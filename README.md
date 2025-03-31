# 🔥 FLAMES - Face & Hand Gesture Detection

A real-time interactive system that combines computer vision (OpenCV + MediaPipe) and PyGame visual effects to create flame and smoke animations triggered by hand gestures and facial expressions.

https://github.com/user-attachments/assets/6bb37ee2-064c-45c0-b641-38ccb5a696e6

## ✨ Key Features

### 👋 Hand Gesture Recognition
- Real-time detection of hand landmarks using MediaPipe
- Trigger flame effects when pointer finger is extended
- Gesture-controlled flame intensity (open/close hand to control fire)

### 😮 Face Expression Detection
- Blowing detection via facial landmark analysis
- Smoke effect activation when blowing is detected
- Adaptive particle system for realistic airflow simulation

### 🎨 PyGame Visual Effects
- Dynamic flame animation with 2D particle system
- Mouse-interactive debug mode for testing

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ (`python --version`)
- Webcam
  
### Installation
```bash
# Clone repository
git clone https://github.com/ElinaAizenberg/flames.git
cd flames

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 🖥 Usage
#### Main Application
```bash
python main.py
```
**How to use:**

- Position your hand in camera view

- Blow toward camera/finger to initiate flame

- Close fist to extinguish flame and to create smoke

#### Effect Testing (Debug Mode)

https://github.com/user-attachments/assets/cc77da08-24ec-470c-84ca-f480cf91e962

```bash
# Test flame effect standalone
python3 -c "from effects.flames import test_flame; test_flame()"

# Test smoke effect standalone
python3 -c "from effects.smoke import test_smoke; test_smoke()"
```

**Debug Controls:**

- Click: to initiate flame or smoke
- Mouse Wheel: Adjust flame particle count
