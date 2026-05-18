import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, call

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "SRC"))
sys.modules.setdefault(
    "dotenv", SimpleNamespace(load_dotenv=lambda *args, **kwargs: None)
)

import close_friends


def make_logger():
    logger = Mock()
    logger.warning = Mock()
    logger.info = Mock()
    logger.error = Mock()
    return logger


def test_add_close_friends_skips_empty_follower_list():
    client = Mock()
    logger = make_logger()

    close_friends.add_close_friends_in_batches(client, [], logger)

    client.private_request.assert_not_called()
    logger.warning.assert_called_once_with("No followers found. Skipping close-friends update.")


def test_add_close_friends_splits_followers_into_batches(monkeypatch):
    client = Mock()
    client.private_request.return_value = {"status": "ok"}
    logger = make_logger()
    sleep = Mock()
    monkeypatch.setattr(close_friends, "BATCH_SIZE", 2)
    monkeypatch.setattr(close_friends, "REQUEST_DELAY_SECONDS", 0)
    monkeypatch.setattr(close_friends.time, "sleep", sleep)

    close_friends.add_close_friends_in_batches(client, [101, 102, 103], logger)

    assert client.private_request.call_args_list == [
        call("friendships/set_besties/", {"add": "101,102"}),
        call("friendships/set_besties/", {"add": "103"}),
    ]
    assert sleep.call_count == 2
    logger.info.assert_any_call("Mass-add loop completed successfully.")


def test_add_close_friends_raises_when_any_batch_fails(monkeypatch):
    client = Mock()
    client.private_request.side_effect = [
        {"status": "ok"},
        {"status": "fail", "message": "rate limited"},
    ]
    logger = make_logger()
    monkeypatch.setattr(close_friends, "BATCH_SIZE", 2)
    monkeypatch.setattr(close_friends, "REQUEST_DELAY_SECONDS", 0)
    monkeypatch.setattr(close_friends.time, "sleep", Mock())

    with pytest.raises(RuntimeError, match="3-3"):
        close_friends.add_close_friends_in_batches(client, [101, 102, 103], logger)

    logger.error.assert_any_call(
        "Batch %d-%d failed: %s",
        3,
        3,
        {"status": "fail", "message": "rate limited"},
    )
    logger.error.assert_any_call(
        "Mass-add loop finished with %d failed batch(es): %s", 1, "3-3"
    )
    assert not any(
        logged_call.args == ("Mass-add loop completed successfully.",)
        for logged_call in logger.info.call_args_list
    )


def test_add_close_friends_rejects_non_positive_batch_size(monkeypatch):
    client = Mock()
    logger = make_logger()
    monkeypatch.setattr(close_friends, "BATCH_SIZE", 0)

    with pytest.raises(ValueError, match="BATCH_SIZE"):
        close_friends.add_close_friends_in_batches(client, [101], logger)

    client.private_request.assert_not_called()
