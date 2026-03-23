from dotenv import load_dotenv
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from openrouter import OpenRouter
import os
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from web_operations import serp_search

load_dotenv()  # load environment variables

model = "deepseek/deepseek-r1"

class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_question: str | None
    google_results: str | None
    youtube_results: str | None
    bing_results: str | None
    instagram_results: str | None
    selected_instagram_results: str | None
    instagram_post_data: str | None
    google_analysis: str | None
    youtube_analysis: str | None
    bing_analysis: str | None
    instagram_analysis: str | None
    final_analysis: str | None


def google_search(state: State):
    user_question = state.get("user_question", "")
    print(f"Searching Google for: {user_question}")
    google_results = serp_search(user_question, engine="google")
    print(google_results)
    return {"google_results": google_results}


def youtube_search(state: State):
    user_question = state.get("user_question", "")
    print(f"Searching youtube for: {user_question}")
    youtube_results = serp_search(user_question, engine="youtube")
    print(youtube_results)
    return {"youtube_results": youtube_results}


def bing_search(state: State):
    user_question = state.get("user_question", "")
    print(f"Searching Bing for: {user_question}")
    bing_results = serp_search(user_question, engine="bing")
    print(bing_results)
    return {"bing_results": bing_results}


def instagram_search(state: State):
    user_question = state.get("user_question", "")
    print(f"Searching Instagram for: {user_question}")
    instagram_results = serp_search(user_question, engine="instagram")
    print(instagram_results)
    return {"instagram_results": instagram_results}


def analysis_instagram_post(state: State):
    return {"selected_instagram_results": []}


def retrive_instagram_post(state: State):
    return {"instagram_post_data": []}


def retrive_youtube_results(state: State):
    return {"youtube_results": state.get("youtube_results", [])}


def analysis_google_results(state: State):
    return {"google_analysis": ""}


def analysis_youtube_results(state: State):
    return {"youtube_analysis": ""}


def analysis_bing_results(state: State):
    return {"bing_analysis": ""}


def analysis_instagram_results(state: State):
    return {"instagram_analysis": ""}


def synthesis_analysis(state: State):
    return {"final_analysis": ""}


graph_builder = StateGraph(State)

# Add nodes

graph_builder.add_node("google_search", google_search)
graph_builder.add_node("youtube_search", youtube_search)
graph_builder.add_node("bing_search", bing_search)
graph_builder.add_node("instagram_search", instagram_search)
graph_builder.add_node("analysis_instagram_post", analysis_instagram_post)
graph_builder.add_node("retrive_instagram_post", retrive_instagram_post)
graph_builder.add_node("analysis_youtube_results", analysis_youtube_results)
graph_builder.add_node("retrive_youtube_results", retrive_youtube_results)
graph_builder.add_node("analysis_google_results", analysis_google_results)
graph_builder.add_node("analysis_bing_results", analysis_bing_results)
graph_builder.add_node("analysis_instagram_results", analysis_instagram_results)
graph_builder.add_node("synthesis_analysis", synthesis_analysis)

# Edges

graph_builder.add_edge(START, "google_search")
graph_builder.add_edge(START, "youtube_search")
graph_builder.add_edge(START, "bing_search")
graph_builder.add_edge(START, "instagram_search")

# Connect to youtube analysis

graph_builder.add_edge("google_search", "analysis_youtube_results")
graph_builder.add_edge("bing_search", "analysis_youtube_results")
graph_builder.add_edge("instagram_search", "analysis_youtube_results")

graph_builder.add_edge("analysis_youtube_results", "retrive_youtube_results")

# After retrieve → analysis

graph_builder.add_edge("retrive_youtube_results", "analysis_google_results")
graph_builder.add_edge("retrive_youtube_results", "analysis_bing_results")
graph_builder.add_edge("retrive_youtube_results", "analysis_youtube_results")

# Synthesis

graph_builder.add_edge("analysis_google_results", "synthesis_analysis")
graph_builder.add_edge("analysis_bing_results", "synthesis_analysis")
graph_builder.add_edge("analysis_youtube_results", "synthesis_analysis")

graph_builder.add_edge("synthesis_analysis", END)

graph = graph_builder.compile()


def run_loise():
    print("LOISE-AGENT YOUR PERSONAL HELPER SIR")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("What can I help you with, sir? ")
        if user_input.lower() == "exit":
            print("Have a good day sir!")
            break

        state = {
            "messages": [{"role": "user", "content": user_input}],
            "user_question": user_input,
            "google_results": None,
            "youtube_results": None,
            "bing_results": None,
            "instagram_results": None,
            "selected_instagram_results": None,
            "instagram_post_data": None,
            "google_analysis": None,
            "youtube_analysis": None,
            "instagram_analysis": None,
            "bing_analysis": None,
            "final_analysis": None,
        }

        print("\nStarting parallel research process....")
        print("Launching Google, youtube, Bing, Instagram searches....\n")

        final_state = graph.invoke(state)

        if final_state.get("final_analysis"):
            print(f"\nFinal answer:\n{final_state['final_analysis']}\n")

        print("-" * 80)


if __name__ == "__main__":
    run_loise()
