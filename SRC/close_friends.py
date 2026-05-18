import json
import logging
import time
from pathlib import Path
from typing import List

from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired

from config import (
    USERNAME,
    PASSWORD,
    TARGET,
    SESSION_FILE,
    LOG_DIR,
    LOG_LEVEL,
    BATCH_SIZE,
    REQUEST_DELAY_SECONDS,
)


def setup_logging() -> logging.Logger:
    log_path = Path(LOG_DIR)
    log_path.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("close_friends_bot")
    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S"
        )

        file_handler = logging.FileHandler(log_path / "close_friends.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


def load_client_session(client: Client, session_file: str, logger: logging.Logger) -> bool:
    session_path = Path(session_file)
    if not session_path.exists():
        logger.info("Session file not found (%s). A fresh login will be used.", session_file)
        return False

    try:
        with session_path.open("r", encoding="utf-8") as fh:
            session_data = json.load(fh)
        client.set_settings(session_data)
        logger.info("Session settings loaded from %s.", session_file)
        return True
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Unable to load session settings file: %s", exc)
        return False


def save_client_session(client: Client, session_file: str, logger: logging.Logger) -> None:
    session_path = Path(session_file)
    session_path.parent.mkdir(parents=True, exist_ok=True)
    with session_path.open("w", encoding="utf-8") as fh:
        json.dump(client.get_settings(), fh, indent=4)
    logger.info("Session settings persisted to %s.", session_file)


def authenticate(client: Client, logger: logging.Logger) -> None:
    had_saved_session = load_client_session(client, SESSION_FILE, logger)

    try:
        if had_saved_session:
            client.login(USERNAME, PASSWORD)
            logger.info("Authenticated using restored session.")
        else:
            raise LoginRequired("No reusable session found")
    except (LoginRequired, ChallengeRequired, Exception) as exc:
        logger.warning("Session login failed (%s). Trying credential login.", exc)
        client.login(USERNAME, PASSWORD)
        logger.info("Authenticated using username/password.")

    save_client_session(client, SESSION_FILE, logger)


def extract_follower_ids(client: Client, target_username: str, logger: logging.Logger) -> List[int]:
    logger.info("Resolving target user '%s'...", target_username)
    target_user_id = client.user_id_from_username(target_username)
    logger.info("Fetching followers for target id %s...", target_user_id)

    followers = client.user_followers(target_user_id, amount=0)
    follower_ids = list(followers.keys())
    logger.info("Extracted %d followers from @%s.", len(follower_ids), target_username)
    return follower_ids


def add_close_friends_in_batches(client: Client, follower_ids: List[int], logger: logging.Logger) -> None:
    if not follower_ids:
        logger.warning("No followers found. Skipping close-friends update.")
        return

    total = len(follower_ids)
    logger.info("Starting mass-add loop for %d users in batches of %d.", total, BATCH_SIZE)

    for index in range(0, total, BATCH_SIZE):
        batch = follower_ids[index : index + BATCH_SIZE]
        start = index + 1
        end = min(index + len(batch), total)

        logger.info("Adding close-friends batch %d-%d of %d...", start, end, total)
        client.private_request("friendships/set_besties/", {"add": ",".join(map(str, batch))})
        logger.info("Batch %d-%d completed.", start, end)
        time.sleep(REQUEST_DELAY_SECONDS)

    logger.info("Mass-add loop completed successfully.")


def main() -> None:
    logger = setup_logging()
    logger.info("Instagram Close Friends BOT started.")

    if not USERNAME or not PASSWORD:
        logger.error("Please set IG_USERNAME and IG_PASSWORD in the .env file before running.")
        return

    if not TARGET:
        logger.error("Please set IG_TARGET in the .env file before running.")
        return

    client = Client()
    authenticate(client, logger)

    target = TARGET.lstrip("@")
    follower_ids = extract_follower_ids(client, target, logger)
    add_close_friends_in_batches(client, follower_ids, logger)

    save_client_session(client, SESSION_FILE, logger)
    logger.info("Run finished.")


if __name__ == "__main__":
    main()
