# jumpingjay

Calculate time durations from the command line.

## Installation

```bash
uvx --from git+https://github.com/gkwa/jumpingjay durationsince 1pm
```

## Available Commands

- `durationsince` - Calculate duration since a given time

```bash
  uvx --from . durationsince 1pm
```

- `durationtill` - Calculate duration until a given time

```bash
  uvx --from . durationtill 2pm
```

- `timein` - Calculate the time at a given duration from now

```bash
  uvx --from . timein 15h30m
```

- `jumpingjay` - Show available commands

```bash
  uvx --from . jumpingjay --list
```

## Examples

```bash
# How long since 1pm?
uvx --from . durationsince 1pm

# How long until 5:30pm?
uvx --from . durationtill 5:30pm

# What time will it be in 15 hours and 30 minutes?
uvx --from . timein 15h30m

# What time will it be in 2 hours (24-hour format)?
uvx --from . timein 2h --format 24h

# With verbose logging
uvx --from . durationsince 1pm -vvv
```
