#!/usr/bin/env python3

import argparse
import enum
import logging
import sched
import subprocess
import time

from typing import Any, Dict


SECOND = 1


class SessionType(enum.Enum):
    ACTIVITY = "ACTIVITY"
    REST = "REST"


def noop():
    return


def say(s: str) -> None:
    logging.debug("say %s", s)
    subprocess.Popen(["say", "-v", "Daniel", s])


def interval(type: SessionType, length: int, notify: int = 5) -> None:
    s = sched.scheduler()
    s.enter(0, 0, say, argument=(f"Begin {type.value}",))

    # Notification begins after `notify_at` seconds.
    notify_at = length - notify

    # Subtract some time because we don't want the "{type.value} ends in" output
    # to overlap into the count down.
    s.enter(notify_at - 1.5, 1, say, argument=(f"{type.value} ends in",))

    for i in range(notify):
        s.enter(notify_at + i, i, say, argument=(f"{notify - i}",))

    # So we're blocking for `length` seconds.
    s.enter(length, 1, noop)

    s.run(blocking=True)


def tabata_session(cycles=8) -> None:
    logging.info("Begin Tabata session")

    cycle = 1
    while cycle <= cycles:
        logging.info("Round %s of %s", cycle, cycles)
        interval(SessionType.ACTIVITY, 20)

        if cycle < cycles:
            interval(SessionType.REST, 10)

        cycle += 1

    logging.info("End Tabata session")

    say("End Tabata session")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--countdown", action="store", type=int, default=0)
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

    if args.countdown > 0:
        say(f"Session begins in {args.countdown} seconds")
        time.sleep(args.countdown)

    tabata_session(args.rounds)
