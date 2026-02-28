import pandas as pd

df = pd.read_csv('data/bank_marketing.csv', sep=';')
print(f"V1 shape: {df.shape}")

df_cleaned = df[
    (df['job'] != 'unknown') & 
    (df['education'] != 'unknown')
]
print(f"V2 shape after cleaning: {df_cleaned.shape}")

df_cleaned.to_csv('data/bank_marketing.csv', index=False)
print("Saved cleaned dataset!")