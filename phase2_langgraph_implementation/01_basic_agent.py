"""
Phase 2, Step 1: Basic LangGraph Agent

This script implements the customer support workflow using LangGraph.
It demonstrates:
1. State management with TypedDict
2. Node functions (agents/tasks)
3. Conditional routing
4. Basic execution

This is the implementation of the NetworkX design from Phase 1.
"""

from typing import TypedDict, Literal, Annotated
from langgraph.graph import StateGraph, END
import random
import time

# STEP 1: Define State Schema
# This is what flows through the graph - like a shared memory
class AgentState(TypedDict):
    """
    State that flows through the agent workflow.
    Each node can read from and write to this state.
    """
    # Input
    query: str
    user_id: str
    
    # Processing
    intent: str  # billing, technical, account
    context: dict
    
    # Output
    response: str
    confidence: float
    
    # Metadata
    cost: float
    time_ms: float
    path_taken: list[str]


# STEP 2: Define Node Functions
# Each function represents a node in the NetworkX graph

def intent_classifier(state: AgentState) -> AgentState:
    """
    Classify user intent from query.
    In production: Call GPT-4 mini with classification prompt
    """
    print(f"🔍 Classifying intent for: '{state['query'][:50]}...'")
    
    start_time = time.time()
    
    # Simulate LLM call
    time.sleep(0.1)  # Simulate 100ms API call
    
    # Mock classification based on keywords
    query_lower = state['query'].lower()
    if 'bill' in query_lower or 'charge' in query_lower or 'payment' in query_lower:
        intent = 'billing'
    elif 'technical' in query_lower or 'error' in query_lower or 'bug' in query_lower:
        intent = 'technical'
    else:
        intent = 'account'
    
    elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
    
    # Update state
    state['intent'] = intent
    state['cost'] += 0.002  # GPT-4 mini cost
    state['time_ms'] += elapsed_time
    state['path_taken'].append('intent_classifier')
    
    print(f"  ✅ Intent: {intent} (cost: $0.002, time: {elapsed_time:.0f}ms)")
    
    return state


def context_enricher(state: AgentState) -> AgentState:
    """
    Fetch user context from database.
    In production: Query user DB, past conversations, etc.
    """
    print(f"📚 Enriching context for user: {state['user_id']}")
    
    start_time = time.time()
    
    # Simulate DB query
    time.sleep(0.05)  # 50ms DB query
    
    # Mock context
    state['context'] = {
        'user_tier': 'premium',
        'past_issues': ['billing_q1', 'technical_q2'],
        'last_contact': '2024-01-15'
    }
    
    elapsed_time = (time.time() - start_time) * 1000
    
    state['time_ms'] += elapsed_time
    state['path_taken'].append('context_enricher')
    
    print(f"  ✅ Context loaded (time: {elapsed_time:.0f}ms)")
    
    return state


def billing_agent(state: AgentState) -> AgentState:
    """
    Handle billing-related queries.
    In production: Call GPT-4 with billing prompt + context
    """
    print(f"💰 Billing agent processing query...")
    
    start_time = time.time()
    
    # Simulate LLM call
    time.sleep(0.15)  # 150ms API call
    
    state['response'] = f"Billing response for: {state['query']}"
    state['confidence'] = 0.92
    state['cost'] += 0.015  # GPT-4 cost
    
    elapsed_time = (time.time() - start_time) * 1000
    state['time_ms'] += elapsed_time
    state['path_taken'].append('billing_agent')
    
    print(f"  ✅ Response generated (cost: $0.015, time: {elapsed_time:.0f}ms)")
    
    return state


