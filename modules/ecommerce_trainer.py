
import tensorflow as tf
import tensorflow_transform as tft
from tfx.components.trainer.fn_args_utils import FnArgs

NUMERICAL_FEATURES = [
    'Tenure', 'CityTier', 'WarehouseToHome', 'HourSpendOnApp',
    'NumberOfDeviceRegistered', 'SatisfactionScore', 'NumberOfAddress',
    'Complain', 'OrderAmountHikeFromlastYear', 'CouponUsed',
    'OrderCount', 'DaySinceLastOrder', 'CashbackAmount'
]

CATEGORICAL_FEATURES = [
    'PreferredLoginDevice', 'PreferredPaymentMode', 'Gender',
    'PreferedOrderCat', 'MaritalStatus'
]

LABEL_KEY = 'Churn'
VOCAB_SIZE = 100
EMBEDDING_DIM = 16

def transformed_name(key):
    return key + '_xf'

def gzip_reader_fn(filenames):
    return tf.data.TFRecordDataset(filenames, compression_type='GZIP')

def input_fn(file_pattern, tf_transform_output, num_epochs=10, batch_size=64):
    transform_feature_spec = tf_transform_output.transformed_feature_spec().copy()

    dataset = tf.data.experimental.make_batched_features_dataset(
        file_pattern=file_pattern,
        batch_size=batch_size,
        features=transform_feature_spec,
        reader=gzip_reader_fn,
        num_epochs=num_epochs,
        label_key=transformed_name(LABEL_KEY)
    )
    return dataset

def build_keras_model(tf_transform_output):
    inputs = []
    encoded_inputs = []

    # Numerical inputs
    for feature in NUMERICAL_FEATURES:
        inp = tf.keras.Input(shape=(1,), name=transformed_name(feature))
        inputs.append(inp)
        encoded_inputs.append(inp)

    # Categorical inputs
    for feature in CATEGORICAL_FEATURES:
        vocab_size = tf_transform_output.vocabulary_size_by_name(feature)
        inp = tf.keras.Input(shape=(1,), name=transformed_name(feature), dtype=tf.int64)
        emb = tf.keras.layers.Embedding(vocab_size + 1, EMBEDDING_DIM)(inp)
        emb = tf.keras.layers.Reshape((EMBEDDING_DIM,))(emb)
        inputs.append(inp)
        encoded_inputs.append(emb)

    x = tf.keras.layers.concatenate(encoded_inputs)
    x = tf.keras.layers.Dense(256, activation='relu')(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    x = tf.keras.layers.Dense(128, activation='relu')(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    x = tf.keras.layers.Dense(64, activation='relu')(x)
    output = tf.keras.layers.Dense(1, activation='sigmoid')(x)

    model = tf.keras.Model(inputs=inputs, outputs=output)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=[
            tf.keras.metrics.AUC(name='auc'),
            tf.keras.metrics.BinaryAccuracy(name='accuracy')
        ]
    )
    return model

def run_fn(fn_args: FnArgs):
    tf_transform_output = tft.TFTransformOutput(fn_args.transform_graph_path)

    train_dataset = input_fn(fn_args.train_files, tf_transform_output, num_epochs=10)
    eval_dataset = input_fn(fn_args.eval_files, tf_transform_output, num_epochs=1)

    model = build_keras_model(tf_transform_output)
    model.summary()

    tensorboard_callback = tf.keras.callbacks.TensorBoard(
        log_dir=fn_args.model_run_dir,
        update_freq='batch'
    )

    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor='val_auc',
        patience=3,
        restore_best_weights=True
    )

    model.fit(
        train_dataset,
        steps_per_epoch=fn_args.train_steps,
        validation_data=eval_dataset,
        validation_steps=fn_args.eval_steps,
        callbacks=[tensorboard_callback, early_stopping]
    )

    # Buat wrapper model dengan transform layer yang ter-track
    inputs_dict = {}
    
    # Raw feature spec untuk input
    raw_feature_spec = tf_transform_output.raw_feature_spec()
    raw_feature_spec.pop(LABEL_KEY)
    
    for feature_name, spec in raw_feature_spec.items():
        inputs_dict[feature_name] = tf.keras.Input(
            shape=spec.shape or (1,),
            name=feature_name,
            dtype=spec.dtype
        )
    
    # Apply transform layer (sudah ter-track)
    transform_layer = tf_transform_output.transform_features_layer()
    transformed = transform_layer(inputs_dict)
    
    # Remove label dari transformed jika ada
    transformed.pop(transformed_name(LABEL_KEY), None)
    
    # Paskan ke model
    output = model(transformed)
    
    # Buat serving model dengan signatures
    serving_model = tf.keras.Model(inputs=inputs_dict, outputs=output)
    
    serving_model.save(
        fn_args.serving_model_dir,
        save_format='tf',
        signatures={
            'serving_default': _get_serve_fn(serving_model).get_concrete_function(
                tf.TensorSpec(shape=[None], dtype=tf.string, name='examples')
            ),
            'serving_json': _get_serve_json_fn(serving_model, raw_feature_spec).get_concrete_function(
                **{
                    k: tf.TensorSpec(shape=[None], dtype=spec.dtype, name=k)
                    for k, spec in raw_feature_spec.items()
                }
            )
        }
    )

def _get_serve_fn(model):
    @tf.function(input_signature=[
        tf.TensorSpec(shape=[None], dtype=tf.string, name='examples')
    ])
    def serve_examples(serialized_examples):
        # Parse serialized examples
        parsed = tf.io.parse_example(
            serialized_examples,
            {k: tf.io.FixedLenFeature([], tf.string) for k in model.input_names}
        )
        return {"output": model(parsed, training=False)}
    return serve_examples


def _get_serve_json_fn(model, raw_feature_spec):
    @tf.function
    def serve_json(**kwargs):
        # kwargs contains all named feature inputs: {"Tenure": ..., "CityTier": ..., etc.}
        normalized_inputs = {
            key: tf.expand_dims(value, -1) if value.shape.rank == 1 else value
            for key, value in kwargs.items()
        }
        return {"output": model(normalized_inputs, training=False)}

    return serve_json
