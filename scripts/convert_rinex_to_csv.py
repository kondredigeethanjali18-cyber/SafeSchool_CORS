from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

rinex_file = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "rinex"
    / "GDKG00IND_R_20261100000_01D_30S_MO.rnx"
)

output_file = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "gnss"
    / "GDKG00IND_observations_understanding.csv"
)