import georinex as gr
import pandas as pd

# RINEX file
rinex_file = r"C:\Users\kgeet\Downloads\GDKG00IND_R_20261100000_01D_30S_MO.rnx"

# Load only 5 minutes of data
obs = gr.load(
    rinex_file,
    tlim=("2026-04-20T00:00:00", "2026-04-20T00:05:00")
)

print("RINEX data loaded successfully!")

# Select important GNSS observations
df = obs[["C1C", "L1C", "D1C", "S1C"]].to_dataframe().reset_index()

# Add GNSS system
df["GNSS_System"] = df["sv"].str[0]

# Rename columns
df.rename(
    columns={
        "time": "Epoch",
        "sv": "Satellite"
    },
    inplace=True
)

# Save CSV
output_file = r"C:\Users\kgeet\Downloads\GDKG00IND_observations_5min.csv"

df.to_csv(output_file, index=False)

print("CSV CREATED SUCCESSFULLY!")
print("File:", output_file)
print("Rows:", len(df))

print("\nFirst 10 rows:")
print(df.head(10))