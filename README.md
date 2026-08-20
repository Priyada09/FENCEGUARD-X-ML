# FENCEGUARD-X — Machine Learning
 
This repository contains the machine learning pipeline and prototype baselines developed for the FENCEGUARD-X / Parsuneth prototype, covering physical-tamper and electrical-fault analysis and detection.
 
## ML Contribution
 
This repository includes the following completed ML work:
 
- Session-aware preprocessing and feature extraction
- Physical-motion exploratory data analysis (EDA)
- Physical-tamper binary target preparation
- Decision Tree baseline for physical-tamper detection
- Electrical-fault baseline notebook (already present)
- Processed, model-ready datasets
- Reproducible Jupyter notebooks
## Physical-Tamper Prototype
 
- Current dataset: 43 rows across 3 sessions
- After target preparation: NORMAL = 35, PHYSICAL_TAMPER = 7
- 1 ELECTRICAL_FAULT row excluded from the physical-tamper target
- 8 motion features used
- Baseline model: Decision Tree (`max_depth=4`, `random_state=42`)
**Note:** The reported 100% result is **training-only performance**, not validation or test accuracy.
 
## Important Limitation
 
All 7 PHYSICAL_TAMPER examples come from a single experimental session. As a result, independent session-level generalization could not be evaluated. This work should be treated as a prototype / proof-of-concept — it does not represent a production-ready or validated-generalization model.
 
## Repository Structure
 
```
README.md
ml/
├── requirements.txt
├── dataset/
├── notebooks/
│   ├── 01_electrical_fault_baseline.ipynb
│   └── 02_physical_motion_eda_and_baseline.ipynb
└── preprocessing/
```
 
See `ml/README.md` for module-level details.
 
## Setup
 
Create a virtual environment and install dependencies:
 
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r ml/requirements.txt
```
 
## Running
 
The notebooks can be opened and run using Jupyter or VS Code:
 
```bash
jupyter notebook ml/notebooks/
```
 
Alternatively, open the `ml/notebooks/` folder directly in VS Code with the Jupyter extension.
 
Integration with the ESP32 device is a separate phase and is not part of this repository's current scope.
 
## Reproducibility
 
The physical-motion notebook (`02_physical_motion_eda_and_baseline.ipynb`) regenerates the processed physical-motion dataset from the repository's raw CSVs using `feature_pipeline.py`.
 
