"""Hugging Face Spaces app for e-commerce churn prediction."""

from pathlib import Path
import os
import logging

import gradio as gr
import tensorflow as tf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


FLOAT_FEATURES = [
    "Tenure",
    "WarehouseToHome",
    "HourSpendOnApp",
    "OrderAmountHikeFromlastYear",
    "CouponUsed",
    "OrderCount",
    "DaySinceLastOrder",
    "CashbackAmount",
]

INT_FEATURES = [
    "CityTier",
    "NumberOfDeviceRegistered",
    "SatisfactionScore",
    "NumberOfAddress",
    "Complain",
]

STRING_FEATURES = {
    "PreferredLoginDevice": ["Computer", "Mobile Phone", "Phone"],
    "PreferredPaymentMode": [
        "CC",
        "COD",
        "Cash on Delivery",
        "Credit Card",
        "Debit Card",
        "E wallet",
        "UPI",
    ],
    "Gender": ["Female", "Male"],
    "PreferedOrderCat": [
        "Fashion",
        "Grocery",
        "Laptop & Accessory",
        "Mobile",
        "Mobile Phone",
        "Others",
    ],
    "MaritalStatus": ["Divorced", "Married", "Single"],
}


def latest_model_dir(base_dir: Path) -> Path:
    version_dirs = sorted(
        [path for path in base_dir.iterdir() if path.is_dir() and path.name.isdigit()],
        key=lambda path: int(path.name),
    )
    if version_dirs:
        return version_dirs[-1]
    return base_dir


def resolve_saved_model_dir(model_dir: Path) -> Path:
    """Return the actual SavedModel directory to load."""
    if (model_dir / "saved_model.pb").exists():
        return model_dir
    if (model_dir / "SavedModel" / "saved_model.pb").exists():
        return model_dir / "SavedModel"
    if (model_dir / "SavedModel").is_dir():
        return model_dir / "SavedModel"
    return latest_model_dir(model_dir)


def build_model_signature():
    """Load model from HF Model Hub."""
    logger.info(f"Downloading model from {MODEL_REPO_ID}...")
    try:
        model_dir = snapshot_download(
            repo_id=MODEL_REPO_ID,
            revision=MODEL_REVISION,
            cache_dir="/tmp/hf_cache",
            repo_type="model",
        )
        logger.info(f"Downloaded model to {model_dir}")
    except Exception as e:
        raise RuntimeError(
            f"Failed to load model from {MODEL_REPO_ID}: {str(e)}. "
            "Ensure the repository exists and is accessible."
        ) from e
    
    model = tf.saved_model.load(str(model_dir))
    signature = model.signatures.get("serving_json")
    if signature is None:
        signature = next(iter(model.signatures.values()))
    return signature, model_dir


SIGNATURE, MODEL_DIR = build_model_signature()


def predict_churn(
    tenure,
    city_tier,
    warehouse_to_home,
    hour_spend_on_app,
    number_of_device_registered,
    satisfaction_score,
    number_of_address,
    complain,
    order_amount_hike_from_last_year,
    coupon_used,
    order_count,
    day_since_last_order,
    cashback_amount,
    preferred_login_device,
    preferred_payment_mode,
    gender,
    prefered_order_cat,
    marital_status,
):
    payload = {
        "Tenure": tf.constant([float(tenure)], dtype=tf.float32),
        "CityTier": tf.constant([int(city_tier)], dtype=tf.int64),
        "WarehouseToHome": tf.constant([float(warehouse_to_home)], dtype=tf.float32),
        "HourSpendOnApp": tf.constant([float(hour_spend_on_app)], dtype=tf.float32),
        "NumberOfDeviceRegistered": tf.constant([int(number_of_device_registered)], dtype=tf.int64),
        "SatisfactionScore": tf.constant([int(satisfaction_score)], dtype=tf.int64),
        "NumberOfAddress": tf.constant([int(number_of_address)], dtype=tf.int64),
        "Complain": tf.constant([int(complain)], dtype=tf.int64),
        "OrderAmountHikeFromlastYear": tf.constant([float(order_amount_hike_from_last_year)], dtype=tf.float32),
        "CouponUsed": tf.constant([float(coupon_used)], dtype=tf.float32),
        "OrderCount": tf.constant([float(order_count)], dtype=tf.float32),
        "DaySinceLastOrder": tf.constant([float(day_since_last_order)], dtype=tf.float32),
        "CashbackAmount": tf.constant([float(cashback_amount)], dtype=tf.float32),
        "PreferredLoginDevice": tf.constant([preferred_login_device], dtype=tf.string),
        "PreferredPaymentMode": tf.constant([preferred_payment_mode], dtype=tf.string),
        "Gender": tf.constant([gender], dtype=tf.string),
        "PreferedOrderCat": tf.constant([prefered_order_cat], dtype=tf.string),
        "MaritalStatus": tf.constant([marital_status], dtype=tf.string),
    }

    result = SIGNATURE(**payload)
    probability = float(result["output"][0][0].numpy())
    prediction = "Churn" if probability >= 0.5 else "Not Churn"
    return {
        "probability": round(probability, 4),
        "prediction": prediction,
        "model_dir": str(MODEL_DIR),
    }


