"""
Phase 1, Step 3: Cost Analysis with NetworkX

This script performs detailed cost analysis:
1. Calculate cost per request
2. Project monthly/annual costs
3. Identify cost optimization opportunities
4. Simulate different traffic patterns

Real-world equivalent: Understanding your AWS bill BEFORE deploying
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import json
from pathlib import Path

# Load graph and previous analysis
print("Loading data...")
import pickle
with open("data/workflow_graph.gpickle", "rb") as f:
    G = pickle.load(f)

with open('data/bottleneck_analysis.json', 'r') as f:
    bottleneck_data = json.load(f)

print("✅ Data loaded\n")

print("=" * 70)
print("COST ANALYSIS")
print("=" * 70)

# 1. BASELINE COST CALCULATION
print("\n1. BASELINE COST PER REQUEST")
print("-" * 70)

# Calculate average cost across all paths
all_paths = list(nx.all_simple_paths(G, 'input', 'output'))
path_costs = []

for path in all_paths:
    path_cost = sum(G.nodes[node].get('cost_per_call', 0) for node in path)
    path_costs.append(path_cost)

avg_cost_per_request = np.mean(path_costs)
min_cost = min(path_costs)
max_cost = max(path_costs)

print(f"\nAverage cost per request: ${avg_cost_per_request:.4f}")
print(f"Minimum cost per request: ${min_cost:.4f}")
print(f"Maximum cost per request: ${max_cost:.4f}")
print(f"Cost variance: ${max_cost - min_cost:.4f}")

# 2. SCALE PROJECTIONS
print("\n\n2. COST PROJECTIONS AT SCALE")
print("-" * 70)

scale_scenarios = [
    ("Small (10K req/month)", 10_000),
    ("Medium (100K req/month)", 100_000),
    ("Large (1M req/month)", 1_000_000),
    ("Enterprise (10M req/month)", 10_000_000),
]

print("\n{:30s} {:>15s} {:>15s}".format("Scale", "Monthly Cost", "Annual Cost"))
print("-" * 70)

for scenario_name, monthly_requests in scale_scenarios:
    monthly_cost = monthly_requests * avg_cost_per_request
    annual_cost = monthly_cost * 12
    
    print(f"{scenario_name:30s} ${monthly_cost:>14,.2f} ${annual_cost:>14,.2f}")

# 3. NODE-BY-NODE COST BREAKDOWN
print("\n\n3. COST BREAKDOWN BY NODE")
print("-" * 70)

# Calculate how often each node is visited (weighted by paths)
node_costs = []
for node in G.nodes():
    node_cost = G.nodes[node].get('cost_per_call', 0)
    
    # Count paths through this node
    paths_through_node = sum(1 for path in all_paths if node in path)
    pct_paths = (paths_through_node / len(all_paths)) * 100
    
    # Contribution to total cost
    cost_contribution = node_cost * (paths_through_node / len(all_paths))
    pct_total_cost = (cost_contribution / avg_cost_per_request) * 100 if avg_cost_per_request > 0 else 0
    
    if node_cost > 0:  # Only show nodes with costs
        node_costs.append({
            'node': node,
            'cost': node_cost,
            'paths_pct': pct_paths,
            'contribution': cost_contribution,
            'pct_total': pct_total_cost
        })

# Sort by total cost contribution
node_costs.sort(key=lambda x: x['contribution'], reverse=True)

print("\n{:25s} {:>10s} {:>12s} {:>15s}".format(
    "Node", "Node Cost", "% of Paths", "% Total Cost"))
print("-" * 70)

for nc in node_costs:
    print(f"{nc['node']:25s} ${nc['cost']:>9.4f} {nc['paths_pct']:>11.1f}% {nc['pct_total']:>14.1f}%")

# 4. OPTIMIZATION OPPORTUNITIES
print("\n\n4. COST OPTIMIZATION OPPORTUNITIES")
print("-" * 70)

# Focus on the top 3 most expensive nodes
top_expensive = node_costs[:3]

print("\nTop 3 cost drivers:\n")
for i, nc in enumerate(top_expensive, 1):
    print(f"{i}. {nc['node']}")
    print(f"   Current cost: ${nc['cost']:.4f} per call")
    print(f"   Contributes {nc['pct_total']:.1f}% of total request cost")
    print()

# Simulation: What if we reduce cost of top node by 50%?
print("\nOptimization Simulation (Reduce top node cost by 50%):\n")

optimized_node = top_expensive[0]['node']
current_node_cost = G.nodes[optimized_node]['cost_per_call']
optimized_node_cost = current_node_cost * 0.5

print(f"Node: {optimized_node}")
print(f"Current cost: ${current_node_cost:.4f}")
print(f"Optimized cost: ${optimized_node_cost:.4f} (50% reduction)")

# Calculate new average cost
cost_reduction = current_node_cost - optimized_node_cost
new_avg_cost = avg_cost_per_request - (cost_reduction * (top_expensive[0]['paths_pct'] / 100))

cost_savings_pct = ((avg_cost_per_request - new_avg_cost) / avg_cost_per_request) * 100

print(f"\nOld average cost per request: ${avg_cost_per_request:.4f}")
print(f"New average cost per request: ${new_avg_cost:.4f}")
print(f"Cost reduction: {cost_savings_pct:.1f}%")

# Calculate savings at scale
print("\nProjected Annual Savings:")
print("-" * 40)
for scenario_name, monthly_requests in scale_scenarios:
    annual_requests = monthly_requests * 12
    annual_savings = (avg_cost_per_request - new_avg_cost) * annual_requests
    
    print(f"{scenario_name:30s} ${annual_savings:>14,.0f}")

# 5. CACHE STRATEGY ANALYSIS
print("\n\n5. CACHING STRATEGY IMPACT")
print("-" * 70)

# Simulate caching on the bottleneck
cache_hit_rates = [0.3, 0.5, 0.7, 0.9]

print("\n{:15s} {:>18s} {:>18s} {:>18s}".format(
    "Cache Hit Rate", "New Avg Cost", "Cost Reduction", "Annual Savings*"))
print("-" * 70)

for hit_rate in cache_hit_rates:
    # With caching, we skip the expensive node on cache hits
    cached_cost = new_avg_cost * (1 - hit_rate) + (new_avg_cost - current_node_cost) * hit_rate
    cost_reduction = avg_cost_per_request - cached_cost
    cost_reduction_pct = (cost_reduction / avg_cost_per_request) * 100
    
    # Calculate annual savings at 1M req/month
    annual_savings = cost_reduction * 1_000_000 * 12
    
    print(f"{hit_rate*100:>13.0f}% ${cached_cost:>17.4f} {cost_reduction_pct:>16.1f}% ${annual_savings:>17,.0f}")

print("\n* Based on 1M requests/month")

# 6. VISUALIZATION
print("\n\n6. GENERATING COST VISUALIZATIONS")
print("-" * 70)

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

# Plot 1: Cost breakdown pie chart
labels = [nc['node'] for nc in node_costs]
sizes = [nc['pct_total'] for nc in node_costs]
colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(labels)))

ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
ax1.set_title('Cost Distribution by Node\n(Larger = More Expensive)', 
              fontsize=12, fontweight='bold')

# Plot 2: Cost per request by scale
scales = [s[1] for s in scale_scenarios]
monthly_costs = [s * avg_cost_per_request for s in scales]
scale_labels = [s[0].split('(')[0].strip() for s in scale_scenarios]

ax2.bar(scale_labels, monthly_costs, color='steelblue')
ax2.set_ylabel('Monthly Cost ($)', fontsize=10, fontweight='bold')
ax2.set_title('Projected Monthly Costs\nAt Different Scales', 
              fontsize=12, fontweight='bold')
ax2.tick_params(axis='x', rotation=45)
ax2.grid(axis='y', alpha=0.3)

# Format y-axis as currency
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

# Plot 3: Optimization impact
optimization_scenarios = ['Current', '50% Top Node', '70% Top Node', '90% Top Node']
costs = [
    avg_cost_per_request,
    avg_cost_per_request * 0.7,  # ~50% reduction on top node
    avg_cost_per_request * 0.5,  # ~70% reduction
    avg_cost_per_request * 0.3   # ~90% reduction
]

bars = ax3.barh(optimization_scenarios, costs)
bars[0].set_color('red')
bars[1].set_color('orange')
bars[2].set_color('yellowgreen')
bars[3].set_color('green')

ax3.set_xlabel('Cost per Request ($)', fontsize=10, fontweight='bold')
ax3.set_title('Cost Reduction Scenarios\n(Green = Optimized)', 
              fontsize=12, fontweight='bold')
ax3.grid(axis='x', alpha=0.3)

# Plot 4: Cache hit rate impact
cache_rates = [f"{int(rate*100)}%" for rate in cache_hit_rates]
cached_costs = []
for hit_rate in cache_hit_rates:
    cached_cost = avg_cost_per_request * (1 - hit_rate * 0.7)  # Assume 70% cost reduction on hit
    cached_costs.append(cached_cost)

ax4.plot(cache_rates, cached_costs, marker='o', linewidth=3, markersize=10, color='purple')
ax4.axhline(y=avg_cost_per_request, color='red', linestyle='--', label='Current Cost', alpha=0.7)
ax4.set_xlabel('Cache Hit Rate', fontsize=10, fontweight='bold')
ax4.set_ylabel('Cost per Request ($)', fontsize=10, fontweight='bold')
ax4.set_title('Impact of Caching Strategy\n(Higher Hit Rate = Lower Cost)', 
              fontsize=12, fontweight='bold')
ax4.legend()
ax4.grid(alpha=0.3)

plt.tight_layout()

output_path = Path("phase1_networkx_design/visualizations/03_cost_analysis.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✅ Cost analysis visualization saved to: {output_path}")

# Save cost analysis results
cost_analysis = {
    'baseline': {
        'avg_cost_per_request': avg_cost_per_request,
        'min_cost': min_cost,
        'max_cost': max_cost
    },
    'scale_projections': {
        s[0]: {
            'monthly_requests': s[1],
            'monthly_cost': s[1] * avg_cost_per_request,
            'annual_cost': s[1] * avg_cost_per_request * 12
        }
        for s in scale_scenarios
    },
    'node_costs': node_costs,
    'optimization_target': {
        'node': optimized_node,
        'current_cost': current_node_cost,
        'potential_savings_pct': cost_savings_pct
    }
}

with open('data/cost_analysis.json', 'w') as f:
    json.dump(cost_analysis, f, indent=2)
print(f"✅ Cost analysis results saved to: data/cost_analysis.json")

print("\n" + "=" * 70)
print("KEY FINDINGS:")
print("=" * 70)
print(f"\n💰 Current cost per request: ${avg_cost_per_request:.4f}")
print(f"📊 Top cost driver: {optimized_node} ({top_expensive[0]['pct_total']:.1f}% of total)")
print(f"🎯 Optimization potential: {cost_savings_pct:.1f}% cost reduction")
print(f"💵 At 1M req/month: ${(avg_cost_per_request - new_avg_cost) * 1_000_000 * 12:,.0f} annual savings")

print("\n" + "=" * 70)
print("NEXT STEP: Run 04_optimization_simulation.py")
print("=" * 70)
