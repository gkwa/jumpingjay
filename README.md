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

- `jumpingjay` - Show available commands

```bash
  uvx --from . jumpingjay --list-commands
```

## Examples

```bash
# How long since 1pm?
uvx --from . durationsince 1pm

# How long until 5:30pm?
uvx --from . durationtill 5:30pm

# With verbose logging
uvx --from . durationsince 1pm -vvv
```
