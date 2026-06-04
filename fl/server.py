import numpy as np

class FederatedServer:
    def __init__(self):
        self.global_weights = None

    def aggregate(self, client_updates):
        """
        Federated Averaging (FedAvg) implementation.
        """
        if not client_updates:
            return None
        
        total_samples = sum(u['n_samples'] for u in client_updates)
        
        # Initialize global weights based on first client
        first_client = client_updates[0]
        avg_coef = np.zeros_like(first_client['coef'])
        avg_intercept = np.zeros_like(first_client['intercept'])
        
        for update in client_updates:
            weight = update['n_samples'] / total_samples
            avg_coef += update['coef'] * weight
            avg_intercept += update['intercept'] * weight
            
        self.global_weights = {
            'coef': avg_coef,
            'intercept': avg_intercept,
            'classes': first_client['classes']
        }
        
        return self.global_weights

    def get_global_model(self):
        return self.global_weights
