import json
from pathlib import Path

root = Path(r"c:\Users\heram\Desktop\MLDL_EXP")
notebooks = [
    r"Exp_0\exp_1.ipynb",
    r"Exp_0\MLDL Exp_1.ipynb",
    r"Exp_0\regression_models_experiment.ipynb",
    r"Exp1_2\1_Linear_Logistic_Regression.ipynb",
    r"Exp1_2\2_Multi_Lasso_Ridge_Regression.ipynb",
    r"Exp3\heart_disease_classification.ipynb",
    r"Exp_4\knn_iris_classification.ipynb",
    r"Exp_5\svm_classification_notebook.ipynb",
    r"Exp_5\svm_classification_notebook_executed.ipynb",
    r"Exp_5\svm_classification_notebook_visualized.ipynb",
    r"Exp_6\clustering_polluted.ipynb",
    r"Exp_7\ann_notebook.ipynb",
    r"Exp_8\cnn_notebook.ipynb",
    r"Exp_8\fashion_mnist_cnn.ipynb",
    r"Exp_9\rnn_lstm_timeseries.ipynb",
    r"Exp_10\autoencoders_denoising.ipynb",
]

results = []

try:
    import nbformat
    from nbconvert.preprocessors import ExecutePreprocessor
except Exception as e:
    print(json.dumps({"fatal": f"Cannot import notebook execution deps: {e}"}, indent=2))
    raise SystemExit(1)

for rel in notebooks:
    p = root / rel
    item = {"path": rel}
    if not p.exists():
        item["status"] = "missing"
        item["output"] = "file not found"
        results.append(item)
        continue

    try:
        with p.open("r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)

        ep = ExecutePreprocessor(timeout=300, kernel_name="python3", allow_errors=False)
        ep.preprocess(nb, {"metadata": {"path": str(p.parent)}})

        texts = []
        for c in nb.cells:
            if c.get("cell_type") != "code":
                continue
            for out in c.get("outputs", []):
                if out.get("output_type") == "stream":
                    t = out.get("text", "")
                    if t:
                        texts.append(t)
                elif out.get("output_type") == "execute_result":
                    t = out.get("data", {}).get("text/plain", "")
                    if t:
                        texts.append(t)
        item["status"] = "success"
        joined = "\n".join(texts).strip()
        item["output"] = joined[-1200:] if joined else "(no text output; likely visual-only)"
    except Exception as e:
        item["status"] = "failed"
        item["output"] = f"{type(e).__name__}: {e}"

    results.append(item)

print(json.dumps(results, indent=2, ensure_ascii=True))
