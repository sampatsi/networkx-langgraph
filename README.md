# NetworkX + LangGraph Demo Project

## 🎯 Project Overview

This is a **complete, working example** of the NetworkX + LangGraph framework for building optimized agent systems.

**Scenario:** Customer Support Agent System
- Handles customer queries
- Routes to appropriate handlers
- Tracks costs and performance
- Demonstrates optimization workflow

---

## 📁 Project Structure

```
networkx_langgraph_demo/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── phase1_networkx_design/
│   ├── 01_workflow_design.py          # Create workflow graph
│   ├── 02_bottleneck_analysis.py     # Find bottlenecks
│   ├── 03_cost_analysis.py           # Calculate costs
│   ├── 04_optimization_simulation.py # Simulate improvements
│   └── visualizations/                # Generated graphs
├── phase2_langgraph_implementation/
│   ├── 01_basic_agent.py             # Basic LangGraph agent
│   ├── 02_optimized_agent.py         # Optimized version
│   ├── 03_with_persistence.py        # Add checkpointing
│   └── 04_production_ready.py        # Full production version
├── phase3_monitoring/
│   ├── 01_metrics_collection.py      # Collect real metrics
│   ├── 02_export_to_networkx.py      # Feed back to NetworkX
│   └── 03_continuous_optimization.py # Re-analyze and improve
├── utils/
│   ├── cost_calculator.py            # Cost tracking utilities
│   ├── visualization.py              # Graph visualization
│   └── mock_llm.py                   # Mock LLM for testing
└── data/
    ├── sample_queries.json           # Test data
    └── metrics.json                  # Performance metrics
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Phase 1: NetworkX Design (5 minutes)

```bash
# Step 1: Design workflow
python phase1_networkx_design/01_workflow_design.py

# Step 2: Find bottlenecks
python phase1_networkx_design/02_bottleneck_analysis.py

# Step 3: Calculate costs
python phase1_networkx_design/03_cost_analysis.py

# Step 4: Simulate optimizations
python phase1_networkx_design/04_optimization_simulation.py
```

**Output:** Graphs showing bottlenecks, cost analysis, optimization opportunities

### 3. Run Phase 2: LangGraph Implementation (10 minutes)

```bash
# Start with basic agent
python phase2_langgraph_implementation/01_basic_agent.py

# Run optimized version
python phase2_langgraph_implementation/02_optimized_agent.py

# Add persistence
python phase2_langgraph_implementation/03_with_persistence.py

# Production ready
python phase2_langgraph_implementation/04_production_ready.py
```

**Output:** Working agent system with metrics

### 4. Run Phase 3: Monitoring & Re-optimization (5 minutes)

```bash
# Collect metrics
python phase3_monitoring/01_metrics_collection.py

# Export to NetworkX
python phase3_monitoring/02_export_to_networkx.py

# Find new optimizations
python phase3_monitoring/03_continuous_optimization.py
```

**Output:** Updated workflow with new optimizations

---

## 📊 What You'll Learn

### NetworkX Skills
- Create workflow graphs
- Calculate betweenness centrality (bottlenecks)
- Compute critical paths
- Simulate workflow changes
- Visualize complex systems
- Cost analysis and prediction

### LangGraph Skills
- Build stateful agents
- Implement conditional routing
- Add checkpointing
- Handle human-in-the-loop
- Stream responses
- Production deployment patterns

### Integration Skills
- Design → Implementation workflow
- Metrics collection
- Continuous optimization
- Cost tracking
- Performance monitoring

---

## 🎓 Key Concepts Demonstrated

### 1. Bottleneck Detection
**File:** `phase1_networkx_design/02_bottleneck_analysis.py`
- Uses betweenness centrality
- Identifies critical nodes
- Quantifies impact

### 2. Cost Optimization
**File:** `phase1_networkx_design/03_cost_analysis.py`
- Token counting per node
- Cost per request calculation
- ROI projections

### 3. State Management
**File:** `phase2_langgraph_implementation/02_optimized_agent.py`
- TypedDict for type safety
- Automatic state propagation
- Conditional routing

### 4. Checkpointing
**File:** `phase2_langgraph_implementation/03_with_persistence.py`
- SQLite checkpointer
- Resume from failures
- Audit trail

### 5. Continuous Improvement
**File:** `phase3_monitoring/03_continuous_optimization.py`
- Production metrics → NetworkX
- Re-analyze workflow
- Deploy improvements

---

## 💡 Real-World Impact

This demo shows the exact process that achieved:
- **68% faster** response times
- **70% cost** reduction
- **97% accurate** predictions
- **$780K** annual savings

---

## 🔍 Cursor AI Exploration Prompts

See **Learning_PROMPTS.md** for detailed prompts to explore this project.

---

## 📈 Expected Results

### After Phase 1 (NetworkX Design):
- Workflow visualization
- Bottleneck identification (e.g., "intent_classifier" at 0.667)
- Cost prediction ($0.111 per request)
- Optimization opportunities (cache intent, parallel processing)

### After Phase 2 (LangGraph Implementation):
- Working agent system
- Actual metrics (response time, cost)
- Validation of predictions (typically 95%+ accurate)

### After Phase 3 (Continuous Optimization):
- Updated workflow based on production data
- New optimization opportunities
- Improved performance

---

## 🛠️ Customization

### To adapt for your use case:

1. **Modify workflow** in `01_workflow_design.py`
   - Add/remove nodes
   - Change connections
   - Adjust node costs

2. **Update agent logic** in `02_optimized_agent.py`
   - Change prompts
   - Add new tools
   - Modify state schema

3. **Adjust metrics** in `01_metrics_collection.py`
   - Track different KPIs
   - Change collection frequency
   - Add custom analysis

---

## 📚 Additional Resources

- **NetworkX Docs:** https://networkx.org/
- **LangGraph Docs:** https://langchain-ai.github.io/langgraph/
- **Blog Post:** https://www.linkedin.com/posts/sivakumar-sampathkumar-91505516_networkx-langgraph-save-500k-on-agent-activity-7399811325851246592-Uk14?utm_source=share&utm_medium=member_desktop&rcm=ACoAAAM12-EBl8j9F-FZTQ3d5di5JIAe97p6D0M

---

## 🤝 Contributing

This is a learning resource. Feel free to:
- Fork and experiment
- Add new examples
- Improve documentation
- Share your results

---

## 📞 Questions?

- Open an issue
- Connect on LinkedIn


---

**Now let's build optimized agent systems!** 🚀
