import argparse

from domain import parse_twitter_message
from tools import solana_tool

AGENT_WALLET_ADDRESS = "5RYHzQuknP2viQjYzP27wXVWKeaxonZgMBPQA86GV92t"


def execute(
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
        # TODO: call out agent now after payment has been validated


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
    execute(
        user_id=args.user_id,
        conversation_id=args.conversation_id,
        twitter_message=args.twitter_message,
    )
