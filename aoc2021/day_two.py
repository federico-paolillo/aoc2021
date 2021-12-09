from dataclasses import dataclass
from typing import Optional, Tuple

_SUBMARINE_COMMAND_SEPARATOR = " "

_FORWARD = "forward"
_DOWN = "down"
_UP = "up"

_KNOWN_SUBMARINE_COMMANDS = [
    _FORWARD,
    _DOWN,
    _UP
]


@dataclass(frozen=True)
class _SubmarineCommand:
    command: str
    value: int


def _parse_one_submarine_command(raw_submarine_command: str) -> Optional[_SubmarineCommand]:
    if not raw_submarine_command:
        return None

    raw_command_parts = raw_submarine_command.split(_SUBMARINE_COMMAND_SEPARATOR)

    if len(raw_command_parts) != 2:
        return None

    raw_command, raw_value = raw_command_parts

    normalized_command: str = raw_command.strip().lower()
    normalized_value: str = raw_value.strip()

    if normalized_command not in _KNOWN_SUBMARINE_COMMANDS:
        return None

    if not normalized_value.isdigit():
        return None

    return _SubmarineCommand(normalized_command, int(normalized_value))


def _parse_raw_submarine_commands(raw_submarine_commands):
    submarine_commands = []
    for raw_submarine_command in raw_submarine_commands:
        maybe_submarine_command = _parse_one_submarine_command(raw_submarine_command)
        if maybe_submarine_command:
            submarine_commands.append(maybe_submarine_command)
    return submarine_commands


def _apply_submarine_commands(start_hposition: int, start_depth: int, submarine_commands: list[_SubmarineCommand]) -> Tuple[int, int]:
    final_hposition = start_hposition
    final_depth = start_depth

    for submarine_command in submarine_commands:
        if submarine_command.command == _FORWARD:
            final_hposition = final_hposition + submarine_command.value
        elif submarine_command.command == _DOWN:
            final_depth = final_depth + submarine_command.value
        elif submarine_command.command == _UP:
            final_depth = final_depth - submarine_command.value

    return final_hposition, final_depth


def part_one(start_hposition: int, start_depth: int, raw_submarine_commands: list[str]):
    submarine_commands = _parse_raw_submarine_commands(raw_submarine_commands)

    final_hposition, final_depth = _apply_submarine_commands(start_hposition, start_depth, submarine_commands)

    return final_hposition, final_depth
