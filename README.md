# DVC Lab 1 — Data Version Control with Google Cloud Storage

## Overview
This lab demonstrates how to use **Data Version Control (DVC)** alongside **Git** and **Google Cloud Storage (GCS)** to version, track, and manage datasets in a machine learning workflow.

Unlike the original lab which used the CC_GENERAL credit card dataset, this submission uses the **UCI Bank Marketing Dataset** to demonstrate real-world data versioning across two versions of the dataset.

---

## Dataset
**Bank Marketing Dataset** — UCI Machine Learning Repository  
Source: https://archive.ics.uci.edu/dataset/222/bank+marketing

The dataset contains information about direct marketing campaigns (phone calls) of a Portuguese banking institution. The classification goal is to predict whether a client will subscribe to a term deposit.

| Property | Details |
|---|---|
| Rows (V1) | 45,211 |
| Rows (V2) | 43,193 |
| Columns | 17 |
| Target | `y` — has the client subscribed? (yes/no) |

---

## Modifications from Original Lab

| Original Lab | This Submission |
|---|---|
| Used `CC_GENERAL.csv` (credit card data) | Used `bank_marketing.csv` (bank marketing data) |
| Single dataset version | Two dataset versions tracked with DVC |
| No preprocessing | V2 includes cleaning of `unknown` values |

---

## Tools & Technologies
- **DVC** — Data versioning and remote storage management
- **Google Cloud Storage (GCS)** — Remote storage backend (`varaa-dvc-lab1` bucket, `us-east1`)
- **Git** — Source code and `.dvc` metadata versioning
- **Python + Pandas** — Data preprocessing

---

## Project Structure

```
DVC-Lab1/
├── .dvc/
│   └── config              # DVC remote configuration
├── data/
│   ├── bank_marketing.csv          # Dataset (tracked by DVC, not Git)
│   └── bank_marketing.csv.dvc      # DVC tracking file (committed to Git)
├── preprocess.py           # Script to generate V2 cleaned dataset
├── README.md
└── requirements.txt
```

---

## Setup

### 1. Install DVC with GCS support
```bash
pip install dvc[gs]
```

### 2. Add GCS bucket as remote
```bash
python -m dvc remote add -d myremote gs://varaa-dvc-lab1
python -m dvc remote modify myremote credentialpath /path/to/credentials.json
```

### 3. Pull data from remote
```bash
dvc pull
```

---

## Dataset Versions

### Version 1 — Raw Dataset
The original `bank_marketing.csv` downloaded directly from UCI with all 45,211 rows.

```bash
python -m dvc add data/bank_marketing.csv
git add data/bank_marketing.csv.dvc
git commit -m "V1: Track raw bank marketing dataset"
python -m dvc push
```

### Version 2 — Cleaned Dataset
Removed rows where `job == 'unknown'` or `education == 'unknown'` to improve data quality. This reduced the dataset from **45,211 to 43,193 rows** (2,018 rows removed).

```bash
python preprocess.py
python -m dvc add data/bank_marketing.csv
git add data/bank_marketing.csv.dvc
git commit -m "V2: Cleaned dataset - removed unknown job and education rows"
python -m dvc push
```

---

## Preprocessing Script
The `preprocess.py` script handles the data cleaning for V2:

```python
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
```

---

## Reverting to a Previous Version

```bash
# View all commits
git log --oneline

# Revert to V1
git checkout <v1-commit-hash>
python -m dvc checkout

# Verify V1 is restored (should print (45211, 17))
python -c "import pandas as pd; df = pd.read_csv('data/bank_marketing.csv', sep=';'); print(df.shape)"

# Return to latest (V2)
git checkout master
python -m dvc checkout
```

---

## Key Takeaways
- DVC tracks datasets using **MD5 hashes** — any change to the file generates a new version
- The actual data lives in **GCS**, only the `.dvc` metadata file is stored in Git
- You can **revert to any previous dataset version** by combining `git checkout` + `dvc checkout`
- This workflow ensures **reproducibility** in ML experiments — you always know exactly what data was used

---