with gr.Blocks(theme=gr.themes.Soft(), title="E-Commerce Churn Predictor") as demo:
    gr.Markdown(
        "# E-Commerce Customer Churn Prediction\n"
        "Deploy this model on Hugging Face Spaces and predict churn from 18 customer features."
    )

    with gr.Row():
        with gr.Column():
            gr.Markdown("## Numeric features")
            tenure = gr.Number(value=3.0, label="Tenure")
            city_tier = gr.Number(value=1, precision=0, label="CityTier")
            warehouse_to_home = gr.Number(value=10.0, label="WarehouseToHome")
            hour_spend_on_app = gr.Number(value=1.0, label="HourSpendOnApp")
            number_of_device_registered = gr.Number(value=2, precision=0, label="NumberOfDeviceRegistered")
            satisfaction_score = gr.Number(value=3, precision=0, label="SatisfactionScore")
            number_of_address = gr.Number(value=1, precision=0, label="NumberOfAddress")
        with gr.Column():
            gr.Markdown("## More numeric features")
            complain = gr.Number(value=0, precision=0, label="Complain")
            order_amount_hike_from_last_year = gr.Number(value=11.0, label="OrderAmountHikeFromlastYear")
            coupon_used = gr.Number(value=0.0, label="CouponUsed")
            order_count = gr.Number(value=3.0, label="OrderCount")
            day_since_last_order = gr.Number(value=5.0, label="DaySinceLastOrder")
            cashback_amount = gr.Number(value=0.0, label="CashbackAmount")

    gr.Markdown("## Categorical features")
    with gr.Row():
        preferred_login_device = gr.Dropdown(
            choices=STRING_FEATURES["PreferredLoginDevice"],
            value="Mobile Phone",
            label="PreferredLoginDevice",
        )
        preferred_payment_mode = gr.Dropdown(
            choices=STRING_FEATURES["PreferredPaymentMode"],
            value="Debit Card",
            label="PreferredPaymentMode",
        )
        gender = gr.Dropdown(
            choices=STRING_FEATURES["Gender"],
            value="Female",
            label="Gender",
        )
        prefered_order_cat = gr.Dropdown(
            choices=STRING_FEATURES["PreferedOrderCat"],
            value="Grocery",
            label="PreferedOrderCat",
        )
        marital_status = gr.Dropdown(
            choices=STRING_FEATURES["MaritalStatus"],
            value="Single",
            label="MaritalStatus",
        )

    predict_button = gr.Button("Predict Churn", variant="primary")
    output = gr.JSON(label="Prediction")

    predict_button.click(
        fn=predict_churn,
        inputs=[
            tenure,
            city_tier,
            warehouse_to_home,
            hour_spend_on_app,
            number_of_device_registered,
            satisfaction_score,
            number_of_address,
            complain,
            order_amount_hike_from_last_year,
            coupon_used,
            order_count,
            day_since_last_order,
            cashback_amount,
            preferred_login_device,
            preferred_payment_mode,
            gender,
            prefered_order_cat,
            marital_status,
        ],
        outputs=output,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "7860"))
    demo.launch(server_name="0.0.0.0", server_port=port)