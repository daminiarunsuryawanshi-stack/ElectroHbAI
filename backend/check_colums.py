import pandas as pd

df = pd.read_csv(
    "app/ml/dataset/DatafinitiElectronicsProductsPricingData.csv",
    low_memory=False
)

print(df.columns.tolist())