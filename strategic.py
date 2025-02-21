import os

# Set environment variables
os.environ['OPENAI_API_KEY'] = 'fake-key'
os.environ['OPENAI_MODEL_NAME'] = 'llama3.2'
os.environ['OPENAI_BASE_URL'] = 'http://localhost:11434/v1'

# Now you can access these environment variables in your Python code
api_key = os.getenv('OPENAI_API_KEY')
model_name = os.getenv('OPENAI_MODEL_NAME')
base_url = os.getenv('OPENAI_BASE_URL')

# Example usage (you can use these variables as per your requirements)
print(f"API Key: {api_key}")
print(f"Model Name: {model_name}")
print(f"Base URL: {base_url}")

from duckduckgo_search import DDGS
from swarm import Swarm, Agent
from datetime import datetime

current_date = datetime.now().strftime("%Y-%m")

# Initialize Swarm client
client = Swarm()

# 1. Create Internet Search Tool

def get_news_articles(topic, **kwargs):
    print(f"Running DuckDuckGo news search for {topic}...")

    # DuckDuckGo search
    ddg_api = DDGS()
    results = ddg_api.text(f"{topic} {current_date}", max_results=7)
    
    if results:
        news_results = "\n\n".join([f"Title: {result['title']}\nURL: {result['href']}\nDescription: {result['body']}" for result in results])
        print(news_results)
        return news_results
    else:
        return f"Could not find news results for {topic}."


   
# 2. Create AI Agents

# News Agent to fetch news
news_agent = Agent(
    name="News Assistant",
    instructions="You provide the latest news articles for a given topic using DuckDuckGo search.",
    functions=[get_news_articles],
    model="llama3.2"
)

# Strategic Analysis Agent to perform analysis
analysis_agent = Agent(
    name="Strategic Analysis Assistant",
    instructions="Perform an international strategic analysis for the given topic. Analyze geopolitical, economic, and social factors in detail.",
    model="llama3.2"
)

# 3. Create workflow

def run_news_workflow(region):
    print("Running News Agent workflow...")
    
    # Step 1: Fetch news
    news_response = client.run(
        agent=news_agent,
        messages=[{"role": "user", "content": f"Get me the news about {region} on {current_date}"}],
    )
    
    raw_news = news_response.messages[-1]["content"]
    
    # Step 2: Pass news to strategic analysis agent for evaluation
    analysis_response = client.run(
        agent=analysis_agent,
        messages=[{"role": "user", "content": raw_news}],
    )
    
    return analysis_response.messages[-1]["content"]

# Example of running the news workflow for a given region
print(run_news_workflow("bitcoin"))
