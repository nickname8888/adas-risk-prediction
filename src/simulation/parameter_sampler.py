import random

from src.simulation.behavior_families import BEHAVIOR_FAMILIES


class ParameterSampler:
    def sample(self, family_name: str):
        family = BEHAVIOR_FAMILIES[family_name]
        ego_speed = random.uniform(*family["ego_speed"])
        speed_delta = random.uniform(*family["npc_speed_delta"])
        params = {
            "family": family_name,
            "ego_speed": round(ego_speed, 2),
            "npc_speed": round(
                ego_speed + speed_delta,
                2,
            ),
            "initial_gap": round(
                random.uniform(*family["initial_gap"]),
                2,
            ),
            "merge_start_time": round(
                random.uniform(*family["merge_start_time"]),
                2,
            ),
            "merge_duration": round(
                random.uniform(*family["merge_duration"]),
                2,
            ),
            "lateral_aggression": round(
                random.uniform(*family["lateral_aggression"]),
                2,
            ),
            "abort": family.get("abort", False),
            "drift_only": family.get("drift_only", False),
            "ego_yields": family.get("ego_yields", False),
            "traffic_density": family.get(
                "traffic_density",
                "low",
            ),
            "oscillation": family.get(
                "oscillation",
                False,
            ),
        }

        return params