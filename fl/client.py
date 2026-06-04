import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from utils.preprocessing import apply_dp

class FederatedClient:
    def __init__(self, client_id, data, epsilon=1.0):
        self.client_id = client_id
        self.data = data
        self.epsilon = epsilon
        self.model = SGDClassifier(loss='log_loss', max_iter=1, warm_start=True)
        self.le = LabelEncoder()
        self.scaler = StandardScaler()
        
    def preprocess(self):
        """
        Apply DP locally before any training.
        """
        X = self.data.drop(columns=["disease"])
        y = self.data["disease"]
        
        # Apply existing DP logic
        X_dp = apply_dp(X, self.epsilon)
        
        # Simple encoding for this simulation
        # For a real scenario, we'd use the same preprocessor as train_dp.py
        # but here we focus on the FL flow.
        X_num = X_dp.drop(columns=["gender"]) 
        # (Assuming gender is handled by dp_gender_series and returned as numeric bits)
        
        X_processed = self.scaler.fit_transform(X_num)
        y_enc = self.le.fit_transform(y)
        
        return X_processed, y_enc

    def train_local(self, global_weights=None):
        X, y = self.preprocess()
        
        # Set global weights if provided
        if global_weights is not None:
            self.model.coef_ = global_weights['coef']
            self.model.intercept_ = global_weights['intercept']
            self.model.classes_ = global_weights['classes']
        
        # Train for one epoch (simulating local update)
        self.model.fit(X, y)
        
        return {
            'coef': self.model.coef_,
            'intercept': self.model.intercept_,
            'classes': self.model.classes_,
            'n_samples': len(X)
        }
