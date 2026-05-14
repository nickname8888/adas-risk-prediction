from src.config.load_config import load_config

from src.simulation.parameter_sampler import (
    ParameterSampler,
)

from src.trajectory.trajectory_generator import (
    TrajectoryGenerator,
)

from src.visualization.bev_from_trajectory import (
    plot_scenario_trajectory,
)

config = load_config()
sampler = ParameterSampler()
generator = TrajectoryGenerator(
    config=config,
)


# ---------------------------------------------------------
# SELECT FAMILY
# ---------------------------------------------------------

family_name = "aborted_merge"

# ---------------------------------------------------------
# SAMPLE PARAMETERS
# ---------------------------------------------------------

params = sampler.sample(
    family_name
)

print("\nSampled Parameters:\n")
for key, value in params.items():
    print(f"{key}: {value}")


# ---------------------------------------------------------
# GENERATE TRAJECTORY
# ---------------------------------------------------------

trajectory = generator.generate(
    family_name=family_name,
    params=params,
)


# ---------------------------------------------------------
# VISUALIZE
# ---------------------------------------------------------

scenario_id = f"{family_name}_0000"

plot_scenario_trajectory(
    trajectory,
    scenario_id=scenario_id,
)