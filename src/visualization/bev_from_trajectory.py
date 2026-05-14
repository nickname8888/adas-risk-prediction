import os
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np

# =========================================================
# VISUAL STYLE
# =========================================================

BACKGROUND_COLOR = "#0e1117"
ROAD_COLOR = "#2a2a2a"
LANE_COLOR = "#e0e0e0"
GRID_COLOR = "#444444"
EGO_COLOR = "#00d4ff"
TARGET_COLOR = "#ff6b35"
EGO_MARKER_COLOR = "#008fb3"
TARGET_MARKER_COLOR = "#cc5522"
TIME_COLOR = "#ffffff"


# =========================================================
# ROAD CONFIG
# =========================================================

LANE_WIDTH = 3.0

LANE_CENTERS = [
    -1.5,
    -4.5,
    -7.5,
]

LANE_BOUNDARIES = [
    0,
    -3,
    -6,
    -9,
]


# =========================================================
# HELPERS
# =========================================================

def build_segments(x, y):
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate(
        [points[:-1], points[1:]],
        axis=1,
    )
    return segments


def sample_time_indices(points):
    sampled = []
    last_second = -1
    for i, point in enumerate(points):
        current_second = int(point.t)
        if current_second != last_second:
            sampled.append(i)
            last_second = current_second
    return sampled


# =========================================================
# MAIN VISUALIZER
# =========================================================

