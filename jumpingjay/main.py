import datetime
import logging

import click
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


@click.command()
@click.argument("time_str")
@click.option("-v", "--verbose", count=True, help="Increase verbosity (-v, -vv, -vvv)")
def durationsince(time_str: str, verbose: int) -> None:
    """Calculate duration since a given time."""
    log_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = log_levels[min(verbose, len(log_levels) - 1)]
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    logger.debug("Parsing time string: %s", time_str)

    try:
        now = datetime.datetime.now(tz=datetime.UTC).astimezone()
        parsed_time = dateutil.parser.parse(
            time_str,
            default=now.replace(hour=0, minute=0, second=0, microsecond=0),
        )

        if parsed_time.tzinfo is None:
            parsed_time = parsed_time.replace(tzinfo=now.tzinfo)

        if parsed_time > now:
            logger.debug("Parsed time is in the future, assuming it was yesterday")
            parsed_time -= datetime.timedelta(days=1)

        logger.debug("Parsed time: %s", parsed_time)
        logger.debug("Current time: %s", now)

        duration = now - parsed_time
        logger.debug("Duration: %s", duration)

        formatted = format_duration(duration)
        click.echo(formatted)

    except Exception as e:
        logger.exception("Error parsing time: %s", e)
        raise click.Abort from e


def main() -> None:
    durationsince()


if __name__ == "__main__":
    main()
