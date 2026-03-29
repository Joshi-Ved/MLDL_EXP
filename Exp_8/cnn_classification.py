"""
Convolutional Neural Network (CNN) Implementation
Complete Python Script for MNIST and CIFAR-10 Classification
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.datasets import mnist, cifar10
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout, BatchNormalization
import warnings
warnings.filterwarnings('ignore')


class CNNClassifier:
    """Convolutional Neural Network for Image Classification"""
    
    def __init__(self, input_shape, num_classes, architecture='advanced', dataset='mnist'):
        """
        Initialize CNN Classifier
        
        Args:
            input_shape: Input shape (height, width, channels)
            num_classes: Number of classes
            architecture: 'simple', 'advanced', or 'deep'
            dataset: 'mnist' or 'cifar10'
        """
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.architecture = architecture
        self.dataset = dataset
        self.model = None
        self.history = None
        
    def build_model(self):
        """Build CNN model"""
        if self.dataset == 'mnist':
            if self.architecture == 'simple':
                self.model = self._build_simple_mnist()
            elif self.architecture == 'advanced':
                self.model = self._build_advanced_mnist()
        elif self.dataset == 'cifar10':
            if self.architecture == 'deep':
                self.model = self._build_deep_cifar()
        else:
            raise ValueError(f"Unknown dataset: {self.dataset}")
    
    def _build_simple_mnist(self):
        """Simple CNN for MNIST"""
        model = models.Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=self.input_shape),
            MaxPooling2D((2, 2)),
            
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            
            Flatten(),
            Dense(128, activation='relu'),
            Dropout(0.5),
            Dense(self.num_classes, activation='softmax')
        ])
        return model
    
    def _build_advanced_mnist(self):
        """Advanced CNN for MNIST"""
        model = models.Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=self.input_shape),
            BatchNormalization(),
            Conv2D(32, (3, 3), activation='relu'),
            BatchNormalization(),
            MaxPooling2D((2, 2)),
            Dropout(0.25),
            
            Conv2D(64, (3, 3), activation='relu'),
            BatchNormalization(),
            Conv2D(64, (3, 3), activation='relu'),
            BatchNormalization(),
            MaxPooling2D((2, 2)),
            Dropout(0.25),
            
            Flatten(),
            Dense(256, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            
            Dense(128, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            
            Dense(self.num_classes, activation='softmax')
        ])
        return model
    
    def _build_deep_cifar(self):
        """Deep CNN for CIFAR-10"""
        model = models.Sequential([
            Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=self.input_shape),
            BatchNormalization(),
            Conv2D(32, (3, 3), padding='same', activation='relu'),
            BatchNormalization(),
            MaxPooling2D((2, 2)),
            Dropout(0.25),
            
            Conv2D(64, (3, 3), padding='same', activation='relu'),
            BatchNormalization(),
            Conv2D(64, (3, 3), padding='same', activation='relu'),
            BatchNormalization(),
            MaxPooling2D((2, 2)),
            Dropout(0.25),
            
            Conv2D(128, (3, 3), padding='same', activation='relu'),
            BatchNormalization(),
            Conv2D(128, (3, 3), padding='same', activation='relu'),
            BatchNormalization(),
            MaxPooling2D((2, 2)),
            Dropout(0.25),
            
            Flatten(),
            Dense(256, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            
            Dense(128, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            
            Dense(self.num_classes, activation='softmax')
        ])
        return model
    
    def compile_model(self, learning_rate=0.001):
        """Compile model"""
        self.model.compile(
            optimizer=Adam(learning_rate=learning_rate),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
    
    def fit(self, X_train, y_train, X_val=None, y_val=None, epochs=20, 
            batch_size=128, augmentation=True, verbose=1):
        """Train model"""
        # Setup callbacks
        callbacks_list = [
            callbacks.EarlyStopping(
                monitor='val_loss',
                patience=5,
                restore_best_weights=True
            ),
            callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=3,
                min_lr=1e-7
            )
        ]
        
        # Data augmentation
        if augmentation:
            if self.dataset == 'mnist':
                datagen = ImageDataGenerator(
                    rotation_range=10,
                    width_shift_range=0.1,
                    height_shift_range=0.1,
                    zoom_range=0.2
                )
            else:  # cifar10
                datagen = ImageDataGenerator(
                    rotation_range=20,
                    width_shift_range=0.2,
                    height_shift_range=0.2,
                    horizontal_flip=True,
                    zoom_range=0.2
                )
            
            self.history = self.model.fit(
                datagen.flow(X_train, y_train, batch_size=batch_size),
                epochs=epochs,
                steps_per_epoch=len(X_train) // batch_size,
                validation_data=(X_val, y_val),
                callbacks=callbacks_list,
                verbose=verbose
            )
        else:
            self.history = self.model.fit(
                X_train, y_train,
                epochs=epochs,
                batch_size=batch_size,
                validation_data=(X_val, y_val),
                callbacks=callbacks_list,
                verbose=verbose
            )
        
        return self.history
    
    def evaluate(self, X_test, y_test):
        """Evaluate model"""
        loss, accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        return loss, accuracy
    
    def predict(self, X):
        """Make predictions"""
        return self.model.predict(X)
    
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
        axes[0].set_title(f'{self.architecture.upper()} CNN - {self.dataset.upper()} Accuracy')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Loss
        axes[1].plot(self.history.history['loss'], label='Training', linewidth=2)
        axes[1].plot(self.history.history['val_loss'], label='Validation', linewidth=2)
        axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('Loss')
        axes[1].set_title(f'{self.architecture.upper()} CNN - {self.dataset.upper()} Loss')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'cnn_training_history_{self.dataset}_{self.architecture}.png', dpi=300)
        plt.show()


def prepare_mnist():
    """Load and prepare MNIST dataset"""
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    
    X_train = X_train.astype('float32') / 255.0
    X_test = X_test.astype('float32') / 255.0
    
    X_train = X_train.reshape(-1, 28, 28, 1)
    X_test = X_test.reshape(-1, 28, 28, 1)
    
    y_train = keras.utils.to_categorical(y_train, 10)
    y_test = keras.utils.to_categorical(y_test, 10)
    
    return X_train, y_train, X_test, y_test


def prepare_cifar10():
    """Load and prepare CIFAR-10 dataset"""
    (X_train, y_train), (X_test, y_test) = cifar10.load_data()
    
    X_train = X_train.astype('float32') / 255.0
    X_test = X_test.astype('float32') / 255.0
    
    y_train = y_train.flatten()
    y_test = y_test.flatten()
    
    y_train = keras.utils.to_categorical(y_train, 10)
    y_test = keras.utils.to_categorical(y_test, 10)
    
    return X_train, y_train, X_test, y_test


def main():
    """Main execution"""
    print("=" * 70)
    print("CONVOLUTIONAL NEURAL NETWORK (CNN) - COMPREHENSIVE EXPERIMENT")
    print("=" * 70)
    
    # MNIST Dataset
    print("\n1. Loading MNIST Dataset...")
    X_train_mnist, y_train_mnist, X_test_mnist, y_test_mnist = prepare_mnist()
    print(f"   Training Shape: {X_train_mnist.shape}")
    print(f"   Test Shape: {X_test_mnist.shape}")
    
    # CIFAR-10 Dataset
    print("\n2. Loading CIFAR-10 Dataset...")
    X_train_cifar, y_train_cifar, X_test_cifar, y_test_cifar = prepare_cifar10()
    print(f"   Training Shape: {X_train_cifar.shape}")
    print(f"   Test Shape: {X_test_cifar.shape}")
    
    # Train on MNIST
    results = {}
    
    print("\n3. Training Simple CNN on MNIST...")
    cnn_simple = CNNClassifier((28, 28, 1), 10, architecture='simple', dataset='mnist')
    cnn_simple.build_model()
    cnn_simple.compile_model()
    cnn_simple.fit(X_train_mnist, y_train_mnist, X_test_mnist, y_test_mnist, 
                   epochs=10, augmentation=False, verbose=1)
    
    test_loss_s, test_acc_s = cnn_simple.evaluate(X_test_mnist, y_test_mnist)
    results['simple_mnist'] = test_acc_s
    print(f"   MNIST Simple CNN Test Accuracy: {test_acc_s:.4f}")
    
    print("\n4. Training Advanced CNN on MNIST...")
    cnn_advanced = CNNClassifier((28, 28, 1), 10, architecture='advanced', dataset='mnist')
    cnn_advanced.build_model()
    cnn_advanced.compile_model()
    cnn_advanced.fit(X_train_mnist, y_train_mnist, X_test_mnist, y_test_mnist, 
                     epochs=20, batch_size=128, verbose=1)
    
    test_loss_a, test_acc_a = cnn_advanced.evaluate(X_test_mnist, y_test_mnist)
    results['advanced_mnist'] = test_acc_a
    print(f"   MNIST Advanced CNN Test Accuracy: {test_acc_a:.4f}")
    
    print("\n5. Training Deep CNN on CIFAR-10...")
    cnn_deep = CNNClassifier((32, 32, 3), 10, architecture='deep', dataset='cifar10')
    cnn_deep.build_model()
    cnn_deep.compile_model()
    cnn_deep.fit(X_train_cifar, y_train_cifar, X_test_cifar, y_test_cifar, 
                 epochs=50, batch_size=64, verbose=1)
    
    test_loss_d, test_acc_d = cnn_deep.evaluate(X_test_cifar, y_test_cifar)
    results['deep_cifar'] = test_acc_d
    print(f"   CIFAR-10 Deep CNN Test Accuracy: {test_acc_d:.4f}")
    
    # Summary
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    comparison_df = pd.DataFrame({
        'Model': ['Simple CNN (MNIST)', 'Advanced CNN (MNIST)', 'Deep CNN (CIFAR-10)'],
        'Test Accuracy': [test_acc_s, test_acc_a, test_acc_d]
    })
    print(comparison_df.to_string(index=False))
    
    # Save best models
    print("\n6. Saving Models...")
    cnn_advanced.save_model('best_cnn_mnist.keras')
    cnn_deep.save_model('best_cnn_cifar10.keras')
    
    print("\n" + "=" * 70)
    print("EXPERIMENT COMPLETED!")
    print("=" * 70)


if __name__ == "__main__":
    main()
