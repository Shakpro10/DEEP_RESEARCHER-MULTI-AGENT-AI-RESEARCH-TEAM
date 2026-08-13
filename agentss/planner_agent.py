from pydantic import BaseModel, Field
from agents import Agent, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)

NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
openai_api_key = os.getenv('NVIDIA_API_KEY_1')
openai_client = AsyncOpenAI(base_url=NVIDIA_BASE_URL, api_key=openai_api_key)
nemotron_model_120b =  OpenAIChatCompletionsModel(
    model="nvidia/nemotron-3-super-120b-a12b", 
    openai_client=openai_client)

HOW_MANY_SEARCHES = int(os.getenv("HOW_MANY_SEARCHES", 5))


INSTRUCTIONS = f"""
You are a research assistant. Given a user query, come up with a set of web searches
to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for.
"""

class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to the query.")
    query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")
    
planner_agent = Agent(
    name="Planner Agent", 
    instructions=INSTRUCTIONS, 
    model=nemotron_model_120b, 
    output_type=WebSearchPlan)