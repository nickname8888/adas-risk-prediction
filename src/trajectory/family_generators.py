from src.trajectory.primitives import (
    safe_merge_y,
    fake_drift_y,
    aborted_merge_y,
)

# ---------------------------------------------------------
# SAFE MERGE
# ---------------------------------------------------------

def generate_safe_merge_y(
    t,
    params,
):

    return safe_merge_y(
        t=t,
        start_time=params["merge_start_time"],
        duration=params["merge_duration"],
        start_lane_y=-1.5,
        target_lane_y=-4.5,
    )


# ---------------------------------------------------------
# FAKE DRIFT
# ---------------------------------------------------------

def generate_fake_drift_y(
    t,
    params,
):

    return fake_drift_y(
        t=t,
        start_time=params["merge_start_time"],
        duration=params["merge_duration"],
        start_lane_y=-1.5,
        drift_strength=1.2,
    )

# ---------------------------------------------------------
# ABORTED MERGE
# ---------------------------------------------------------

def generate_aborted_merge_y(
    t,
    params,
):

    return aborted_merge_y(
        t=t,
        start_time=params["merge_start_time"],
        duration=params["merge_duration"],
        start_lane_y=-1.5,
        target_lane_y=-3.2,
    )

# ---------------------------------------------------------
# FAMILY REGISTRY
# ---------------------------------------------------------

FAMILY_Y_GENERATORS = {
    "safe_merge": generate_safe_merge_y,
    "fake_drift": generate_fake_drift_y,
    "aborted_merge": generate_aborted_merge_y,
}