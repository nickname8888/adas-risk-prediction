import os
import argparse

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np


LANE_WIDTH = 3.0

ROAD_LEFT = -10.5
ROAD_RIGHT = 1.5

ROAD_COLOR = "#2f2f2f"
LANE_COLOR = "white"

EGO_COLOR = "#00d4ff"
TARGET_COLOR = "#ff6b35"


parser = argparse.ArgumentParser()

parser.add_argument(
    "--csv",
    required=True,
)

args = parser.parse_args()

csv_path = args.csv


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

df = pd.read_csv(csv_path)

df.columns = df.columns.str.strip()

df["name"] = df["name"].str.strip()

print(df.columns)

print(df["name"].unique())

ego_df = df[df["name"] == "Ego"]

target_df = df[df["name"] == "Target"]


# ------------------------------------------------------------
# FIGURE SETUP
# ------------------------------------------------------------

fig, ax = plt.subplots(
    figsize=(16, 8),
)

fig.patch.set_facecolor("#111111")

ax.set_facecolor("#111111")


# ------------------------------------------------------------
# ROAD SURFACE
# ------------------------------------------------------------

ax.fill_between(
    [0, 10000],
    ROAD_LEFT,
    ROAD_RIGHT,
    color=ROAD_COLOR,
)


# ------------------------------------------------------------
# LANE BOUNDARIES
# ------------------------------------------------------------

lane_boundaries = [
    0,
    -3,
    -6,
    -9,
]

for lane_y in lane_boundaries:

    ax.plot(
        [0, 10000],
        [lane_y, lane_y],
        linestyle="--",
        linewidth=2,
        color=LANE_COLOR,
        alpha=0.7,
    )


# ------------------------------------------------------------
# LANE CENTERS
# ------------------------------------------------------------

lane_centers = [
    -1.5,
    -4.5,
    -7.5,
]

for lane_y in lane_centers:

    ax.plot(
        [0, 10000],
        [lane_y, lane_y],
        linestyle=":",
        linewidth=1,
        color="#666666",
        alpha=0.4,
    )


# ------------------------------------------------------------
# TRAJECTORY HELPERS
# ------------------------------------------------------------

def build_segments(x, y):

    points = np.array([x, y]).T.reshape(-1, 1, 2)

    segments = np.concatenate(
        [points[:-1], points[1:]],
        axis=1,
    )

    return segments


# ------------------------------------------------------------
# EGO TRAJECTORY
# ------------------------------------------------------------

segments = build_segments(
    ego_df["x"].values,
    ego_df["y"].values,
)

ego_lc = LineCollection(
    segments,
    linewidths=5,
    colors=EGO_COLOR,
    alpha=0.95,
)

ax.add_collection(ego_lc)


# ------------------------------------------------------------
# TARGET TRAJECTORY
# ------------------------------------------------------------

segments = build_segments(
    target_df["x"].values,
    target_df["y"].values,
)

target_lc = LineCollection(
    segments,
    linewidths=5,
    colors=TARGET_COLOR,
    alpha=0.95,
)

ax.add_collection(target_lc)


# ------------------------------------------------------------
# START / END MARKERS
# ------------------------------------------------------------

ax.scatter(
    ego_df["x"].iloc[0],
    ego_df["y"].iloc[0],
    s=150,
    color=EGO_COLOR,
    edgecolors="white",
    linewidths=2,
    zorder=5,
)

ax.scatter(
    target_df["x"].iloc[0],
    target_df["y"].iloc[0],
    s=150,
    color=TARGET_COLOR,
    edgecolors="white",
    linewidths=2,
    zorder=5,
)

ax.scatter(
    ego_df["x"].iloc[-1],
    ego_df["y"].iloc[-1],
    s=220,
    color=EGO_COLOR,
    marker="X",
    edgecolors="white",
    linewidths=2,
    zorder=5,
)

ax.scatter(
    target_df["x"].iloc[-1],
    target_df["y"].iloc[-1],
    s=220,
    color=TARGET_COLOR,
    marker="X",
    edgecolors="white",
    linewidths=2,
    zorder=5,
)


# ------------------------------------------------------------
# LEGEND
# ------------------------------------------------------------

ax.plot(
    [],
    [],
    color=EGO_COLOR,
    linewidth=5,
    label="Ego Vehicle",
)

ax.plot(
    [],
    [],
    color=TARGET_COLOR,
    linewidth=5,
    label="Target Vehicle",
)

legend = ax.legend(
    loc="upper right",
    fontsize=16,
    facecolor="#222222",
    edgecolor="#444444",
)

for text in legend.get_texts():

    text.set_color("white")


# ------------------------------------------------------------
# TITLES
# ------------------------------------------------------------

ax.set_title(
    "ADAS Interaction Trajectory Visualization",
    fontsize=24,
    color="white",
    pad=20,
)

ax.set_xlabel(
    "Longitudinal Position (m)",
    fontsize=18,
    color="white",
)

ax.set_ylabel(
    "Lateral Position (m)",
    fontsize=18,
    color="white",
)


# ------------------------------------------------------------
# GRID / AXES
# ------------------------------------------------------------

ax.grid(
    alpha=0.15,
    color="white",
)

ax.tick_params(
    colors="white",
    labelsize=14,
)

for spine in ax.spines.values():

    spine.set_color("white")


# ------------------------------------------------------------
# VIEWPORT
# ------------------------------------------------------------

x_min = min(
    ego_df["x"].min(),
    target_df["x"].min(),
) - 20

x_max = max(
    ego_df["x"].max(),
    target_df["x"].max(),
) + 20

ax.set_xlim(x_min, x_max)

ax.set_ylim(-10, 1)

# exaggerate lateral motion slightly
ax.set_aspect(6)


# ------------------------------------------------------------
# OUTPUT
# ------------------------------------------------------------

os.makedirs(
    "outputs/figures",
    exist_ok=True,
)

output_path = "outputs/figures/bev_plot_v2.png"

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight",
    facecolor=fig.get_facecolor(),
)

print(f"\nSaved professional BEV plot to: {output_path}\n")