"""
Phase 1, Step 1: Workflow Design with NetworkX

This script creates a customer support agent workflow graph.
It demonstrates how to:
1. Define agent workflow as a directed graph
2. Add nodes (agents/tasks) and edges (flow)
3. Attach metadata (cost, time, LLM model)
4. Visualize the workflow

Real-world equivalent: Mapping out your agent system on paper
"""

import networkx as nx
import matplotlib.pyplot as plt
import json
from pathlib import Path

# Create directed graph (workflow flows in one direction)
G = nx.DiGraph()

# Define nodes (each node is an agent or processing step)
nodes = [
    # Node format: (id, attributes)
    ("input", {
        "type": "entry",
        "description": "User query input",
        "cost_per_call": 0.0,
        "avg_time_ms": 5,
        "llm_model": None
    }),
    ("intent_classifier", {
        "type": "classifier",
        "description": "Classify user intent (billing, technical, account)",
        "cost_per_call": 0.002,  # GPT-4 mini
        "avg_time_ms": 800,
        "llm_model": "gpt-4-mini",
        "token_count": 150
    }),
    ("context_enricher", {
        "type": "enricher",
        "description": "Fetch user context from DB",
        "cost_per_call": 0.0,  # No LLM, just DB query
        "avg_time_ms": 200,
        "llm_model": None
    }),
    ("billing_agent", {
        "type": "specialist",
        "description": "Handle billing queries",
        "cost_per_call": 0.015,  # GPT-4
        "avg_time_ms": 1500,
        "llm_model": "gpt-4",
        "token_count": 1000
    }),
    ("technical_agent", {
        "type": "specialist",
        "description": "Handle technical support",
        "cost_per_call": 0.020,  # GPT-4 with more tokens
        "avg_time_ms": 2000,
        "llm_model": "gpt-4",
        "token_count": 1300
    }),
    ("account_agent", {
        "type": "specialist",
        "description": "Handle account management",
        "cost_per_call": 0.012,  # GPT-4
        "avg_time_ms": 1200,
        "llm_model": "gpt-4",
        "token_count": 800
    }),
    ("response_formatter", {
        "type": "formatter",
        "description": "Format final response",
        "cost_per_call": 0.001,
        "avg_time_ms": 100,
        "llm_model": "gpt-4-mini",
        "token_count": 50
    }),
    ("quality_check", {
        "type": "validator",
        "description": "Validate response quality",
        "cost_per_call": 0.003,
        "avg_time_ms": 500,
        "llm_model": "gpt-4-mini",
        "token_count": 200
    }),
    ("output", {
        "type": "exit",
        "description": "Final output to user",
        "cost_per_call": 0.0,
        "avg_time_ms": 5,
        "llm_model": None
    })
]

# Add nodes to graph
for node_id, attrs in nodes:
    G.add_node(node_id, **attrs)

# Define edges (workflow connections)
edges = [
    # Format: (from, to, weight)
    # Weight represents probability/frequency of this path
    ("input", "intent_classifier", {"weight": 1.0, "probability": 1.0}),
    ("intent_classifier", "context_enricher", {"weight": 1.0, "probability": 1.0}),
    
    # After context enrichment, route to appropriate agent
    # These probabilities represent real traffic distribution
    ("context_enricher", "billing_agent", {"weight": 0.4, "probability": 0.4}),
    ("context_enricher", "technical_agent", {"weight": 0.35, "probability": 0.35}),
    ("context_enricher", "account_agent", {"weight": 0.25, "probability": 0.25}),
    
    # All specialist agents go to quality check
    ("billing_agent", "quality_check", {"weight": 1.0, "probability": 1.0}),
    ("technical_agent", "quality_check", {"weight": 1.0, "probability": 1.0}),
    ("account_agent", "quality_check", {"weight": 1.0, "probability": 1.0}),
    
    # Quality check decision
    ("quality_check", "response_formatter", {"weight": 0.95, "probability": 0.95}),
    ("quality_check", "intent_classifier", {"weight": 0.05, "probability": 0.05}),  # Retry loop
    
    # Final output
    ("response_formatter", "output", {"weight": 1.0, "probability": 1.0})
]

