# ML Model Directory (`saved_models/`)

This directory is where you can place your trained Machine Learning model!

## Supported Model Formats:
- Scikit-Learn Pipeline / Estimator (`.pkl` or `.joblib`)
- XGBoost / LightGBM (`.joblib` or `.json` / `.model`)
- ONNX (`.onnx`)
- PyTorch / TensorFlow weights

## How to Connect Your Model:
1. Save your trained model:
   ```python
   import joblib
   joblib.dump(your_trained_model, "heart_model.joblib")
   ```
2. Place `heart_model.joblib` or `heart_model.pkl` in this folder:
   `backend/app/ml/saved_models/heart_model.pkl`

3. The backend automatically detects the model when it starts!
4. In `backend/app/ml/model_loader.py`, you can customize the input feature list if your model expects specific column ordering.
