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


def format_time(future_time: datetime.datetime, time_format: str) -> str:
    """Format time based on the specified format."""
    if time_format == "am/pm":
        return future_time.strftime("%I:%M %p")
    return future_time.strftime("%H:%M")


def durationsince() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate duration since a given time",
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
        description="Calculate duration until a given time",
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


def at() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate the time at a given duration from now",
    )
    _ = parser.add_argument(
        "duration_str", help="Duration from now (e.g., 8h2m, 2d, 30m)",
    )
    _ = parser.add_argument(
        "-f",
        "--format",
        choices=["24h", "am/pm"],
        default="am/pm",
        help="Time format (default: am/pm)",
    )
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

    duration_str: str = args.duration_str
    time_format: str = args.format

    try:
        now = datetime.datetime.now(tz=datetime.UTC).astimezone()
        parsed_duration = dateutil.parser.parse(
            f"1970-01-01 {duration_str}",
            default=datetime.datetime(1970, 1, 1),
        )

        duration_obj = parsed_duration - datetime.datetime(
            1970, 1, 1, tzinfo=parsed_duration.tzinfo,
        )
        future_time = now + duration_obj
        formatted_time = format_time(future_time, time_format)

        logger.debug("Parsing duration string: %s", duration_str)
        logger.debug("Parsed duration: %s", duration_obj)
        logger.debug("Current time: %s", now)
        logger.debug("Future time: %s", future_time)
        logger.debug("Time format: %s", time_format)

    except Exception:
        logger.exception("Error parsing duration")
        sys.exit(1)

    print(formatted_time)


def list_commands() -> None:
    """List all available commands."""
    parser = argparse.ArgumentParser(
        description="jumpingjay - Calculate time durations",
        epilog="Available commands: durationsince, durationtill, at",
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
        print("at")
    else:
        parser.print_help()


def main() -> None:
    durationsince()


if __name__ == "__main__":
    main()
