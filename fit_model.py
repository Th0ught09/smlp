#!/usr/bin/env python3
"""
Fit a model to the plot data using columns 1, 2, 3 as inputs and column 6 as output.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt

# Read the data
data = []
with open('project/plot_data.tsv', 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        
        # Split by whitespace to get first 3 columns
        parts = line.split()
        col1 = float(parts[0])
        col2 = float(parts[1])
        col3 = float(parts[2])
        
        # The rest is a comma-separated list of floats
        # Rejoin everything after column 3 and split by comma
        rest = ' '.join(parts[3:])
        values = [float(x.strip().rstrip(',')) for x in rest.split(',') if x.strip()]
        
        # Column 6 is at index 5 (0-indexed)
        if len(values) > 5:
            col6_value = values[5]
            data.append([col1, col2, col3, col6_value])

# Convert to DataFrame
df = pd.DataFrame(data, columns=['X1', 'X2', 'X3', 'Y'])

print("Data shape:", df.shape)
print("\nFirst few rows:")
print(df.head(10))
print("\nData statistics:")
print(df.describe())

# Split features and target
X = df[['X1', 'X2', 'X3']].values
y = df['Y'].values

# Split into train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\n" + "="*60)
print("MODEL FITTING RESULTS")
print("="*60)

# 1. Linear Regression
print("\n1. LINEAR REGRESSION")
print("-" * 40)
lr = LinearRegression()
lr.fit(X_train_scaled, y_train)
y_pred_lr = lr.predict(X_test_scaled)

mse_lr = mean_squared_error(y_test, y_pred_lr)
rmse_lr = np.sqrt(mse_lr)
mae_lr = mean_absolute_error(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr)

print(f"MSE:  {mse_lr:.6f}")
print(f"RMSE: {rmse_lr:.6f}")
print(f"MAE:  {mae_lr:.6f}")
print(f"R²:   {r2_lr:.6f}")
print(f"Coefficients: {lr.coef_}")
print(f"Intercept: {lr.intercept_}")

# 2. Random Forest Regressor
print("\n2. RANDOM FOREST REGRESSOR")
print("-" * 40)
rf = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
rf.fit(X_train, y_train)  # RF doesn't need scaling
y_pred_rf = rf.predict(X_test)

mse_rf = mean_squared_error(y_test, y_pred_rf)
rmse_rf = np.sqrt(mse_rf)
mae_rf = mean_absolute_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print(f"MSE:  {mse_rf:.6f}")
print(f"RMSE: {rmse_rf:.6f}")
print(f"MAE:  {mae_rf:.6f}")
print(f"R²:   {r2_rf:.6f}")
print(f"Feature importance: X1={rf.feature_importances_[0]:.4f}, X2={rf.feature_importances_[1]:.4f}, X3={rf.feature_importances_[2]:.4f}")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Linear Regression plots
axes[0, 0].scatter(y_test, y_pred_lr, alpha=0.6)
axes[0, 0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
axes[0, 0].set_xlabel('Actual')
axes[0, 0].set_ylabel('Predicted')
axes[0, 0].set_title(f'Linear Regression (R² = {r2_lr:.4f})')
axes[0, 0].grid(True, alpha=0.3)

# Random Forest plots
axes[0, 1].scatter(y_test, y_pred_rf, alpha=0.6, color='green')
axes[0, 1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
axes[0, 1].set_xlabel('Actual')
axes[0, 1].set_ylabel('Predicted')
axes[0, 1].set_title(f'Random Forest (R² = {r2_rf:.4f})')
axes[0, 1].grid(True, alpha=0.3)

# Residuals for Linear Regression
residuals_lr = y_test - y_pred_lr
axes[1, 0].scatter(y_pred_lr, residuals_lr, alpha=0.6)
axes[1, 0].axhline(y=0, color='r', linestyle='--', lw=2)
axes[1, 0].set_xlabel('Predicted')
axes[1, 0].set_ylabel('Residuals')
axes[1, 0].set_title('Linear Regression Residuals')
axes[1, 0].grid(True, alpha=0.3)

# Residuals for Random Forest
residuals_rf = y_test - y_pred_rf
axes[1, 1].scatter(y_pred_rf, residuals_rf, alpha=0.6, color='green')
axes[1, 1].axhline(y=0, color='r', linestyle='--', lw=2)
axes[1, 1].set_xlabel('Predicted')
axes[1, 1].set_ylabel('Residuals')
axes[1, 1].set_title('Random Forest Residuals')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('project/model_fit_analysis.png', dpi=150, bbox_inches='tight')
print("\n✓ Visualization saved to: project/model_fit_analysis.png")

# Summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
if r2_rf > r2_lr:
    print(f"✓ Random Forest performs better (R² = {r2_rf:.6f} vs {r2_lr:.6f})")
else:
    print(f"✓ Linear Regression performs better (R² = {r2_lr:.6f} vs {r2_rf:.6f})")

print("\nBest model on test set:")
best_model_name = "Random Forest" if r2_rf > r2_lr else "Linear Regression"
best_r2 = max(r2_rf, r2_lr)
best_rmse = rmse_rf if r2_rf > r2_lr else rmse_lr
print(f"  Model: {best_model_name}")
print(f"  R² Score: {best_r2:.6f}")
print(f"  RMSE: {best_rmse:.6f}")

