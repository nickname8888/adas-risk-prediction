import os
import subprocess

LOG_DIR = "outputs/logs"
CSV_DIR = "outputs/trajectory_csv"

os.makedirs(CSV_DIR, exist_ok=True)

ESMINI_DAT2CSV = "/home/nickname8888/esmini/bin/dat2csv"

for filename in os.listdir(LOG_DIR):
    if not filename.endswith(".dat"):
        continue
    dat_path = os.path.join(LOG_DIR, filename)
    csv_name = filename.replace(".dat", ".csv")
    csv_path = os.path.join(CSV_DIR, csv_name)

    cmd = [
        ESMINI_DAT2CSV,
        "--file",
        dat_path,
        "--csv",
        csv_path,
    ]
    print(f"Converting: {filename}")
    subprocess.run(cmd) 

print("\nTrajectory extraction complete.\n")