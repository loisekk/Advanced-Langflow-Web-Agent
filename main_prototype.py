from dotenv import load_dotenv
from typing import Annotated
from langgraph.graph import StateGraph , START , END 
from langgraph.graph.message import add_messages
# from langchain.chat_models import init_chat_model
# for an apikey uses the openrouter model for free genereation of  key
from openrouter import OpenRouter
import os
from typing_extensions import TypedDict
from pydantic import BaseModel , Field
from web_operations  import serp_search
load_dotenv # we loaded  environment variable file 

model = "deepseek/deepseek-r1" # Initilized the language 

class State(TypedDict):        # initial state 
    messages = Annotated[list ,add_messages]
    user_question             : str | None 
    google_results            : str | None
    brave_results              : str | None 
    youtube_results           : str | None
    bing_results              : str | None 
    instagram_results           : str | None 
    selected_instagram_results: str | None
    instagram_post_data         : str | None
    google_analysis           : str | None 
    brave_analysis             : str | None
    youtube_analysis           : str | None
    bing_analysis             : str | None
    instagram_analysis          : str | None
    final_analysis            : str | None

def google_search(state : State):  # it runs the class state 
    user_questions = state.get("user_questions", "") # if user questions is empty then it provide an empty string "" 
    print(f"Searching Google for :{user_questions}") # searching at first google search 
    google_results = serp_search(user_questions , engine="google")
    print(google_results )                         # it create an empty list  currently there is no search it's just a place holder
    return {"google_results": google_results}  #LangGraph expects nodes to return a dict of state updates.
                                               # LangGraph will merge this dict into the global state (so downstream nodes can read google_results)
# google results matching with google results " sates data "

def brave_search(state : State):
    user_questions = state.get("user_questions", "") 
    print(f"Searching Brave for :{user_questions}") 
    brave_results = serp_search(user_questions , engine="brave")
    print(brave_results)
    return {"brave_results": brave_results}


def bing_search(state : State):
    user_questions = state.get("user_questions", "") 
    print(f"Searching Bing for :{user_questions}") 
    bing_results =serp_search(user_questions , engine="bing")
    print(bing_results)
    return {"google_results": bing_results}


def youtube_search(state : State):
    user_questions = state.get("user_questions", "") 
    print(f"Searching youtube for :{user_questions}") 
    youtube_results =serp_search(user_questions , engine="bing")
    print(youtube_results)
    return {"google_results": youtube_results}


def instagram_search(state : State):
    user_questions = state.get("user_questions", "") 
    print(f"Searching Instagram for :{user_questions}") 
    instagram_results =serp_search(user_questions , engine="instagram")
    print(instagram_results)
    return {"google_results": instagram_results}


def analysis_instagram_post(state : State):
   return {"selected_instagram_urls": []}


def retrive_instagram_post(state : State):
    return {"instagram_post_data ": []}


def retrive_brave_results(state : State):
     return {"brave_analysis": []}


def retrive_youtube_results(state : State):
     return {"youtube_analysis": []}


def analysis_google_results(state : State):
   return {"google_analysis ":""}


def analysis_brave_results(state : State):
     return {"brave_analysis ":""}


def analysis_youtube_results(state : State):
     return {"youtube_analysis ":""}


def analysis_bing_results(state : State):
     return {"bing_analysis ":""}


def analysis_instagram_results(state : State):
    return {"instagram_analysis ":""}


def synthesis_analysis(state : State):
    return {"final answer":""}

# we have a bunch of nodes which is an operations and  function so we have to connect 1 to t of them eachother 

# so we put all of them into a graph oprator 
graph_builder = StateGraph(State)  
 
 # NODES FOR SEARCHING , ANALYSISING AND RETREVING THE DATA 

graph_builder.add_node("google_search",google_search)
graph_builder.add_node("brave_search",brave_search)
graph_builder.add_node("bing_search",bing_search)
graph_builder.add_node("youtube_search",youtube_search)
graph_builder.add_node("instagram_search",instagram_search)
graph_builder.add_node("analysis_instagram_post",analysis_instagram_post)
graph_builder.add_node("retrive_instagram_post",retrive_instagram_post)
graph_builder.add_node("analysis_brave_results",analysis_brave_results)
graph_builder.add_node("analysis_youtube_results",analysis_brave_results)
graph_builder.add_node("retrive_brave_results",retrive_brave_results)
graph_builder.add_node("retrive_youtube_results",retrive_brave_results)
graph_builder.add_node("analysis_google_results",analysis_google_results)
graph_builder.add_node("analysis_bing_results",analysis_bing_results)
graph_builder.add_node("analysis_instagram_results",analysis_instagram_results)
graph_builder.add_node("synthesis_analysis", synthesis_analysis)


