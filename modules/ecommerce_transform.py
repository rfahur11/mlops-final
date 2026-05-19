"""
ecommerce_transform.py
Transform module untuk TFX Pipeline - E-Commerce Customer Churn Prediction.
Username: rfahrur6045
"""

import tensorflow as tf
import tensorflow_transform as tft

# ──────────────────────────────────────────────
# Definisi fitur
# ──────────────────────────────────────────────

NUMERICAL_FEATURES = [
    'Tenure',
    'CityTier',
    'WarehouseToHome',
    'HourSpendOnApp',
    'NumberOfDeviceRegistered',
    'SatisfactionScore',
    'NumberOfAddress',
    'Complain',
    'OrderAmountHikeFromlastYear',
    'CouponUsed',
    'OrderCount',
    'DaySinceLastOrder',
    'CashbackAmount',
]

CATEGORICAL_FEATURES = [
    'PreferredLoginDevice',
    'PreferredPaymentMode',
    'Gender',
    'PreferedOrderCat',
    'MaritalStatus',
]

LABEL_KEY = 'Churn'


def transformed_name(key):
    """Menambahkan suffix _xf pada nama fitur hasil transformasi."""
    return key + '_xf'


def preprocessing_fn(inputs):
    """
    Fungsi preprocessing utama yang dipanggil oleh TFX Transform component.

    Args:
        inputs: dict berisi raw feature tensors dari dataset.

    Returns:
        dict berisi transformed feature tensors.
    """
    outputs = {}

    # ── Normalisasi fitur numerik dengan z-score ──────────────────
    for feature in NUMERICAL_FEATURES:
        outputs[transformed_name(feature)] = tft.scale_to_z_score(
            tf.cast(inputs[feature], tf.float32)
        )

    # ── Encode fitur kategorik ke integer vocabulary ──────────────
    for feature in CATEGORICAL_FEATURES:
        outputs[transformed_name(feature)] = tft.compute_and_apply_vocabulary(
            inputs[feature],
            num_oov_buckets=1,
            vocab_filename=feature,
        )

    # ── Label (cast ke int64) ─────────────────────────────────────
    outputs[transformed_name(LABEL_KEY)] = tf.cast(
        inputs[LABEL_KEY], tf.int64
    )

    return outputs
