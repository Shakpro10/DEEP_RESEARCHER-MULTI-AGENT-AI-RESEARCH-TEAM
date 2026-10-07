# ============================================
# STEP 1: import necessary modules and classes
# ============================================
from pydantic import BaseModel, Field
from agents import Agent, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True) # Load environment variables from .env file, overriding existing ones if necessary

NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1" # Base URL for NVIDIA's API, used for making requests to the OpenAI-compatible endpoints
openai_api_key = os.getenv('NVIDIA_API_KEY_1') # Retrieve the NVIDIA API key from environment variables for authentication with the OpenAI-compatible endpoints
openai_client = AsyncOpenAI(base_url=NVIDIA_BASE_URL, api_key=openai_api_key) # Create an instance of the AsyncOpenAI client with the specified base URL and API key, allowing for asynchronous interactions with the OpenAI-compatible endpoints
nemotron_model_120b =  OpenAIChatCompletionsModel(
    model="nvidia/nemotron-3-super-120b-a12b", 
    openai_client=openai_client) # Instantiate OpenAIChatCompletionsModel with the model name and AsyncOpenAI client to use Nemotron 3 Super 120B A12B for chat completions.

HOW_MANY_SEARCHES = int(os.getenv("HOW_MANY_SEARCHES", 5)) # Retrieve the number of web searches to perform from environment variables, defaulting to 5 if not set. This value is used in the instructions for the planner agent to determine how many search terms to generate for a given user query.


INSTRUCTIONS = f"""
You are a research assistant. Given a user query, come up with a set of web searches
to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for.
"""

# ========================================================================================================================================================
# STEP 2: Define the data models for the web search items and the overall web search plan, which will be used to structure the output of the planner agent
# ========================================================================================================================================================
class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to the query.")
    query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")

# ========================================================================================
# STEP 3: Create the Planner Agent with the specified instructions, model, and output type
# ========================================================================================   
planner_agent = Agent(
    name="Planner Agent", 
    instructions=INSTRUCTIONS, 
    model=nemotron_model_120b, 
    output_type=WebSearchPlan)
