import numpy as np

class AdvancedFederatedServer:
    def __init__(self, model_type="logistic"):
        self.model_type = model_type
        self.global_weights = None

    def aggregate(self, updates):
        if not updates: return None
        
        total_samples = sum(u['n_samples'] for u in updates)
        weights_list = [u['weights'] for u in updates]
        samples_list = [u['n_samples'] for u in updates]
        
        if self.model_type == "logistic":
            avg_coef = np.zeros_like(weights_list[0]['coef'])
            avg_intercept = np.zeros_like(weights_list[0]['intercept'])
            
            for w, s in zip(weights_list, samples_list):
                factor = s / total_samples
                avg_coef += w['coef'] * factor
                avg_intercept += w['intercept'] * factor
                
            self.global_weights = {
                'coef': avg_coef,
                'intercept': avg_intercept,
                'classes': weights_list[0]['classes']
            }
            
        elif self.model_type == "mlp":
            # Aggregate Neural Network layers
            avg_coefs = [np.zeros_like(c) for c in weights_list[0]['coefs']]
            avg_intercepts = [np.zeros_like(i) for i in weights_list[0]['intercepts']]
            
            for w, s in zip(weights_list, samples_list):
                factor = s / total_samples
                for i in range(len(avg_coefs)):
                    avg_coefs[i] += w['coefs'][i] * factor
                    avg_intercepts[i] += w['intercepts'][i] * factor
            
            self.global_weights = {
                'coefs': avg_coefs,
                'intercepts': avg_intercepts,
                'classes': weights_list[0]['classes']
            }

        return self.global_weights
