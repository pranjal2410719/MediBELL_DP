import pandas as pd

# Load dataset
df = pd.read_csv("data/synthetic_dataset_25k_40symptoms.csv")

print("\n==============================")
print("RESEARCH DATASET SUMMARY")
print("==============================")

# Basic shape
rows, cols = df.shape
print(f"\nTotal Samples: {rows}")
print(f"Total Features (including target): {cols}")

# Missing values
total_missing = df.isnull().sum().sum()
print(f"\nTotal Missing Values: {total_missing}")

# Feature categorization
demographic = ["age", "gender", "smoker"]
physiological = ["heart_rate", "blood_pressure", "cholesterol_level"]

symptoms = [col for col in df.columns 
            if col not in demographic + physiological + ["disease"]]

print("\nFeature Categories:")
print(f"Demographic: {len(demographic)}")
print(f"Physiological: {len(physiological)}")
print(f"Symptom Features: {len(symptoms)}")
print(f"Target Classes: {df['disease'].nunique()}")

# Class distribution
print("\nClass Distribution:")
class_counts = df["disease"].value_counts()
class_percent = df["disease"].value_counts(normalize=True) * 100

class_summary = pd.DataFrame({
    "Count": class_counts,
    "Percentage (%)": class_percent.round(2)
})

print(class_summary)

# Imbalance ratio
imbalance_ratio = class_counts.max() / class_counts.min()
print(f"\nImbalance Ratio (Max/Min): {round(imbalance_ratio, 2)}")
