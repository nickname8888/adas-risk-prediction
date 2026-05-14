import sys

from src.config.load_config import (
    load_config,
)

from src.simulation.parameter_sampler import (
    ParameterSampler,
)

from src.trajectory.trajectory_generator import (
    TrajectoryGenerator,
)

from src.visualization.bev_from_trajectory import (
    plot_scenario_trajectory,
)


# =========================================================
# LOAD CONFIG
# =========================================================

config = load_config()

sampler = ParameterSampler()

generator = TrajectoryGenerator(
    config=config,
)


# =========================================================
# FAMILY INDEX MAP
# =========================================================

FAMILY_MAP = {

    1: "safe_merge",

    2: "aggressive_cutin",

    3: "hesitant_merge",

    4: "aborted_merge",

    5: "fake_drift",

    6: "late_commit",

    7: "cooperative_yield",

    8: "dense_pressure",

    9: "oscillatory_indecision",
}


# =========================================================
# CLI ARGUMENT
# =========================================================

if len(sys.argv) != 2:

    print("\nUsage:\n")

    print(
        "python3 -m "
        "src.trajectory.generate_trajectory_demo "
        "<family_index>\n"
    )

    print("Available Families:\n")

    for idx, family in FAMILY_MAP.items():

        print(f"{idx}: {family}")

    print()

    sys.exit(1)


try:

    family_index = int(
        sys.argv[1]
    )

except ValueError:

    print(
        "\nFamily index must be an integer.\n"
    )

    sys.exit(1)


if family_index not in FAMILY_MAP:

    print(
        "\nInvalid family index.\n"
    )

    print("Available Families:\n")

    for idx, family in FAMILY_MAP.items():

        print(f"{idx}: {family}")

    print()

    sys.exit(1)


family_name = FAMILY_MAP[
    family_index
]


# =========================================================
# SAMPLE PARAMETERS
# =========================================================

params = sampler.sample(
    family_name
)

print("\n=================================================")

print(
    f"Generating Family: {family_name}"
)

print("=================================================\n")

print("Sampled Parameters:\n")

for key, value in params.items():

    print(f"{key}: {value}")

print("\n=================================================\n")


# =========================================================
# GENERATE TRAJECTORY
# =========================================================

trajectory = generator.generate(
    family_name=family_name,
    params=params,
)


# =========================================================
# VISUALIZE
# =========================================================

scenario_id = (
    f"{family_name}_0000"
)

plot_scenario_trajectory(
    trajectory,
    scenario_id=scenario_id,
)


# =========================================================
# DONE
# =========================================================

print(
    "\nTrajectory generation complete.\n"
)