import argparse
import asyncio

import agent
from domain import parse_twitter_message
from domain import post_proof
from domain.entities import TwitterMessage
from repositories.memory_repository import MemoryRepository
from tools import solana_tool

AGENT_WALLET_ADDRESS = "5RYHzQuknP2viQjYzP27wXVWKeaxonZgMBPQA86GV92t"


async def execute(
    user_id: str,
    conversation_id: str,
    twitter_message: str,
):
    twitter_message = parse_twitter_message.execute(twitter_message)
    print("Twitter_message:", twitter_message)
    if twitter_message:
        is_payment_valid = solana_tool.solana_payment_tool(
            signature=twitter_message.payment_signature,
            wallet_address=AGENT_WALLET_ADDRESS,
        )
        print("is_payment_valid:", is_payment_valid)
        # call out agent now after payment has been validated
        repository = MemoryRepository()
        if not repository.add_payment_signature(
            twitter_message.payment_signature, twitter_message.task
        ):
            print("ERROR: Payment has been already used!")
            return
        answer = await agent.execute(
            repository, user_id, conversation_id, twitter_message.task
        )
        _post_proof(twitter_message, answer)


def _post_proof(twitter_message: TwitterMessage, answer: str):
    request = {"task": twitter_message.task}
    response = {"answer": answer}
    print("\nPosting proof:")
    print("  request:", request)
    print("  response:", response)
    post_proof.execute(request, response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--user_id", help="User ID (either user_id or email required)", required=True
    )
    parser.add_argument(
        "--conversation_id", help="Twitter conversation ID", required=True
    )
    parser.add_argument(
        "--twitter_message",
        help="Twitter message with the task the Agent needs to solve",
        required=True,
    )
    args = parser.parse_args()

    asyncio.run(
        execute(
            user_id=args.user_id,
            conversation_id=args.conversation_id,
            twitter_message=args.twitter_message,
        )
    )
