# ============================================
# STEP 1: import necessary modules and classes 
# ============================================
from pydantic import BaseModel, Field
from agents import Agent, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True) # Load environment variables from .env file, overriding existing ones if necessary

# Set up the Nemotron model and client for the Writer Agent
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
openai_api_key = os.getenv('NVIDIA_API_KEY_1')
openai_client = AsyncOpenAI(base_url=NVIDIA_BASE_URL, api_key=openai_api_key)
nemotron_model_550b = OpenAIChatCompletionsModel(model="nvidia/nemotron-3-ultra-550b-a55b", openai_client=openai_client)
oss_big_model = OpenAIChatCompletionsModel(model="openai/gpt-oss-120b", openai_client=openai_client)

INSTRUCTIONS = """
You are a senior researcher tasked with writing a cohesive report for a research query.
You will be provided with the original query, and some research.
Generate a comprehensive report based on the research and the query.
The final output should be in markdown format, and it should be lengthy and detailed. Aim 
for 5-10 pages of content, at least 1000 words.
"""

# =================================================================================================================
# STEP 2: Define the data model for the report data, which will be used to structure the output of the writer agent
# =================================================================================================================
class ReportData(BaseModel):
    short_summary: str = Field(description="A short 2-3 sentence summary of the findings.")
    markdown_report: str = Field(description="The final report")
    follow_up_questions: list[str] = Field(description="Suggested topics to research further")


# =======================================================================================
# STEP 3: Create the Writer Agent with the specified instructions, model, and output type
# =======================================================================================
writer_agent = Agent(
    name="Writer Agent", 
    instructions=INSTRUCTIONS, 
    model=oss_big_model,
    output_type=ReportData)
