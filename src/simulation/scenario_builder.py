from scenariogeneration import ScenarioGenerator, xodr, xosc

class HighwayScenario(ScenarioGenerator):

    def __init__(
        self,
        params,
        context_vehicles,
        output_name,
    ):

        super().__init__()

        self.params = params
        self.context_vehicles = context_vehicles
        self.output_name = output_name
        self.naming = "numerical"

    def create_shared_road(self):
        road = xodr.create_road(
            [
                xodr.Line(2000),
            ],
            id=0,
            left_lanes=0,
            right_lanes=3,
        )
        odr = xodr.OpenDrive("highway_3lane")
        odr.add_road(road)
        odr.adjust_roads_and_lanes()
        return odr

    def write_shared_road(self):
        odr = self.create_shared_road()
        odr.write_xml(
            "scenarios/base/highway_3lane.xodr"
        )

    def scenario(self, **kwargs):

        road = xosc.RoadNetwork(
            "scenarios/base/highway_3lane.xodr"
        )
        entities = xosc.Entities()
        catalog = xosc.Catalog()
        catalog.add_catalog(
            "VehicleCatalog",
            "/home/nickname8888/esmini/resources/xosc/Catalogs/Vehicles",
        )

        ego_name = "Ego"
        npc_name = "Target"

        entities.add_scenario_object(
            ego_name,
            xosc.CatalogReference(
                "VehicleCatalog",
                "car_white",
            ),
        )

        entities.add_scenario_object(
            npc_name,
            xosc.CatalogReference(
                "VehicleCatalog",
                "car_red",
            ),
        )

        for vehicle in self.context_vehicles:
            entities.add_scenario_object(
                vehicle["name"],
                xosc.CatalogReference(
                    "VehicleCatalog",
                    "car_blue",
                ),
            )

        init = xosc.Init()

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

        init.add_init_action(
            ego_name,
            xosc.AbsoluteSpeedAction(
                self.params["ego_speed"],
                xosc.TransitionDynamics(
                    xosc.DynamicsShapes.step,
                    xosc.DynamicsDimension.time,
                    1,
                ),
            ),
        )

        npc_start_s = 50 + self.params["initial_gap"]

        init.add_init_action(
            npc_name,
            xosc.TeleportAction(
                xosc.LanePosition(
                    npc_start_s,
                    0,
                    -1,
                    0,
                )
            ),
        )

        init.add_init_action(
            npc_name,
            xosc.AbsoluteSpeedAction(
                self.params["npc_speed"],
                xosc.TransitionDynamics(
                    xosc.DynamicsShapes.step,
                    xosc.DynamicsDimension.time,
                    1,
                ),
            ),
        )

        for vehicle in self.context_vehicles:

            init.add_init_action(
                vehicle["name"],
                xosc.TeleportAction(
                    xosc.LanePosition(
                        vehicle["s"],
                        0,
                        vehicle["lane"],
                        0,
                    )
                ),
            )

            init.add_init_action(
                vehicle["name"],
                xosc.AbsoluteSpeedAction(
                    vehicle["speed"],
                    xosc.TransitionDynamics(
                        xosc.DynamicsShapes.step,
                        xosc.DynamicsDimension.time,
                        1,
                    ),
                ),
            )

        lane_change_target = -2

        if self.params["drift_only"]:
            lane_change_target = -1

        event = xosc.Event(
            "lane_change_event",
            xosc.Priority.overwrite,
        )

        event.add_action(
            "lane_change",
            xosc.AbsoluteLaneChangeAction(
                lane_change_target,
                xosc.TransitionDynamics(
                    xosc.DynamicsShapes.linear,
                    xosc.DynamicsDimension.time,
                    self.params["merge_duration"],
                ),
            ),
        )

        event.add_trigger(
            xosc.ValueTrigger(
                "merge_trigger",
                0,
                xosc.ConditionEdge.none,
                xosc.SimulationTimeCondition(
                    self.params["merge_start_time"],
                    xosc.Rule.greaterThan,
                ),
            )
        )

        maneuver = xosc.Maneuver(
            "merge_maneuver"
        )

        maneuver.add_event(event)
        storyboard = xosc.StoryBoard(
            init,
            stoptrigger=xosc.ValueTrigger(
                "stop_trigger",
                0,
                xosc.ConditionEdge.none,
                xosc.SimulationTimeCondition(
                    15,
                    xosc.Rule.greaterThan,
                ),
                "stop",
            ),
        )

        storyboard.add_maneuver(
            maneuver,
            npc_name,
        )

        scenario = xosc.Scenario(
            self.output_name,
            "L",
            xosc.ParameterDeclarations(),
            entities,
            storyboard,
            road,
            catalog,
        )
        return scenario

    def build(self):
        osc = self.scenario()
        return osc