def technical_agent(state: AgentState) -> AgentState:
    """
    Handle technical support queries.
    In production: Call GPT-4 with technical prompt + context
    """
    print(f"🔧 Technical agent processing query...")
    
    start_time = time.time()
    time.sleep(0.20)  # 200ms API call
    
    state['response'] = f"Technical support for: {state['query']}"
    state['confidence'] = 0.88
    state['cost'] += 0.020  # GPT-4 cost (more tokens)
    
    elapsed_time = (time.time() - start_time) * 1000
    state['time_ms'] += elapsed_time
    state['path_taken'].append('technical_agent')
    
    print(f"  ✅ Response generated (cost: $0.020, time: {elapsed_time:.0f}ms)")
    
    return state


def account_agent(state: AgentState) -> AgentState:
    """
    Handle account management queries.
    In production: Call GPT-4 with account management prompt
    """
    print(f"👤 Account agent processing query...")
    
    start_time = time.time()
    time.sleep(0.12)  # 120ms API call
    
    state['response'] = f"Account management for: {state['query']}"
    state['confidence'] = 0.90
    state['cost'] += 0.012  # GPT-4 cost
    
    elapsed_time = (time.time() - start_time) * 1000
    state['time_ms'] += elapsed_time
    state['path_taken'].append('account_agent')
    
    print(f"  ✅ Response generated (cost: $0.012, time: {elapsed_time:.0f}ms)")
    
    return state


def quality_check(state: AgentState) -> AgentState:
    """
    Validate response quality.
    In production: Call GPT-4 mini to check response
    """
    print(f"✓ Quality check (confidence: {state['confidence']:.2f})...")
    
    start_time = time.time()
    time.sleep(0.05)  # 50ms API call
    
    state['cost'] += 0.003  # GPT-4 mini cost
    
    elapsed_time = (time.time() - start_time) * 1000
    state['time_ms'] += elapsed_time
    state['path_taken'].append('quality_check')
    
    print(f"  ✅ Quality validated (cost: $0.003, time: {elapsed_time:.0f}ms)")
    
    return state


def response_formatter(state: AgentState) -> AgentState:
    """
    Format final response for user.
    In production: Format with templates, add disclaimers, etc.
    """
    print(f"📝 Formatting response...")
    
    start_time = time.time()
    time.sleep(0.01)  # 10ms formatting
    
    state['response'] = f"[FORMATTED] {state['response']}"
    state['cost'] += 0.001  # GPT-4 mini cost
    
    elapsed_time = (time.time() - start_time) * 1000
    state['time_ms'] += elapsed_time
    state['path_taken'].append('response_formatter')
    
    print(f"  ✅ Response formatted (cost: $0.001, time: {elapsed_time:.0f}ms)")
    
    return state


# STEP 3: Define Routing Functions
# These determine which path to take based on state

def route_to_agent(state: AgentState) -> Literal["billing_agent", "technical_agent", "account_agent"]:
    """
    Route to appropriate specialist agent based on intent.
    This implements the conditional edges from NetworkX graph.
    """
    intent = state['intent']
    print(f"🔀 Routing to {intent} agent...")
    return f"{intent}_agent"


def route_after_quality(state: AgentState) -> Literal["response_formatter", "intent_classifier"]:
    """
    Route based on quality check results.
    If confidence is low, retry. Otherwise, continue to formatter.
    """
    if state['confidence'] < 0.5:
        print(f"⚠️  Low confidence ({state['confidence']:.2f}), retrying...")
        return "intent_classifier"
    else:
        print(f"✓ Good confidence ({state['confidence']:.2f}), formatting...")
        return "response_formatter"


# STEP 4: Build the Graph

