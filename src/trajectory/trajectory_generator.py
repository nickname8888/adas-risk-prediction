import random
import numpy as np

from src.trajectory.family_generators import (
    generate_family_trajectory,
    sample_family_lane_configuration,
    FAMILY_BEHAVIORS,
)

from src.trajectory.primitives import (
    longitudinal_position,
    longitudinal_speed_profile,
)

from src.trajectory.trajectory_types import (
    TrajectoryPoint,
    VehicleTrajectory,
    ScenarioTrajectory,
)


class TrajectoryGenerator:

    def __init__(
        self,
        config,
    ):

        self.config = config

        self.dt = config["simulation"]["timestep"]

        self.duration = config["simulation"]["duration"]

    # =====================================================
    # MAIN GENERATION
    # =====================================================

    def generate(
        self,
        family_name,
        params,
    ):

        timesteps = np.arange(
            0,
            self.duration,
            self.dt,
        )

        # -------------------------------------------------
        # FAMILY-AWARE LANE CONFIGURATION
        # -------------------------------------------------

        (
            ego_lane_y,
            target_lane_y,
        ) = sample_family_lane_configuration(
            family_name
        )

        # -------------------------------------------------
        # EGO TRAJECTORY
        # -------------------------------------------------

        ego_points = self.generate_ego_trajectory(
            timesteps=timesteps,
            params=params,
            lane_y=ego_lane_y,
            family_name=family_name,
        )

        # -------------------------------------------------
        # TARGET TRAJECTORY
        # -------------------------------------------------

        target_points = (
            self.generate_target_trajectory(
                timesteps=timesteps,
                family_name=family_name,
                params=params,
                start_lane_y=target_lane_y,
                target_lane_y=ego_lane_y,
            )
        )

        # -------------------------------------------------
        # WRAP OUTPUT
        # -------------------------------------------------

        ego_trajectory = VehicleTrajectory(
            name="Ego",
            points=ego_points,
        )

        target_trajectory = VehicleTrajectory(
            name="Target",
            points=target_points,
        )

        return ScenarioTrajectory(
            family=family_name,
            ego=ego_trajectory,
            target=target_trajectory,
        )

    # =====================================================
    # EGO TRAJECTORY
    # =====================================================

    def generate_ego_trajectory(
        self,
        timesteps,
        params,
        lane_y,
        family_name,
    ):

        points = []

        initial_x = 50

        base_speed = params["ego_speed"]

        family = FAMILY_BEHAVIORS[
            family_name
        ]

        variation_strength = random.uniform(
            *family["speed_variation"]
        )

        for t in timesteps:

            speed = longitudinal_speed_profile(
                base_speed=base_speed,
                t=t,
                variation_strength=(
                    variation_strength * 0.2
                ),
            )

            # cooperative yielding
            if family_name == "cooperative_yield":

                if (
                    params["merge_start_time"]
                    <= t
                    <= params["merge_start_time"] + 2
                ):

                    speed -= 2.0

            x = longitudinal_position(
                initial_x,
                speed,
                t,
            )

            points.append(
                TrajectoryPoint(
                    t=float(t),
                    x=float(x),
                    y=float(lane_y),
                    speed=float(speed),
                )
            )

        return points

    # =====================================================
    # TARGET TRAJECTORY
    # =====================================================

    def generate_target_trajectory(
        self,
        timesteps,
        family_name,
        params,
        start_lane_y,
        target_lane_y,
    ):

        points = []

        initial_x = (
            50
            + params["initial_gap"]
        )

        base_speed = params["npc_speed"]

        family = FAMILY_BEHAVIORS[
            family_name
        ]

        variation_strength = random.uniform(
            *family["speed_variation"]
        )

        for t in timesteps:

            # -------------------------------------------------
            # LONGITUDINAL DYNAMICS
            # -------------------------------------------------

            speed = longitudinal_speed_profile(
                base_speed=base_speed,
                t=t,
                variation_strength=variation_strength,
            )

            # aggressive acceleration
            if family_name == "aggressive_cutin":

                if (
                    params["merge_start_time"]
                    <= t
                    <= params["merge_start_time"] + 2
                ):

                    speed += 3.0

            # hesitant slowdown
            elif family_name == "hesitant_merge":

                if (
                    params["merge_start_time"]
                    <= t
                    <= params["merge_start_time"] + 2
                ):

                    speed -= 1.5

            # late acceleration
            elif family_name == "late_commit":

                if (
                    t
                    >= params["merge_start_time"]
                ):

                    speed += 2.0

            x = longitudinal_position(
                initial_x,
                speed,
                t,
            )

            # -------------------------------------------------
            # LATERAL FAMILY BEHAVIOR
            # -------------------------------------------------

            y = generate_family_trajectory(
                family_name=family_name,
                t=t,
                params=params,
                start_lane_y=start_lane_y,
                target_lane_y=target_lane_y,
            )

            points.append(
                TrajectoryPoint(
                    t=float(t),
                    x=float(x),
                    y=float(y),
                    speed=float(speed),
                )
            )

        return points