import numpy as np

def apply_laplace_ldp(X, epsilon):
    """
    Apply Local Differential Privacy using Laplace mechanism
    Assumes numeric, bounded features
    """
    if epsilon <= 0:
        raise ValueError("Epsilon must be positive")

    scale = 1.0 / epsilon
    noise = np.random.laplace(0, scale, X.shape)

    X_noisy = X + noise
    X_noisy[X_noisy < 0] = 0  # keep domain valid

    return X_noisy
