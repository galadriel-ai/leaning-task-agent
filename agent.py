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

from smolagents import LiteLLMModel
from research_agent import ResearchAgent

from dependencies import get_memory_repository
from entities import ShortTermMemory
from repositories.memory_repository import MemoryRepository
from tools.dex_screener_tool import dex_screener_api
from tools.coin_price_tool import coin_price_api
from tools.memory_tool import update_long_term_memory


# TODO: basic interface for now
async def execute(
    repository: MemoryRepository,
    user_id: str,
    conversation_id: str,
    task: str,
) -> str:
    model = LiteLLMModel(
        model_id="openai/gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    short_term_memory = repository.get_short_term_memory(user_id, conversation_id)
    long_term_memory = repository.query_long_term_memory(user_id, task)
    agent = ResearchAgent(
        tools=[
            coin_price_api,
            dex_screener_api,
        ],
        model=model,
        add_base_tools=True,
        short_term_memory=short_term_memory,
        long_term_memory=long_term_memory,
    )
    answer = agent.run(task)
    memory = ShortTermMemory(task=(task), result=str(answer))
    repository.add_short_term_memory(user_id, conversation_id, memory)
    update_long_term_memory(repository, user_id, memory)
    return answer


async def research():
    repository = get_memory_repository()
    questions = [
        "What is the market cap of ethereum rn?",
        "What is the price of bitcoin rn?",
        "I prefer bitcoin over ethereum",
        "Which one to buy?",
    ]
    for question in questions:
        await execute(
            repository,
            "123",
            "123",
            question,
        )
    questions = [
        "What is the market cap of ethereum rn?",
        "What is the price of bitcoin rn?",
        "Which one to buy?",
    ]
    for question in questions:
        await execute(
            repository,
            "123",
            "125",
            question,
        )


if __name__ == "__main__":
    asyncio.run(research())