# Add edges to graph
G.add_edges_from([(e[0], e[1], e[2]) for e in edges])

# Calculate total nodes and edges
print("=" * 60)
print("WORKFLOW DESIGN SUMMARY")
print("=" * 60)
print(f"\nTotal Nodes: {G.number_of_nodes()}")
print(f"Total Edges: {G.number_of_edges()}")
print(f"\nNode Types:")
node_types = {}
for node in G.nodes():
    node_type = G.nodes[node]['type']
    node_types[node_type] = node_types.get(node_type, 0) + 1

for node_type, count in node_types.items():
    print(f"  - {node_type}: {count}")

# Calculate theoretical maximum cost (if all paths taken)
max_cost = sum(G.nodes[node].get('cost_per_call', 0) for node in G.nodes())
print(f"\nTheoretical Maximum Cost per Request: ${max_cost:.4f}")

# Calculate average path cost (considering probabilities)
print("\nMost Common Paths:")
paths = [
    ["input", "intent_classifier", "context_enricher", "billing_agent", 
     "quality_check", "response_formatter", "output"],
    ["input", "intent_classifier", "context_enricher", "technical_agent", 
     "quality_check", "response_formatter", "output"],
    ["input", "intent_classifier", "context_enricher", "account_agent", 
     "quality_check", "response_formatter", "output"]
]

for i, path in enumerate(paths, 1):
    path_cost = sum(G.nodes[node].get('cost_per_call', 0) for node in path)
    path_time = sum(G.nodes[node].get('avg_time_ms', 0) for node in path)
    print(f"\n  Path {i}: {' → '.join(path)}")
    print(f"    Cost: ${path_cost:.4f}")
    print(f"    Time: {path_time}ms ({path_time/1000:.2f}s)")

# Visualize the workflow
plt.figure(figsize=(16, 10))

# Use hierarchical layout for better visualization
pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

# Color nodes by type
color_map = {
    'entry': '#4CAF50',
    'classifier': '#2196F3',
    'enricher': '#9C27B0',
    'specialist': '#FF9800',
    'formatter': '#00BCD4',
    'validator': '#F44336',
    'exit': '#4CAF50'
}

node_colors = [color_map[G.nodes[node]['type']] for node in G.nodes()]

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                       node_size=3000, alpha=0.9)

# Draw edges with varying thickness based on probability
edge_widths = [G[u][v]['weight'] * 3 for u, v in G.edges()]
nx.draw_networkx_edges(G, pos, width=edge_widths, 
                       edge_color='gray', alpha=0.6,
                       arrows=True, arrowsize=20, arrowstyle='->')

# Draw labels
labels = {node: node.replace('_', '\n') for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels, font_size=9, font_weight='bold')

# Add legend
legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                              markerfacecolor=color, label=node_type.title(), 
                              markersize=10)
                  for node_type, color in color_map.items()]
plt.legend(handles=legend_elements, loc='upper left', fontsize=10)

plt.title("Customer Support Agent Workflow\n(Node size represents processing, edge width represents traffic)", 
          fontsize=14, fontweight='bold')
plt.axis('off')
plt.tight_layout()

# Save visualization
output_path = Path("phase1_networkx_design/visualizations/01_workflow_design.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"\n✅ Workflow visualization saved to: {output_path}")

# Save graph data for next steps
graph_data = {
    'nodes': dict(G.nodes(data=True)),
    'edges': [(u, v, data) for u, v, data in G.edges(data=True)]
}

data_path = Path("data/workflow_graph.json")
with open(data_path, 'w') as f:
    json.dump(graph_data, f, indent=2)
print(f"✅ Workflow data saved to: {data_path}")

# Save NetworkX graph as pickle for easy loading
import pickle
with open("data/workflow_graph.gpickle", "wb") as f:
    pickle.dump(G, f)
print(f"✅ NetworkX graph saved to: data/workflow_graph.gpickle")

print("\n" + "=" * 60)
print("NEXT STEP: Run 02_bottleneck_analysis.py")
print("=" * 60)
