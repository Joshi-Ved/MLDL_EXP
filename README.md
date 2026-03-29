# Deep Learning Experiments: ANN & CNN

## Overview
This package contains two comprehensive machine learning experiments focused on deep neural networks:
- **Exp_7**: Artificial Neural Networks (ANN) with Keras/TensorFlow
- **Exp_8**: Convolutional Neural Networks (CNN) on Image Datasets

---

## 📁 Exp_7: Artificial Neural Network (ANN)

### Purpose
Explore and implement Artificial Neural Networks for classification tasks, with focus on:
- Network architecture design
- Regularization techniques
- Hyperparameter optimization
- Performance comparison

### Structure
```
Exp_7/
├── ann_notebook.ipynb           # Complete Jupyter notebook
├── ann_classification.py         # Standalone Python script
├── plan.md                       # Detailed documentation
└── (Models saved during execution)
```

### Key Components

**1. Datasets Used**
- **Iris Dataset**: 4 features, 3 classes (classic ML benchmark)
- **Digits Dataset**: 64 features, 10 classes (from sklearn)

**2. Models Implemented**
| Model | Architecture | Features | Best For |
|-------|--------------|----------|----------|
| Simple ANN | 4→64→32→3 | Baseline | Quick prototyping |
| Advanced ANN | 4→128→64→32→3 | Dropout, BatchNorm | Iris classification |
| Deep ANN | 64→256→128→64→32→10 | Multiple layers | Complex datasets |

**3. Regularization Techniques**
- **Dropout**: Prevents overfitting (0.2-0.4 rate)
- **Batch Normalization**: Normalizes layer inputs
- **Early Stopping**: Prevents overtraining
- **Learning Rate Scheduling**: Adaptive learning

### Expected Results
```
Simple ANN   → ~95% test accuracy on Iris
Advanced ANN → ~97% test accuracy on Iris  
Deep ANN     → ~97% test accuracy on Digits
```

### Quick Start
```python
# Using the script
python ann_classification.py

# In notebook
jupyter notebook ann_notebook.ipynb
# Run all cells for complete analysis
```

---

## 📁 Exp_8: Convolutional Neural Network (CNN)

### Purpose
Build and train CNNs on image datasets with focus on:
- Convolutional operations
- Image data preprocessing
- Data augmentation
- Dataset complexity comparison

### Structure
```
Exp_8/
├── cnn_notebook.ipynb           # Complete Jupyter notebook
├── cnn_classification.py         # Standalone Python script
├── plan.md                       # Detailed documentation
└── (Models saved during execution)
```

### Datasets

**MNIST**
- 70,000 images (60k train, 10k test)
- 28×28 grayscale images
- 10 digit classes (0-9)
- Relatively simple dataset

**CIFAR-10**
- 60,000 images (50k train, 10k test)
- 32×32 RGB images
- 10 object classes
- More complex, real-world data

### Models Implemented
| Model | Dataset | Architecture | Features |
|-------|---------|--------------|----------|
| Simple CNN | MNIST | Conv32→Conv64→FC | Baseline |
| Advanced CNN | MNIST | 2×Conv Blocks | BatchNorm, Dropout |
| Deep CNN | CIFAR-10 | 3×Conv Blocks | Extensive Regularization |

### CNN Architecture Details
```
Simple CNN (MNIST):
  Conv2D(32) → MaxPool → Conv2D(64) → MaxPool → Flatten → Dense(128) → Dense(10)

Advanced CNN (MNIST):
  [Conv32 → BN → Conv32 → BN → Pool → Dropout]×2 → FC(256) → FC(128) → Output

Deep CNN (CIFAR-10):
  [Conv32→BN→Conv32→BN→Pool→Dropout] → [Conv64→...] → [Conv128→...] → FC → Output
```

### Expected Results
```
Simple CNN (MNIST)    → ~98% test accuracy
Advanced CNN (MNIST)  → ~99% test accuracy
Deep CNN (CIFAR-10)   → ~85-90% test accuracy
```

### Data Augmentation
```python
# MNIST Augmentation
- Rotation: ±10°
- Width shift: 10%
- Height shift: 10%
- Zoom: 20%

# CIFAR-10 Augmentation (more aggressive)
- Rotation: ±20°
- Width shift: 20%
- Height shift: 20%
- Horizontal flip: Yes
- Zoom: 20%
```

### Quick Start
```python
# Using the script
python cnn_classification.py

# In notebook
jupyter notebook cnn_notebook.ipynb
# Run all cells to train models
```

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install tensorflow>=2.10
pip install keras>=2.10
pip install numpy pandas matplotlib seaborn scikit-learn
```

### Installation
The datasets (MNIST, CIFAR-10) are automatically downloaded by TensorFlow on first use.

### Running Experiments

**Option 1: Jupyter Notebooks (Recommended)**
```bash
cd c:\Users\heram\Desktop\MLDL_EXP\Exp_7
jupyter notebook ann_notebook.ipynb

