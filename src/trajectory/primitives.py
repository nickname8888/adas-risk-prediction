import numpy as np


# ---------------------------------------------------------
# BASIC SMOOTH INTERPOLATION
# ---------------------------------------------------------

def smooth_step(start, end, alpha):
    alpha = np.clip(alpha, 0.0, 1.0)
    smooth_alpha = 3 * alpha**2 - 2 * alpha**3
    return start + (end - start) * smooth_alpha


# ---------------------------------------------------------
# SAFE MERGE
# ---------------------------------------------------------

def safe_merge_y(
    t,
    start_time,
    duration,
    start_lane_y,
    target_lane_y,
):

    if t < start_time:
        return start_lane_y
    alpha = (t - start_time) / duration

    return smooth_step(
        start_lane_y,
        target_lane_y,
        alpha,
    )


# ---------------------------------------------------------
# FAKE DRIFT
# ---------------------------------------------------------

def fake_drift_y(
    t,
    start_time,
    duration,
    start_lane_y,
    drift_strength=0.8,
):

    drift_target = start_lane_y - drift_strength
    half_duration = duration / 2
    if t < start_time:
        return start_lane_y
    elapsed = t - start_time

    # drift toward adjacent lane
    if elapsed <= half_duration:
        alpha = elapsed / half_duration

        return smooth_step(
            start_lane_y,
            drift_target,
            alpha,
        )

    # drift back
    alpha = (elapsed - half_duration) / half_duration

    return smooth_step(
        drift_target,
        start_lane_y,
        alpha,
    )


# ---------------------------------------------------------
# ABORTED MERGE
# ---------------------------------------------------------

def aborted_merge_y(
    t,
    start_time,
    duration,
    start_lane_y,
    target_lane_y,
):
    half_duration = duration / 2
    if t < start_time:
        return start_lane_y

    elapsed = t - start_time

    # initiate merge
    if elapsed <= half_duration:
        alpha = elapsed / half_duration
        return smooth_step(
            start_lane_y,
            target_lane_y,
            alpha,
        )

    # reverse back
    alpha = (elapsed - half_duration) / half_duration

    return smooth_step(
        target_lane_y,
        start_lane_y,
        alpha,
    )


# ---------------------------------------------------------
# LONGITUDINAL MOTION
# ---------------------------------------------------------

def longitudinal_position(
    initial_x,
    speed,
    t,
):
    return initial_x + speed * t