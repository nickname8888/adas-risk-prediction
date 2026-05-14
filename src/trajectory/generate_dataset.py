import os
import sys
import json
import random

from src.config.load_config import (
    load_config,
)

from src.simulation.parameter_sampler import (
    ParameterSampler,
)

from src.trajectory.trajectory_generator import (
    TrajectoryGenerator,
)

from src.trajectory.family_generators import (
    FAMILY_BEHAVIORS,
)

from src.trajectory.save_trajectory import (
    save_scenario_trajectory,
)

from src.visualization.bev_from_trajectory import (
    plot_scenario_trajectory,
)

from src.conversion.trajectory_to_xosc import (
    export_scenario_to_xosc,
)

from src.simulation.run_esmini import (
    run_esmini_headless,
)

from src.preprocessing.convert_dat_to_csv import (
    convert_dat_to_csv,
)


# =========================================================
# LOAD CONFIG
# =========================================================

config = load_config()

simulation_config = config["simulation"]

dataset_config = config["dataset"]

output_config = config["output"]

esmini_config = config["esmini"]


# =========================================================
# RANDOM SEED
# =========================================================

random.seed(
    dataset_config["random_seed"]
)


# =========================================================
# OUTPUT DIRECTORIES
# =========================================================

XOSC_DIR = output_config["xosc_dir"]

METADATA_DIR = output_config["metadata_dir"]

LOG_DIR = output_config["log_dir"]

CSV_DIR = output_config["csv_dir"]

FIGURE_DIR = output_config["figure_dir"]

TRAJECTORY_DIR = output_config[
    "trajectory_dir"
]


# =========================================================
# INITIALIZE COMPONENTS
# =========================================================

sampler = ParameterSampler()

generator = TrajectoryGenerator(
    config=config,
)


# =========================================================
# CLI ARGUMENT
# =========================================================

if len(sys.argv) != 2:

    print("\nUsage:\n")

    print(
        "python3 -m "
        "src.trajectory.generate_dataset "
        "<scenarios_per_family>\n"
    )

    sys.exit(1)


try:

    scenarios_per_family = int(
        sys.argv[1]
    )

except ValueError:

    print(
        "\nScenario count must be integer.\n"
    )

    sys.exit(1)


# =========================================================
# MAIN GENERATION LOOP
# =========================================================

def generate_dataset():

    print(
        "\n================================================="
    )

    print(
        "GENERATING SYNTHETIC ADAS DATASET"
    )

    print(
        "=================================================\n"
    )

    family_names = list(
        FAMILY_BEHAVIORS.keys()
    )

    total_scenarios = (
        len(family_names)
        * scenarios_per_family
    )

    scenario_counter = 0

    for family_name in family_names:

        print(
            "\n-------------------------------------------------"
        )

        print(
            f"Generating family: "
            f"{family_name}"
        )

        print(
            "-------------------------------------------------\n"
        )

        for scenario_idx in range(
            scenarios_per_family
        ):

            scenario_counter += 1

            scenario_id = (
                f"{family_name}_"
                f"{scenario_idx:04d}"
            )

            print(
                f"[{scenario_counter}/"
                f"{total_scenarios}] "
                f"{scenario_id}"
            )

            # =============================================
            # SAMPLE PARAMETERS
            # =============================================

            params = sampler.sample(
                family_name
            )

            # =============================================
            # GENERATE TRAJECTORY
            # =============================================

            trajectory = generator.generate(
                family_name=family_name,
                params=params,
            )

            # =============================================
            # SAVE TRAJECTORY JSON
            # =============================================

            save_scenario_trajectory(
                scenario_trajectory=trajectory,
                scenario_id=scenario_id,
                output_dir=TRAJECTORY_DIR,
            )

            # =============================================
            # EXPORT XOSC
            # =============================================

            xosc_path = (
                export_scenario_to_xosc(
                    scenario_trajectory=trajectory,
                    scenario_id=scenario_id,
                    output_dir=XOSC_DIR,
                )
            )

            # =============================================
            # RUN ESMINI
            # =============================================

            dat_path = (
                run_esmini_headless(
                    esmini_path=(
                        esmini_config[
                            "executable_path"
                        ]
                    ),
                    xosc_path=xosc_path,
                    output_log_dir=LOG_DIR,
                )
            )

            # =============================================
            # DAT → CSV
            # =============================================

            csv_path = (
                convert_dat_to_csv(
                    dat2csv_path=(
                        esmini_config[
                            "dat2csv_path"
                        ]
                    ),
                    dat_path=dat_path,
                    output_csv_dir=CSV_DIR,
                )
            )

            # =============================================
            # SAVE METADATA
            # =============================================

            os.makedirs(
                METADATA_DIR,
                exist_ok=True,
            )

            metadata = {

                "scenario_id":
                    scenario_id,

                "family":
                    family_name,

                "parameters":
                    params,

                "trajectory_json":
                    os.path.join(
                        TRAJECTORY_DIR,
                        (
                            f"{scenario_id}"
                            "_trajectory.json"
                        ),
                    ),

                "xosc":
                    xosc_path,

                "dat":
                    dat_path,

                "csv":
                    csv_path,
            }

            metadata_path = os.path.join(
                METADATA_DIR,
                f"{scenario_id}.json",
            )

            with open(
                metadata_path,
                "w",
            ) as f:

                json.dump(
                    metadata,
                    f,
                    indent=4,
                )

            # =============================================
            # SAVE BEV PLOT
            # =============================================

            plot_scenario_trajectory(
                trajectory,
                scenario_id=scenario_id,
            )

            print()

    print(
        "\n================================================="
    )

    print(
        "DATASET GENERATION COMPLETE"
    )

    print(
        "=================================================\n"
    )


# =========================================================
# ENTRYPOINT
# =========================================================

if __name__ == "__main__":
    generate_dataset()