def plot_scenario_trajectory(
    scenario_trajectory,
    scenario_id,
):

    ego_points = scenario_trajectory.ego.points
    target_points = scenario_trajectory.target.points
    ego_x = [p.x for p in ego_points]
    ego_y = [p.y for p in ego_points]
    target_x = [p.x for p in target_points]
    target_y = [p.y for p in target_points]

    # -----------------------------------------------------
    # FIGURE
    # -----------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(18, 9),
    )

    fig.patch.set_facecolor(
        BACKGROUND_COLOR
    )

    ax.set_facecolor(
        BACKGROUND_COLOR
    )

    # -----------------------------------------------------
    # ROAD SURFACE
    # -----------------------------------------------------

    ax.fill_between(
        [0, 10000],
        -10.5,
        1.5,
        color=ROAD_COLOR,
        alpha=1.0,
    )

    # -----------------------------------------------------
    # LANE BOUNDARIES
    # -----------------------------------------------------

    for lane_y in LANE_BOUNDARIES:
        ax.plot(
            [0, 10000],
            [lane_y, lane_y],
            linestyle="--",
            linewidth=2.5,
            color=LANE_COLOR,
            alpha=0.7,
        )

    # -----------------------------------------------------
    # LANE CENTER GUIDES
    # -----------------------------------------------------

    for lane_y in LANE_CENTERS:
        ax.plot(
            [0, 10000],
            [lane_y, lane_y],
            linestyle=":",
            linewidth=1,
            color="#777777",
            alpha=0.25,
        )

    # -----------------------------------------------------
    # EGO TRAJECTORY
    # -----------------------------------------------------

    ego_segments = build_segments(
        ego_x,
        ego_y,
    )

    ego_collection = LineCollection(
        ego_segments,
        linewidths=5,
        colors=EGO_COLOR,
        alpha=0.75,
        zorder=2,
    )

    ax.add_collection(
        ego_collection
    )

    # -----------------------------------------------------
    # TARGET TRAJECTORY
    # -----------------------------------------------------

    target_segments = build_segments(
        target_x,
        target_y,
    )

    target_collection = LineCollection(
        target_segments,
        linewidths=7,
        colors=TARGET_COLOR,
        alpha=0.95,
        zorder=3,
    )

    ax.add_collection(
        target_collection
    )

    # -----------------------------------------------------
    # TEMPORAL POSITION MARKERS
    # -----------------------------------------------------

    ego_sample_indices = sample_time_indices(
        ego_points
    )

    target_sample_indices = sample_time_indices(
        target_points
    )

    # Ego markers
    for idx in ego_sample_indices:
        point = ego_points[idx]
        ax.scatter(
            point.x,
            point.y,
            s=65,
            color=EGO_MARKER_COLOR,
            edgecolors="white",
            linewidths=1,
            alpha=0.9,
            zorder=5,
        )

    # Target markers + labels
    for idx in target_sample_indices:
        point = target_points[idx]
        ax.scatter(
            point.x,
            point.y,
            s=75,
            color=TARGET_MARKER_COLOR,
            edgecolors="white",
            linewidths=1,
            alpha=0.95,
            zorder=6,
        )

        ax.text(
            point.x,
            point.y + 0.9,
            f"{int(point.t)}s",
            fontsize=9,
            color=TIME_COLOR,
            alpha=0.85,
            ha="center",
            fontweight="bold",
        )

    # -----------------------------------------------------
    # START MARKERS
    # -----------------------------------------------------

    ax.scatter(
        ego_x[0],
        ego_y[0],
        s=260,
        color=EGO_COLOR,
        edgecolors="white",
        linewidths=2.5,
        zorder=7,
    )

    ax.scatter(
        target_x[0],
        target_y[0],
        s=260,
        color=TARGET_COLOR,
        edgecolors="white",
        linewidths=2.5,
        zorder=7,
    )

    # -----------------------------------------------------
    # END MARKERS
    # -----------------------------------------------------

    ax.scatter(
        ego_x[-1],
        ego_y[-1],
        s=360,
        color=EGO_COLOR,
        marker="X",
        edgecolors="white",
        linewidths=2.5,
        zorder=8,
    )

    ax.scatter(
        target_x[-1],
        target_y[-1],
        s=360,
        color=TARGET_COLOR,
        marker="X",
        edgecolors="white",
        linewidths=2.5,
        zorder=8,
    )

    # -----------------------------------------------------
    # LEGEND
    # -----------------------------------------------------

    ax.plot(
        [],
        [],
        color=EGO_COLOR,
        linewidth=5,
        alpha=0.8,
        label="Ego Vehicle",
    )

    ax.plot(
        [],
        [],
        color=TARGET_COLOR,
        linewidth=7,
        label="Target Vehicle",
    )

    legend = ax.legend(
        loc="upper right",
        fontsize=20,
        facecolor="#1c1c1c",
        edgecolor="#555555",
    )

    for text in legend.get_texts():
        text.set_color("white")

    # -----------------------------------------------------
    # TITLES
    # -----------------------------------------------------

    ax.set_title(
        f"ADAS Behavioral Trajectory: {scenario_trajectory.family}",
        fontsize=34,
        color="white",
        pad=24,
        fontweight="bold",
    )

    ax.set_xlabel(
        "Longitudinal Position (meters)",
        fontsize=22,
        color="white",
        labelpad=16,
    )

    ax.set_ylabel(
        "Lateral Position (meters)",
        fontsize=22,
        color="white",
        labelpad=16,
    )

    # -----------------------------------------------------
    # GRID / AXES
    # -----------------------------------------------------

    ax.grid(
        alpha=0.18,
        color=GRID_COLOR,
        linewidth=1,
    )

    ax.tick_params(
        colors="white",
        labelsize=16,
    )

    for spine in ax.spines.values():
        spine.set_color("white")

    # -----------------------------------------------------
    # VIEWPORT
    # -----------------------------------------------------

    x_min = min(
        min(ego_x),
        min(target_x),
    ) - 20

    x_max = max(
        max(ego_x),
        max(target_x),
    ) + 20

    ax.set_xlim(
        x_min,
        x_max,
    )

    ax.set_ylim(
        -10,
        1,
    )

    ax.set_aspect(6)

    # -----------------------------------------------------
    # OUTPUT
    # -----------------------------------------------------

    os.makedirs(
        "outputs/figures",
        exist_ok=True,
    )

    output_path = (
        f"outputs/figures/"
        f"{scenario_id}_trajectory.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
        facecolor=fig.get_facecolor(),
    )

    print(
        f"\nSaved trajectory visualization to:\n{output_path}\n"
    )