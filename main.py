"""
Token Research Agent

* given SOL tokens on the Solana mainnet does research
    * agent checks for SOL transfer
    * after SOL received executes the task
    * after task executed posts the proof (signed hash of (question + answer))
* is a full degen trader focused on meme coins, no utility tokens
* fetches coin info from coingecko
* short term memory about user current session
* long term memory about user previous sessions and favourite coins, trades etc...
* RAG system to cache previous coin researches

"""
import asyncio
import os

from smolagents import DuckDuckGoSearchTool
from smolagents import LiteLLMModel
from smolagents import CodeAgent
from smolagents import tool


@tool
def coin_price_tool(task: str) -> str:
    """
    This is a tool that returns the price of given crypto token.
    It returns the price as float formatted as str.

    Args:
        task: The name of the token.
    """
    return "123.45"  # TODO: sometimes crypto is volatile and price may change


# TODO: this API seems to break the Agent loop?
# TODO: tried to format the results as simple string output
@tool
def dex_screener_api(task: str) -> str:
    """
    Get the latest token profiles. Returns the results as a big chunk of text with
    the chain, token address and the description of the Token.
    Args:
         task: empty
    """
    import requests

    response = requests.get(
        "https://api.dexscreener.com/token-profiles/latest/v1",
        headers={},
    )
    data = response.json()
    result = ""
    for token in data:
        try:
            d = "Chain: " + token["chainId"]
            d += ", tokenAddress: " + token["tokenAddress"]
            d += ", description: " + token["description"]
            for link in token["links"]:
                d += f', {link["type"]}: {link["url"]}'
            result += d + "\n"
        except:
            pass
    return result


async def main():
    model = LiteLLMModel(
        model_id="openai/gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    search_tool = DuckDuckGoSearchTool()
    agent = CodeAgent(tools=[search_tool, coin_price_tool, dex_screener_api], model=model,
                      add_base_tools=True)
    agent.run("Give me the latest token profiles?")


if __name__ == '__main__':
    asyncio.run(main())