cd c:\Users\heram\Desktop\MLDL_EXP\Exp_8
jupyter notebook cnn_notebook.ipynb
```

**Option 2: Python Scripts**
```bash
cd Exp_7
python ann_classification.py

cd Exp_8
python cnn_classification.py
```

---

## 📊 Outputs

### Generated Artifacts

**Exp_7**
- `training_history_*.png` - Training/validation curves
- `ann_comparison.png` - Model performance comparison
- `best_ann_*.keras` - Saved model weights

**Exp_8**
- `cnn_training_history_*.png` - Training/validation curves
- `confusion_matrix_*.png` - Classification matrices
- `best_cnn_*.keras` - Saved model weights

---

## 🔬 Key Concepts

### Neural Networks (Exp_7)
```
Input Layer → Hidden Layers → Output Layer
              ↓
        Dense connections
        Activation functions (ReLU, Softmax)
        Regularization (Dropout, BatchNorm)
```

### Convolutional Networks (Exp_8)
```
Input Image → Conv Filters → Feature Maps → Pooling → Fully Connected
              ↓
        Parameter sharing
        Local connectivity
        Spatial structure preservation
```

### Optimization Techniques
- **Adam Optimizer**: Adaptive learning rates
- **Early Stopping**: Monitor validation loss
- **Learning Rate Reduction**: 0.5× factor on plateau
- **Batch Normalization**: Normalize activations
- **Dropout**: Random neuron deactivation

---

## 📈 Visualization Features

Both experiments include:
1. **Training History**: Accuracy and loss curves
2. **Confusion Matrix**: Classification performance per class
3. **Model Comparison**: Performance across architectures
4. **Sample Visualization**: Show sample predictions
5. **Classification Report**: Precision, recall, F1-score

---

## 🎯 Advanced Exercises

### Exp_7 (ANN) Extensions
1. Implement L1/L2 regularization
2. Test different optimizers (SGD, RMSprop, Nadam)
3. Grid search for hyperparameters
4. Cross-validation implementation
5. Custom activation functions
6. Neural network visualization (heatmaps)

### Exp_8 (CNN) Extensions
1. Implement ResNet or VGG architectures
2. Transfer learning with ImageNet
3. Gradient-based visualization (CAM)
4. Test with other datasets (Fashion-MNIST, SVHN)
5. Experiment with different kernel sizes
6. Depthwise separable convolutions

---

## 📚 Learning Resources

### Concepts Covered
- Forward and backward propagation
- Convolutional operations
- Pooling and downsampling
- Regularization techniques
- Optimization algorithms
- Data augmentation
- Model evaluation metrics

### Theory References
- Neural Networks: http://neuralnetworksanddeeplearning.com/
- ConvNets: https://cs231n.github.io/
- TensorFlow Docs: https://www.tensorflow.org/

---

## 🔧 Troubleshooting

### Common Issues

**Memory Issues**
```python
# Reduce batch size
batch_size = 32  # instead of 128

# Reduce model complexity
model = create_simple_ann()  # instead of deep
```

**Slow Training**
```python
# Use GPU
physical_devices = tf.config.list_physical_devices('GPU')
print(physical_devices)

# Reduce epochs
epochs = 10  # test run
```

**Dataset Download Errors**
```python
# Manual download:
# MNIST: keras.datasets.mnist.load_data()
# CIFAR-10: keras.datasets.cifar10.load_data()
```

---

## 📝 Notes

### Exp_7 (ANN)
- Iris dataset is small but well-structured
- Deep networks may overfit on small datasets
- Regularization is crucial
- Early stopping prevents overtraining

### Exp_8 (CNN)
- MNIST is too simple for deep CNNs (overengineering)
- CIFAR-10 benefits from deeper architectures
- Data augmentation essential for limited data
- GPU acceleration recommended for large models

---

## ✅ Experiment Checklist

- [ ] Install required packages
- [ ] Run Exp_7 (ANN) notebook
- [ ] Review ANN results and visualizations
- [ ] Run Exp_8 (CNN) notebook
- [ ] Review CNN results and visualizations
- [ ] Compare model architectures
- [ ] Save best performing models
- [ ] Experiment with hyperparameters
- [ ] Test on additional datasets

---

## 📞 Support

For issues with:
- **TensorFlow/Keras**: https://stackoverflow.com/questions/tagged/tensorflow
- **Deep Learning**: https://discuss.pytorch.org/
- **Datasets**: https://www.kaggle.com/

---

**Created**: March 2026
**Framework**: TensorFlow 2.x / Keras
**Status**: Ready for experimentation ✅