# at this point they are not connected 
# the graph_builder function of edge is an connection between the nodes 

graph_builder.add_edge(START , end_key= "google_search")
graph_builder.add_edge(START , end_key= "brave_search")    # FIRST FOUR PARALLEL SEARCH 
graph_builder.add_edge(START , end_key= "bing_search")    # FIRST FOUR PARALLEL SEARCH 
graph_builder.add_edge(START , end_key= "youtube_search")  
graph_builder.add_edge(START , end_key= "instagram_search") 

# it searches the user info abt what his request at parallel b/t this
# connecting the next step "graph_builder"."add_edge" = add_edge is an connection function and graph_builder is and operation for connecting the nodes  

graph_builder.add_edge(start_key="google_search", end_key="brave_analysis")
graph_builder.add_edge(start_key="bing_search", end_key="brave_analysis")    # CONNECTED ALL ANALYSIS WITH BRAVE SEARCH NODE 
graph_builder.add_edge(start_key="youtube_search", end_key="brave_analysis")   
graph_builder.add_edge(start_key="instagram_search", end_key="brave_analysis")  
graph_builder.add_edge(start_key="analysis_brave_results", end_key="retrive_brave_results")

# after retriving the brave result we are gonna analysis all of our results 

graph_builder.add_edge(start_key="retrive_brave_results", end_key="analysis_google_results")
graph_builder.add_edge(start_key="retrive_brave_results", end_key="analysis_bing_results")
graph_builder.add_edge(start_key="retrive_brave_results", end_key="analysis_brave_results")
graph_builder.add_edge(start_key="retrive_brave_results", end_key="analysis_youtube_results")
graph_builder.add_edge(start_key="retrive_brave_results", end_key="analysis_instagram_results")

# after analysising all the results we are goona synthesis all analysis
graph_builder.add_edge(start_key="analysis_google_results", end_key="synthesis_analysis")
graph_builder.add_edge(start_key="analysis_bing_results", end_key="synthesis_analysis")   # SYNTHESISING ALL THE NODES RESULTS 
graph_builder.add_edge(start_key="analysis_brave_results", end_key="synthesis_analysis")
graph_builder.add_edge(start_key="analysis_youtube_results", end_key="synthesis_analysis")
graph_builder.add_edge(start_key="analysis_instagram_results", end_key="synthesis_analysis")

# after synthesising all the results 

graph_builder.add_edge("synthesis_analysis", END)  # Because LangGraph's add_edge() does NOT accept keyword arguments like start_key= or end_key=.

 #It accepts positional arguments only:
# graph is equal to graph and this will excute all the results 
# we are going to pass a messages it will search through allover the nodes at parallel state and it will that state 
graph = graph_builder.compile()  

def run_loise():
    print("LOISE-AGENT YOUR PERSONAL HELPER SIR ")
    print("type 'exit to quite\n'")

while True:
    user_input = input(" What can i help you sir ")
    if user_input.lower() == "exit":
        print(" Have a good day sir ")
        break

    state = {
        "message": [{"role":"user","content":user_input}],
        "user_questions": user_input,
        "google_results": None ,
        "brave_results": None ,
        "bing_results": None ,
        "youtube_results": None ,
        "instagram_results": None ,
        "instagram_post_data": None ,
        "google_analysis": None ,
        "brave_analysis": None ,
        "youtube_analysis": None ,
        "instagram_analysis": None ,
        "bing_analysis": None ,
        "final_anyalsis": None ,
    }

    print("\n Starting parallel research process....")
    print("Launching Google , Brave , Bing ,Instagram searching ....\n")
    final_state = graph.invoke(State) # using invoke functions to use one shot call means it "It sends the input → waits → returns the output."
    # no synchoronous in invoke "Just a plain, blocking, one-shot call"
    if final_state.get("final answer"):
        print(f"\nFinal answer:\n{final_state.get(final_state)}\n")
    print("-" * 80 ) # for seaprations here b/w what is appearing 

if __name__ == "__main__":
    run_loise()