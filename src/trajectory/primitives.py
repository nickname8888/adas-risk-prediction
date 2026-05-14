import numpy as np


# =========================================================
# BASIC SMOOTH INTERPOLATION
# =========================================================

def smooth_step(alpha):

    alpha = np.clip(
        alpha,
        0.0,
        1.0,
    )

    return (
        3 * alpha**2
        - 2 * alpha**3
    )


# =========================================================
# HUMAN-LIKE ASYMMETRIC INTERPOLATION
# =========================================================

def asymmetric_smooth(
    alpha,
    aggression=0.5,
):

    alpha = np.clip(
        alpha,
        0.0,
        1.0,
    )

    exponent = (
        1.5
        - aggression
    )

    alpha = alpha**exponent

    return smooth_step(
        alpha
    )


# =========================================================
# SAFE / GENERAL MERGE
# =========================================================

def smooth_lane_change(
    t,
    start_time,
    duration,
    start_y,
    target_y,
    aggression=0.5,
):

    if t < start_time:

        return start_y

    alpha = (
        t - start_time
    ) / duration

    alpha = asymmetric_smooth(
        alpha,
        aggression,
    )

    return (
        start_y
        + (target_y - start_y)
        * alpha
    )


# =========================================================
# ABORTED MERGE
# =========================================================

def aborted_merge_motion(
    t,
    start_time,
    duration,
    start_y,
    target_y,
    abort_depth=0.7,
):

    if t < start_time:

        return start_y

    elapsed = (
        t - start_time
    )

    half_duration = (
        duration / 2
    )

    partial_target = (
        start_y
        + (target_y - start_y)
        * abort_depth
    )

    # -----------------------------------------------------
    # INITIATE MERGE
    # -----------------------------------------------------

    if elapsed <= half_duration:

        alpha = (
            elapsed
            / half_duration
        )

        alpha = smooth_step(
            alpha
        )

        return (
            start_y
            + (partial_target - start_y)
            * alpha
        )

    # -----------------------------------------------------
    # RETURN TO ORIGINAL LANE
    # -----------------------------------------------------

    alpha = (
        elapsed - half_duration
    ) / half_duration

    alpha = smooth_step(
        alpha
    )

    return (
        partial_target
        + (start_y - partial_target)
        * alpha
    )


# =========================================================
# FAKE DRIFT
# =========================================================

def fake_drift_motion(
    t,
    start_time,
    duration,
    start_y,
    drift_strength=0.8,
):

    if t < start_time:

        return start_y

    elapsed = (
        t - start_time
    )

    half_duration = (
        duration / 2
    )

    drift_target = (
        start_y
        + drift_strength
    )

    # -----------------------------------------------------
    # DRIFT OUTWARD
    # -----------------------------------------------------

    if elapsed <= half_duration:

        alpha = (
            elapsed
            / half_duration
        )

        alpha = smooth_step(
            alpha
        )

        return (
            start_y
            + (drift_target - start_y)
            * alpha
        )

    # -----------------------------------------------------
    # RETURN BACK
    # -----------------------------------------------------

    alpha = (
        elapsed - half_duration
    ) / half_duration

    alpha = smooth_step(
        alpha
    )

    return (
        drift_target
        + (start_y - drift_target)
        * alpha
    )


# =========================================================
# OSCILLATORY INDECISION
# =========================================================

def oscillatory_motion(
    t,
    start_time,
    duration,
    start_y,
    target_y,
    strength=0.5,
):

    if t < start_time:

        return start_y

    alpha = (
        t - start_time
    ) / duration

    alpha = np.clip(
        alpha,
        0.0,
        1.0,
    )

    base = (
        start_y
        + (target_y - start_y)
        * alpha
    )

    oscillation = (
        np.sin(alpha * np.pi * 4)
        * strength
    )

    return (
        base
        + oscillation
    )


# =========================================================
# HUMAN-LIKE MICRO CORRECTIONS
# =========================================================

def add_lateral_noise(
    y,
    t,
    noise_strength=0.02,
):

    low_freq = (
        np.sin(t * 0.7)
        * noise_strength
    )

    high_freq = (
        np.sin(t * 3.1)
        * noise_strength
        * 0.4
    )

    return (
        y
        + low_freq
        + high_freq
    )


# =========================================================
# LONGITUDINAL SPEED VARIATION
# =========================================================

def longitudinal_speed_profile(
    base_speed,
    t,
    variation_strength=0.5,
):

    modulation = (
        np.sin(t * 0.4)
        * variation_strength
    )

    return (
        base_speed
        + modulation
    )


# =========================================================
# LONGITUDINAL POSITION
# =========================================================

def longitudinal_position(
    initial_x,
    speed,
    t,
):

    return (
        initial_x
        + speed * t
    )