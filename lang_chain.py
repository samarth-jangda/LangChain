# the following script is intended to search the asked query as per the 
# context being asked by the user

import argparse, requests, googlesearch, json, datetime
from langchain import LangChain

parser = argparse.ArgumentParser(description="Following arguments will be used to take action on user query as per its context",
                                 epilog="",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("--user-query", type=str, default="", required=True,
                    help="The following argument is the query being asked by the user")

parser.add_argument("--openai-api-key", type=str, default="", required=True,
                    help="Specify the api key of openai to be used te get the corresponding response")

parser.add_argument("--num-google-results", type=str, default="5", required=False,
                    help="Specify the maximun search results of the asked query from google")

parser.add_argument("--output-path", type=str, default="", required=True,
                    help="Path to save the response to the user query")

args=parser.parse_args()

lc=LangChain()

def gpt_answer(prompt_query):
    """
    
    """
    openai_api_key=args.openai_api_key
    url='https://api.openai.com/v1/engines/davinci-codex/completions'
    headers = {
        'Authorization': f'Bearer {openai_api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'query': prompt_query,
        'max_tokens': 150,
        'temperature': 0.85
    }
    
    response = requests.post(url,headers=headers, json=data)
    
def check_context(query=args.user_query):
    """
    The following function is used to check the context of the query being asked by the user 
    NOTE: Consider the following conditions
    1) If the sentiment is [-1] then it is a negative emotional question and will be send to gpt
    2) If the sentiment is [1] then it is a positive emotional question and will be send to gpt
    3) If the sentiment is [0] then it is a neutral question and will be send to google
    """
    # checking the context
    sentiment=lc.sentiment(query)
    if sentiment > 0.5 or sentiment < -0.5:
        print("The query is treated as a positive emotional query")
        return {"QueryType":"GPTQuery"}
    elif sentiment == 0.5 or sentiment == -0.5:
        print("The query is treated as both factual and emotional")
        return {"QueryType":"FirstGoogleLink"}
    elif sentiment == 0:
        print("The qeury is treated as factual or non-emotional")
        return {"QueryType":"GoogleQuery"}    
    
def answer_prompt(query=args.user_query, output_response=args.output_path):
    """
    The following function is used to answer the query asked by the user as per
    1) answer from google: If it is a factual question
    2) answer from gpt: If it is a emotional question
    3) hybrid answer: If it is both then scrape first link of google and asked from gpt
    """
    check_query_type=check_context(query=query)
    # case of gpt type query
    if check_query_type.get("QueryType") == "GPTQuery":
        response=gpt_answer(prompt_query=query)
    # case of google type query
    elif check_query_type.get("QueryType") == "GoogleQuery":
        search_google=googlesearch.search(query,num_results=args.num_google_results)
        response={}
        for res in search_google:
            response.append({'title':res.name, 'link':res.link})
            response[f'Response{query}':]={'title':res.name, 'link':res.link}
            result=json.dumps(response)
    current_time=datetime.datetime.now()
    with open(f"{output_response}/{current_time}.json", 'w', encoding='utf-8') as json_file:
        json.dump(response, json_file)
    return {"QueryResponse":response}