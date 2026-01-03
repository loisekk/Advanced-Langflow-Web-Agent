from dotenv import load_dotenv
import os
import requests  # Sending HTTP GET requests (to fetch data) overall to communicate with websites or an apis
from urllib.parse import quote_plus # it is allow us to turn a normal string into a string that 
# we would include in a query params in our url which we will see in a minute 
from snapshot_operations import download_snapshot, poll_snapshot_status
load_dotenv()
dataset_id ="sd_miiulq1fw66gwqi8e" # snapshot_id 

def _make_api_request(url,**kwargs): # url is a required params.
                                     # **kwargs collects any additional keyword arguments into a dictionary.
    api_key =os.getenv("BRIGHTDATA_API_KEY")
 # used the header type fuctions to tell who we are like the author or user 
    headers = {
        "Authorization":f"Bearer {api_key}", # used personal api_key , # for the bearer token with transfering using the key it checks your are valid or not 
        "Content-type":"application/json", # using json to format the data 
    }

# "Bearer" You are sending a Bearer Token for authentication

# A Bearer Token is a type of access token.
# It tells the server:
# “This request is from someone who has this token, so allow access.”
# No username/password needed — just the token.

# " json "
# The server sees your header and understands:

# “The body of this request is JSON. I should read it as JSON.”

    try:
       response = requests.post(url, headers=headers,**kwargs)
       response.raise_for_status()
       return response.json()
        
        # it is releated to the network requests 
    except requests.exceptions.RequestException as e:
        print(f"API requests failed : {e}")
        return None
       # if it's not releated to the network requests then we deal with it here through "Unknown error"
    except Exception as e:
        print(f"Unknown error : {e}")
        return None

def serp_search(query, engine = "google"): # to  allows search any search engine that "BRIGHT_DATA" supports.
   if engine == "google":
       base_url = "https://www.google.com/search"
   elif engine == "bing":
       base_url = "https://www.bing.com/search"
   else:
       raise ValueError(f"Unknown engine {engine}") # whatever engine you passed 
   
   url = "https://api.brightdata.com/requests" # the correct end point must be use in "s" like plural unless brightdata will reject the request 

   payload = {
       "zone" : "loise",
       "url" : f"{base_url}?q={quote_plus(query)}&brd_json=1",
       "format":"raw"
   }

   full_response =_make_api_request(url,json=payload )
   if not full_response:
       return None 
   # this will only pulls some the data which is care about and the all over data is on the bright data server 
   extracted_data = {
       "knowledge": full_response.get("knowledge",{}),
       "Organic": full_response.get("Organic",[]), # used Organic in form of List   

   }
   return extracted_data    # it's very scalable it runs as many tines as we wants smothly with different requests  

 # this whole function trigger and download the snapshot 
def _Trigger_and_Download_snapshot(trigger_url, params , data , operation_name = "operation"): 
    trigger_results = _make_api_request(trigger_url, params = params , json = data ) # giving parameter as params cause make_api_requests does not except the parameter arg .
    if not trigger_results :
        return None 
    
    snapshot_id = trigger_results.get("snapshot_id")
    if not snapshot_id:
        return None 
   
    if not poll_snapshot_status(snapshot_id):
        return None 
    
    raw_data = download_snapshot(snapshot_id)
    return raw_data
def reddit_search_api(keyword, date = "All time", sort_by ="Hot", num_of_post= 75):
    trigger_url = "https://api.brightdata.com/datasets/v3/trigger"


    params = {  # for brefelye search into reddit search to connect the api management 
        "dataset_id": "sd_miiulq1fw66gwqi8e", # snapshot_id 
        "include_errors" : "true",
        "type" : "Discover_new",
        "Discover_by": "keywords"
    }

    data = [ # diff parameter 
        {
         "keyword": keyword, # making space b/w the " " will reject the requests 
         "date" : date ,
         "sort_by" : sort_by,
         "num_of_post" : num_of_post,
    }
    ]
    raw_data = _Trigger_and_Download_snapshot(
        trigger_url , params , data , operation_name = "reddit"
    )

    if not raw_data :
        return None 
    
    parsed_data = []
    for post in raw_data:
        parsed_post = {
            "title" : post.get("title"),
            "url": post.get("url")
        }
        parsed_data.append(parsed_post) # this makes the functions returns after the FIRST post , "so it only get 1 post no extra stuff "
        return{"parsed_post" : parsed_data , "total_found" : len(parsed_data)}
    # NOW the next step after this would be to get the URLs from the parsed data 
    # then for further explore and then to downlaod all of the comments of all over the posts .

# " IT WILL CREATE THE ABILTIY TO GET ALL OF THE DIFFERENT , COMMENTS FOR A PARTICULAR POST  "

def reddit_post_retrieval(urls , days_back = 10 , load_all_replies = False , comment_limit = ""): # it will wrap up all the operations and it go back to "LANG GRAPH" 
    # and it will prompting with "LLM CALLS & PROMPTING " = " it will analyze all the data "
    if not urls : # if not passing the urls then it will return with none  
        return None 
    
    trigger_url = "https://api.brightdata.com/datasets/v3/trigger"

    params = {
        "dataset_id" :"",
        "include_errors" : "True"
    } 

    Data = [
        {  # creating all of this entries for all "urls " by this we get all over the comments by these url parameters 
            "url" :url ,
            "Days_back" : days_back ,
            "load_all_replies" : load_all_replies,
            "comment_limit" : comment_limit
        }
        for url in urls 
    ]

    raw_data = _Trigger_and_Download_snapshot(
        trigger_url , params , Data , operation_name= "reddit comments "
    )
    if not raw_data :
        return None 
    # and if having the raw_data then 
    parsed_comments = []
    for comment in raw_data :
        parsed_comment = { # putting allover the around stuff's in an single post or the comment's
            "comment_id" : comment.get("comment_id"),
            "content" : comment.get("comment"),
            "date" : comment.get("date_posted"),
            
        }
        parsed_comments.append(parsed_comment) # "parsed_comments" is a list which is store all over my "parsed_comment" which is "Dict_Type" 
        # and the append fun will add my dict into the mentioned list "putting the item in the box"

    return {"comments" : parsed_comments , "total_retrieved" : len(parsed_comments)}

# "COMMENTS" = will contain the list of all parsed comments . "the list of all comments"
# "TOTAL_RETRIEVED" = gives the number of all comments in your list ." how many comments were parsed" .

