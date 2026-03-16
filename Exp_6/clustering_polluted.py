import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


RANDOM_STATE = 42
NOISE_STD = {
    "Age": 3.0,
    "Annual Income (k$)": 4.0,
    "Spending Score (1-100)": 8.0,
}
OUTLIER_FRACTION = 0.06


def add_noise_and_outliers(df: pd.DataFrame, random_state: int = RANDOM_STATE) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)
    polluted = df.copy()

    # Add Gaussian perturbation to selected numeric columns.
    for col, std in NOISE_STD.items():
        polluted[col] = polluted[col] + rng.normal(0.0, std, size=len(polluted))

    # Inject synthetic outlier rows with extreme but plausible ranges.
    outlier_count = max(1, int(len(polluted) * OUTLIER_FRACTION))
    outliers = pd.DataFrame(
        {
            "CustomerID": np.arange(polluted["CustomerID"].max() + 1, polluted["CustomerID"].max() + 1 + outlier_count),
            "Gender": rng.choice(["Male", "Female"], size=outlier_count),
            "Age": rng.integers(15, 80, size=outlier_count),
            "Annual Income (k$)": rng.integers(5, 180, size=outlier_count),
            "Spending Score (1-100)": rng.integers(1, 100, size=outlier_count),
        }
    )

    polluted = pd.concat([polluted, outliers], ignore_index=True)

    # Keep values in known domain bounds.
    polluted["Age"] = polluted["Age"].clip(15, 80)
    polluted["Annual Income (k$)"] = polluted["Annual Income (k$)"].clip(5, 180)
    polluted["Spending Score (1-100)"] = polluted["Spending Score (1-100)"].clip(1, 100)

    return polluted


def choose_k_with_silhouette(X_scaled: np.ndarray, k_min: int = 2, k_max: int = 8) -> tuple[int, dict[int, float]]:
    scores: dict[int, float] = {}
    for k in range(k_min, k_max + 1):
        model = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=20)
        labels = model.fit_predict(X_scaled)
        scores[k] = silhouette_score(X_scaled, labels)

    best_k = max(scores, key=scores.get)
    return best_k, scores


def plot_cluster_comparison(df: pd.DataFrame, output_path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), constrained_layout=True)

    axes[0].scatter(
        df["Annual Income (k$)"],
        df["Spending Score (1-100)"],
        c=df["KMeansCluster"],
        cmap="tab10",
        s=35,
        alpha=0.85,
    )
    axes[0].set_title("K-Means on Polluted Data")
    axes[0].set_xlabel("Annual Income (k$)")
    axes[0].set_ylabel("Spending Score (1-100)")

    axes[1].scatter(
        df["Annual Income (k$)"],
        df["Spending Score (1-100)"],
        c=df["HierarchicalCluster"],
        cmap="tab10",
        s=35,
        alpha=0.85,
    )
    axes[1].set_title("Hierarchical (Ward) on Polluted Data")
    axes[1].set_xlabel("Annual Income (k$)")
    axes[1].set_ylabel("Spending Score (1-100)")

    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    input_csv = base_dir / "Mall_Customers.csv"
    polluted_csv = base_dir / "Mall_Customers_polluted.csv"
    clustered_csv = base_dir / "Mall_Customers_polluted_clustered.csv"
    figure_path = base_dir / "cluster_comparison_polluted.png"

    df = pd.read_csv(input_csv)
    polluted = add_noise_and_outliers(df)
    polluted.to_csv(polluted_csv, index=False)

    feature_cols = ["Age", "Annual Income (k$)", "Spending Score (1-100)"]
    X = polluted[feature_cols].to_numpy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    best_k, silhouette_map = choose_k_with_silhouette(X_scaled)

    kmeans = KMeans(n_clusters=best_k, random_state=RANDOM_STATE, n_init=20)
    polluted["KMeansCluster"] = kmeans.fit_predict(X_scaled)

    hierarchical = AgglomerativeClustering(n_clusters=best_k, linkage="ward")
    polluted["HierarchicalCluster"] = hierarchical.fit_predict(X_scaled)

    km_score = silhouette_score(X_scaled, polluted["KMeansCluster"])
    hc_score = silhouette_score(X_scaled, polluted["HierarchicalCluster"])

    polluted.to_csv(clustered_csv, index=False)
    plot_cluster_comparison(polluted, figure_path)

    print("Polluted data saved to:", polluted_csv)
    print("Clustered polluted data saved to:", clustered_csv)
    print("Cluster plot saved to:", figure_path)
    print("Selected k (via silhouette scan):", best_k)
    print("Silhouette scores by k:", {k: round(v, 4) for k, v in silhouette_map.items()})
    print("K-Means silhouette:", round(km_score, 4))
    print("Hierarchical silhouette:", round(hc_score, 4))


if __name__ == "__main__":
    main()
