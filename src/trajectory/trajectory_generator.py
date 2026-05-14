import numpy as np

from src.trajectory.family_generators import (
    FAMILY_Y_GENERATORS,
)

from src.trajectory.primitives import (
    longitudinal_position,
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

    # -----------------------------------------------------
    # MAIN GENERATION
    # -----------------------------------------------------

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

        # ego vehicle trajectory
        ego_points = self.generate_ego_trajectory(
            timesteps,
            params,
        )

        # target vehicle trajectory
        target_points = self.generate_target_trajectory(
            timesteps,
            family_name,
            params,
        )

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

    # -----------------------------------------------------
    # EGO TRAJECTORY
    # -----------------------------------------------------

    def generate_ego_trajectory(
        self,
        timesteps,
        params,
    ):
        points = []
        initial_x = 50
        lane_y = -4.5
        speed = params["ego_speed"]

        for t in timesteps:
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

    # -----------------------------------------------------
    # TARGET TRAJECTORY
    # -----------------------------------------------------
    def generate_target_trajectory(
        self,
        timesteps,
        family_name,
        params,
    ):

        points = []
        initial_x = 50 + params["initial_gap"]
        speed = params["npc_speed"]
        y_generator = FAMILY_Y_GENERATORS[
            family_name
        ]

        for t in timesteps:
            x = longitudinal_position(
                initial_x,
                speed,
                t,
            )

            y = y_generator(
                t,
                params,
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