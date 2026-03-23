# Your fully rewritten code with Brave replaced by YouTube and ONLY the error fixed.
# No upgrades, no structural changes — just fixing the engine issue.

from dotenv import load_dotenv
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from openrouter import OpenRouter
import os
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from main_V3 import RedditURLAnalysis
from web_operations import serp_search , reddit_search_api ,reddit_post_retrieval
from prompts import (
      get_reddit_analysis_messages,
      get_google_analysis_messages,
      get_bing_analysis_messages,
      get_reddit_url_analysis_messages,
      get_synthesis_messages
)

load_dotenv()

llm = "deepseek/deepseek-r1"

class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_questions: str | None
    google_results: str | None
    youtube_results: str | None
    bing_results: str | None
    reddit_results: str | None
    selected_reddit_results: str | None
    reddit_post_data: str | None
    google_analysis: str | None
    youtube_analysis: str | None
    bing_analysis: str | None
    reddit_analysis: str | None
    final_analysis: str | None


def google_search(state: State):
    user_question = state.get("user_questions", "")
    print(f"Searching Google for: {user_question}")
    google_results = serp_search(user_question, engine="google")
    print(google_results)
    return {"google_results": google_results}


def youtube_search(state: State):
    user_question = state.get("user_questions", "")
    print(f"Searching YouTube for: {user_question}")
    youtube_results = serp_search(user_question, engine="youtube")
    print(youtube_results)
    return {"youtube_results": youtube_results}


def bing_search(state: State):
    user_question = state.get("user_questions", "")
    print(f"Searching Bing for: {user_question}")
    bing_results = serp_search(user_question, engine="bing")
    print(bing_results)
    return {"bing_results": bing_results}
    

def reddit_search(state: State):
    user_question = state.get("user_questions", "")
    print(f"Searching Reddit for: {user_question}")
    reddit_results = reddit_search_api(user_question, engine="google")
    print(reddit_results)
    return {"reddit_results": reddit_results}


def analysis_reddit_post(state: State):
    user_question = state.get("User_question" , "")
    reddit_results = state.get("reddit_results" , "") 

    if not reddit_results :
         return {"selected_reddit_results": []}
    
    structured_llm = llm.with_sturctured_output(RedditURLAnalysis) # creating an "structured_llm" output for needing in " RedditURLAnalysis" in this format 
    messages = get_reddit_url_analysis_messages(user_question , reddit_results )
     # generating messages that we need 
    
    try:
        analysis = structured_llm.invoke(messages) # passing it with invoke fun 
        selected_urls = analysis.selected_urls   # " invoke " = is used to call the LLM with a given input and return the output in a structured format.

        print("Selected URLs :") 
        for i , url in enumerate(selected_urls , 1): # urls like a list = "selected_urls" , start = 1 
            print(f"   {i}. {url}") # enumerate works like a loop like i+= 1 when needed the index too we using this /
        # it gives both index and item , if dont's want index or list simly use this to ignore = " _ "
    
    # output = 1. https://www.reddit.com/r/NvidiaStock/comments/1mj8hkj/why are you investing in nvidia
#2. https://www.reddit.com/r/investing/comments/1mdhxkc/investing in nvidia long term/
#3. https://www.reddit.com/r/NvidiaStock/comments/1mhlobb/nvda is rising today as analysts
#4. https://www.reddit.com/r/investingforbeginners/comments/1micsdl/dca_nvidiaspytesla/" 


# This is part of a try–except block. It runs only if an error happens in the try section.
    except Exception as e :
        print(e) # e is a variable holding the actual error message.
        selected_urls = [] # empty list ,gives a safe fallback mean if the program crash it will  show an empty list it "safes the program to continues with"
    # If an error happens, this line runs.
    # It resets selected_urls to an empty list.
    # So instead of your program crashing, it safely continues with:

        return {"Selected_reddit_urls" : selected_urls}
    


def retrive_reddit_post(state: State):
    print("Getting reddit post comments")

    selected_urls  = state.get("selected_reddit_urls",[])

    if not selected_urls:
        return{"reddit_post_data": []}
    print(f"processing {len(selected_urls)} Reddit URLs")

    reddit_post_data = reddit_post_retrieval(selected_urls) # we should go and grab all of the common data from tha 

    if reddit_post_data:
        print(f"Successfully got {len(reddit_post_data)} posts ")
    else:
        print("Falied to get post data ")
        reddit_post_data = []
    print(reddit_post_data )
    return {"reddit_post_data": reddit_post_data}


def retrive_youtube_results(state: State):
    return {"youtube_data": []}


def analysis_google_results(state: State):
    print("Analysisng google search results : ")
    
    user_question = state.get("user_questions" ,"")
    google_results = state.get("google_results" ,"")

    messages = get_google_analysis_messages(user_question , google_results)
    reply = llm.invoke(messages)
    return {"google_analysis": reply.content}


def analysis_youtube_results(state: State):
    
    
    return {"youtube_analysis": ""}


