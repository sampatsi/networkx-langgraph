"""
Streamlit UI for NetworkX + LangGraph Workflow Visualization

This app provides an interactive interface to explore:
- Workflow graph structure
- Bottleneck analysis
- Cost analysis
- Optimization opportunities
"""

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import json
import pickle
from pathlib import Path
import numpy as np
import pandas as pd

# Page config
st.set_page_config(
    page_title="NetworkX + LangGraph Workflow Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better visibility
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2C3E50;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background-color: #F8F9FA;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border: 1px solid #DEE2E6;
    }
    .stMetric {
        background-color: #FFFFFF;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #E9ECEF;
    }
    /* Improve text visibility */
    .stMarkdown {
        color: #2C3E50;
    }
    h1, h2, h3 {
        color: #2C3E50 !important;
    }
    /* Better table visibility */
    .dataframe {
        background-color: #FFFFFF;
        border: 1px solid #DEE2E6;
    }
    /* Sidebar improvements */
    .css-1d391kg {
        background-color: #F8F9FA;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_graph():
    """Load the NetworkX graph"""
    try:
        with open("data/workflow_graph.gpickle", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        st.error("Graph file not found. Please run Phase 1 scripts first.")
        st.stop()

@st.cache_data
def load_analysis_data():
    """Load analysis results"""
    data = {}
    try:
        with open("data/bottleneck_analysis.json", "r") as f:
            data['bottleneck'] = json.load(f)
    except FileNotFoundError:
        data['bottleneck'] = None
    
    try:
        with open("data/cost_analysis.json", "r") as f:
            data['cost'] = json.load(f)
    except FileNotFoundError:
        data['cost'] = None
    
    return data

def create_interactive_graph(G):
    """Create an interactive Plotly graph visualization with improved visibility"""
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Extract node positions
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    
    # Create edge traces with better visibility
    edge_traces = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        weight = G[edge[0]][edge[1]].get('weight', 1.0)
        
        edge_trace = go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            mode='lines',
            line=dict(
                width=max(weight*6, 2),  # Thicker edges for visibility
                color='#4A90E2'  # Bright blue for better contrast
            ),
            hoverinfo='none',
            showlegend=False
        )
        edge_traces.append(edge_trace)
    
    # Create node trace with better colors
    node_info = []
    node_colors = []
    node_sizes = []
    
    # Color mapping by node type for better distinction
    type_colors = {
        'entry': '#2ECC71',      # Green
        'exit': '#2ECC71',       # Green
        'classifier': '#3498DB',  # Blue
        'enricher': '#9B59B6',    # Purple
        'specialist': '#E67E22',  # Orange
        'formatter': '#1ABC9C',   # Teal
        'validator': '#E74C3C',   # Red
        'unknown': '#95A5A6'      # Gray
    }
    
    for node in G.nodes():
        node_data = G.nodes[node]
        cost = node_data.get('cost_per_call', 0)
        time_ms = node_data.get('avg_time_ms', 0)
        node_type = node_data.get('type', 'unknown')
        
        # Use type-based color, fallback to cost-based
        base_color = type_colors.get(node_type, '#95A5A6')
        node_colors.append(base_color)
        
        # Size based on cost (larger = more expensive)
        base_size = 40
        cost_multiplier = max(cost * 200, 1)  # Scale cost to size
        node_sizes.append(base_size + cost_multiplier)
        
        info = f"<b style='color: #2C3E50;'>{node}</b><br>"
        info += f"Type: {node_type}<br>"
        info += f"Cost: ${cost:.4f}<br>"
        info += f"Time: {time_ms}ms"
        node_info.append(info)
    
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=[node.replace('_', '<br>') for node in G.nodes()],
        textposition="middle center",
        textfont=dict(
            size=12,  # Larger font
            color='white',  # White text for contrast
            family='Arial Black'  # Bold font
        ),
        hovertext=node_info,
        hoverinfo='text',
        marker=dict(
            size=node_sizes,
            color=node_colors,
            line=dict(
                width=3,  # Thicker border
                color='#2C3E50'  # Dark border for contrast
            ),
            opacity=0.9
        ),
        showlegend=False
    )
    
    fig = go.Figure(data=edge_traces + [node_trace],
                    layout=go.Layout(
                        title=dict(
                            text='<b>Workflow Graph Visualization</b>',
                            x=0.5,
                            font=dict(size=22, color='#2C3E50', family='Arial')
                        ),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=40, l=40, r=40, t=60),
                        annotations=[dict(
                            text="<b>Node colors represent type | Size represents cost</b>",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.5, y=-0.05,
                            xanchor="center", yanchor="top",
                            font=dict(color='#34495E', size=13, family='Arial')
                        )],
                        xaxis=dict(
                            showgrid=False, 
                            zeroline=False, 
                            showticklabels=False,
                            range=[min(node_x) - 0.2, max(node_x) + 0.2]
                        ),
                        yaxis=dict(
                            showgrid=False, 
                            zeroline=False, 
                            showticklabels=False,
                            range=[min(node_y) - 0.2, max(node_y) + 0.2]
                        ),
                        plot_bgcolor='#F8F9FA',  # Light gray background
                        paper_bgcolor='#FFFFFF',  # White paper background
                        height=700,  # Taller for better visibility
                        font=dict(family='Arial', color='#2C3E50')
                    ))
    
    return fig

