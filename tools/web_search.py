"""
Custom Web Search Tool for the OpenAI Agents SDK.

Compatible with:

- Gemini
- DeepSeek
- Claude
- Qwen
- Llama
- OpenAI-compatible endpoints

Uses Tavily Search API.
"""

import os

from tavily import TavilyClient

from agents import function_tool

# Create the Tavily client once.
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@function_tool
def web_search(query: str) -> str:
    """
    Search the web and return a concise text summary.

    Parameters
    ----------
    query : str
        Search query.

    Returns
    -------
    str
        Formatted search results for the LLM.
    """

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=5,
        include_answer=True,
        include_raw_content=False,
        include_images=False,
    )

    output = []

    if response.get("answer"):
        output.append(f"Summary:\n{response['answer']}\n")

    output.append("Sources:\n")

    for index, result in enumerate(response["results"], start=1):

        output.append(
            f"""
        {index}.
        Title: {result['title']}
        URL: {result['url']}
        Content:
        {result['content']}
        """
                )

    return "\n".join(output)