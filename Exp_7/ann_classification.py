"""
Artificial Neural Network (ANN) Implementation
Complete Python Script for Training and Evaluation
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris, load_digits
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.optimizers import Adam, SGD, RMSprop
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
import warnings
warnings.filterwarnings('ignore')


class ANNClassifier:
    """Artificial Neural Network Classifier"""
    
    def __init__(self, input_dim, num_classes, architecture='advanced'):
        """
        Initialize ANN Classifier
        
        Args:
            input_dim: Input dimension
            num_classes: Number of classes
            architecture: 'simple', 'advanced', or 'deep'
        """
        self.input_dim = input_dim
        self.num_classes = num_classes
        self.architecture = architecture
        self.model = None
        self.history = None
        self.scaler = StandardScaler()
        
    def build_model(self):
        """Build ANN model based on architecture"""
        if self.architecture == 'simple':
            self.model = self._build_simple()
        elif self.architecture == 'advanced':
            self.model = self._build_advanced()
        elif self.architecture == 'deep':
            self.model = self._build_deep()
        else:
            raise ValueError(f"Unknown architecture: {self.architecture}")
            
    def _build_simple(self):
        """Build simple ANN"""
        model = models.Sequential([
            Dense(64, activation='relu', input_shape=(self.input_dim,)),
            Dense(32, activation='relu'),
            Dense(self.num_classes, activation='softmax')
        ])
        return model
    
    def _build_advanced(self):
        """Build advanced ANN with regularization"""
        model = models.Sequential([
            Dense(128, activation='relu', input_shape=(self.input_dim,)),
            BatchNormalization(),
            Dropout(0.3),
            
            Dense(64, activation='relu'),
            BatchNormalization(),
            Dropout(0.3),
            
            Dense(32, activation='relu'),
            BatchNormalization(),
            Dropout(0.2),
            
            Dense(self.num_classes, activation='softmax')
        ])
        return model
    
    def _build_deep(self):
        """Build deep ANN"""
        model = models.Sequential([
            Dense(256, activation='relu', input_shape=(self.input_dim,)),
            BatchNormalization(),
            Dropout(0.4),
            
            Dense(128, activation='relu'),
            BatchNormalization(),
            Dropout(0.3),
            
            Dense(64, activation='relu'),
            BatchNormalization(),
            Dropout(0.2),
            
            Dense(32, activation='relu'),
            Dropout(0.2),
            
            Dense(self.num_classes, activation='softmax')
        ])
        return model
    
    def compile_model(self, optimizer='adam', learning_rate=0.001):
        """Compile model"""
        if optimizer == 'adam':
            opt = Adam(learning_rate=learning_rate)
        elif optimizer == 'sgd':
            opt = SGD(learning_rate=learning_rate)
        elif optimizer == 'rmsprop':
            opt = RMSprop(learning_rate=learning_rate)
        else:
            opt = optimizer
            
        self.model.compile(
            optimizer=opt,
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
    
    def fit(self, X_train, y_train, epochs=100, batch_size=32, 
            validation_split=0.2, early_stopping=True, verbose=1):
        """Train model"""
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Prepare callbacks
        cb_list = []
        if early_stopping:
            cb_list.append(callbacks.EarlyStopping(
                monitor='val_loss',
                patience=15,
                restore_best_weights=True
            ))
            cb_list.append(callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7
            ))
        
        # Train
        self.history = self.model.fit(
            X_train_scaled, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            callbacks=cb_list,
            verbose=verbose
        )
        
        return self.history
    
    def evaluate(self, X_test, y_test):
        """Evaluate model"""
        X_test_scaled = self.scaler.transform(X_test)
        loss, accuracy = self.model.evaluate(X_test_scaled, y_test, verbose=0)
        return loss, accuracy
    
    def predict(self, X):
        """Make predictions"""
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def save_model(self, filepath):
        """Save model"""
        self.model.save(filepath)
        print(f"Model saved to {filepath}")
    
    def plot_training_history(self):
        """Plot training history"""
        if self.history is None:
            print("No training history available")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 4))
        
        # Accuracy
        axes[0].plot(self.history.history['accuracy'], label='Training', linewidth=2)
        axes[0].plot(self.history.history['val_accuracy'], label='Validation', linewidth=2)
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Accuracy')
        axes[0].set_title(f'{self.architecture.upper()} ANN - Accuracy')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Loss
        axes[1].plot(self.history.history['loss'], label='Training', linewidth=2)
        axes[1].plot(self.history.history['val_loss'], label='Validation', linewidth=2)
        axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('Loss')
        axes[1].set_title(f'{self.architecture.upper()} ANN - Loss')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'training_history_{self.architecture}.png', dpi=300, bbox_inches='tight')
        plt.show()


def main():
    """Main execution"""
    print("=" * 60)
    print("ARTIFICIAL NEURAL NETWORK (ANN) - COMPREHENSIVE EXPERIMENT")
    print("=" * 60)
    
    # Load Iris dataset
    print("\n1. Loading Iris Dataset...")
    iris = load_iris()
    X = iris.data
    y = iris.target
    print(f"   Dataset Shape: {X.shape}")
    print(f"   Number of Classes: {len(np.unique(y))}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # One-hot encode
    y_train_enc = keras.utils.to_categorical(y_train)
    y_test_enc = keras.utils.to_categorical(y_test)
    
    # Train models
    architectures = ['simple', 'advanced', 'deep']
    results = {}
    
    for arch in architectures:
        print(f"\n2. Training {arch.upper()} ANN...")
        ann = ANNClassifier(input_dim=4, num_classes=3, architecture=arch)
        ann.build_model()
        ann.compile_model()
        ann.fit(X_train, y_train_enc, epochs=150, batch_size=32, verbose=0)
        
        train_loss, train_acc = ann.evaluate(X_train, y_train_enc)
        test_loss, test_acc = ann.evaluate(X_test, y_test_enc)
        
        results[arch] = {
            'train_acc': train_acc,
            'test_acc': test_acc,
            'train_loss': train_loss,
            'test_loss': test_loss,
            'model': ann
        }
        
        print(f"   Train Accuracy: {train_acc:.4f}")
        print(f"   Test Accuracy: {test_acc:.4f}")
    
    # Create comparison dataframe
    print("\n3. Model Comparison:")
    comparison_df = pd.DataFrame({
        'Architecture': architectures,
        'Train Accuracy': [results[a]['train_acc'] for a in architectures],
        'Test Accuracy': [results[a]['test_acc'] for a in architectures],
        'Train Loss': [results[a]['train_loss'] for a in architectures],
        'Test Loss': [results[a]['test_loss'] for a in architectures]
    })
    print(comparison_df.to_string(index=False))
    
    # Plot comparison
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(architectures))
    width = 0.35
    ax.bar(x - width/2, comparison_df['Train Accuracy'], width, label='Train', alpha=0.8)
    ax.bar(x + width/2, comparison_df['Test Accuracy'], width, label='Test', alpha=0.8)
    ax.set_xlabel('Architecture')
    ax.set_ylabel('Accuracy')
    ax.set_title('ANN Model Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels([a.upper() for a in architectures])
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('ann_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Save best model
    best_arch = comparison_df.loc[comparison_df['Test Accuracy'].idxmax(), 'Architecture']
    print(f"\n4. Best Model: {best_arch.upper()} ANN")
    results[best_arch]['model'].save_model(f'best_ann_{best_arch}.keras')
    
    print("\n" + "=" * 60)
    print("EXPERIMENT COMPLETED!")
    print("=" * 60)


if __name__ == "__main__":
    main()
