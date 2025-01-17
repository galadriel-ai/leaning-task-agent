from smolagents import tool


@tool
def coin_price_api(task: str) -> str:
    """
    This is a tool that returns the price of given crypto token.
    It returns the price as float formatted as str.

    Args:
        task: The name of the token.
    """
    return "123.45"  # TODO: sometimes crypto is volatile and price may change
