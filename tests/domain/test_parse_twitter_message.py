from domain import parse_twitter_message


def test_empty():
    assert not parse_twitter_message.execute(None)
    assert not parse_twitter_message.execute("")


def test_no_payment():
    assert not parse_twitter_message.execute(
        "How long should I hold my ETH portfolio before selling? "
    )


def test_valid_signature_without_solscan():
    msg = "How long should I hold my ETH portfolio before selling? 5aqB4BGzQyFybjvKBjdcP8KAstZo81ooUZnf64vSbLLWbUqNSGgXWaGHNteiK2EJrjTmDKdLYHamJpdQBFevWuvy"
    result = parse_twitter_message.execute(msg)
    assert result.task == "How long should I hold my ETH portfolio before selling?"
    assert (
        result.payment_signature
        == "5aqB4BGzQyFybjvKBjdcP8KAstZo81ooUZnf64vSbLLWbUqNSGgXWaGHNteiK2EJrjTmDKdLYHamJpdQBFevWuvy"
    )


def test_valid_signature_before_task():
    msg = "5aqB4BGzQyFybjvKBjdcP8KAstZo81ooUZnf64vSbLLWbUqNSGgXWaGHNteiK2EJrjTmDKdLYHamJpdQBFevWuvy How long should I hold my ETH portfolio before selling?"
    result = parse_twitter_message.execute(msg)
    assert result.task == "How long should I hold my ETH portfolio before selling?"
    assert (
        result.payment_signature
        == "5aqB4BGzQyFybjvKBjdcP8KAstZo81ooUZnf64vSbLLWbUqNSGgXWaGHNteiK2EJrjTmDKdLYHamJpdQBFevWuvy"
    )


def test_valid_signature_with_solscan():
    msg = "How long should I hold my ETH portfolio before selling? https://solscan.io/tx/5aqB4BGzQyFybjvKBjdcP8KAstZo81ooUZnf64vSbLLWbUqNSGgXWaGHNteiK2EJrjTmDKdLYHamJpdQBFevWuvy"
    result = parse_twitter_message.execute(msg)
    assert result.task == "How long should I hold my ETH portfolio before selling?"
    assert (
        result.payment_signature
        == "5aqB4BGzQyFybjvKBjdcP8KAstZo81ooUZnf64vSbLLWbUqNSGgXWaGHNteiK2EJrjTmDKdLYHamJpdQBFevWuvy"
    )
