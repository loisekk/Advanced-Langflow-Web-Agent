# cleaned_agent.py
from dotenv import load_dotenv
import os
from typing import Annotated, List, Dict, Any
try:
    from typing import TypedDict
except Exception:
    from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

load_dotenv()  # call this!

# Use a plain model id string — actual OpenRouter client used at call time
MODEL_ID = "deepseek/deepseek-r1"

class State(TypedDict, total=False):
    messages: Annotated[List[Dict[str, str]], add_messages]
    user_questions: str
    google_results: List[Dict[str, Any]]
    brave_results: List[Dict[str, Any]]
    bing_results: List[Dict[str, Any]]
    instagram_results: List[Dict[str, Any]]
    selected_instagram_results: List[str]
    instagram_post_data: List[Dict[str, Any]]
    google_analysis: str
    brave_analysis: str
    bing_analysis: str
    instagram_analysis: str
    final_analysis: str

# --- Nodes (placeholders) ---
def google_search(state: State) -> Dict[str, Any]:
    q = state.get("user_questions", "").strip()
    print("google_search:", q)
    return {"google_results": [{"title": "Example", "link": "https://example.com"}]}

def brave_search(state: State) -> Dict[str, Any]:
    q = state.get("user_questions", "").strip()
    print("brave_search:", q)
    return {"brave_results": []}

def bing_search(state: State) -> Dict[str, Any]:
    q = state.get("user_questions", "").strip()
    print("bing_search:", q)
    return {"bing_results": []}

def instagram_search(state: State) -> Dict[str, Any]:
    q = state.get("user_questions", "").strip()
    print("instagram_search:", q)
    return {"instagram_results": []}

def retrieve_brave_results(state: State) -> Dict[str, Any]:
    print("retrieve_brave_results")
    return {"brave_results": state.get("brave_results", [])}

def analysis_google_results(state: State) -> Dict[str, Any]:
    print("analysis_google_results")
    # summarize example
    items = state.get("google_results", [])
    return {"google_analysis": " | ".join(i.get("title","") for i in items)}

def analysis_brave_results(state: State) -> Dict[str, Any]:
    print("analysis_brave_results")
    return {"brave_analysis": "summary of brave"}

def analysis_bing_results(state: State) -> Dict[str, Any]:
    print("analysis_bing_results")
    return {"bing_analysis": "summary of bing"}

def analysis_instagram_results(state: State) -> Dict[str, Any]:
    print("analysis_instagram_results")
    return {"instagram_analysis": "summary of instagram"}

def synthesis_analysis(state: State) -> Dict[str, Any]:
    print("synthesis_analysis")
    parts = [
        state.get("google_analysis", ""),
        state.get("brave_analysis", ""),
        state.get("bing_analysis", ""),
        state.get("instagram_analysis", ""),
    ]
    final = " || ".join(p for p in parts if p)
    return {"final_analysis": final or "No results."}

# --- Build graph ---
graph_builder = StateGraph(dict)

# add nodes (names must match edges)
graph_builder.add_node("google_search", google_search)
graph_builder.add_node("brave_search", brave_search)
graph_builder.add_node("bing_search", bing_search)
graph_builder.add_node("instagram_search", instagram_search)
graph_builder.add_node("retrieve_brave_results", retrieve_brave_results)
graph_builder.add_node("analysis_google_results", analysis_google_results)
graph_builder.add_node("analysis_brave_results", analysis_brave_results)
graph_builder.add_node("analysis_bing_results", analysis_bing_results)
graph_builder.add_node("analysis_instagram_results", analysis_instagram_results)
graph_builder.add_node("synthesis_analysis", synthesis_analysis)

# connect edges (positional args!)
graph_builder.add_edge(START, "google_search")
graph_builder.add_edge(START, "brave_search")
graph_builder.add_edge(START, "bing_search")
graph_builder.add_edge(START, "instagram_search")

# wire searches into retrieval/analysis
graph_builder.add_edge("google_search", "analysis_google_results")
graph_builder.add_edge("brave_search", "retrieve_brave_results")
graph_builder.add_edge("retrieve_brave_results", "analysis_brave_results")
graph_builder.add_edge("bing_search", "analysis_bing_results")
graph_builder.add_edge("instagram_search", "analysis_instagram_results")

# analyses -> synthesis
graph_builder.add_edge("analysis_google_results", "synthesis_analysis")
graph_builder.add_edge("analysis_brave_results", "synthesis_analysis")
graph_builder.add_edge("analysis_bing_results", "synthesis_analysis")
graph_builder.add_edge("analysis_instagram_results", "synthesis_analysis")

graph_builder.add_edge("synthesis_analysis", END)

graph = graph_builder.compile()  # should succeed now

# --- CLI loop ---
def run_loise():
    print("LOISE-AGENT — type 'exit' to quit")
    while True:
        user_input = input("What can I help you with? ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        state: State = {
            "messages": [{"role": "user", "content": user_input}],
            "user_questions": user_input,
            # initial empties
            "google_results": [],
            "brave_results": [],
            "bing_results": [],
            "instagram_results": [],
            "instagram_post_data": [],
            "google_analysis": "",
            "brave_analysis": "",
            "bing_analysis": "",
            "instagram_analysis": "",
            "final_analysis": " give me the api key so that i can give you the answer",
        }

        print("\nStarting parallel research...")
        final_state = graph.invoke(state)   # pass the instance, not the type
        print("\nFinal state keys:", list(final_state.keys()))
        print("Final answer:", final_state.get("final_analysis", "No final answer"))
        print("-" * 80)

if __name__ == "__main__":
    run_loise()
