import json
import os

# =========================================================
# TRAJECTORY POINT SERIALIZATION
# =========================================================

def trajectory_point_to_dict(
    point,
):
    return {
        "t": point.t,
        "x": point.x,
        "y": point.y,
        "speed": point.speed,
    }


# =========================================================
# VEHICLE TRAJECTORY SERIALIZATION
# =========================================================

def vehicle_trajectory_to_dict(
    trajectory,
):
    return {
        "name": trajectory.name,
        "points": [
            trajectory_point_to_dict(
                point
            )
            for point in trajectory.points
        ],
    }


# =========================================================
# SCENARIO TRAJECTORY SERIALIZATION
# =========================================================

def scenario_trajectory_to_dict(
    scenario_trajectory,
):
    return {
        "family": (
            scenario_trajectory.family
        ),
        "ego": vehicle_trajectory_to_dict(
            scenario_trajectory.ego
        ),
        "target": vehicle_trajectory_to_dict(
            scenario_trajectory.target
        ),
    }


# =========================================================
# SAVE TRAJECTORY JSON
# =========================================================

def save_scenario_trajectory(
    scenario_trajectory,
    scenario_id,
    output_dir,
):
    os.makedirs(
        output_dir,
        exist_ok=True,
    )

    output_path = os.path.join(
        output_dir,
        f"{scenario_id}_trajectory.json",
    )

    trajectory_dict = (
        scenario_trajectory_to_dict(
            scenario_trajectory
        )
    )

    with open(
        output_path,
        "w",
    ) as f:

        json.dump(
            trajectory_dict,
            f,
            indent=4,
        )

    print(
        f"\nSaved trajectory JSON:\n"
        f"{output_path}\n"
    )

    return output_path