import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.osm_client import (
    get_road_graph,
    get_graph_summary,
    get_nearest_node,
    get_node_coordinates,
    get_candidate_nodes_by_distance,
)


def main():
    lat = 35.8721
    lon = 140.0106
    dist_m = 1000

    print("OSMnx road graph check")
    print(f"center: lat={lat}, lon={lon}")
    print(f"dist_m: {dist_m}")

    graph = get_road_graph(
        lat=lat,
        lon=lon,
        dist_m=dist_m,
    )

    summary = get_graph_summary(graph)

    print("Graph summary:")
    print(f"nodes: {summary['nodes']}")
    print(f"edges: {summary['edges']}")

    nearest_node_id = get_nearest_node(
        graph=graph,
        lat=lat,
        lon=lon,
    )

    nearest_node = get_node_coordinates(
        graph=graph,
        node_id=nearest_node_id,
    )

    print("Nearest node:")
    print(f"node_id: {nearest_node['node_id']}")
    print(f"lat: {nearest_node['lat']}")
    print(f"lon: {nearest_node['lon']}")

    target_loop_distance_km = 2.0
    target_oneway_distance_m = target_loop_distance_km * 1000 / 2

    candidate_nodes = get_candidate_nodes_by_distance(
        graph=graph,
        start_node=nearest_node_id,
        target_distance_m=target_oneway_distance_m,
        tolerance_m=200,
        max_candidates=10,
    )

    print("Candidate nodes:")
    print(f"target_loop_distance_km: {target_loop_distance_km}")
    print(f"target_oneway_distance_m: {target_oneway_distance_m}")

    for candidate in candidate_nodes:
        print(
            f"node_id: {candidate['node_id']} / "
            f"lat: {candidate['lat']} / "
            f"lon: {candidate['lon']} / "
            f"distance_m: {candidate['distance_m']} / "
            f"error_m: {candidate['distance_error_m']}"
        )


if __name__ == "__main__":
    main()