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

### TODO

* API

"""
import asyncio
import os

from smolagents import DuckDuckGoSearchTool
from smolagents import LiteLLMModel
from smolagents import CodeAgent
from smolagents import GradioUI

from tools.dex_screener_tool import dex_screener_api
from tools.coin_price_tool import coin_price_api


async def main():
    model = LiteLLMModel(
        model_id="openai/gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    search_tool = DuckDuckGoSearchTool()
    agent = CodeAgent(
        tools=[search_tool, coin_price_api, dex_screener_api],
        model=model,
        add_base_tools=True)
    agent.run("What is the market cap of ethereum rn?")
    # GradioUI(agent).launch()


if __name__ == '__main__':
    asyncio.run(main())
