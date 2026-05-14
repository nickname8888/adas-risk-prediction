import random
import numpy as np

from src.trajectory.primitives import (
    smooth_lane_change,
    aborted_merge_motion,
    fake_drift_motion,
    oscillatory_motion,
    add_lateral_noise,
    longitudinal_speed_profile,
)


# =========================================================
# LANE CONFIG
# =========================================================

LANE_CENTERS = [
    -1.5,
    -4.5,
    -7.5,
]


# =========================================================
# FAMILY PARAMETER DISTRIBUTIONS
# =========================================================

FAMILY_BEHAVIORS = {

    # -----------------------------------------------------
    # SAFE MERGE
    # -----------------------------------------------------

    "safe_merge": {

        "merge_aggression": (0.2, 0.4),
        "noise_strength": (0.01, 0.03),
        "speed_variation": (0.1, 0.3),
        "commitment": "full",
        "behavior": "smooth_merge",
    },

    # -----------------------------------------------------
    # AGGRESSIVE CUTIN
    # -----------------------------------------------------

    "aggressive_cutin": {
        "merge_aggression": (0.85, 1.0),
        "noise_strength": (0.02, 0.05),
        "speed_variation": (0.8, 1.5),
        "commitment": "full",
        "behavior": "aggressive_merge",
    },

    # -----------------------------------------------------
    # HESITANT MERGE
    # -----------------------------------------------------

    "hesitant_merge": {
        "merge_aggression": (0.2, 0.4),
        "hesitation_strength": (0.4, 0.8),
        "noise_strength": (0.03, 0.07),
        "speed_variation": (0.2, 0.5),
        "commitment": "full",
        "behavior": "hesitant_merge",
    },

    # -----------------------------------------------------
    # ABORTED MERGE
    # -----------------------------------------------------

    "aborted_merge": {
        "merge_aggression": (0.4, 0.7),
        "abort_depth": (0.5, 0.9),
        "noise_strength": (0.03, 0.08),
        "speed_variation": (0.2, 0.6),
        "commitment": "abort",
        "behavior": "aborted_merge",
    },

    # -----------------------------------------------------
    # FAKE DRIFT
    # -----------------------------------------------------

    "fake_drift": {
        "drift_strength": (0.3, 1.2),
        "noise_strength": (0.02, 0.05),
        "speed_variation": (0.05, 0.2),
        "commitment": "none",
        "behavior": "fake_drift",
    },

    # -----------------------------------------------------
    # LATE COMMIT
    # -----------------------------------------------------

    "late_commit": {
        "merge_aggression": (0.75, 1.0),
        "noise_strength": (0.03, 0.07),
        "speed_variation": (0.5, 1.0),
        "commitment": "late",
        "behavior": "late_commit",
    },

    # -----------------------------------------------------
    # COOPERATIVE YIELD
    # -----------------------------------------------------

    "cooperative_yield": {
        "merge_aggression": (0.3, 0.5),
        "noise_strength": (0.02, 0.04),
        "speed_variation": (0.1, 0.4),
        "commitment": "full",
        "behavior": "cooperative_merge",
    },

    # -----------------------------------------------------
    # DENSE PRESSURE
    # -----------------------------------------------------

    "dense_pressure": {
        "merge_aggression": (0.6, 0.9),
        "noise_strength": (0.05, 0.1),
        "speed_variation": (0.5, 1.2),
        "commitment": "full",
        "behavior": "dense_pressure",
    },

    # -----------------------------------------------------
    # OSCILLATORY INDECISION
    # -----------------------------------------------------

    "oscillatory_indecision": {
        "oscillation_strength": (0.4, 1.0),
        "noise_strength": (0.04, 0.09),
        "speed_variation": (0.2, 0.6),
        "commitment": "oscillatory",
        "behavior": "oscillatory",
    },
}


# =========================================================
# RANDOMIZED LANE PAIRING
# =========================================================

# def sample_lane_configuration():
#     ego_lane = random.choice(
#         [-1.5, -4.5]
#     )

#     if ego_lane == -1.5:
#         target_lane = -4.5

#     else:
#         target_lane = -1.5

#     return ego_lane, target_lane

# =========================================================
# FAMILY-AWARE LANE CONFIGURATION
# =========================================================

def sample_family_lane_configuration(
    family_name,
):

    lane_rule = FAMILY_LANE_RULES[
        family_name
    ]

    # -----------------------------------------------------
    # STANDARD MERGE INTERACTIONS
    # -----------------------------------------------------

    if lane_rule == "adjacent_merge":

        valid_pairs = [

            # target left -> ego middle
            (-4.5, -1.5),

            # target right -> ego middle
            (-4.5, -7.5),

            # target middle -> ego left
            (-1.5, -4.5),

            # target middle -> ego right
            (-7.5, -4.5),
        ]

        ego_lane_y, target_lane_y = (
            random.choice(valid_pairs)
        )

        return (
            ego_lane_y,
            target_lane_y,
        )

    # -----------------------------------------------------
    # FAKE DRIFT
    # -----------------------------------------------------

    elif lane_rule == "same_lane_drift":

        # fake drift should stay safely inside road

        safe_lanes = [
            -1.5,
            -4.5,
            -7.5,
        ]

        ego_lane_y = random.choice(
            safe_lanes
        )

        # target remains in same lane
        target_lane_y = ego_lane_y

        return (
            ego_lane_y,
            target_lane_y,
        )

    # -----------------------------------------------------
    # FALLBACK
    # -----------------------------------------------------

    else:

        raise ValueError(
            f"Unknown lane rule: {lane_rule}"
        )

