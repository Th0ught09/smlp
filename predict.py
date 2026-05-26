#!/usr/bin/env python3
"""
Measure MSE and R² scores after SMLP optimization with weight dropping.
"""

from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from keras.models import load_model as keras_load_model
from tensorflow import keras
import json
import os


def evaluate_model_with_weight_dropping(
    model_path,
    X_test,
    y_test,
    weights_precision=None,
    drop_percentage=None,
    response_names=None,
):
    """
    Evaluate MSE and R² scores for a model with optional weight dropping.

    Args:
        model_path: Path to the .h5 model file
        X_test: Test features (numpy array or DataFrame)
        y_test: Test responses (numpy array or DataFrame)
        weights_precision: Decimal places to round weights to (optional)
        drop_percentage: Percentage of weights to drop (0-100) (optional)
        features_config_path: Path to model_features_dict.json
        response_names: List of response names (optional)

    Returns:
        DataFrame with metrics for each response
    """
    # Load the original model
    model = keras_load_model(model_path)
    print(f"Loaded model from: {model_path}")
    print(f"  Model input shape: {model.input_shape}")

    pca = PCA()
    pca.fit(X_test)
    cumsum = np.cumsum(pca.explained_variance_ratio_)
    d = np.argmax(cumsum >= 80) + 1
    pca = PCA(n_components=d)
    X_test = pca.fit_transform(X_test)

    # Verify input shape
    print(f"\nInput validation:")
    print(f"  Expected input features: {model.input_shape[1]}")
    print(f"  Provided input features: {X_test.shape[1]}")

    if model.input_shape[1] != X_test.shape[1]:
        raise ValueError(
            f"Input shape mismatch: model expects {model.input_shape[1]} features, "
            f"but got {X_test.shape[1]} features"
        )
    print(f"  ✓ Shapes match")

    # Make predictions
    print(f"\nMaking predictions...")
    y_pred = model.predict(X_test, verbose=0)
    print(f"  ✓ Prediction successful")
    # print(f"  Output shape: {y_pred.shape}")

    if isinstance(y_pred, list):
        print(f"  Converting list output to numpy array...")
        if len(y_pred) > 0 and isinstance(y_pred[0], np.ndarray):
            y_pred = np.concatenate(y_pred, axis=1)
        else:
            y_pred = np.array(y_pred)

    # Handle output format (single or multiple responses)
    if isinstance(y_test, pd.DataFrame):
        resp_names = (
            y_test.columns.tolist() if response_names is None else response_names
        )
        orig_resp_df = y_test
        if isinstance(y_pred, list):
            if isinstance(y_pred[0], np.ndarray):
                y_pred = np.concatenate(y_pred, axis=1)
        orig_pred_df = pd.DataFrame(y_pred, columns=resp_names)
    else:
        resp_names = response_names if response_names else ["response"]
        orig_resp_df = pd.DataFrame(y_test, columns=resp_names)
        if y_pred.ndim == 1:
            y_pred = y_pred.reshape(-1, 1)
        orig_pred_df = pd.DataFrame(y_pred, columns=resp_names)

    # Compute metrics
    print(f"\nComputing metrics...")
    r2_vec = [
        r2_score(
            orig_resp_df[resp_names[i]],
            orig_pred_df[resp_names[i]],
            multioutput="uniform_average",
        )
        for i in range(len(resp_names))
    ]
    msqe_vec = [
        mean_squared_error(
            orig_resp_df[resp_names[i]],
            orig_pred_df[resp_names[i]],
            multioutput="uniform_average",
        )
        for i in range(len(resp_names))
    ]

    # Create results DataFrame
    precisions_df = pd.DataFrame(
        data={"response": resp_names, "msqe": msqe_vec, "r2_score": r2_vec}
    )

    # Overall metrics
    orig_pred_df_renamed = orig_pred_df.copy()
    orig_pred_df_renamed.columns = resp_names
    overall_mse = mean_squared_error(orig_resp_df, orig_pred_df_renamed)
    overall_r2 = r2_score(orig_resp_df, orig_pred_df_renamed)

    print("\n" + "=" * 60)
    print("MODEL EVALUATION RESULTS")
    print("=" * 60)
    print("\nPer-Response Metrics:")
    print(precisions_df.to_string(index=False))
    print(f"\nOverall MSE: {overall_mse:.6f}")
    print(f"Overall R²: {overall_r2:.6f}")

    return precisions_df, overall_mse, overall_r2, model


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("SMLP MODEL EVALUATION WITH WEIGHT DROPPING")
    print("=" * 60 + "\n")

    # Load test data
    print("Loading test data...")
    test_data = pd.read_csv("bench/intel/data/s2_rx_anonym.csv")

    # Use the features from config
    features_to_use = ["p0", "p1", "p2", "p3", "p4", "p5", "CH", "RANK", "Byte"]
    X_test = test_data[features_to_use].values
    y_test = test_data[["o0", "o1"]].values
    print(f"  ✓ Test data loaded: {X_test.shape}")

    # Model paths
    original_model_path = "project/running_model_checkpoint.h5"
    # features_config_path = "project/Test113_s2_rx_anonym_model_features_dict.json"

    # Evaluation parameters (adjust based on your adjust.py call)
    weights_precision = 8  # From adjust.py first argument
    drop_percentage = 80  # From adjust.py second argument

    # Evaluate
    if os.path.exists(original_model_path):
        try:
            precisions_df, mse, r2, final_model = evaluate_model_with_weight_dropping(
                original_model_path,
                X_test,
                y_test,
                weights_precision=weights_precision,
                drop_percentage=drop_percentage,
                response_names=["o0", "o1"],
            )

            # Save results
            results_file = "project/optimization_metrics.csv"
            precisions_df.to_csv(results_file, index=False)
            print(f"\n✓ Metrics saved to: {results_file}")

            # Optionally save the processed model
            model_output_file = "project/evaluated_model.h5"
            final_model.save(model_output_file)
            print(f"✓ Processed model saved to: {model_output_file}")

        except Exception as e:
            print(f"\n✗ Evaluation failed: {e}")
            import traceback

            traceback.print_exc()
    else:
        print(f"Model not found at: {original_model_path}")
