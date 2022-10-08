#!/usr/bin/env python3

import argparse
import enum
import logging
import subprocess
import time

from typing import Any, Dict


SECOND = 1


class SessionType(enum.Enum):
    ACTIVITY = "ACTIVITY"
    REST = "REST"


def say(s: str) -> None:
    logging.debug("say %s", s)
    subprocess.run(["say", s])


def session(type: SessionType, countdown: int, notify: int = 5) -> None:
    say(f"Begin {type.value}")
    i = countdown
    while i > 0:
        if i == notify:
            say(f"{type.value} ends in")

        if i <= notify:
            say(f"{i}")

        time.sleep(SECOND)
        i -= 1

    return


def tabata_session(rounds=8):
    logging.info("Begin Tabata session")

    round = 1
    while round <= rounds:
        logging.info("Round %s of %s", round, rounds)
        session(SessionType.ACTIVITY, 20)

        if round < rounds:
            session(SessionType.REST, 10)

        round += 1

    logging.info("End Tabata session")

    say("End Tabata session")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true", default=False)
    parser.add_argument("rounds", action="store", nargs="?", type=int, default=8)

    args = parser.parse_args()

    logging_kwargs: Dict[str, Any] = {
        "format": "%(asctime)s %(levelname)s %(message)s",
        "level": logging.INFO,
    }

    if args.debug:
        logging_kwargs["level"] = logging.DEBUG

    logging.basicConfig(**logging_kwargs)

    tabata_session(args.rounds)
