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
from typing import List
from typing import Dict

from smolagents import LiteLLMModel
from research_agent import ResearchAgent
from smolagents import GradioUI

from entities import ShortTermMemory, LongTermMemory
from repositories.memory_repository import MemoryRepository
from tools.dex_screener_tool import dex_screener_api
from tools.coin_price_tool import coin_price_api
from tools.solana_tool import solana_payment_tool


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
        tools=[coin_price_api, dex_screener_api, solana_payment_tool],
        model=model,
        add_base_tools=True,
        short_term_memory=short_term_memory,
        long_term_memory=long_term_memory,
    )
    answer = agent.run(task)
    repository.add_short_term_memory(
        user_id, conversation_id, ShortTermMemory(task=(task), result=str(answer))
    )
    repository.add_long_term_memory(user_id, LongTermMemory(content=str(answer)))
    return answer


async def research():
    repository = MemoryRepository()
    questions = [
        "What is the market cap of ethereum rn?",
        "What is the price of bitcoin rn?",
        "Which one to buy?",
    ]
    for question in questions:
        await execute(
            repository,
            "123",
            "123",
            question,
        )


if __name__ == "__main__":
    asyncio.run(research())
