#!/usr/bin/env python3
"""
Benchmark script to measure time reduction from weight dropping on SMLP neural networks.

This script measures:
1. Training time (baseline)
2. Weight dropping overhead
3. Inference speed improvement
4. Model size reduction
5. Accuracy retention

Usage:
    python benchmark_weight_dropping.py -data training.csv -spec spec.json
"""

import sys
import os
import time
import argparse
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from smlp_py.train_keras import ModelKeras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class WeightDroppingBenchmark:
    """Benchmark weight dropping performance and impacts."""

    def __init__(self, verbose=True):
        self.verbose = verbose
        self.results = {}
        self.keras_model = ModelKeras()

    def log(self, message: str):
        """Log message if verbose."""
        if self.verbose:
            print(message)

    def measure_inference_time(self, model, X_test: np.ndarray, warmup_runs=3,
                               test_runs=10) -> float:
        """
        Measure average inference time.

        Args:
            model: Trained Keras model
            X_test: Test data
            warmup_runs: Number of warmup runs (to stabilize)
            test_runs: Number of actual test runs

        Returns:
            Average inference time in seconds
        """
        # Warmup runs
        for _ in range(warmup_runs):
            _ = model.predict(X_test, verbose=0)

        # Measured runs
        times = []
        for _ in range(test_runs):
            start = time.perf_counter()
            _ = model.predict(X_test, verbose=0)
            times.append(time.perf_counter() - start)

        return np.mean(times)

    def calculate_model_size(self, model) -> int:
        """Calculate total model size in bytes."""
        total_size = 0
        for layer in model.layers:
            for weight in layer.get_weights():
                total_size += weight.nbytes
        return total_size

    def calculate_sparsity(self, model) -> float:
        """Calculate model sparsity (percentage of zero weights)."""
        total_weights = 0
        zero_weights = 0

        for layer in model.layers:
            for weight in layer.get_weights():
                total_weights += weight.size
                zero_weights += np.count_nonzero(weight == 0)

        if total_weights == 0:
            return 0.0
        return 100.0 * zero_weights / total_weights

    def benchmark_single_drop_percentage(self, X_train_df, X_test_df, y_train_df,
                                         y_test_df, hparams: dict, drop_pct: int,
                                         seed: int = 42) -> Dict:
        """
        Benchmark a single drop percentage.

        Returns dict with timing, accuracy, sparsity metrics.
        """
        self.log(f"\n{'='*70}")
        self.log(f"Benchmarking: {drop_pct}% weight dropping")
        self.log(f"{'='*70}")

        metrics = {'drop_percentage': drop_pct}

        # Train model
        train_start = time.perf_counter()

        model = self.keras_model.keras_main(
            resp_names=['response'],
            algo='nn',
            X_train=X_train_df,
            X_test=X_test_df,
            y_train=y_train_df,
            y_test=y_test_df,
            hparam_dict=hparams,
            interactive_plots=False,
            seed=seed,
            weights_coef=None,
            model_per_response=False,
            weights_drop=drop_pct
        )

        train_time = time.perf_counter() - train_start
        metrics['train_time'] = train_time
        self.log(f"Training time: {train_time:.4f}s")

        # Evaluate accuracy
        test_loss, test_mse = model.evaluate(X_test_df, y_test_df, verbose=0)
        metrics['test_loss'] = test_loss
        metrics['test_mse'] = test_mse
        self.log(f"Test MSE: {test_mse:.6f}")

        # Measure inference time
        inference_time = self.measure_inference_time(model, X_test_df.values)
        metrics['inference_time'] = inference_time
        self.log(f"Inference time: {inference_time:.6f}s")

        # Model size
        model_size = self.calculate_model_size(model)
        metrics['model_size_bytes'] = model_size
        metrics['model_size_mb'] = model_size / (1024 * 1024)
        self.log(f"Model size: {metrics['model_size_mb']:.2f} MB")

        # Sparsity
        sparsity = self.calculate_sparsity(model)
        metrics['sparsity'] = sparsity
        self.log(f"Sparsity: {sparsity:.2f}%")

        return metrics

    def run_benchmark(self, X_train_df, X_test_df, y_train_df, y_test_df,
                     hparams: dict, drop_percentages: List[int] = None,
                     seed: int = 42):
        """
        Run benchmark with multiple drop percentages.

        Args:
            X_train_df, X_test_df, y_train_df, y_test_df: Data
            hparams: Model hyperparameters
            drop_percentages: List of percentages to test
            seed: Random seed
        """
        if drop_percentages is None:
            drop_percentages = [0, 10, 20, 30, 50]

        self.results = {}
        baseline_metrics = None

        for drop_pct in drop_percentages:
            metrics = self.benchmark_single_drop_percentage(
                X_train_df, X_test_df, y_train_df, y_test_df,
                hparams, drop_pct, seed
            )
            self.results[drop_pct] = metrics

            if drop_pct == 0:
                baseline_metrics = metrics

        # Calculate improvements relative to baseline
        self.log(f"\n{'='*70}")
        self.log("SUMMARY: Improvements vs Baseline (0% drop)")
        self.log(f"{'='*70}")

        for drop_pct in drop_percentages:
            if drop_pct == 0:
                continue

            metrics = self.results[drop_pct]

            # Calculate improvements
            speedup = baseline_metrics['inference_time'] / metrics['inference_time']
            time_reduction = 100 * (1 - metrics['inference_time'] / baseline_metrics['inference_time'])
            size_reduction = 100 * (1 - metrics['model_size_bytes'] / baseline_metrics['model_size_bytes'])
            accuracy_retention = (baseline_metrics['test_mse'] - metrics['test_mse']) / baseline_metrics['test_mse']

            self.log(f"\n{drop_pct}% Weight Drop:")
            self.log(f"  Speedup: {speedup:.2f}x")
            self.log(f"  Inference time reduction: {time_reduction:.1f}%")
            self.log(f"  Model size reduction: {size_reduction:.1f}%")
            self.log(f"  Sparsity: {metrics['sparsity']:.1f}%")
            self.log(f"  MSE change: {metrics['test_mse'] - baseline_metrics['test_mse']:+.6f}")

            metrics['speedup'] = speedup
            metrics['time_reduction_pct'] = time_reduction
            metrics['size_reduction_pct'] = size_reduction

    def save_results_csv(self, output_file: str):
        """Save benchmark results to CSV."""
        df_data = []
        for drop_pct, metrics in self.results.items():
            row = {
                'drop_percentage': drop_pct,
                'train_time_s': metrics['train_time'],
                'inference_time_s': metrics['inference_time'],
                'model_size_mb': metrics['model_size_mb'],
                'sparsity_pct': metrics['sparsity'],
                'test_mse': metrics['test_mse'],
            }
            if 'speedup' in metrics:
                row['speedup_x'] = metrics['speedup']
                row['time_reduction_pct'] = metrics['time_reduction_pct']
                row['size_reduction_pct'] = metrics['size_reduction_pct']
            df_data.append(row)

        df = pd.DataFrame(df_data)
        df.to_csv(output_file, index=False)
        self.log(f"\nResults saved to: {output_file}")

    def print_results_table(self):
        """Print results as formatted table."""
        self.log("\n" + "="*100)
        self.log("DETAILED RESULTS TABLE")
        self.log("="*100)

        header = f"{'Drop%':<8} {'Train(s)':<10} {'Inf(s)':<10} {'Size(MB)':<12} {'Sparse%':<10} {'MSE':<12} {'Speedup':<10}"
        self.log(header)
        self.log("-"*100)

        for drop_pct in sorted(self.results.keys()):
            metrics = self.results[drop_pct]
            speedup = metrics.get('speedup', 1.0)

            self.log(f"{drop_pct:<8} {metrics['train_time']:<10.4f} {metrics['inference_time']:<10.6f} "
                    f"{metrics['model_size_mb']:<12.2f} {metrics['sparsity']:<10.1f} {metrics['test_mse']:<12.6f} "
                    f"{speedup:<10.2f}x")


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark weight dropping on SMLP neural networks"
    )
    parser.add_argument('-data', '--data', required=True, help='Path to training data (CSV)')
    parser.add_argument('-drop', '--drop_percentages', nargs='+', type=int,
                       default=[0, 10, 20, 30, 50],
                       help='Drop percentages to test')
    parser.add_argument('-o', '--output', default='benchmark_results.csv',
                       help='Output CSV file for results')
    parser.add_argument('-v', '--verbose', action='store_true', default=True,
                       help='Verbose output')
    parser.add_argument('-seed', '--seed', type=int, default=42, help='Random seed')
    parser.add_argument('-epochs', type=int, default=100, help='Training epochs')
    parser.add_argument('-batch', type=int, default=32, help='Batch size')

    args = parser.parse_args()

    # Load data
    print(f"Loading data from {args.data}")
    data = pd.read_csv(args.data)

    if data.shape[1] < 2:
        print("Error: Need at least 2 columns (features and response)")
        sys.exit(1)

    # Assume last column is response
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1:]

    # Split and scale
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=args.seed)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    X_train = pd.DataFrame(X_train_scaled, columns=X.columns)
    X_test = pd.DataFrame(X_test_scaled, columns=X.columns)

    # Setup hyperparameters
    hparams = {
        'nn_keras_layers': '0.5,0.25',
        'nn_keras_epochs': args.epochs,
        'nn_keras_batch_size': args.batch,
        'nn_keras_optimizer': 'adam',
        'nn_keras_learning_rate': 0.001,
        'nn_keras_loss_function': 'mse',
        'nn_keras_metrics': ['mse'],
        'nn_keras_hid_activation': 'relu',
        'nn_keras_out_activation': 'linear',
    }

    # Run benchmark
    benchmark = WeightDroppingBenchmark(verbose=args.verbose)
    benchmark.run_benchmark(
        X_train, X_test, y_train, y_test,
        hparams,
        drop_percentages=args.drop_percentages,
        seed=args.seed
    )

    # Save and display results
    benchmark.print_results_table()
    benchmark.save_results_csv(args.output)

    print("\nBenchmark complete!")


if __name__ == '__main__':
    main()

