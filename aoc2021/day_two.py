from dataclasses import dataclass

_SUBMARINE_COMMAND_SEPARATOR = " "

_KNOWN_SUBMARINE_COMMANDS = [
    "forward",
    "down",
    "up"
]


@dataclass(frozen=True, slots=True)
class _SubmarineCommand:
    command: str
    value: int


def _parse_command(command):
    command_parts = command.split(_SUBMARINE_COMMAND_SEPARATOR)

    if len(command_parts) != 2:
        return None

    command, value = command_parts

    if command not in _KNOWN_SUBMARINE_COMMANDS:
        return None

    if not value.is_digit():
        return None

    return command, int(value)


def part_one(start_hposition, start_depth, commands):
    return 0, 0
