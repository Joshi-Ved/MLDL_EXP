# Exp 6: Pollution + Clustering Explanation

## What Was Done

1. Loaded `Mall_Customers.csv`.
2. Polluted the clean data in two ways:
- Added Gaussian noise to `Age`, `Annual Income (k$)`, and `Spending Score (1-100)`.
- Added synthetic outlier rows (about 6% extra samples) with extreme values.
3. Standardized numerical features before clustering.
4. Scanned `k=2..8` using silhouette score and selected the best `k`.
5. Applied:
- K-Means clustering.
- Hierarchical Agglomerative clustering (Ward linkage).
6. Saved results:
- `Mall_Customers_polluted.csv` (after noise + outliers)
- `Mall_Customers_polluted_clustered.csv` (with both cluster labels)
- `cluster_comparison_polluted.png` (visual comparison)

## Why These Particular Choices Were Selected

- Feature set (`Age`, `Annual Income`, `Spending Score`):
  This is the common segmentation space for this dataset and avoids IDs and raw category labels for clustering.

- Gaussian noise:
  Real-world sensors and data entry usually create small random perturbations, which Gaussian noise approximates well.

- Outlier injection:
  Many practical datasets contain rare or extreme customers; this tests model robustness under non-ideal conditions.

- StandardScaler:
  Distance-based methods (K-Means, Ward hierarchical clustering) are sensitive to feature scale. Standardization prevents one feature from dominating distance.

- Silhouette-based `k` selection:
  Instead of fixing `k` manually, silhouette gives a quantitative, unsupervised way to pick cluster count.

- Ward linkage for hierarchical clustering:
  Ward minimizes within-cluster variance and often gives compact, interpretable clusters on numeric data.

## What You Should Observe

- Pollution usually lowers cluster quality and can reduce silhouette score.
- K-Means may shift centroids toward outliers because it optimizes squared distances.
- Hierarchical clustering can produce different boundaries and may react differently to outliers.

## How We Can Improve This Experiment

1. Use robust preprocessing:
- Replace StandardScaler with RobustScaler.
- Cap extreme values with winsorization or IQR clipping before clustering.

2. Improve outlier handling:
- Detect outliers with Isolation Forest or Local Outlier Factor.
- Run clustering with and without detected outliers and compare quality.

3. Better model selection:
- Evaluate with multiple metrics: silhouette, Calinski-Harabasz, Davies-Bouldin.
- Use stability checks by repeating experiments with different random seeds.

4. Try alternative clustering methods:
- DBSCAN or HDBSCAN for noise-aware clustering.
- Gaussian Mixture Models for soft/probabilistic clusters.

5. Better feature engineering:
- Encode `Gender` and test whether it improves separation.
- Use PCA for visualization and denoising.

## How To Run

Run this from the project root:

```powershell
python Exp_6/clustering_polluted.py
```

If your environment is activated, this command will generate all outputs automatically.
