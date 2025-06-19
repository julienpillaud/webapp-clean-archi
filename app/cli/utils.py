from typing import Any

from rich import print
from rich.panel import Panel
from rich.pretty import Pretty


def print_result(result: Any, title: str, border_style: str = "none") -> None:
    print(Panel(Pretty(result), title=title, width=120, border_style=border_style))
