"""
=============================================================
 Plant Disease Detection System — Enhanced Model Training
=============================================================
Improvements over baseline:
  • MobileNetV2 transfer learning (faster, more accurate)
  • Data augmentation pipeline
  • Learning-rate scheduling + early stopping
  • Saves training history for Tableau export
"""

import os, json
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, Model
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import (
    EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
)

# ── Config ────────────────────────────────────────────────────────────────────
IMG_SIZE   = (224, 224)   # MobileNetV2 native size (better than 128×128)
BATCH_SIZE = 32
EPOCHS     = 20
LR         = 1e-4
NUM_CLASSES = 38
TRAIN_DIR  = "Dataset/train"
VALID_DIR  = "Dataset/valid"
MODEL_OUT  = "models/plant_disease_model.keras"
HIST_OUT   = "outputs/training_history.json"

# ── Data Pipeline (with Augmentation) ────────────────────────────────────────
def build_datasets(train_dir: str, valid_dir: str):
    """Return (train_ds, val_ds, class_names)."""
    # Augmentation only for training
    augment = tf.keras.Sequential([
        layers.RandomFlip("horizontal_and_vertical"),
        layers.RandomRotation(0.2),
        layers.RandomZoom(0.15),
        layers.RandomBrightness(0.1),
    ], name="augmentation")

    def preprocess_train(image, label):
        image = augment(image, training=True)
        image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
        return image, label

    def preprocess_val(image, label):
        image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
        return image, label

    train_ds = tf.keras.utils.image_dataset_from_directory(
        train_dir, label_mode="categorical",
        image_size=IMG_SIZE, batch_size=BATCH_SIZE, shuffle=True, seed=42
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        valid_dir, label_mode="categorical",
        image_size=IMG_SIZE, batch_size=BATCH_SIZE, shuffle=False
    )
    class_names = train_ds.class_names

    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = (train_ds.map(preprocess_train, num_parallel_calls=AUTOTUNE)
                        .cache().prefetch(AUTOTUNE))
    val_ds   = (val_ds.map(preprocess_val,   num_parallel_calls=AUTOTUNE)
                      .cache().prefetch(AUTOTUNE))

    return train_ds, val_ds, class_names


# ── Model: MobileNetV2 Transfer Learning ─────────────────────────────────────
def build_model(num_classes: int) -> Model:
    """
    Two-phase training:
      Phase 1 – train only the classification head (base frozen)
      Phase 2 – fine-tune top 30 layers of MobileNetV2
    This file handles Phase 1; call unfreeze_and_finetune() for Phase 2.
    """
    base = MobileNetV2(include_top=False, weights="imagenet",
                       input_shape=(*IMG_SIZE, 3))
    base.trainable = False          # freeze for Phase 1

    inputs = layers.Input(shape=(*IMG_SIZE, 3))
    x = base(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(512, activation="relu")(x)
    x = layers.Dropout(0.4)(x)
    x = layers.Dense(256, activation="relu")(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = Model(inputs, outputs, name="PlantDiseaseNet")
    return model


def unfreeze_and_finetune(model: Model, train_ds, val_ds,
                          unfreeze_from: int = 100):
    """Phase 2 – fine-tune the top layers with a very small LR."""
    base = model.layers[1]          # MobileNetV2
    base.trainable = True
    for layer in base.layers[:unfreeze_from]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-5),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    callbacks = [
        EarlyStopping(patience=4, restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(factor=0.5, patience=2, min_lr=1e-7, verbose=1),
    ]
    history = model.fit(train_ds, validation_data=val_ds,
                        epochs=10, callbacks=callbacks)
    return history


# ── Main Training Loop ────────────────────────────────────────────────────────
def train():
    os.makedirs("models",   exist_ok=True)
    os.makedirs("outputs",  exist_ok=True)

    print("Loading datasets …")
    train_ds, val_ds, class_names = build_datasets(TRAIN_DIR, VALID_DIR)

    print("Building model …")
    model = build_model(NUM_CLASSES)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(LR),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    model.summary()

    callbacks = [
        EarlyStopping(monitor="val_accuracy", patience=5,
                      restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5,
                          patience=3, min_lr=1e-7, verbose=1),
        ModelCheckpoint(MODEL_OUT, save_best_only=True,
                        monitor="val_accuracy", verbose=1),
    ]

    # Phase 1
    print("\n=== Phase 1: Training head ===")
    hist1 = model.fit(train_ds, validation_data=val_ds,
                      epochs=EPOCHS, callbacks=callbacks)

    # Phase 2
    print("\n=== Phase 2: Fine-tuning ===")
    hist2 = unfreeze_and_finetune(model, train_ds, val_ds)

    # Merge histories & save
    full_hist = {
        "accuracy":     hist1.history["accuracy"]     + hist2.history["accuracy"],
        "val_accuracy": hist1.history["val_accuracy"] + hist2.history["val_accuracy"],
        "loss":         hist1.history["loss"]         + hist2.history["loss"],
        "val_loss":     hist1.history["val_loss"]     + hist2.history["val_loss"],
    }
    with open(HIST_OUT, "w") as f:
        json.dump(full_hist, f, indent=2)

    # Save class names
    with open("outputs/class_names.json", "w") as f:
        json.dump(class_names, f, indent=2)

    model.save(MODEL_OUT)
    print(f"\nModel saved → {MODEL_OUT}")
    print(f"History  saved → {HIST_OUT}")


if __name__ == "__main__":
    train()
