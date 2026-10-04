from pathlib import Path
import pandas as pd
import numpy as np

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Input: final cleaned observation CSV
input_file = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "gnss"
    / "GDKG00IND_observations_understanding.csv"
)

# Output: GNSS epoch feature CSV
output_file = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "gnss"
    / "GDKG00IND_gnss_epoch_features.csv"
)

print("Input file:")
print(input_file)

print("\nOutput file:")
print(output_file)


from pathlib import Path
import pandas as pd
import numpy as np

# ==================================================
# 1. PROJECT PATHS
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

input_file = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "gnss"
    / "GDKG00IND_observations_understanding.csv"
)

output_file = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "gnss"
    / "GDKG00IND_gnss_epoch_features.csv"
)


# ==================================================
# 2. LOAD CLEAN GNSS OBSERVATIONS
# ==================================================

print("Loading GNSS observation data...")

df = pd.read_csv(input_file)

print("Data loaded successfully!")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# ==================================================
# 3. CONVERT EPOCH TO DATETIME
# ==================================================

df["Epoch"] = pd.to_datetime(df["Epoch"])


# ==================================================
# 4. CONVERT MEASUREMENTS TO NUMERIC
# ==================================================

measurement_columns = [
    "Code_Value",
    "Carrier_Phase_Value",
    "Doppler_Value",
    "Signal_Strength_Value"
]

for column in measurement_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ==================================================
# 5. CREATE EPOCH-LEVEL GNSS FEATURES
# ==================================================

features = df.groupby("Epoch").agg(

    Total_Satellites=(
        "Satellite",
        "nunique"
    ),

    Mean_Code=(
        "Code_Value",
        "mean"
    ),

    Mean_Carrier_Phase=(
        "Carrier_Phase_Value",
        "mean"
    ),

    Mean_Doppler=(
        "Doppler_Value",
        "mean"
    ),

    Doppler_STD=(
        "Doppler_Value",
        "std"
    ),

    Mean_Signal_Strength=(
        "Signal_Strength_Value",
        "mean"
    ),

    Min_Signal_Strength=(
        "Signal_Strength_Value",
        "min"
    ),

    Max_Signal_Strength=(
        "Signal_Strength_Value",
        "max"
    ),

    Signal_Strength_STD=(
        "Signal_Strength_Value",
        "std"
    )

).reset_index()


# ==================================================
# 6. COUNT SATELLITES BY GNSS SYSTEM
# ==================================================

system_counts = (
    df.groupby(
        ["Epoch", "GNSS_System"]
    )["Satellite"]
    .nunique()
    .unstack(fill_value=0)
    .reset_index()
)


# ==================================================
# 7. RENAME GNSS SYSTEM COLUMNS
# ==================================================

system_counts = system_counts.rename(
    columns={
        "GPS": "GPS_Count",
        "Galileo": "Galileo_Count",
        "BeiDou": "BeiDou_Count",
        "GLONASS": "GLONASS_Count",
        "QZSS": "QZSS_Count",
        "NavIC": "NavIC_Count",
        "SBAS": "SBAS_Count"
    }
)


# ==================================================
# 8. ENSURE ALL EXPECTED SYSTEM COLUMNS EXIST
# ==================================================

expected_columns = [
    "GPS_Count",
    "Galileo_Count",
    "BeiDou_Count",
    "GLONASS_Count",
    "QZSS_Count",
    "NavIC_Count",
    "SBAS_Count"
]

for column in expected_columns:

    if column not in system_counts.columns:
        system_counts[column] = 0


# ==================================================
# 9. MERGE FEATURES
# ==================================================

features = features.merge(
    system_counts,
    on="Epoch",
    how="left"
)


# ==================================================
# 10. CLEAN SATELLITE COUNTS
# ==================================================

features[expected_columns] = (
    features[expected_columns]
    .fillna(0)
    .astype(int)
)


# ==================================================
# 11. ADD TOTAL SIGNAL OBSERVATIONS
# ==================================================

signal_count = (
    df.groupby("Epoch")["Signal_Strength_Value"]
    .count()
    .reset_index(name="Valid_Signal_Observations")
)

features = features.merge(
    signal_count,
    on="Epoch",
    how="left"
)


# ==================================================
# 12. SORT BY TIME
# ==================================================

features = features.sort_values("Epoch")


# ==================================================
# 13. SAVE FEATURE DATASET
# ==================================================

features.to_csv(
    output_file,
    index=False
)


# ==================================================
# 14. DISPLAY RESULTS
# ==================================================

print()
print("=" * 50)
print("GNSS EPOCH FEATURE DATASET CREATED")
print("=" * 50)

print("\nOutput:")
print(output_file)

print("\nNumber of epochs:", len(features))

print("\nColumns:")
for column in features.columns:
    print("-", column)

print("\nFeature dataset:")
print(features.to_string(index=False))