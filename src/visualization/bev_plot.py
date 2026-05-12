import pandas as pd
import matplotlib.pyplot as plt
import argparse


LANE_WIDTH = 3.0


def draw_lanes():

    for lane_y in [0, -3, -6, -9]:

        plt.axhline(
            y=lane_y,
            linestyle="--",
            linewidth=1,
        )


parser = argparse.ArgumentParser()

parser.add_argument(
    "--csv",
    required=True,
)

args = parser.parse_args()

csv_path = args.csv

df = pd.read_csv(csv_path)
df.columns = df.columns.str.strip()
df["name"] = df["name"].str.strip()

# print(df.columns)
# print(df["name"].unique())

ego_df = df[df["name"] == "Ego"]

target_df = df[df["name"] == "Target"]

plt.figure(figsize=(12, 6))

draw_lanes()

plt.plot(
    ego_df["x"],
    ego_df["y"],
    linewidth=3,
    label="Ego",
)

plt.plot(
    target_df["x"],
    target_df["y"],
    linewidth=3,
    label="Target",
)

plt.xlabel("Longitudinal Position")

plt.ylabel("Lateral Position")

plt.title("BEV Trajectory Visualization")

plt.legend()

plt.grid(True)

plt.axis("equal")

output_path = "outputs/figures/bev_plot.png"

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight",
)

print(f"\nSaved BEV plot to: {output_path}\n")