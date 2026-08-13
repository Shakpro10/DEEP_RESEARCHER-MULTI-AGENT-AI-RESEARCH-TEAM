# ============================================
# STEP 1: import necessary modules and classes
# ============================================
from agents import Agent, function_tool, ModelSettings, OpenAIChatCompletionsModel
from tools.messenger import send_email, push
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True) # Load environment variables from .env file, overriding existing ones if necessary


NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1" # Base URL for NVIDIA's API, used for making requests to the OpenAI-compatible endpoints
openai_api_key = os.getenv('NVIDIA_API_KEY_1') # Retrieve the NVIDIA API key from environment variables for authentication with the OpenAI-compatible endpoints
openai_client = AsyncOpenAI(base_url=NVIDIA_BASE_URL, api_key=openai_api_key) # Create an instance of the AsyncOpenAI client with the specified base URL and API key, allowing for asynchronous interactions with the OpenAI-compatible endpoints
llama_model =  OpenAIChatCompletionsModel(model="meta/llama-3.3-70b-instruct", openai_client=openai_client) # Instantiate OpenAIChatCompletionsModel with the model name and AsyncOpenAI client to use LLaMA 3.3 70B Instruct for chat completions.

USE_EMAIL = os.getenv("USE_EMAIL", "true").lower() == "true" 

settings = ModelSettings(tool_choice="required") # Create an instance of ModelSettings with tool_choice set to "required", indicating that the model must use the provided tools for its operations.

# ==========================================
# STEP 2: Define the tool for sending emails
# ==========================================
@function_tool
def send_email_tool(subject: str, text_body: str, html_body: str) -> str:
    """
    Send out an email with the given subject and body
    
    Args:
        subject: The subject of the email
        text_body: The body of the email as plain text
        html_body: The HTML body of the email
    """
    if USE_EMAIL:
        send_email(subject, text_body, html_body)
    else:
        push(f"Subject: {subject}\n\n{text_body}")
    return "Email sent successfully"


INSTRUCTIONS = """
You are provided with a detailed report. Use your tool to send an email, converting the report into
a clean, well presented HTML email with an appropriate subject line.
"""

# ==========================================================================================
# STEP 3: Create the Email Agent with the specified instructions, tools, model, and settings
# ==========================================================================================
email_agent = Agent(
    name="Email Agent", 
    instructions=INSTRUCTIONS, 
    tools=[send_email_tool], 
    model=llama_model, 
    model_settings=settings)