def main():
    # Header
    st.markdown('<div class="main-header">📊 NetworkX + LangGraph Workflow Analyzer</div>', unsafe_allow_html=True)
    
    # Load data
    G = load_graph()
    analysis_data = load_analysis_data()
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Select View",
            ["Overview", "Workflow Graph", "Bottleneck Analysis", "Cost Analysis", "Optimization"]
        )
        
        st.divider()
        st.header("Quick Stats")
        st.metric("Total Nodes", G.number_of_nodes())
        st.metric("Total Edges", G.number_of_edges())
        
        if analysis_data['cost']:
            avg_cost = analysis_data['cost']['baseline']['avg_cost_per_request']
            st.metric("Avg Cost/Request", f"${avg_cost:.4f}")
    
    # Main content based on selected page
    if page == "Overview":
        show_overview(G, analysis_data)
    elif page == "Workflow Graph":
        show_workflow_graph(G)
    elif page == "Bottleneck Analysis":
        show_bottleneck_analysis(G, analysis_data)
    elif page == "Cost Analysis":
        show_cost_analysis(G, analysis_data)
    elif page == "Optimization":
        show_optimization(G, analysis_data)

def show_overview(G, analysis_data):
    """Show overview dashboard"""
    st.header("📈 Overview Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Nodes", G.number_of_nodes())
    with col2:
        st.metric("Total Edges", G.number_of_edges())
    with col3:
        if analysis_data['cost']:
            avg_cost = analysis_data['cost']['baseline']['avg_cost_per_request']
            st.metric("Avg Cost/Request", f"${avg_cost:.4f}")
        else:
            st.metric("Avg Cost/Request", "N/A")
    with col4:
        if analysis_data['bottleneck']:
            bottleneck = analysis_data['bottleneck']['bottleneck_node']
            st.metric("Primary Bottleneck", bottleneck.replace('_', ' ').title())
        else:
            st.metric("Primary Bottleneck", "N/A")
    
    st.divider()
    
    # Node types breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Node Types")
        node_types = {}
        for node in G.nodes():
            node_type = G.nodes[node].get('type', 'unknown')
            node_types[node_type] = node_types.get(node_type, 0) + 1
        
        fig_pie = px.pie(
            values=list(node_types.values()),
            names=list(node_types.keys()),
            title="Distribution of Node Types"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("Node Costs")
        node_costs = []
        for node in G.nodes():
            cost = G.nodes[node].get('cost_per_call', 0)
            if cost > 0:
                node_costs.append({
                    'Node': node.replace('_', ' ').title(),
                    'Cost': cost
                })
        
        if node_costs:
            df_costs = pd.DataFrame(node_costs)
            df_costs = df_costs.sort_values('Cost', ascending=False)
            
            fig_bar = px.bar(
                df_costs,
                x='Node',
                y='Cost',
                title="Cost per Node",
                labels={'Cost': 'Cost ($)', 'Node': 'Node Name'}
            )
            fig_bar.update_xaxes(tickangle=45)
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # Path analysis
    st.subheader("Workflow Paths")
    all_paths = list(nx.all_simple_paths(G, 'input', 'output'))
    
    path_data = []
    for path in all_paths:
        total_cost = sum(G.nodes[node].get('cost_per_call', 0) for node in path)
        total_time = sum(G.nodes[node].get('avg_time_ms', 0) for node in path)
        path_data.append({
            'Path': ' → '.join(path),
            'Cost ($)': total_cost,
            'Time (ms)': total_time
        })
    
    df_paths = pd.DataFrame(path_data)
    st.dataframe(df_paths, use_container_width=True, hide_index=True)

def show_workflow_graph(G):
    """Show interactive workflow graph"""
    st.header("🕸️ Workflow Graph Visualization")
    
    st.markdown("""
    <div style='background-color: #E8F4F8; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #3498DB; margin-bottom: 1rem;'>
    <h4 style='color: #2C3E50; margin-top: 0;'>📋 How to Read the Graph:</h4>
    <ul style='color: #34495E;'>
        <li><strong>Node Colors:</strong> Represent node types (Green=Entry/Exit, Blue=Classifier, Purple=Enricher, Orange=Specialist, Teal=Formatter, Red=Validator)</li>
        <li><strong>Node Size:</strong> Larger nodes = Higher cost</li>
        <li><strong>Edge Width:</strong> Thicker edges = Higher traffic probability</li>
        <li><strong>Hover:</strong> Move your mouse over any node to see detailed information</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    fig = create_interactive_graph(G)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
    
    # Node details table
    st.subheader("Node Details")
    node_data = []
    for node in G.nodes():
        node_attrs = G.nodes[node]
        node_data.append({
            'Node': node,
            'Type': node_attrs.get('type', 'N/A'),
            'Cost ($)': node_attrs.get('cost_per_call', 0),
            'Time (ms)': node_attrs.get('avg_time_ms', 0),
            'LLM Model': node_attrs.get('llm_model', 'N/A')
        })
    
    df_nodes = pd.DataFrame(node_data)
    st.dataframe(df_nodes, use_container_width=True, hide_index=True)

def show_bottleneck_analysis(G, analysis_data):
    """Show bottleneck analysis"""
    st.header("🔴 Bottleneck Analysis")
    
    if not analysis_data['bottleneck']:
        st.warning("Bottleneck analysis data not found. Please run 02_bottleneck_analysis.py first.")
        return
    
    bottleneck_data = analysis_data['bottleneck']
    bottleneck_node = bottleneck_data['bottleneck_node']
    bottleneck_score = bottleneck_data['bottleneck_score']
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Primary Bottleneck", bottleneck_node.replace('_', ' ').title())
    with col2:
        st.metric("Centrality Score", f"{bottleneck_score:.3f}")
    with col3:
        st.metric("Traffic Impact", f"{bottleneck_score * 100:.1f}%")
    
    st.divider()
    
    # Betweenness centrality chart
    st.subheader("Node Criticality Ranking")
    betweenness = bottleneck_data['betweenness_centrality']
    
    df_centrality = pd.DataFrame([
        {'Node': node, 'Centrality': score}
        for node, score in sorted(betweenness.items(), key=lambda x: x[1], reverse=True)
    ])
    
    fig = px.bar(
        df_centrality,
        x='Centrality',
        y='Node',
        orientation='h',
        title="Betweenness Centrality (Higher = More Critical)",
        labels={'Centrality': 'Centrality Score', 'Node': 'Node Name'},
        color='Centrality',
        color_continuous_scale='YlOrRd'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Critical paths
    st.subheader("Critical Paths (Slowest)")
    if 'critical_paths' in bottleneck_data:
        path_data = []
        for path_info in bottleneck_data['critical_paths'][:5]:
            path_data.append({
                'Path': ' → '.join(path_info['path']),
                'Time (ms)': path_info['time_ms'],
                'Cost ($)': path_info['cost']
            })
        
        df_paths = pd.DataFrame(path_data)
        st.dataframe(df_paths, use_container_width=True, hide_index=True)
    
    # Optimization scenarios
    st.subheader("Optimization Scenarios")
    if 'optimization_opportunities' in bottleneck_data:
        opt_data = []
        for opt in bottleneck_data['optimization_opportunities']:
            opt_data.append({
                'Scenario': opt['scenario'],
                'Time Multiplier': opt['time_multiplier'],
                'Cost Multiplier': opt['cost_multiplier']
            })
        
        df_opt = pd.DataFrame(opt_data)
        st.dataframe(df_opt, use_container_width=True, hide_index=True)

def show_cost_analysis(G, analysis_data):
    """Show cost analysis"""
    st.header("💰 Cost Analysis")
    
    if not analysis_data['cost']:
        st.warning("Cost analysis data not found. Please run 03_cost_analysis.py first.")
        return
    
    cost_data = analysis_data['cost']
    baseline = cost_data['baseline']
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg Cost/Request", f"${baseline['avg_cost_per_request']:.4f}")
    with col2:
        st.metric("Min Cost/Request", f"${baseline['min_cost']:.4f}")
    with col3:
        st.metric("Max Cost/Request", f"${baseline['max_cost']:.4f}")
    with col4:
        variance = baseline['max_cost'] - baseline['min_cost']
        st.metric("Cost Variance", f"${variance:.4f}")
    
    st.divider()
    
    # Scale projections
    st.subheader("Cost Projections at Scale")
    if 'scale_projections' in cost_data:
        scale_data = []
        for scale_name, scale_info in cost_data['scale_projections'].items():
            scale_data.append({
                'Scale': scale_name,
                'Monthly Requests': scale_info['monthly_requests'],
                'Monthly Cost ($)': scale_info['monthly_cost'],
                'Annual Cost ($)': scale_info['annual_cost']
            })
        
        df_scale = pd.DataFrame(scale_data)
        
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(df_scale, use_container_width=True, hide_index=True)
        
        with col2:
            fig = px.bar(
                df_scale,
                x='Scale',
                y='Annual Cost ($)',
                title="Annual Cost Projections",
                labels={'Scale': 'Scale', 'Annual Cost ($)': 'Annual Cost ($)'}
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    
    # Cost breakdown by node
    st.subheader("Cost Breakdown by Node")
    if 'node_costs' in cost_data:
        node_costs = cost_data['node_costs']
        df_node_costs = pd.DataFrame(node_costs)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pie = px.pie(
                df_node_costs,
                values='contribution',
                names='node',
                title="Cost Distribution by Node"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            fig_bar = px.bar(
                df_node_costs,
                x='node',
                y='contribution',
                title="Cost Contribution per Node",
                labels={'node': 'Node', 'contribution': 'Cost Contribution ($)'}
            )
            fig_bar.update_xaxes(tickangle=45)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        st.dataframe(df_node_costs, use_container_width=True, hide_index=True)

def show_optimization(G, analysis_data):
    """Show optimization opportunities"""
    st.header("⚡ Optimization Opportunities")
    
    st.markdown("""
    This section shows potential optimizations and their impact.
    """)
    
    if not analysis_data['cost'] or not analysis_data['bottleneck']:
        st.warning("Analysis data not found. Please run Phase 1 scripts first.")
        return
    
    # Optimization target
    cost_data = analysis_data['cost']
    if 'optimization_target' in cost_data:
        opt_target = cost_data['optimization_target']
        
        st.subheader("Primary Optimization Target")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Target Node", opt_target['node'].replace('_', ' ').title())
        with col2:
            st.metric("Current Cost", f"${opt_target['current_cost']:.4f}")
        with col3:
            st.metric("Potential Savings", f"{opt_target['potential_savings_pct']:.1f}%")
    
    # Interactive optimization calculator
    st.subheader("Optimization Calculator")
    
    selected_node = st.selectbox(
        "Select Node to Optimize",
        [node for node in G.nodes() if G.nodes[node].get('cost_per_call', 0) > 0]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        cost_reduction = st.slider("Cost Reduction (%)", 0, 90, 50, 5)
    with col2:
        monthly_requests = st.number_input("Monthly Requests", min_value=1000, value=1000000, step=10000)
    
    if selected_node:
        current_cost = G.nodes[selected_node].get('cost_per_call', 0)
        new_cost = current_cost * (1 - cost_reduction / 100)
        savings_per_request = current_cost - new_cost
        
        # Calculate how often this node is visited
        all_paths = list(nx.all_simple_paths(G, 'input', 'output'))
        paths_through_node = sum(1 for path in all_paths if selected_node in path)
        visit_probability = paths_through_node / len(all_paths) if all_paths else 0
        
        annual_savings = savings_per_request * visit_probability * monthly_requests * 12
        
        st.success(f"""
        **Optimization Impact:**
        - Current cost: ${current_cost:.4f} per call
        - New cost: ${new_cost:.4f} per call
        - Savings per request: ${savings_per_request:.4f}
        - Node visit probability: {visit_probability*100:.1f}%
        - **Annual savings: ${annual_savings:,.0f}** (at {monthly_requests:,} req/month)
        """)

if __name__ == "__main__":
    main()

