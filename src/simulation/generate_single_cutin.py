from scenariogeneration import ScenarioGenerator, xodr, xosc


class CutInScenario(ScenarioGenerator):

    def __init__(self):
        super().__init__()
        self.naming = "numerical"

    # ---------------------------------------------------------
    # ROAD DEFINITION
    # ---------------------------------------------------------
    def road(self, **kwargs):

        road = xodr.create_road(
            xodr.Line(500),
            id=0,
            left_lanes=2,
            right_lanes=2,
        )

        odr = xodr.OpenDrive("highway_road")
        odr.add_road(road)

        odr.adjust_roads_and_lanes()

        return odr

    # ---------------------------------------------------------
    # SCENARIO DEFINITION
    # ---------------------------------------------------------
    def scenario(self, **kwargs):

        road = xosc.RoadNetwork(self.road_file)

        # -----------------------------------------------------
        # ENTITIES
        # -----------------------------------------------------
        entities = xosc.Entities()

        ego_name = "Ego"
        npc_name = "NPC"

        entities.add_scenario_object(
            ego_name,
            xosc.CatalogReference("VehicleCatalog", "car_white"),
        )

        entities.add_scenario_object(
            npc_name,
            xosc.CatalogReference("VehicleCatalog", "car_red"),
        )

        # -----------------------------------------------------
        # CATALOG
        # -----------------------------------------------------
        catalog = xosc.Catalog()

        catalog.add_catalog(
            "VehicleCatalog",
            "../esmini/resources/xosc/Catalogs/Vehicles",
        )

        # -----------------------------------------------------
        # INIT
        # -----------------------------------------------------
        init = xosc.Init()

        # Ego starts in right lane
        init.add_init_action(
            ego_name,
            xosc.TeleportAction(
                xosc.LanePosition(
                    50,
                    0,
                    -2,
                    0,
                )
            ),
        )

        # Ego speed
        init.add_init_action(
            ego_name,
            xosc.AbsoluteSpeedAction(
                kwargs["ego_speed"],
                xosc.TransitionDynamics(
                    xosc.DynamicsShapes.step,
                    xosc.DynamicsDimension.time,
                    1,
                ),
            ),
        )

        # NPC starts in adjacent lane
        init.add_init_action(
            npc_name,
            xosc.TeleportAction(
                xosc.LanePosition(
                    kwargs["npc_start_s"],
                    0,
                    -1,
                    0,
                )
            ),
        )

        # NPC speed
        init.add_init_action(
            npc_name,
            xosc.AbsoluteSpeedAction(
                kwargs["npc_speed"],
                xosc.TransitionDynamics(
                    xosc.DynamicsShapes.step,
                    xosc.DynamicsDimension.time,
                    1,
                ),
            ),
        )

        # -----------------------------------------------------
        # LANE CHANGE EVENT
        # -----------------------------------------------------
        event = xosc.Event(
            "cutin_event",
            xosc.Priority.overwrite,
        )

        event.add_action(
            "npc_lane_change",
            xosc.AbsoluteLaneChangeAction(
                -2,
                xosc.TransitionDynamics(
                    xosc.DynamicsShapes.sinusoidal,
                    xosc.DynamicsDimension.time,
                    kwargs["lane_change_duration"],
                ),
            ),
        )

        # Trigger lane change after X seconds
        event.add_trigger(
            xosc.ValueTrigger(
                "lane_change_trigger",
                0,
                xosc.ConditionEdge.none,
                xosc.SimulationTimeCondition(
                    kwargs["lane_change_start_time"],
                    xosc.Rule.greaterThan,
                ),
            )
        )

        # -----------------------------------------------------
        # MANEUVER
        # -----------------------------------------------------
        maneuver = xosc.Maneuver("cutin_maneuver")
        maneuver.add_event(event)

        # -----------------------------------------------------
        # STORYBOARD
        # -----------------------------------------------------
        storyboard = xosc.StoryBoard(
            init,
            stoptrigger=xosc.ValueTrigger(
                "stop_simulation",
                0,
                xosc.ConditionEdge.none,
                xosc.SimulationTimeCondition(
                    15,
                    xosc.Rule.greaterThan,
                ),
                "stop",
            ),
        )

        # IMPORTANT:
        # maneuver applies to NPC
        storyboard.add_maneuver(
            maneuver,
            npc_name,
        )

        # -----------------------------------------------------
        # FINAL SCENARIO
        # -----------------------------------------------------
        scenario = xosc.Scenario(
            "highway_cutin",
            "YourName",
            xosc.ParameterDeclarations(),
            entities,
            storyboard,
            road,
            catalog,
        )

        return scenario


# -------------------------------------------------------------
# MAIN
# -------------------------------------------------------------
if __name__ == "__main__":

    scenario = CutInScenario()

    parameters = {
        "ego_speed": [25],
        "npc_speed": [30],
        "npc_start_s": [70],
        "lane_change_start_time": [4],
        "lane_change_duration": [3],
    }

    scenario.generate(
        "scenarios/generated",
        parameters,
    )

    print("Scenario generation complete!")