import random

class ContextGenerator:
    def generate(self, traffic_density="low"):
        vehicles = []
        if traffic_density == "low":
            return vehicles
        if traffic_density == "high":
            num_vehicles = random.randint(3, 6)
            for i in range(num_vehicles):
                vehicle = {
                    "name": f"traffic_{i}",
                    "lane": random.choice([
                        -1,
                        -2,
                        -3,
                    ]),
                    "s": round(
                        random.uniform(20, 120),
                        2,
                    ),
                    "speed": round(
                        random.uniform(18, 32),
                        2,
                    ),
                }
                vehicles.append(vehicle)
        return vehicles