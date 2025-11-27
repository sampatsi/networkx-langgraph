# 🎨 Streamlit UI for NetworkX + LangGraph Visualization

## Quick Start

### 1. Run Phase 1 Scripts (if not already done)

```bash
# Generate all analysis data
python phase1_networkx_design/01_workflow_design.py
python phase1_networkx_design/02_bottleneck_analysis.py
python phase1_networkx_design/03_cost_analysis.py
```

### 2. Launch the UI

```bash
streamlit run app.py
```

The UI will open in your browser at `http://localhost:8501`

## Features

### 📊 Overview Dashboard
- Key metrics at a glance
- Node type distribution
- Cost breakdown
- Workflow paths analysis

### 🕸️ Workflow Graph
- Interactive graph visualization
- Hover to see node details
- Color-coded by cost
- Edge width shows traffic probability

### 🔴 Bottleneck Analysis
- Node criticality ranking
- Betweenness centrality scores
- Critical path identification
- Optimization scenarios

### 💰 Cost Analysis
- Cost per request breakdown
- Scale projections (10K to 10M req/month)
- Node-by-node cost contribution
- Annual cost projections

### ⚡ Optimization
- Interactive optimization calculator
- Select any node to optimize
- Calculate potential savings
- Real-time ROI calculations

## Navigation

Use the sidebar to switch between different views:
- **Overview**: High-level dashboard
- **Workflow Graph**: Interactive graph visualization
- **Bottleneck Analysis**: Critical node identification
- **Cost Analysis**: Detailed cost breakdown
- **Optimization**: Calculate optimization impact

## Tips

1. **Hover over nodes** in the graph to see detailed information
2. **Use the optimization calculator** to simulate different scenarios
3. **Check scale projections** to understand costs at your volume
4. **Review bottleneck analysis** to identify optimization targets

## Troubleshooting

**UI shows "Data not found" errors:**
- Make sure you've run all Phase 1 scripts first
- Check that `data/` directory contains:
  - `workflow_graph.gpickle`
  - `bottleneck_analysis.json`
  - `cost_analysis.json`

**Graph not displaying:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check browser console for JavaScript errors

**Performance issues:**
- The UI caches data for faster loading
- If data changes, refresh the page or clear cache

