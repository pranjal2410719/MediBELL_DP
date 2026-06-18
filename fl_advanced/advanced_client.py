import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import f1_score, precision_score, recall_score
from utils.preprocessing import apply_dp
import warnings

# Suppress convergence warnings for clean logging
warnings.filterwarnings("ignore")

class AdvancedFederatedClient:
    def __init__(self, client_id, data, model_type="logistic", epsilon=1.0):
        self.client_id = client_id
        self.data = data
        self.epsilon = epsilon
        self.model_type = model_type
        self.scaler = StandardScaler()
        self.le = LabelEncoder()
        
        # Pre-cache processed data for performance in simulation
        self.X_cached, self.y_cached = self.preprocess()
        
        if model_type == "logistic":
            self.model = SGDClassifier(loss='log_loss', max_iter=20, warm_start=True, random_state=42)
        elif model_type == "mlp":
            # Multi-Layer Perceptron optimized for fast Federated convergence
            self.model = MLPClassifier(
                hidden_layer_sizes=(128, 64, 32), 
                max_iter=10, 
                warm_start=True, 
                random_state=42,
                learning_rate_init=0.01
            )
        
    def preprocess(self):
        X = self.data.drop(columns=["disease"])
        y = self.data["disease"]
        
        # Apply DP
        X_dp = apply_dp(X, self.epsilon)
        
        # Track noise
        numeric_cols = [c for c in X.columns if c != "gender"]
        self.avg_noise = np.abs(X_dp[numeric_cols].values - X[numeric_cols].values).mean()

        # Handle features
        X_num = X_dp.drop(columns=["gender"]) 
        X_processed = self.scaler.fit_transform(X_num)
        y_enc = self.le.fit_transform(y)
        
        return X_processed, y_enc

    def get_weights(self):
        if self.model_type == "logistic":
            return {
                'coef': self.model.coef_,
                'intercept': self.model.intercept_,
                'classes': self.model.classes_
            }
        elif self.model_type == "mlp":
            return {
                'coefs': self.model.coefs_,
                'intercepts': self.model.intercepts_,
                'classes': self.model.classes_
            }

    def set_weights(self, weights):
        if weights is None: return
        
        if self.model_type == "logistic":
            self.model.coef_ = weights['coef']
            self.model.intercept_ = weights['intercept']
            self.model.classes_ = weights['classes']
        elif self.model_type == "mlp":
            self.model.coefs_ = weights['coefs']
            self.model.intercepts_ = weights['intercepts']
            self.model.classes_ = weights['classes']

    def train_local(self, global_weights=None):
        X, y = self.X_cached, self.y_cached
        
        if global_weights:
            self.set_weights(global_weights)
        
        # Train
        self.model.fit(X, y)
        
        # Metrics
        acc = self.model.score(X, y)
        pred = self.model.predict(X)
        
        # Calculate F1, Precision, and Recall (weighted for multi-class)
        f1 = f1_score(y, pred, average='weighted', zero_division=0)
        precision = precision_score(y, pred, average='weighted', zero_division=0)
        recall = recall_score(y, pred, average='weighted', zero_division=0)
        
        return {
            'weights': self.get_weights(),
            'n_samples': len(X),
            'acc': acc,
            'f1': f1,
            'precision': precision,
            'recall': recall,
            'noise': self.avg_noise
        }
