BEHAVIOR_FAMILIES = {
    "safe_merge": {
        "ego_speed": (20, 30),
        "npc_speed_delta": (-2, 4),
        "initial_gap": (15, 30),
        "merge_start_time": (3, 7),
        "merge_duration": (3, 5),
        "lateral_aggression": (0.1, 0.3),
    },

    "aggressive_cutin": {
        "ego_speed": (20, 35),
        "npc_speed_delta": (5, 15),
        "initial_gap": (4, 10),
        "merge_start_time": (2, 5),
        "merge_duration": (0.8, 2.0),
        "lateral_aggression": (0.8, 1.0),
    },

    "hesitant_merge": {
        "ego_speed": (20, 30),
        "npc_speed_delta": (-1, 5),
        "initial_gap": (10, 20),
        "merge_start_time": (3, 8),
        "merge_duration": (4, 7),
        "lateral_aggression": (0.2, 0.5),
    },

    "aborted_merge": {
        "ego_speed": (20, 30),
        "npc_speed_delta": (-2, 4),
        "initial_gap": (8, 18),
        "merge_start_time": (2, 6),
        "merge_duration": (2, 4),
        "abort": True,
        "lateral_aggression": (0.3, 0.6),
    },

    "fake_drift": {
        "ego_speed": (20, 30),
        "npc_speed_delta": (-2, 3),
        "initial_gap": (10, 25),
        "merge_start_time": (2, 6),
        "merge_duration": (4, 6),
        "drift_only": True,
        "lateral_aggression": (0.1, 0.3),
    },

    "late_commit": {
        "ego_speed": (20, 35),
        "npc_speed_delta": (3, 12),
        "initial_gap": (6, 15),
        "merge_start_time": (6, 10),
        "merge_duration": (0.8, 1.5),
        "lateral_aggression": (0.8, 1.0),
    },

    "cooperative_yield": {
        "ego_speed": (20, 30),
        "npc_speed_delta": (-2, 5),
        "initial_gap": (8, 15),
        "merge_start_time": (3, 6),
        "merge_duration": (2, 4),
        "ego_yields": True,
        "lateral_aggression": (0.3, 0.5),
    },

    "dense_pressure": {
        "ego_speed": (15, 30),
        "npc_speed_delta": (0, 10),
        "initial_gap": (5, 12),
        "merge_start_time": (2, 6),
        "merge_duration": (1.5, 3.5),
        "traffic_density": "high",
        "lateral_aggression": (0.5, 0.9),
    },

    "oscillatory_indecision": {
        "ego_speed": (20, 30),
        "npc_speed_delta": (-1, 5),
        "initial_gap": (10, 20),
        "merge_start_time": (3, 8),
        "merge_duration": (5, 8),
        "oscillation": True,
        "lateral_aggression": (0.2, 0.4),
    },
}