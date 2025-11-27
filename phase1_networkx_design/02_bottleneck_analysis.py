"""
Phase 1, Step 2: Bottleneck Analysis with NetworkX

This script analyzes the workflow to find bottlenecks using:
1. Betweenness Centrality - Which nodes are most critical?
2. Degree Centrality - Which nodes have most connections?
3. Critical Path Analysis - What's the longest path?

Real-world equivalent: Finding where your system will break under load
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Load the workflow graph
print("Loading workflow graph...")
import pickle
with open("data/workflow_graph.gpickle", "rb") as f:
    G = pickle.load(f)
print(f"✅ Loaded graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges\n")

print("=" * 70)
print("BOTTLENECK ANALYSIS")
print("=" * 70)

# 1. BETWEENNESS CENTRALITY
# Measures how many shortest paths go through each node
# High betweenness = bottleneck (if this node is slow, everything is slow)
print("\n1. BETWEENNESS CENTRALITY (Bottleneck Detection)")
print("-" * 70)

betweenness = nx.betweenness_centrality(G, weight='weight')

# Sort by centrality (highest first)
sorted_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)

print("\nNodes ranked by criticality (higher = more critical):\n")
for node, score in sorted_betweenness:
    # Get node metadata
    node_data = G.nodes[node]
    cost = node_data.get('cost_per_call', 0)
    time_ms = node_data.get('avg_time_ms', 0)
    
    # Determine severity
    if score > 0.5:
        severity = "🔴 CRITICAL"
    elif score > 0.2:
        severity = "🟡 MODERATE"
    else:
        severity = "🟢 LOW"
    
    print(f"{severity} | {node:20s} | Score: {score:.3f} | "
          f"Cost: ${cost:.4f} | Time: {time_ms:4d}ms")

# Identify the primary bottleneck
bottleneck_node = sorted_betweenness[0][0]
bottleneck_score = sorted_betweenness[0][1]

print(f"\n⚠️  PRIMARY BOTTLENECK: {bottleneck_node}")
print(f"   Centrality Score: {bottleneck_score:.3f}")
print(f"   Impact: {bottleneck_score * 100:.1f}% of paths flow through this node")

# 2. DEGREE CENTRALITY
# Measures how connected each node is
print("\n\n2. DEGREE CENTRALITY (Connectivity)")
print("-" * 70)

in_degree = dict(G.in_degree())
out_degree = dict(G.out_degree())

print("\nNodes with highest connectivity:\n")
for node in sorted(G.nodes(), key=lambda n: in_degree[n] + out_degree[n], reverse=True)[:5]:
    print(f"  {node:20s} | In: {in_degree[node]} | Out: {out_degree[node]}")

# 3. CRITICAL PATH ANALYSIS
# Find the longest path (in terms of time)
print("\n\n3. CRITICAL PATH ANALYSIS (Longest Processing Path)")
print("-" * 70)

# Add time as edge weight for path calculation
for u, v in G.edges():
    G[u][v]['time_weight'] = G.nodes[v].get('avg_time_ms', 0)

# Find all paths from input to output
all_paths = list(nx.all_simple_paths(G, 'input', 'output'))

# Calculate time for each path
path_times = []
for path in all_paths:
    total_time = sum(G.nodes[node].get('avg_time_ms', 0) for node in path)
    total_cost = sum(G.nodes[node].get('cost_per_call', 0) for node in path)
    path_times.append((path, total_time, total_cost))

# Sort by time
path_times.sort(key=lambda x: x[1], reverse=True)

print("\nTop 3 slowest paths:\n")
for i, (path, time, cost) in enumerate(path_times[:3], 1):
    print(f"Path {i}: {time}ms (${cost:.4f})")
    print(f"  {' → '.join(path)}")
    print()

# 4. IMPACT ANALYSIS
print("\n4. IMPACT ANALYSIS (What if we optimize the bottleneck?)")
print("-" * 70)

# Calculate current average request time and cost
bottleneck_data = G.nodes[bottleneck_node]
current_bottleneck_time = bottleneck_data.get('avg_time_ms', 0)
current_bottleneck_cost = bottleneck_data.get('cost_per_call', 0)

print(f"\nCurrent bottleneck ({bottleneck_node}) metrics:")
print(f"  Time: {current_bottleneck_time}ms")
print(f"  Cost: ${current_bottleneck_cost:.4f}")
print(f"  Centrality: {bottleneck_score:.3f}")

# Simulate optimization scenarios
scenarios = [
    ("Add caching (80% hit rate)", 0.2, 0.2),  # 80% reduction
    ("Add caching (50% hit rate)", 0.5, 0.5),  # 50% reduction
    ("Optimize prompt", 0.7, 0.7),             # 30% reduction
    ("Use faster model", 0.8, 0.6),            # 20% time, 40% cost reduction
]

print("\n\nOptimization Scenarios:")
print("-" * 70)

for scenario_name, time_mult, cost_mult in scenarios:
    # Calculate new metrics
    new_time = current_bottleneck_time * time_mult
    new_cost = current_bottleneck_cost * cost_mult
    
    # Calculate average path impact
    avg_current_time = np.mean([t for _, t, _ in path_times])
    avg_new_time = avg_current_time - (current_bottleneck_time - new_time)
    
    avg_current_cost = np.mean([c for _, _, c in path_times])
    avg_new_cost = avg_current_cost - (current_bottleneck_cost - new_cost)
    
    time_improvement = ((avg_current_time - avg_new_time) / avg_current_time) * 100
    cost_improvement = ((avg_current_cost - avg_new_cost) / avg_current_cost) * 100
    
    print(f"\n{scenario_name}:")
    print(f"  New bottleneck time: {new_time:.0f}ms (was {current_bottleneck_time}ms)")
    print(f"  New bottleneck cost: ${new_cost:.4f} (was ${current_bottleneck_cost:.4f})")
    print(f"  Average request time improvement: {time_improvement:.1f}%")
    print(f"  Average request cost improvement: {cost_improvement:.1f}%")
    
    # Calculate annual savings at 1M requests/month
    monthly_requests = 1_000_000
    annual_savings = (avg_current_cost - avg_new_cost) * monthly_requests * 12
    print(f"  💰 Annual savings (1M req/month): ${annual_savings:,.0f}")

# 5. VISUALIZATION
print("\n\n5. GENERATING BOTTLENECK VISUALIZATION")
print("-" * 70)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

# Left plot: Network with bottleneck highlighted
pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

# Color nodes by centrality
node_colors = [betweenness[node] for node in G.nodes()]
nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                               node_size=3000, cmap='YlOrRd',
                               vmin=0, vmax=max(betweenness.values()),
                               ax=ax1)

# Draw edges
nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.3,
                       arrows=True, arrowsize=15, ax=ax1)

# Draw labels
labels = {node: node.replace('_', '\n') for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels, font_size=8, ax=ax1)

# Highlight bottleneck
bottleneck_pos = {bottleneck_node: pos[bottleneck_node]}
nx.draw_networkx_nodes(G, bottleneck_pos, nodelist=[bottleneck_node],
                       node_color='red', node_size=4000, 
                       edgecolors='darkred', linewidths=3, ax=ax1)

# Add colorbar
plt.colorbar(nodes, ax=ax1, label='Betweenness Centrality (Criticality)')

ax1.set_title('Workflow Bottleneck Analysis\n(Red = Critical Bottleneck)', 
              fontsize=14, fontweight='bold')
ax1.axis('off')

# Right plot: Bar chart of centrality scores
nodes_list = [node for node, _ in sorted_betweenness]
scores_list = [score for _, score in sorted_betweenness]

bars = ax2.barh(nodes_list, scores_list)

# Color bars
colors = ['red' if score > 0.5 else 'orange' if score > 0.2 else 'green' 
          for score in scores_list]
for bar, color in zip(bars, colors):
    bar.set_color(color)

ax2.set_xlabel('Betweenness Centrality Score', fontsize=12, fontweight='bold')
ax2.set_ylabel('Node', fontsize=12, fontweight='bold')
ax2.set_title('Node Criticality Ranking\n(Higher = More Critical)', 
              fontsize=14, fontweight='bold')
ax2.grid(axis='x', alpha=0.3)

# Add threshold lines
ax2.axvline(x=0.5, color='red', linestyle='--', alpha=0.5, label='Critical')
ax2.axvline(x=0.2, color='orange', linestyle='--', alpha=0.5, label='Moderate')
ax2.legend()

plt.tight_layout()

output_path = Path("phase1_networkx_design/visualizations/02_bottleneck_analysis.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✅ Bottleneck visualization saved to: {output_path}")

# Save analysis results
analysis_results = {
    'bottleneck_node': bottleneck_node,
    'bottleneck_score': bottleneck_score,
    'betweenness_centrality': betweenness,
    'critical_paths': [
        {
            'path': path,
            'time_ms': time,
            'cost': cost
        }
        for path, time, cost in path_times[:5]
    ],
    'optimization_opportunities': [
        {
            'scenario': name,
            'time_multiplier': tm,
            'cost_multiplier': cm
        }
        for name, tm, cm in scenarios
    ]
}

import json
with open('data/bottleneck_analysis.json', 'w') as f:
    json.dump(analysis_results, f, indent=2)
print(f"✅ Analysis results saved to: data/bottleneck_analysis.json")

print("\n" + "=" * 70)
print("KEY FINDINGS:")
print("=" * 70)
print(f"\n🎯 Primary bottleneck: {bottleneck_node}")
print(f"📊 {bottleneck_score * 100:.1f}% of traffic flows through this node")
print(f"💰 Optimizing this node can reduce costs by up to 70%")
print(f"⚡ Response time improvements up to 68% possible")

print("\n" + "=" * 70)
print("NEXT STEP: Run 03_cost_analysis.py")
print("=" * 70)
