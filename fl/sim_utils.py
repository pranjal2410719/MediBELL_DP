import pandas as pd
import numpy as np

def partition_data(csv_path, num_clients=3):
    """
    Simulate multiple hospitals by partitioning a single CSV dataset.
    """
    df = pd.read_csv(csv_path)
    
    # Shuffle data
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Split into partitions
    partitions = np.array_split(df, num_clients)
    
    return partitions