# =========================================================
# FAMILY TRAJECTORY GENERATION
# =========================================================

def generate_family_trajectory(
    family_name,
    t,
    params,
    start_lane_y,
    target_lane_y,
):

    family = FAMILY_BEHAVIORS[
        family_name
    ]
    behavior = family["behavior"]
    noise_strength = random.uniform(
        *family["noise_strength"]
    )

    # -----------------------------------------------------
    # SAFE MERGE
    # -----------------------------------------------------

    if behavior == "smooth_merge":
        y = smooth_lane_change(
            t=t,
            start_time=params["merge_start_time"],
            duration=params["merge_duration"],
            start_y=start_lane_y,
            target_y=target_lane_y,
            aggression=random.uniform(
                *family["merge_aggression"]
            ),
        )

    # -----------------------------------------------------
    # AGGRESSIVE CUTIN
    # -----------------------------------------------------

    elif behavior == "aggressive_merge":
        y = smooth_lane_change(
            t=t,
            start_time=params["merge_start_time"],
            duration=params["merge_duration"] * 0.6,
            start_y=start_lane_y,
            target_y=target_lane_y,
            aggression=1.0,
        )

    # -----------------------------------------------------
    # HESITANT MERGE
    # -----------------------------------------------------

    elif behavior == "hesitant_merge":
        hesitation = random.uniform(
            *family["hesitation_strength"]
        )
        y = smooth_lane_change(
            t=t,
            start_time=params["merge_start_time"] + hesitation,
            duration=params["merge_duration"] * 1.5,
            start_y=start_lane_y,
            target_y=target_lane_y,
            aggression=0.3,
        )

    # -----------------------------------------------------
    # ABORTED MERGE
    # -----------------------------------------------------

    elif behavior == "aborted_merge":
        y = aborted_merge_motion(
            t=t,
            start_time=params["merge_start_time"],
            duration=params["merge_duration"],
            start_y=start_lane_y,
            target_y=target_lane_y,
            abort_depth=random.uniform(
                *family["abort_depth"]
            ),
        )

    # -----------------------------------------------------
    # FAKE DRIFT
    # -----------------------------------------------------

    elif behavior == "fake_drift":
        y = fake_drift_motion(
            t=t,
            start_time=params["merge_start_time"],
            duration=params["merge_duration"],
            start_y=start_lane_y,
            drift_strength=random.uniform(
                *family["drift_strength"]
            ),
        )

    # -----------------------------------------------------
    # LATE COMMIT
    # -----------------------------------------------------

    elif behavior == "late_commit":
        y = smooth_lane_change(
            t=t,
            start_time=params["merge_start_time"] + 2.0,
            duration=params["merge_duration"] * 0.5,
            start_y=start_lane_y,
            target_y=target_lane_y,
            aggression=1.0,
        )

    # -----------------------------------------------------
    # COOPERATIVE YIELD
    # -----------------------------------------------------

    elif behavior == "cooperative_merge":
        y = smooth_lane_change(
            t=t,
            start_time=params["merge_start_time"],
            duration=params["merge_duration"],
            start_y=start_lane_y,
            target_y=target_lane_y,
            aggression=0.4,
        )

    # -----------------------------------------------------
    # DENSE PRESSURE
    # -----------------------------------------------------

    elif behavior == "dense_pressure":
        y = smooth_lane_change(
            t=t,
            start_time=params["merge_start_time"],
            duration=params["merge_duration"] * 0.7,
            start_y=start_lane_y,
            target_y=target_lane_y,
            aggression=0.8,
        )

    # -----------------------------------------------------
    # OSCILLATORY
    # -----------------------------------------------------

    elif behavior == "oscillatory":
        y = oscillatory_motion(
            t=t,
            start_time=params["merge_start_time"],
            duration=params["merge_duration"],
            start_y=start_lane_y,
            target_y=target_lane_y,
            strength=random.uniform(
                *family["oscillation_strength"]
            ),
        )

    else:
        y = start_lane_y

    # add small human-like imperfections
    y = add_lateral_noise(
        y,
        t,
        noise_strength,
    )

    return y

FAMILY_LANE_RULES = {
    "safe_merge": "adjacent_merge",
    "aggressive_cutin": "adjacent_merge",
    "hesitant_merge": "adjacent_merge",
    "aborted_merge": "adjacent_merge",
    "late_commit": "adjacent_merge",
    "cooperative_yield": "adjacent_merge",
    "dense_pressure": "adjacent_merge",
    "oscillatory_indecision": "adjacent_merge",
    "fake_drift": "adjacent_merge",
}