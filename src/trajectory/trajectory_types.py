from dataclasses import dataclass
from typing import List


@dataclass
class TrajectoryPoint:
    t: float
    x: float
    y: float
    speed: float


@dataclass
class VehicleTrajectory:
    name: str
    points: List[TrajectoryPoint]


@dataclass
class ScenarioTrajectory:
    family: str
    ego: VehicleTrajectory
    target: VehicleTrajectory