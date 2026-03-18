import pandas as pd
import numpy as np

# Number of entreprises
n = 20

# Column structure
columns = [
    "Entreprise",
    "Boeuf Achetee", "Boeuf Jetee",
    "Volaie Achetee", "Volaie Jetee",
    "Viande Blanche Achetee", "Viande Blanche Jetee",
    "Poisson Achetee", "Poisson Jetee",
    "Fruit Achetee", "Fruit Jetee",
    "Legumes Achetee", "Legumes Jetee",
    "LSF Achetee", "LSF Jetee",
    "Sec Achetee", "Sec Jetee",
    "DPH Achetee", "DPH Jetee"
]

data = []

for i in range(n):
    row = [f"Entreprise {i+1}"]

    # Generate random values
    values = np.random.randint(0, 51, size=18)

    # Ensure waste <= bought for each pair
    for j in range(0, len(values), 2):
        bought = values[j]
        waste = np.random.randint(0, bought + 1) if bought > 0 else 0
        values[j+1] = waste

    row.extend(values)
    data.append(row)

# Create DataFrame
df = pd.DataFrame(data, columns=columns)

# Calculate totals
achat_cols = [col for col in df.columns if "Achetee" in col]
waste_cols = [col for col in df.columns if "Jetee" in col]

df["Total bought"] = df[achat_cols].sum(axis=1)
df["Total Waste"] = df[waste_cols].sum(axis=1)

df["Score"] = df.apply(
    lambda row: round(
        row["Total Waste"] / row["Total bought"], 2
    ) if row["Total bought"] > 0 else 0,
    axis=1
)

# Contact rule
df["Contact?"] = df["Score"] > 0.6

# Save full BDD
df.to_csv("bdd_generated.csv", index=False)

# Filter entreprises to contact
df_contact = df[df["Contact?"] == True]
df_contact.to_csv("entreprises_to_contact.csv", index=False)

print("Files generated:")
print("- bdd_generated.csv")
print("- entreprises_to_contact.csv")