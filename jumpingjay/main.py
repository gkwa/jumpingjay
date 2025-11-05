import logging
import datetime
import click
import dateutil.parser

logger = logging.getLogger(__name__)


def format_duration(td: datetime.timedelta) -> str:
    """Format timedelta as XdXhXm without seconds."""
    total_seconds = int(td.total_seconds())
    
    days = total_seconds // 86400
    remaining = total_seconds % 86400
    hours = remaining // 3600
    remaining = remaining % 3600
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
@click.argument('time_str')
@click.option('-v', '--verbose', count=True, help='Increase verbosity (-v, -vv, -vvv)')
def durationsince(time_str: str, verbose: int) -> None:
    """Calculate duration since a given time."""
    log_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = log_levels[min(verbose, len(log_levels) - 1)]
    logging.basicConfig(level=level, format='%(levelname)s: %(message)s')
    
    logger.debug(f"Parsing time string: {time_str}")
    
    try:
        parsed_time = dateutil.parser.parse(time_str, default=datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
        now = datetime.datetime.now()
        
        if parsed_time > now:
            logger.debug("Parsed time is in the future, assuming it was yesterday")
            parsed_time = parsed_time - datetime.timedelta(days=1)
        
        logger.debug(f"Parsed time: {parsed_time}")
        logger.debug(f"Current time: {now}")
        
        duration = now - parsed_time
        logger.debug(f"Duration: {duration}")
        
        formatted = format_duration(duration)
        print(formatted)
        
    except Exception as e:
        logger.error(f"Error parsing time: {e}")
        raise click.Abort()


def main() -> None:
    durationsince()


if __name__ == "__main__":
    main()