def build_agent_graph():
    """
    Build the LangGraph workflow.
    This mirrors the NetworkX design from Phase 1.
    """
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes (same as NetworkX nodes)
    workflow.add_node("intent_classifier", intent_classifier)
    workflow.add_node("context_enricher", context_enricher)
    workflow.add_node("billing_agent", billing_agent)
    workflow.add_node("technical_agent", technical_agent)
    workflow.add_node("account_agent", account_agent)
    workflow.add_node("quality_check", quality_check)
    workflow.add_node("response_formatter", response_formatter)
    
    # Set entry point
    workflow.set_entry_point("intent_classifier")
    
    # Add edges (same as NetworkX edges)
    workflow.add_edge("intent_classifier", "context_enricher")
    
    # Conditional routing from context_enricher to specialist agents
    workflow.add_conditional_edges(
        "context_enricher",
        route_to_agent,
        {
            "billing_agent": "billing_agent",
            "technical_agent": "technical_agent",
            "account_agent": "account_agent"
        }
    )
    
    # All specialists go to quality check
    workflow.add_edge("billing_agent", "quality_check")
    workflow.add_edge("technical_agent", "quality_check")
    workflow.add_edge("account_agent", "quality_check")
    
    # Conditional routing from quality check
    workflow.add_conditional_edges(
        "quality_check",
        route_after_quality,
        {
            "response_formatter": "response_formatter",
            "intent_classifier": "intent_classifier"  # Retry loop
        }
    )
    
    # Final edge to end
    workflow.add_edge("response_formatter", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app


# STEP 5: Run the Agent

def run_agent(query: str, user_id: str = "user_123"):
    """
    Execute the agent workflow for a query.
    """
    print("=" * 70)
    print(f"PROCESSING QUERY: {query}")
    print("=" * 70)
    print()
    
    # Build graph
    app = build_agent_graph()
    
    # Initial state
    initial_state = {
        "query": query,
        "user_id": user_id,
        "intent": "",
        "context": {},
        "response": "",
        "confidence": 0.0,
        "cost": 0.0,
        "time_ms": 0.0,
        "path_taken": []
    }
    
    # Run the graph
    start_time = time.time()
    final_state = app.invoke(initial_state)
    total_time = (time.time() - start_time) * 1000
    
    # Print results
    print()
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"\nIntent: {final_state['intent']}")
    print(f"Confidence: {final_state['confidence']:.2f}")
    print(f"\nResponse: {final_state['response']}")
    print(f"\nPath taken: {' → '.join(final_state['path_taken'])}")
    print(f"\nCost: ${final_state['cost']:.4f}")
    print(f"Time: {final_state['time_ms']:.0f}ms (wall clock: {total_time:.0f}ms)")
    print()
    
    return final_state


# STEP 6: Example Usage

if __name__ == "__main__":
    # Example queries
    queries = [
        "I have a question about my bill from last month",
        "I'm getting an error when I try to login",
        "How do I update my email address?",
    ]
    
    print("\n" + "🚀 " * 30)
    print("LANGGRAPH AGENT DEMO - Basic Implementation")
    print("🚀 " * 30 + "\n")
    
    results = []
    for query in queries:
        result = run_agent(query)
        results.append(result)
        print("\n" + "-" * 70 + "\n")
    
    # Summary statistics
    print("\n" + "=" * 70)
    print("SUMMARY STATISTICS")
    print("=" * 70)
    print(f"\nTotal queries: {len(results)}")
    print(f"Average cost: ${sum(r['cost'] for r in results) / len(results):.4f}")
    print(f"Average time: {sum(r['time_ms'] for r in results) / len(results):.0f}ms")
    print(f"Total cost: ${sum(r['cost'] for r in results):.4f}")
    
    # Cost breakdown by intent
    print("\nCost by intent:")
    intents = {}
    for r in results:
        intent = r['intent']
        if intent not in intents:
            intents[intent] = []
        intents[intent].append(r['cost'])
    
    for intent, costs in intents.items():
        avg_cost = sum(costs) / len(costs)
        print(f"  {intent}: ${avg_cost:.4f} (n={len(costs)})")
    
    print("\n" + "=" * 70)
    print("✅ DEMO COMPLETE")
    print("=" * 70)
    print("\nThis implementation matches the NetworkX design from Phase 1.")
    print("The actual metrics should be within 5-10% of predicted values.")
    print("\nNext: Add optimizations, persistence, and monitoring!")
