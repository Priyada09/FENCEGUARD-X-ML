"""Physical-tamper live inference package for FENCEGUARD-X (Task 2).

Wires together, without duplicating any existing logic:

- the existing MQTT payload shape (payload_adapter.py maps it to the raw
  sample dict expected by the feature pipeline)
- the existing, unmodified LiveMotionFeatureExtractor from
  ml.preprocessing.feature_pipeline, one instance per sensorId
  (session_manager.py)
- the existing, unmodified trained physical_tamper_model.joblib
  (physical_predictor.py)

Scope (Task 2 only):
- Locally callable Python component. No MQTT connection, no HTTP/API
  endpoint (FastAPI/Flask), no backend integration, no electrical
  inference. Those are explicitly out of scope until a later task.
"""