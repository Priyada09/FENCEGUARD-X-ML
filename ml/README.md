# ML README

## Overview
FENCEGUARD-X ML pipeline handles dataset preparation, model training, evaluation, and deployment to ESP32.

## Quick Start

### Prerequisites
- Python 3.9+
- Jupyter Notebook (for exploration)
- pip packages: pandas, numpy, scikit-learn, tensorflow

### Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter
jupyter notebook notebooks/
```

## ML Directory Structure

```
ml/
├─ dataset/
│  ├─ raw/               # Original sensor data
│  ├─ processed/         # Cleaned, feature-engineered
│  └─ splits/            # Train/test/val splits
│
├─ notebooks/
│  ├─ 01_data_exploration.ipynb      # EDA
│  ├─ 02_feature_engineering.ipynb   # Feature creation
│  ├─ 03_model_training.ipynb        # Training & tuning
│  ├─ 04_model_evaluation.ipynb      # Performance analysis
│  └─ 05_model_conversion.ipynb      # TFLite export
│
├─ models/
│  ├─ baseline.pkl                   # Scikit-learn model
│  ├─ model_v1.tflite               # TensorFlow Lite (for ESP32)
│  └─ model_metadata.json           # Model info
│
├─ training/
│  ├─ train.py                       # Training script
│  ├─ evaluate.py                    # Evaluation metrics
│  ├─ convert_tflite.py             # Model conversion
│  └─ config.yaml                    # Training config
│
├─ requirements.txt
└─ README.md
```

## Dataset Preparation

### Data Collection & Schema

Raw experimental telemetry captured by ESP32:

```csv
timestamp_ms,zone1_v,zone2_v,zone3_v,bus_voltage_v,current_ma,power_mw,ax,ay,az,gx,gy,gz,label
```

### Feature Engineering

```
Input Features:
├─ zone1_v, zone2_v, zone3_v  # 3-Zone electrical voltages
├─ bus_voltage_v, current_ma  # INA219 power telemetry
├─ power_mw                   # Calculated power (V x I)
├─ ax, ay, az                 # MPU6050 Accelerometer raw outputs
├─ gx, gy, gz                 # MPU6050 Gyroscope raw outputs
├─ accel_magnitude, gyro_mag  # Derived 3D motion magnitudes
├─ delta_accel, delta_gyro    # Derived temporal motion changes
└─ rolling_std_accel/gyro     # Derived windowed variance

Target Classes:
├─ NORMAL
├─ ELECTRICAL_FAULT
├─ PHYSICAL_TAMPER
```

## Model Training

### Option 1: Random Forest (Recommended for SIH)

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)
rf_model.fit(X_train, y_train)

# Evaluate
score = rf_model.score(X_test, y_test)
print(f"Accuracy: {score:.2%}")
```

### Option 2: Neural Network (TensorFlow)

```python
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation='relu', input_shape=(6,)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(X_train, y_train_onehot, epochs=50, batch_size=32)
```

## Model Conversion to TensorFlow Lite

```python
# Convert trained model to TFLite
converter = tf.lite.TFLiteConverter.from_saved_model("saved_model_path")
converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS
]
converter.optimizations = [tf.lite.Optimize.DEFAULT]  # Quantization
tflite_model = converter.convert()

# Save for ESP32
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)
```

## Model Evaluation

### Performance Metrics
```bash
# Run evaluation
python training/evaluate.py --model models/model_v1.tflite

# Output:
# Accuracy:    0.94 (94% correct predictions)
# Precision:   0.92 (false alarms suppressed)
# Recall:      0.91 (misses minimized)
# F1-Score:    0.91 (balanced performance)
```

### Confusion Matrix
```
              Predicted
             N  A  C
Actual  N   95  4  1
        A    2 88  4
        C    0  3 95

N=NORMAL, A=ALERT, C=CRITICAL
```

### ROC Curve
- AUC: 0.97 (excellent discrimination)
- Threshold tuned for False Positive Rate < 5%

## Deployment to ESP32

### Step 1: Verify Model Size
```bash
# Model must fit in ESP32 flash (~4MB available)
ls -lh models/model_v1.tflite
# Expected: <1MB for fast inference
```

### Step 2: Generate C Header
```bash
# Convert .tflite to hexdump
python -c "
import binascii
with open('model.tflite', 'rb') as f:
    data = f.read()
print(f'// Model size: {len(data)} bytes')
print('const unsigned char model_data[] = {')
for i in range(0, len(data), 16):
    hex_vals = ', '.join(f'0x{b:02x}' for b in data[i:i+16])
    print(f'  {hex_vals},')
print('};')
" > models/model.h
```

### Step 3: Copy to Firmware
```bash
cp models/model.h firmware/esp32/
# Include in ml_model.cpp: #include "model.h"
```

### Step 4: Validate on Device
```bash
# Upload firmware and monitor
platformio run --target upload
platformio device monitor

# Look for:
# [INFO] Model loaded: 524288 bytes
# [INFO] Inference time: 45ms
```

## Retraining & Updating

### Regular Model Updates (Monthly)
```bash
# Collect new data from deployed systems
python training/collect_new_data.py --from-backend

# Retrain with combined dataset
python training/train.py --dataset dataset/combined/ --epochs 50

# Evaluate performance
python training/evaluate.py

# If performance improved: Deploy new model
# If degraded: Keep previous version (rollback)
```

### A/B Testing
```
Version 1 (deployed): 94% accuracy
Version 2 (new): 95% accuracy
├─ Deploy to 10% of devices (canary)
├─ Monitor false alarm rate
└─ If OK: Roll out to 100%
```

## Performance Optimization

### Latency
- Model size: <1 MB
- Quantization: INT8 (4× smaller)
- Inference: <50ms on ESP32

### Accuracy
- Target: >85% overall
- False Positive: <5%
- False Negative: <10%

### Resource Usage
- RAM during inference: <50 KB
- Flash storage: ~4 MB available

## Notebooks Overview

### 1. Data Exploration (01_data_exploration.ipynb)
- Load sensor data
- Statistical summaries
- Visualize distributions
- Identify patterns

### 2. Feature Engineering (02_feature_engineering.ipynb)
- Create time-domain features
- Normalize/standardize
- Feature selection
- Visualization

### 3. Model Training (03_model_training.ipynb)
- Train multiple models
- Hyperparameter tuning
- Cross-validation
- Model comparison

### 4. Model Evaluation (04_model_evaluation.ipynb)
- Confusion matrix
- ROC/AUC curves
- Precision/Recall
- Threshold optimization

### 5. Model Conversion (05_model_conversion.ipynb)
- Convert to TFLite
- Quantization verification
- Size/latency check
- Generate C header

## Testing the Model

```bash
# Unit tests
pytest training/tests/ -v

# Integration test (with firmware)
python training/integration_test.py --device /dev/ttyUSB0

# Expected output:
# PASS: Inference produces valid class
# PASS: Latency <100ms
# PASS: False alarm rate <5%
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Model accuracy low | Collect more diverse data, retrain |
| Model too slow | Reduce complexity, quantize more |
| TFLite conversion fails | Check model architecture, simplify |
| ESP32 RAM overflow | Reduce batch size, use lighter model |
| False alarms high | Adjust threshold, add more NORMAL samples |

## Next Steps

1. [Review Firmware Setup](../firmware/README.md)
2. [Configure Backend](../backend/README.md)
3. [Deploy to Dashboard](../dashboard/README.md)

---

**Contact**: Priyada (ML Lead)
**Last Updated**: 14 August 2026
