import numpy as np
import math

# -------------------------------------------------
# Encode gender → numeric
# male   -> 0
# female -> 1
# -------------------------------------------------

def encode_gender(g):
    g = str(g).strip().lower()

    if g == "male":
        return 0
    elif g == "female":
        return 1
    else:
        return 0   # default safety


# -------------------------------------------------
# Randomized Response (Local Differential Privacy)
#
# p_keep  = e^ε / (e^ε + 1)
# p_flip  = 1 / (e^ε + 1)
#
# For each user independently:
#   keep with p
#   flip with 1-p
# -------------------------------------------------

def dp_gender(bit, epsilon=1.0):

    p_keep = math.exp(epsilon) / (math.exp(epsilon) + 1)

    if np.random.rand() < p_keep:
        return bit
    else:
        return 1 - bit


# -------------------------------------------------
# Vectorized version (FASTER for pandas column)
# Recommended for datasets
# -------------------------------------------------

def dp_gender_series(series, epsilon=1.0):

    p_keep = math.exp(epsilon) / (math.exp(epsilon) + 1)

    rand = np.random.rand(len(series))
    flipped = 1 - series

    return np.where(rand < p_keep, series, flipped)
