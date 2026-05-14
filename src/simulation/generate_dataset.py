from src.config.load_config import load_config

from src.simulation.behavior_families import BEHAVIOR_FAMILIES
from src.simulation.context_generator import ContextGenerator
from src.simulation.parameter_sampler import ParameterSampler
from src.simulation.scenario_builder import HighwayScenario
from src.simulation.utils import ensure_dir, save_metadata

config = load_config()

XOSC_DIR = config["output"]["xosc_dir"]
META_DIR = config["output"]["metadata_dir"]
SCENARIOS_PER_FAMILY = config["dataset"]["scenarios_per_family"]

ensure_dir(XOSC_DIR)
ensure_dir(META_DIR)

sampler = ParameterSampler()
context_generator = ContextGenerator()

def generate_shared_road():
    print("\nGenerating shared highway road...\n")
    road_builder = HighwayScenario(
    config=config,
    params={},
    context_vehicles=[],
    output_name="shared_road",
    )
    road_builder.write_shared_road()
    print("Shared road generated.\n")


def main():
    generate_shared_road()
    print("Generating validation dataset...\n")

    for family_name in BEHAVIOR_FAMILIES.keys():
        print(f"\nGenerating family: {family_name}")
        for i in range(SCENARIOS_PER_FAMILY):
            scenario_id = f"{family_name}_{i:04d}"
            params = sampler.sample(family_name)
            context = context_generator.generate(
                traffic_density=params["traffic_density"]
            )
            scenario = HighwayScenario(
                config=config,
                params=params,
                context_vehicles=context,
                output_name=scenario_id,
            )
            osc = scenario.build()
            xosc_path = f"{XOSC_DIR}/{scenario_id}.xosc"
            osc.write_xml(xosc_path)

            metadata = {
                "scenario_id": scenario_id,
                **params,
                "num_context_vehicles": len(context),
            }
            save_metadata(
                f"{META_DIR}/{scenario_id}.json",
                metadata,
            )
            print(f"Generated: {scenario_id}")
    print("\nDataset generation complete.\n")

if __name__ == "__main__":
    main()