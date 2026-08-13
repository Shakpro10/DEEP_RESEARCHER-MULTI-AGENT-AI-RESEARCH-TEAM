from agents import Agent, ModelSettings, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
from tools.web_search import web_search

import os

load_dotenv(override=True)

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
google_api_key = os.getenv('GOOGLE_API_KEY')
gemini_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)
gemini_model = OpenAIChatCompletionsModel(model="gemini-3.1-flash-lite", 
                                          openai_client=gemini_client)

INSTRUCTIONS = """
You are an expert research assistant.

Whenever the user asks about:

- current events
- recent AI models
- latest frameworks
- companies
- products
- statistics
- news
- anything requiring up-to-date information

ALWAYS use the web_search tool before answering.

When writing the response:

- Combine information from multiple sources.
- Remove duplicate information.
- Prefer recent information.
- Produce 2–3 concise summary of the results.
- Keep the response under 300 words.
- Capture the main points and be succinct.
- Never fabricate information.
"""

settings = ModelSettings(tool_choice="required")
tools = [web_search]

search_agent = Agent(    name="Search Agent", 
    instructions=INSTRUCTIONS, 
    tools=tools, 
    model=gemini_model, 
    model_settings=settings)