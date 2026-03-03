#!/usr/bin/env python3
"""
Example script demonstrating the weight dropping algorithm for neural networks.

This script shows how to use the weight dropping feature to compress trained models
by removing the smallest magnitude weights.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import sys
import os

# Add the src directory to path to import smlp modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from smlp_py.train_keras import ModelKeras


def create_sample_data(n_samples=1000, n_features=20):
    """Create sample regression data for demonstration."""
    print(f"Creating sample data: {n_samples} samples, {n_features} features")

    X, y = make_regression(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=10,
        noise=10,
        random_state=42
    )

    # Scale features
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Create DataFrames
    feature_names = [f'feature_{i}' for i in range(n_features)]
    X_df = pd.DataFrame(X, columns=feature_names)
    y_df = pd.DataFrame(y, columns=['response'])

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_df, y_df, test_size=0.2, random_state=42
    )

    return X_train, X_test, y_train, y_test


def example_basic_weight_dropping():
    """Basic example: Train a model and drop weights."""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Weight Dropping")
    print("="*80)

    # Create sample data
    X_train, X_test, y_train, y_test = create_sample_data(n_samples=500, n_features=10)

    # Initialize Keras model
    keras_model = ModelKeras()

    # Set up logging (you would normally do this in a real application)
    # keras_model.set_logger(logger)
    # keras_model.set_model_file_prefix("test_model")
    # keras_model.set_report_file_prefix("test_model")

    # Define hyperparameters
    hparams = {
        'nn_keras_layers': '0.5,0.25',  # Two hidden layers
        'nn_keras_epochs': 100,
        'nn_keras_batch_size': 32,
        'nn_keras_optimizer': 'adam',
        'nn_keras_learning_rate': 0.001,
        'nn_keras_loss_function': 'mse',
        'nn_keras_metrics': ['mse'],
        'nn_keras_hid_activation': 'relu',
        'nn_keras_out_activation': 'linear',
    }

    print("\nTraining model without weight dropping...")
    model_no_drop = keras_model.keras_main(
        resp_names=['response'],
        algo='nn',
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
        hparam_dict=hparams,
        interactive_plots=False,
        seed=42,
        weights_coef=None,
        model_per_response=False,
        weights_drop=0  # No weight dropping
    )

    # Count non-zero weights
    total_weights_original = sum([np.count_nonzero(w) for layer in model_no_drop.layers
                                   for w in layer.get_weights()])
    print(f"Model without dropping: {total_weights_original} non-zero weights")

    print("\nTraining model WITH 30% weight dropping...")
    model_with_drop = keras_model.keras_main(
        resp_names=['response'],
        algo='nn',
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
        hparam_dict=hparams,
        interactive_plots=False,
        seed=42,
        weights_coef=None,
        model_per_response=False,
        weights_drop=30  # Drop 30% of smallest weights
    )

    # Count non-zero weights
    total_weights_dropped = sum([np.count_nonzero(w) for layer in model_with_drop.layers
                                  for w in layer.get_weights()])
    print(f"Model with 30% dropping: {total_weights_dropped} non-zero weights")
    print(f"Sparsity improvement: {100*(1-total_weights_dropped/total_weights_original):.1f}%")


def example_progressive_pruning():
    """Example: Progressive pruning with different drop percentages."""
    print("\n" + "="*80)
    print("EXAMPLE 2: Progressive Weight Dropping")
    print("="*80)

    # Create sample data
    X_train, X_test, y_train, y_test = create_sample_data(n_samples=500, n_features=10)

    # Initialize Keras model
    keras_model = ModelKeras()

    # Define hyperparameters
    hparams = {
        'nn_keras_layers': '0.5,0.25',
        'nn_keras_epochs': 100,
        'nn_keras_batch_size': 32,
        'nn_keras_optimizer': 'adam',
        'nn_keras_learning_rate': 0.001,
        'nn_keras_loss_function': 'mse',
        'nn_keras_metrics': ['mse'],
        'nn_keras_hid_activation': 'relu',
        'nn_keras_out_activation': 'linear',
    }

    drop_percentages = [0, 10, 20, 30, 50]
    results = []

    for drop_pct in drop_percentages:
        print(f"\nTraining with {drop_pct}% weight dropping...")

        model = keras_model.keras_main(
            resp_names=['response'],
            algo='nn',
            X_train=X_train,
            X_test=X_test,
            y_train=y_train,
            y_test=y_test,
            hparam_dict=hparams,
            interactive_plots=False,
            seed=42,
            weights_coef=None,
            model_per_response=False,
            weights_drop=drop_pct
        )

        # Evaluate on test set
        test_loss = model.evaluate(X_test, y_test, verbose=0)[0]

        # Count weights
        total_weights = sum([np.size(w) for layer in model.layers for w in layer.get_weights()])
        nonzero_weights = sum([np.count_nonzero(w) for layer in model.layers
                               for w in layer.get_weights()])
        sparsity = 100 * (1 - nonzero_weights / total_weights)

        results.append({
            'drop_pct': drop_pct,
            'test_loss': test_loss,
            'sparsity': sparsity,
            'nonzero_weights': nonzero_weights
        })

        print(f"  Test Loss: {test_loss:.6f}")
        print(f"  Sparsity: {sparsity:.1f}%")
        print(f"  Non-zero weights: {nonzero_weights}/{total_weights}")

    # Print summary
    print("\n" + "-"*80)
    print("Summary of Progressive Pruning:")
    print("-"*80)
    print(f"{'Drop %':<10} {'Test Loss':<15} {'Sparsity':<15} {'Non-zero Weights':<20}")
    print("-"*80)
    for r in results:
        print(f"{r['drop_pct']:<10} {r['test_loss']:<15.6f} {r['sparsity']:<14.1f}% {r['nonzero_weights']:<20}")


def example_layer_analysis():
    """Example: Analyze weight dropping impact per layer."""
    print("\n" + "="*80)
    print("EXAMPLE 3: Per-Layer Weight Dropping Analysis")
    print("="*80)

    # Create sample data
    X_train, X_test, y_train, y_test = create_sample_data(n_samples=500, n_features=10)

    # Initialize Keras model
    keras_model = ModelKeras()

    # Define hyperparameters
    hparams = {
        'nn_keras_layers': '0.5,0.25',
        'nn_keras_epochs': 100,
        'nn_keras_batch_size': 32,
        'nn_keras_optimizer': 'adam',
        'nn_keras_learning_rate': 0.001,
        'nn_keras_loss_function': 'mse',
        'nn_keras_metrics': ['mse'],
        'nn_keras_hid_activation': 'relu',
        'nn_keras_out_activation': 'linear',
    }

    print("\nTraining model with 30% weight dropping...")

    model = keras_model.keras_main(
        resp_names=['response'],
        algo='nn',
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
        hparam_dict=hparams,
        interactive_plots=False,
        seed=42,
        weights_coef=None,
        model_per_response=False,
        weights_drop=30
    )

    # Analyze per layer
    print("\nPer-Layer Analysis:")
    print("-" * 80)
    print(f"{'Layer':<20} {'Total Weights':<20} {'Non-zero':<20} {'Sparsity':<15}")
    print("-" * 80)

    for layer in model.layers:
        weights = layer.get_weights()
        if len(weights) > 0:
            kernel = weights[0]
            total = np.size(kernel)
            nonzero = np.count_nonzero(kernel)
            sparsity = 100 * (1 - nonzero / total)

            print(f"{layer.name:<20} {total:<20} {nonzero:<20} {sparsity:<14.1f}%")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("WEIGHT DROPPING ALGORITHM - DEMONSTRATION EXAMPLES")
    print("="*80)

    try:
        # Run examples
        example_basic_weight_dropping()
        example_progressive_pruning()
        example_layer_analysis()

        print("\n" + "="*80)
        print("All examples completed successfully!")
        print("="*80)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

