"""
Diagnostic utilities for debugging pathfinding failures
"""

import networkx as nx
from networkx import MultiDiGraph


def check_connectivity(graph: MultiDiGraph, start: int, goal: int):
    """
    Check if there's ANY path between start and goal.
    Returns: (is_connected, info_dict)
    """
    result = {
        "start_exists": start in graph.nodes,
        "goal_exists": goal in graph.nodes,
        "is_connected": False,
        "is_strongly_connected": False,
        "same_component": False,
        "path_exists": False,
        "components_count": 0,
        "start_component": None,
        "goal_component": None,
    }

    if not result["start_exists"] or not result["goal_exists"]:
        return False, result

    # Check if graph is strongly connected (all nodes can reach all others)
    result["is_strongly_connected"] = nx.is_strongly_connected(graph)

    # Find weakly connected components
    weak_components = list(nx.weakly_connected_components(graph))
    result["components_count"] = len(weak_components)

    # Find which component each node belongs to
    for i, component in enumerate(weak_components):
        if start in component:
            result["start_component"] = i
        if goal in component:
            result["goal_component"] = i

    result["same_component"] = (result["start_component"] == result["goal_component"])

    # Check if path exists (considering direction)
    try:
        result["path_exists"] = nx.has_path(graph, start, goal)
        result["is_connected"] = result["path_exists"]
    except:
        result["path_exists"] = False
        result["is_connected"] = False

    return result["is_connected"], result


def get_graph_stats(graph: MultiDiGraph):
    """Get overall graph statistics."""
    stats = {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "is_directed": graph.is_directed(),
        "is_strongly_connected": nx.is_strongly_connected(graph),
        "weak_components": nx.number_weakly_connected_components(graph),
        "strong_components": nx.number_strongly_connected_components(graph),
    }

    # Get largest component
    if stats["weak_components"] > 1:
        largest = max(nx.weakly_connected_components(graph), key=len)
        stats["largest_component_size"] = len(largest)
        stats["largest_component_pct"] = (len(largest) / stats["nodes"]) * 100
    else:
        stats["largest_component_size"] = stats["nodes"]
        stats["largest_component_pct"] = 100.0

    return stats


def find_valid_endpoints(graph: MultiDiGraph, max_attempts=100):
    """
    Find two random nodes that are definitely connected.
    Returns: (start, goal, attempts_made)
    """
    import random

    # Get largest strongly connected component
    strong_components = list(nx.strongly_connected_components(graph))
    if not strong_components:
        return None, None, 0

    # Use largest component
    largest_component = max(strong_components, key=len)
    component_nodes = list(largest_component)

    if len(component_nodes) < 2:
        return None, None, 0

    # Pick two random nodes from the same component
    for attempt in range(max_attempts):
        start, goal = random.sample(component_nodes, 2)

        # Verify path exists
        if nx.has_path(graph, start, goal):
            return start, goal, attempt + 1

    return None, None, max_attempts


def suggest_fixes(diagnostic_result):
    """Suggest fixes based on diagnostic results."""
    suggestions = []

    if not diagnostic_result["start_exists"]:
        suggestions.append("❌ Start node doesn't exist in graph!")

    if not diagnostic_result["goal_exists"]:
        suggestions.append("❌ Goal node doesn't exist in graph!")

    if not diagnostic_result["same_component"]:
        suggestions.append(
            f"⚠️ Start and goal are in different network components "
            f"(Component {diagnostic_result['start_component']} → "
            f"Component {diagnostic_result['goal_component']})"
        )
        suggestions.append("💡 Try: Use 'Smart Random' button to pick connected points")

    if diagnostic_result["same_component"] and not diagnostic_result["path_exists"]:
        suggestions.append(
            "⚠️ Nodes are in same component but no directed path exists "
            "(likely due to one-way streets)"
        )
        suggestions.append("💡 Try: Convert to undirected graph or pick different points")

    if diagnostic_result["components_count"] > 10:
        suggestions.append(
            f"⚠️ Graph has {diagnostic_result['components_count']} separate components!"
        )
        suggestions.append("💡 Consider loading a more connected area or larger region")

    return suggestions


def format_diagnostic_report(stats, diagnostic=None):
    """Format diagnostic information for display."""
    report = []
    report.append("📊 GRAPH STATISTICS")
    report.append("=" * 50)
    report.append(f"Nodes: {stats['nodes']:,}")
    report.append(f"Edges: {stats['edges']:,}")
    report.append(f"Type: {'Directed' if stats['is_directed'] else 'Undirected'}")
    report.append(f"Weak Components: {stats['weak_components']}")
    report.append(f"Strong Components: {stats['strong_components']}")
    report.append(
        f"Largest Component: {stats['largest_component_size']:,} nodes "
        f"({stats['largest_component_pct']:.1f}%)"
    )
    report.append(f"Fully Connected: {'Yes' if stats['is_strongly_connected'] else 'No'}")

    if diagnostic:
        report.append("\n🔍 PATH ANALYSIS")
        report.append("=" * 50)
        report.append(f"Start Node Valid: {'✅' if diagnostic['start_exists'] else '❌'}")
        report.append(f"Goal Node Valid: {'✅' if diagnostic['goal_exists'] else '❌'}")
        report.append(f"Same Component: {'✅' if diagnostic['same_component'] else '❌'}")
        report.append(f"Path Exists: {'✅' if diagnostic['path_exists'] else '❌'}")

        if diagnostic['start_component'] is not None:
            report.append(f"Start Component ID: {diagnostic['start_component']}")
        if diagnostic['goal_component'] is not None:
            report.append(f"Goal Component ID: {diagnostic['goal_component']}")

        # Add suggestions
        suggestions = suggest_fixes(diagnostic)
        if suggestions:
            report.append("\n💡 SUGGESTIONS")
            report.append("=" * 50)
            for suggestion in suggestions:
                report.append(suggestion)

    return "\n".join(report)