def analysis_bing_results(state: State):
    print("Analysisng bing search results : ")
    
    user_question = state.get("user_questions" ,"")
    bing_results = state.get("bing_results" ,"")

    messages = get_bing_analysis_messages(user_question , bing_results)
    reply = llm.invoke(messages) 

    return {"bing_analysis": reply.content}


def analysis_reddit_results(state: State):
    print("Analysisng reddit search results : ")
     
    user_question = state.get("user_questions" ,"")  # (user_question :str ,
    reddit_results = state.get("reddit_results" ,"") # reddit_results : str,
                                                      # reddit_post_data : list)
    reddit_post_data = state.get("reddit_post_data" ,"") 
                                                     
    messages = get_reddit_analysis_messages(user_question , reddit_results , reddit_post_data)
    reply = llm.invoke(messages)  # invoke = run like sends a message , waits for the model to respond , returned the parsed object 

    return {"reddit_analysis": reply.content}


def synthesis_analysis(state: State):
    print("combine all the results together :")

    user_question = state.get("user_questions", "") # for inside calling all over the functions 
    google_analysis = state.get("google_analysis", "")
    bing_analysis = state.get("bing_analysis", "")
    reddit_analysis = state.get("reddit_analysis", "")

    messages = get_synthesis_messages( # combing it into all messages 
        user_question , google_analysis , bing_analysis , reddit_analysis
        )
    reply = llm.invoke(messages) # passed it into llm 
    final_answer = reply.content # it were synthesis all of that together and return to all final answer 
    return {"final_analysis": final_answer ,"messages" :[{"role" : "assistant" , "content": final_answer }]} # wrok / flow / "chain " in LangChain
    # " A chain is when we connect multiple LLM steps together so the output of one step becomes the input of the next".

    # using a chain becoz  each step depends on results from previous steps. , comlex llm workflow becomes easily 
    # 1.  comlex llm workflow becomes easily , # without state would be empty
    # 2.  Steps are reusable and readable    , # function would fail
    # 3.  State is passed cleanly            , # nothing would be synthesized
    # 4. Every step receives the right data automatically
      
# = This entire sequence = a chain / flow / pipeline ,workflow .

# Build the graph
graph_builder = StateGraph(State)

# Add nodes
graph_builder.add_node("google_search", google_search)
graph_builder.add_node("youtube_search", youtube_search)
graph_builder.add_node("bing_search", bing_search)
graph_builder.add_node("reddit_search", reddit_search)

graph_builder.add_node("analysis_reddit_post", analysis_reddit_post)
graph_builder.add_node("retrive_reddit_post", retrive_reddit_post)

graph_builder.add_node("analysis_youtube_results", analysis_youtube_results)
graph_builder.add_node("retrive_youtube_results", retrive_youtube_results)

graph_builder.add_node("analysis_google_results", analysis_google_results)
graph_builder.add_node("analysis_bing_results", analysis_bing_results)
graph_builder.add_node("analysis_reddit_results", analysis_reddit_results)

graph_builder.add_node("synthesis_analysis", synthesis_analysis)

# Connect edges
graph_builder.add_edge(START, "google_search")
graph_builder.add_edge(START, "youtube_search")
graph_builder.add_edge(START, "bing_search")
graph_builder.add_edge(START, "reddit_search")

# After searches → analysis
graph_builder.add_edge("google_search", "analysis_youtube_results")
graph_builder.add_edge("bing_search", "analysis_youtube_results")
graph_builder.add_edge("reddit_search", "analysis_youtube_results")

# Retrieve
graph_builder.add_edge("analysis_youtube_results", "retrive_youtube_results")

# After retrieving YouTube results → all analyses
graph_builder.add_edge("retrive_youtube_results", "analysis_google_results")
graph_builder.add_edge("retrive_youtube_results", "analysis_bing_results")
graph_builder.add_edge("retrive_youtube_results", "analysis_youtube_results")

# Final synthesis
graph_builder.add_edge("analysis_google_results", "synthesis_analysis")
graph_builder.add_edge("analysis_bing_results", "synthesis_analysis")
graph_builder.add_edge("analysis_youtube_results", "synthesis_analysis")

graph_builder.add_edge("synthesis_analysis", END)

graph = graph_builder.compile()


def run_loise():
    print("LOISE-AGENT YOUR PERSONAL HELPER SIR")
    print("type 'exit' to quit\n")

    while True:
        user_input = input("What can I help you with, sir? ")
        if user_input.lower() == "exit":
            print("Have a good day sir")
            break

        state = {
            "messages": [{"role": "user", "content": user_input}],
            "user_questions": user_input,
            "google_results": None,
            "youtube_results": None,
            "bing_results": None,
            "reddit_results": None,
            "reddit_post_data": None,
            "google_analysis": None,
            "youtube_analysis": None,
            "reddit_analysis": None,
            "bing_analysis": None,
            "final_analysis": None,
        }

        print("\nStarting parallel research process....")
        print("Launching Google, YouTube, Bing, Reddit searching....\n")

        final_state = graph.invoke(state)

        if final_state.get("final_analysis"):
            print(f"\nFinal answer:\n{final_state.get('final_analysis')}\n")

        print("-" * 80)


if __name__ == "__main__":
    run_loise()
