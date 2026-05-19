"""
Secure script to upload SavedModel to Hugging Face Model Hub.

Usage:
  1. Create a model repo on HF: https://huggingface.co/new (choose "Model")
  2. Set environment variables:
     export HF_TOKEN="hf_your_token_here"
     export MODEL_REPO_ID="your-username/ecommerce-churn-model"
  3. Run: python upload_model_to_hub.py

The script will upload the latest SavedModel from serving_model/rfahrur6045-pipeline/
"""

import os
from pathlib import Path
from huggingface_hub import HfApi

# Get config from environment
HF_TOKEN = os.environ.get("HF_TOKEN")
MODEL_REPO_ID = os.environ.get("MODEL_REPO_ID", "rfahrur11/ecommerce-churn-model")
LOCAL_MODEL_DIR = Path(__file__).parent / "serving_model" / "rfahrur6045-pipeline"

if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable not set. Please set it before running this script.")

if not LOCAL_MODEL_DIR.exists():
    raise FileNotFoundError(f"Model directory not found: {LOCAL_MODEL_DIR}")

# Find latest model version
version_dirs = sorted(
    [d for d in LOCAL_MODEL_DIR.iterdir() if d.is_dir() and d.name.isdigit()],
    key=lambda d: int(d.name),
)

if not version_dirs:
    raise FileNotFoundError(f"No model versions found in {LOCAL_MODEL_DIR}")

latest_model_dir = version_dirs[-1]
print(f"Uploading model from: {latest_model_dir}")

# Upload to Model Hub
api = HfApi(token=HF_TOKEN)
try:
    api.upload_folder(
        folder_path=str(latest_model_dir),
        repo_id=MODEL_REPO_ID,
        repo_type="model",
        path_in_repo="SavedModel",
        commit_message="Upload e-commerce churn SavedModel",
    )
    print(f"✅ Successfully uploaded to {MODEL_REPO_ID}")
    print(f"Model URL: https://huggingface.co/{MODEL_REPO_ID}")
except Exception as e:
    print(f"❌ Upload failed: {e}")
    raise
