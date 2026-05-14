import os

from scenariogeneration import xosc


# =========================================================
# ROAD + CATALOG CONFIG
# =========================================================

ROAD_PATH = (
    "scenarios/base/highway_3lane.xodr"
)

VEHICLE_CATALOG_PATH = (
    "/home/nickname8888/esmini/resources/"
    "xosc/Catalogs/Vehicles"
)


# =========================================================
# BUILD POLYLINE
# =========================================================

def build_polyline_from_points(
    trajectory_points,
):

    times = []

    positions = []

    for point in trajectory_points:

        times.append(
            point.t
        )

        positions.append(

            xosc.WorldPosition(
                x=point.x,
                y=point.y,
                z=0,
                h=0,
                p=0,
                r=0,
            )
        )

    polyline = xosc.Polyline(
        times,
        positions,
    )

    return polyline


# =========================================================
# CREATE FOLLOW TRAJECTORY ACTION
# =========================================================

def create_follow_trajectory_action(
    trajectory,
):

    polyline = build_polyline_from_points(
        trajectory.points
    )

    trajectory_shape = xosc.Trajectory(
        f"{trajectory.name}_trajectory",
        closed=False,
    )

    trajectory_shape.add_shape(
        polyline
    )

    follow_action = xosc.FollowTrajectoryAction(
        trajectory_shape,
        xosc.FollowingMode.position,
        xosc.ReferenceContext.absolute,
        1.0,
        0,
    )

    return follow_action


# =========================================================
# INIT ACTIONS
# =========================================================

def create_init_actions(
    init,
    trajectory,
):

    first_point = trajectory.points[0]

    # -----------------------------------------------------
    # TELEPORT
    # -----------------------------------------------------

    init.add_init_action(
        trajectory.name,
        xosc.TeleportAction(

            xosc.WorldPosition(
                x=first_point.x,
                y=first_point.y,
                z=0,
                h=0,
                p=0,
                r=0,
            )
        ),
    )

    # -----------------------------------------------------
    # INITIAL SPEED
    # -----------------------------------------------------

    init.add_init_action(
        trajectory.name,
        xosc.AbsoluteSpeedAction(
            first_point.speed,

            xosc.TransitionDynamics(
                xosc.DynamicsShapes.step,
                xosc.DynamicsDimension.time,
                0,
            ),
        ),
    )


# =========================================================
# ENTITIES
# =========================================================

def create_entities():

    entities = xosc.Entities()

    # -----------------------------------------------------
    # EGO
    # -----------------------------------------------------

    entities.add_scenario_object(
        "Ego",

        xosc.CatalogReference(
            "VehicleCatalog",
            "car_white",
        ),
    )

    # -----------------------------------------------------
    # TARGET
    # -----------------------------------------------------

    entities.add_scenario_object(
        "Target",

        xosc.CatalogReference(
            "VehicleCatalog",
            "car_red",
        ),
    )

    return entities


# =========================================================
# VEHICLE MANEUVER
# =========================================================

def create_vehicle_maneuver(
    trajectory,
):

    # -----------------------------------------------------
    # EVENT
    # -----------------------------------------------------

    event = xosc.Event(
        f"{trajectory.name}_event",
        xosc.Priority.override,
    )

    # -----------------------------------------------------
    # FOLLOW ACTION
    # -----------------------------------------------------

    follow_action = (
        create_follow_trajectory_action(
            trajectory
        )
    )

    event.add_action(
        f"{trajectory.name}_follow_action",
        follow_action,
    )

    # -----------------------------------------------------
    # TRIGGER
    # -----------------------------------------------------

    event.add_trigger(

        xosc.ValueTrigger(
            f"{trajectory.name}_start_trigger",

            0,

            xosc.ConditionEdge.rising,

            xosc.SimulationTimeCondition(
                0,
                xosc.Rule.greaterThan,
            ),
        )
    )

    # -----------------------------------------------------
    # MANEUVER
    # -----------------------------------------------------

    maneuver = xosc.Maneuver(
        f"{trajectory.name}_maneuver"
    )

    maneuver.add_event(
        event
    )

    return maneuver


# =========================================================
# EXPORT XOSC
# =========================================================

def export_scenario_to_xosc(
    scenario_trajectory,
    scenario_id,
    output_dir,
):

    os.makedirs(
        output_dir,
        exist_ok=True,
    )

    # -----------------------------------------------------
    # ROAD NETWORK
    # -----------------------------------------------------

    road = xosc.RoadNetwork(
        ROAD_PATH
    )

    # -----------------------------------------------------
    # CATALOG
    # -----------------------------------------------------

    catalog = xosc.Catalog()

    catalog.add_catalog(
        "VehicleCatalog",
        VEHICLE_CATALOG_PATH,
    )

    # -----------------------------------------------------
    # ENTITIES
    # -----------------------------------------------------

    entities = create_entities()

    # -----------------------------------------------------
    # INIT
    # -----------------------------------------------------

    init = xosc.Init()

    create_init_actions(
        init,
        scenario_trajectory.ego,
    )

    create_init_actions(
        init,
        scenario_trajectory.target,
    )

    # -----------------------------------------------------
    # STORYBOARD
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # EGO MANEUVER
    # -----------------------------------------------------

    ego_maneuver = (
        create_vehicle_maneuver(
            scenario_trajectory.ego
        )
    )

    storyboard.add_maneuver(
        ego_maneuver,
        "Ego",
    )

    # -----------------------------------------------------
    # TARGET MANEUVER
    # -----------------------------------------------------

    target_maneuver = (
        create_vehicle_maneuver(
            scenario_trajectory.target
        )
    )

    storyboard.add_maneuver(
        target_maneuver,
        "Target",
    )

    # -----------------------------------------------------
    # SCENARIO
    # -----------------------------------------------------

    scenario = xosc.Scenario(

        scenario_id,

        "ADAS-Risk-Prediction",

        xosc.ParameterDeclarations(),

        entities,

        storyboard,

        road,

        catalog,
    )

    # -----------------------------------------------------
    # OUTPUT
    # -----------------------------------------------------

    output_path = os.path.join(
        output_dir,
        f"{scenario_id}.xosc",
    )

    scenario.write_xml(
        output_path
    )

    print(
        f"\nExported OpenSCENARIO:\n"
        f"{output_path}\n"
    )

    return output_path