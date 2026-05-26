"""
Comprehensive data analysis of weight dropping, dimension reduction, and rounding effects
on model performance (MSQE, R²) and optimization time.

Generates multiple visualizations and detailed statistical analysis.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr
import warnings

warnings.filterwarnings("ignore")


data = []
with open("project/plot_data.tsv", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        try:
            dim_reduction = float(parts[0])
            weight_drop = float(parts[1])
            rounding = float(parts[2])
            msqe = float(parts[3])
            r2_score_val = float(parts[4])
            time_taken = float(parts[5])

            data.append(
                [dim_reduction, weight_drop, rounding, msqe, r2_score_val, time_taken]
            )
        except (ValueError, IndexError):
            continue

df = pd.DataFrame(
    data,
    columns=[
        "Dimension Reduction",
        "% Of Weights Dropped",
        "Rounding",
        "MSQE",
        "R2",
        "Time",
    ],
)


ind_vars = df[["Dimension Reduction", "% Of Weights Dropped", "Rounding"]]

dep_vars = df[["MSQE", "R2", "Time"]]


corr_matrix = df.corr(method="pearson")

spearman_corr = df.corr(method="spearman")


params = ["Dimension Reduction", "% Of Weights Dropped", "Rounding"]
outcomes = ["MSQE", "R2", "Time"]

for outcome in outcomes:
    print(f"\n{outcome.upper()} - Correlation with parameters:")
    print("-" * 40)
    for param in params:
        pearson_corr, p_val_pearson = pearsonr(df[param], df[outcome])
        spearman_corr, p_val_spearman = spearmanr(df[param], df[outcome])

        print(
            f"  {param:15s}: Pearson={pearson_corr:+.4f} (p={p_val_pearson:.4f}), Spearman={spearman_corr:+.4f} (p={p_val_spearman:.4f})"
        )


dim_groups = df.groupby("Dimension Reduction")[["MSQE", "R2", "Time"]].agg(
    ["mean", "std", "min", "max"]
)

weight_groups = df.groupby("% Of Weights Dropped")[["MSQE", "R2", "Time"]].agg(
    ["mean", "std", "min", "max"]
)

round_groups = df.groupby("Rounding")[["MSQE", "R2", "Time"]].agg(
    ["mean", "std", "min", "max"]
)


best_msqe = df.nsmallest(5, "MSQE")[
    ["Dimension Reduction", "% Of Weights Dropped", "Rounding", "MSQE", "R2", "Time"]
]

best_r2 = df.nlargest(5, "R2")[
    ["Dimension Reduction", "% Of Weights Dropped", "Rounding", "MSQE", "R2", "Time"]
]

fastest = df.nsmallest(5, "Time")[
    ["Dimension Reduction", "% Of Weights Dropped", "Rounding", "MSQE", "R2", "Time"]
]

slowest = df.nlargest(5, "Time")[
    ["Dimension Reduction", "% Of Weights Dropped", "Rounding", "MSQE", "R2", "Time"]
]


fig, axes = plt.subplots(3, 3, figsize=(16, 12))
fig.suptitle(
    "Parameter Effects on Model Performance and Optimization Time",
    fontsize=16,
    fontweight="bold",
)

ax = axes[0, 0]
dim_msqe = df.groupby("Dimension Reduction")["MSQE"].agg(["mean", "std"])
ax.errorbar(
    dim_msqe.index,
    dim_msqe["mean"],
    yerr=dim_msqe["std"],
    marker="o",
    capsize=5,
    linewidth=2,
    markersize=8,
)
ax.set_xlabel("Dimension Reduction (%)", fontsize=11)
ax.set_ylabel("MSQE", fontsize=11)
ax.set_title("MSQE vs Dimension Reduction", fontsize=12, fontweight="bold")
ax.grid(True, alpha=0.3)

ax = axes[0, 1]
dim_r2 = df.groupby("Dimension Reduction")["R2"].agg(["mean", "std"])
ax.errorbar(
    dim_r2.index,
    dim_r2["mean"],
    yerr=dim_r2["std"],
    marker="s",
    capsize=5,
    linewidth=2,
    markersize=8,
    color="green",
)
ax.set_xlabel("Dimension Reduction (%)", fontsize=11)
ax.set_ylabel("R²", fontsize=11)
ax.set_title("R² vs Dimension Reduction", fontsize=12, fontweight="bold")
ax.grid(True, alpha=0.3)

ax = axes[0, 2]
dim_time = df.groupby("Dimension Reduction")["Time"].agg(["mean", "std"])
ax.errorbar(
    dim_time.index,
    dim_time["mean"],
    yerr=dim_time["std"],
    marker="^",
    capsize=5,
    linewidth=2,
    markersize=8,
    color="red",
)
ax.set_xlabel("Dimension Reduction (%)", fontsize=11)
ax.set_ylabel("Time (s)", fontsize=11)
ax.set_title("Time vs Dimension Reduction", fontsize=12, fontweight="bold")
ax.grid(True, alpha=0.3)

ax = axes[1, 0]
wd_msqe = df.groupby("% Of Weights Dropped")["MSQE"].agg(["mean", "std"])
ax.errorbar(
    wd_msqe.index,
    wd_msqe["mean"],
    yerr=wd_msqe["std"],
    marker="o",
    capsize=5,
    linewidth=2,
    markersize=8,
    color="purple",
)
ax.set_xlabel("Weight Dropping (%)", fontsize=11)
ax.set_ylabel("MSQE", fontsize=11)
ax.set_title("MSQE vs Weight Dropping", fontsize=12, fontweight="bold")
ax.grid(True, alpha=0.3)

ax = axes[1, 1]
wd_r2 = df.groupby("% Of Weights Dropped")["R2"].agg(["mean", "std"])
ax.errorbar(
    wd_r2.index,
    wd_r2["mean"],
    yerr=wd_r2["std"],
    marker="s",
    capsize=5,
    linewidth=2,
    markersize=8,
    color="orange",
)
ax.set_xlabel("Weight Dropping (%)", fontsize=11)
ax.set_ylabel("R²", fontsize=11)
ax.set_title("R² vs Weight Dropping", fontsize=12, fontweight="bold")
ax.grid(True, alpha=0.3)

ax = axes[1, 2]
wd_time = df.groupby("% Of Weights Dropped")["Time"].agg(["mean", "std"])
ax.errorbar(
    wd_time.index,
    wd_time["mean"],
    yerr=wd_time["std"],
    marker="^",
    capsize=5,
    linewidth=2,
    markersize=8,
    color="brown",
)
ax.set_xlabel("Weight Dropping (%)", fontsize=11)
ax.set_ylabel("Time (s)", fontsize=11)
ax.set_title("Time vs Weight Dropping", fontsize=12, fontweight="bold")
ax.grid(True, alpha=0.3)

ax = axes[2, 0]
round_msqe = df.groupby("Rounding")["MSQE"].agg(["mean", "std"])
ax.errorbar(
    round_msqe.index,
    round_msqe["mean"],
    yerr=round_msqe["std"],
    marker="o",
    capsize=5,
    linewidth=2,
    markersize=8,
    color="cyan",
)
ax.set_xlabel("Rounding (decimals)", fontsize=11)
ax.set_ylabel("MSQE", fontsize=11)
ax.set_title("MSQE vs Rounding", fontsize=12, fontweight="bold")
ax.grid(True, alpha=0.3)

ax = axes[2, 1]
round_r2 = df.groupby("Rounding")["R2"].agg(["mean", "std"])
ax.errorbar(
    round_r2.index,
    round_r2["mean"],
    yerr=round_r2["std"],
    marker="s",
    capsize=5,
    linewidth=2,
    markersize=8,
    color="magenta",
)
ax.set_xlabel("Rounding (decimals)", fontsize=11)
ax.set_ylabel("R²", fontsize=11)
ax.set_title("R² vs Rounding", fontsize=12, fontweight="bold")
ax.grid(True, alpha=0.3)

ax = axes[2, 2]
round_time = df.groupby("Rounding")["Time"].agg(["mean", "std"])
ax.errorbar(
    round_time.index,
    round_time["mean"],
    yerr=round_time["std"],
    marker="^",
    capsize=5,
    linewidth=2,
    markersize=8,
    color="lime",
)
ax.set_xlabel("Rounding (decimals)", fontsize=11)
ax.set_ylabel("Time (s)", fontsize=11)
ax.set_title("Time vs Rounding", fontsize=12, fontweight="bold")
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("project/analysis_parameter_effects.png", dpi=300, bbox_inches="tight")
plt.close()


fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle("Two-Way Interaction Heatmaps", fontsize=16, fontweight="bold")

pivot_msqe_1 = df.pivot_table(
    values="MSQE",
    index="Dimension Reduction",
    columns="% Of Weights Dropped",
    aggfunc="mean",
)
sns.heatmap(
    pivot_msqe_1,
    annot=True,
    fmt=".4f",
    cmap="RdYlGn_r",
    ax=axes[0, 0],
    cbar_kws={"label": "MSQE"},
)
axes[0, 0].set_title(
    "MSQE: Dimension Reduction × % Of Weights Dropped", fontsize=12, fontweight="bold"
)

pivot_msqe_2 = df.pivot_table(
    values="MSQE", index="Dimension Reduction", columns="Rounding", aggfunc="mean"
)
sns.heatmap(
    pivot_msqe_2,
    annot=True,
    fmt=".4f",
    cmap="RdYlGn_r",
    ax=axes[0, 1],
    cbar_kws={"label": "MSQE"},
)
axes[0, 1].set_title(
    "MSQE: Dimension Reduction × Rounding", fontsize=12, fontweight="bold"
)

pivot_msqe_3 = df.pivot_table(
    values="MSQE", index="% Of Weights Dropped", columns="Rounding", aggfunc="mean"
)
sns.heatmap(
    pivot_msqe_3,
    annot=True,
    fmt=".4f",
    cmap="RdYlGn_r",
    ax=axes[0, 2],
    cbar_kws={"label": "MSQE"},
)
axes[0, 2].set_title(
    "MSQE: % Of Weights Dropped × Rounding", fontsize=12, fontweight="bold"
)

pivot_time_1 = df.pivot_table(
    values="Time",
    index="Dimension Reduction",
    columns="% Of Weights Dropped",
    aggfunc="mean",
)
sns.heatmap(
    pivot_time_1,
    annot=True,
    fmt=".4f",
    cmap="YlOrRd",
    ax=axes[1, 0],
    cbar_kws={"label": "Time (s)"},
)
axes[1, 0].set_title(
    "Time: Dimension Reduction × % Of Weights Dropped", fontsize=12, fontweight="bold"
)

pivot_time_2 = df.pivot_table(
    values="Time", index="Dimension Reduction", columns="Rounding", aggfunc="mean"
)
sns.heatmap(
    pivot_time_2,
    annot=True,
    fmt=".4f",
    cmap="YlOrRd",
    ax=axes[1, 1],
    cbar_kws={"label": "Time (s)"},
)
axes[1, 1].set_title(
    "Time: Dimension Reduction × Rounding", fontsize=12, fontweight="bold"
)

pivot_time_3 = df.pivot_table(
    values="Time", index="% Of Weights Dropped", columns="Rounding", aggfunc="mean"
)
sns.heatmap(
    pivot_time_3,
    annot=True,
    fmt=".4f",
    cmap="YlOrRd",
    ax=axes[1, 2],
    cbar_kws={"label": "Time (s)"},
)
axes[1, 2].set_title(
    "Time: % Of Weights Dropped × Rounding", fontsize=12, fontweight="bold"
)

plt.tight_layout()
plt.savefig("project/analysis_heatmaps.png", dpi=300, bbox_inches="tight")
plt.close()


fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle(
    "Correlations Between Outcomes & Distributions", fontsize=16, fontweight="bold"
)

ax = axes[0, 0]
ax.scatter(df["MSQE"], df["R2"], alpha=0.6, s=50, edgecolors="black", linewidth=0.5)
r, p = pearsonr(df["MSQE"], df["R2"])
ax.set_xlabel("MSQE", fontsize=11)
ax.set_ylabel("R²", fontsize=11)
ax.set_title(f"MSQE vs R² (r={r:.4f}, p={p:.4f})", fontsize=12, fontweight="bold")
ax.grid(True, alpha=0.3)

ax = axes[0, 1]
ax.scatter(
    df["MSQE"],
    df["Time"],
    alpha=0.6,
    s=50,
    color="green",
    edgecolors="black",
    linewidth=0.5,
)
r, p = pearsonr(df["MSQE"], df["Time"])
ax.set_xlabel("MSQE", fontsize=11)
ax.set_ylabel("Time (s)", fontsize=11)
ax.set_title(f"MSQE vs Time (r={r:.4f}, p={p:.4f})", fontsize=12, fontweight="bold")
ax.grid(True, alpha=0.3)

ax = axes[0, 2]
ax.scatter(
    df["R2"],
    df["Time"],
    alpha=0.6,
    s=50,
    color="orange",
    edgecolors="black",
    linewidth=0.5,
)
r, p = pearsonr(df["R2"], df["Time"])
ax.set_xlabel("R²", fontsize=11)
ax.set_ylabel("Time (s)", fontsize=11)
ax.set_title(f"R² vs Time (r={r:.4f}, p={p:.4f})", fontsize=12, fontweight="bold")
ax.grid(True, alpha=0.3)

ax = axes[1, 0]
ax.hist(df["MSQE"], bins=20, edgecolor="black", alpha=0.7, color="skyblue")
ax.set_xlabel("MSQE", fontsize=11)
ax.set_ylabel("Frequency", fontsize=11)
ax.set_title(
    f"MSQE Distribution (μ={df['MSQE'].mean():.4f}, σ={df['MSQE'].std():.4f})",
    fontsize=12,
    fontweight="bold",
)
ax.grid(True, alpha=0.3, axis="y")

ax = axes[1, 1]
ax.hist(df["R2"], bins=20, edgecolor="black", alpha=0.7, color="lightgreen")
ax.set_xlabel("R²", fontsize=11)
ax.set_ylabel("Frequency", fontsize=11)
ax.set_title(
    f"R² Distribution (μ={df['R2'].mean():.4f}, σ={df['R2'].std():.4f})",
    fontsize=12,
    fontweight="bold",
)
ax.grid(True, alpha=0.3, axis="y")

ax = axes[1, 2]
ax.hist(df["Time"], bins=20, edgecolor="black", alpha=0.7, color="lightyellow")
ax.set_xlabel("Time (s)", fontsize=11)
ax.set_ylabel("Frequency", fontsize=11)
ax.set_title(
    f"Time Distribution (μ={df['Time'].mean():.4f}, σ={df['Time'].std():.4f})",
    fontsize=12,
    fontweight="bold",
)
ax.grid(True, alpha=0.3, axis="y")

plt.tight_layout()
plt.savefig("project/analysis_correlations.png", dpi=300, bbox_inches="tight")
plt.close()


fig, axes = plt.subplots(3, 3, figsize=(16, 12))
fig.suptitle(
    "Distribution of Outcomes by Parameter Values", fontsize=16, fontweight="bold"
)

dim_vals = sorted(df["Dimension Reduction"].unique())
ax = axes[0, 0]
df.boxplot(column="MSQE", by="Dimension Reduction", ax=ax)
ax.set_xlabel("Dimension Reduction (%)", fontsize=11)
ax.set_ylabel("MSQE", fontsize=11)
ax.set_title("MSQE by Dimension Reduction", fontsize=12, fontweight="bold")
plt.sca(ax)
plt.xticks(rotation=0)

ax = axes[0, 1]
df.boxplot(column="R2", by="Dimension Reduction", ax=ax)
ax.set_xlabel("Dimension Reduction (%)", fontsize=11)
ax.set_ylabel("R²", fontsize=11)
ax.set_title("R² by Dimension Reduction", fontsize=12, fontweight="bold")
plt.sca(ax)
plt.xticks(rotation=0)

ax = axes[0, 2]
df.boxplot(column="Time", by="Dimension Reduction", ax=ax)
ax.set_xlabel("Dimension Reduction (%)", fontsize=11)
ax.set_ylabel("Time (s)", fontsize=11)
ax.set_title("Time by Dimension Reduction", fontsize=12, fontweight="bold")
plt.sca(ax)
plt.xticks(rotation=0)

ax = axes[1, 0]
df.boxplot(column="MSQE", by="% Of Weights Dropped", ax=ax)
ax.set_xlabel("Weight Dropping (%)", fontsize=11)
ax.set_ylabel("MSQE", fontsize=11)
ax.set_title("MSQE by % Of Weights Dropped", fontsize=12, fontweight="bold")
plt.sca(ax)
plt.xticks(rotation=0)

ax = axes[1, 1]
df.boxplot(column="R2", by="% Of Weights Dropped", ax=ax)
ax.set_xlabel("Weight Dropping (%)", fontsize=11)
ax.set_ylabel("R²", fontsize=11)
ax.set_title("R² by % Of Weights Dropped", fontsize=12, fontweight="bold")
plt.sca(ax)
plt.xticks(rotation=0)

ax = axes[1, 2]
df.boxplot(column="Time", by="% Of Weights Dropped", ax=ax)
ax.set_xlabel("Weight Dropping (%)", fontsize=11)
ax.set_ylabel("Time (s)", fontsize=11)
ax.set_title("Time by % Of Weights Dropped", fontsize=12, fontweight="bold")
plt.sca(ax)
plt.xticks(rotation=0)

ax = axes[2, 0]
df.boxplot(column="MSQE", by="Rounding", ax=ax)
ax.set_xlabel("Rounding (decimals)", fontsize=11)
ax.set_ylabel("MSQE", fontsize=11)
ax.set_title("MSQE by Rounding", fontsize=12, fontweight="bold")
plt.sca(ax)
plt.xticks(rotation=0)

ax = axes[2, 1]
df.boxplot(column="R2", by="Rounding", ax=ax)
ax.set_xlabel("Rounding (decimals)", fontsize=11)
ax.set_ylabel("R²", fontsize=11)
ax.set_title("R² by Rounding", fontsize=12, fontweight="bold")
plt.sca(ax)
plt.xticks(rotation=0)

ax = axes[2, 2]
df.boxplot(column="Time", by="Rounding", ax=ax)
ax.set_xlabel("Rounding (decimals)", fontsize=11)
ax.set_ylabel("Time (s)", fontsize=11)
ax.set_title("Time by Rounding", fontsize=12, fontweight="bold")
plt.sca(ax)
plt.xticks(rotation=0)

plt.suptitle("")  # Remove automatic title
plt.tight_layout()
plt.savefig("project/analysis_boxplots.png", dpi=300, bbox_inches="tight")
plt.close()


corr_flat = corr_matrix.unstack()
corr_flat = corr_flat[corr_flat != 1.0]  # Remove self-correlations
strongest = corr_flat.abs().nlargest(10)
for idx, val in strongest.items():
    print(f"  {idx[0]:15s} ← → {idx[1]:15s}: {val:+.4f}")

for outcome in outcomes:
    print(f"\n  {outcome}:")
    impact = {}
    for param in params:
        corr_val, _ = pearsonr(df[param], df[outcome])
        impact[param] = abs(corr_val)

    sorted_impact = sorted(impact.items(), key=lambda x: x[1], reverse=True)
    for param, corr_abs in sorted_impact:
        print(f"    {param:15s}: {corr_abs:.4f}")

for param in params:
    for outcome in outcomes:
        groups = df.groupby(param)[outcome].mean()
        between_var = np.var(groups)
        total_var = np.var(df[outcome])
        r2_explained = between_var / total_var if total_var > 0 else 0
        print(f"  {param:15s} explains {r2_explained:6.2%} of {outcome:5s} variance")

df["norm_msqe"] = (df["MSQE"] - df["MSQE"].min()) / (
    df["MSQE"].max() - df["MSQE"].min()
)
df["norm_r2_neg"] = (1 - df["R2"]) / (1 - df["R2"].min())  # Lower is better
df["norm_time"] = (df["Time"] - df["Time"].min()) / (
    df["Time"].max() - df["Time"].min()
)
df["balanced_score"] = (df["norm_msqe"] + df["norm_r2_neg"] + df["norm_time"]) / 3

optimal_idx = df["balanced_score"].idxmin()
optimal_config = df.loc[optimal_idx]
