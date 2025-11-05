import argparse
import datetime
import logging
import sys

import dateutil.parser

logger = logging.getLogger(__name__)


def format_duration(td: datetime.timedelta) -> str:
    """Format timedelta as XdXhXm without seconds."""
    total_seconds = int(td.total_seconds())

    days = total_seconds // 86400
    remaining = total_seconds % 86400
    hours = remaining // 3600
    remaining %= 3600
    minutes = remaining // 60

    parts: list[str] = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")

    return "".join(parts) if parts else "0m"


def durationsince() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate duration since a given time"
    )
    _ = parser.add_argument("time_str", help="Time to calculate duration from")
    _ = parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (-v, -vv, -vvv)",
    )

    args = parser.parse_args()

    log_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level: int = log_levels[min(args.verbose, len(log_levels) - 1)]
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    time_str: str = args.time_str

    try:
        now = datetime.datetime.now(tz=datetime.UTC).astimezone()
        parsed_time = dateutil.parser.parse(
            time_str,
            default=now.replace(hour=0, minute=0, second=0, microsecond=0),
        )

        if parsed_time.tzinfo is None:
            parsed_time = parsed_time.replace(tzinfo=now.tzinfo)

        if parsed_time > now:
            parsed_time -= datetime.timedelta(days=1)

        duration = now - parsed_time
        formatted = format_duration(duration)

        logger.debug("Parsing time string: %s", time_str)
        logger.debug("Parsed time: %s", parsed_time)
        logger.debug("Current time: %s", now)
        logger.debug("Duration: %s", duration)

    except Exception:
        logger.exception("Error parsing time")
        sys.exit(1)

    print(formatted)


def durationtill() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate duration until a given time"
    )
    _ = parser.add_argument("time_str", help="Time to calculate duration until")
    _ = parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (-v, -vv, -vvv)",
    )

    args = parser.parse_args()

    log_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level: int = log_levels[min(args.verbose, len(log_levels) - 1)]
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    time_str: str = args.time_str

    try:
        now = datetime.datetime.now(tz=datetime.UTC).astimezone()
        parsed_time = dateutil.parser.parse(
            time_str,
            default=now.replace(hour=0, minute=0, second=0, microsecond=0),
        )

        if parsed_time.tzinfo is None:
            parsed_time = parsed_time.replace(tzinfo=now.tzinfo)

        if parsed_time < now:
            parsed_time += datetime.timedelta(days=1)

        duration = parsed_time - now
        formatted = format_duration(duration)

        logger.debug("Parsing time string: %s", time_str)
        logger.debug("Parsed time: %s", parsed_time)
        logger.debug("Current time: %s", now)
        logger.debug("Duration: %s", duration)

    except Exception:
        logger.exception("Error parsing time")
        sys.exit(1)

    print(formatted)


def list_commands() -> None:
    """List all available commands."""
    parser = argparse.ArgumentParser(
        description="jumpingjay - Calculate time durations",
        epilog="Available commands: durationsince, durationtill",
    )
    _ = parser.add_argument(
        "--list",
        action="store_true",
        help="List available commands",
    )

    args = parser.parse_args()

    if args.list:
        print("durationsince")
        print("durationtill")
    else:
        parser.print_help()


def main() -> None:
    durationsince()


if __name__ == "__main__":
    main()
