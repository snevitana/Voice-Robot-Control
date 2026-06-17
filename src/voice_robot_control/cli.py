from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from voice_robot_control.app import build_backend, build_matcher, process_text, run_microphone_loop
from voice_robot_control.config import AppConfig, ConfigError, load_config
from voice_robot_control.logging_setup import setup_logging

app = typer.Typer(no_args_is_help=True)
console = Console()


def _load_config_or_exit(config: Path) -> AppConfig:
    try:
        loaded_config = load_config(config)
    except ConfigError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
    setup_logging(loaded_config.log_level)
    return loaded_config


@app.command()
def run(
    config: Annotated[Path, typer.Option("--config", "-c", help="Path to YAML config")],
) -> None:
    loaded_config = _load_config_or_exit(config)
    try:
        run_microphone_loop(loaded_config)
    except RuntimeError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc


@app.command("list-commands")
def list_commands(
    config: Annotated[Path, typer.Option("--config", "-c", help="Path to YAML config")],
) -> None:
    loaded_config = _load_config_or_exit(config)
    table = Table(title="Voice commands")
    table.add_column("Command")
    table.add_column("Phrases")
    for command, phrases in build_matcher(loaded_config).list_phrases().items():
        table.add_row(command.name, ", ".join(phrases))
    console.print(table)


@app.command("test-match")
def test_match(
    text: Annotated[str, typer.Argument(help="Text command to match")],
    config: Annotated[Path, typer.Option("--config", "-c", help="Path to YAML config")],
) -> None:
    loaded_config = _load_config_or_exit(config)
    command = build_matcher(loaded_config).match(text)
    console.print(command.name if command else "UNKNOWN")


@app.command("check-config")
def check_config(
    config: Annotated[Path, typer.Option("--config", "-c", help="Path to YAML config")],
) -> None:
    loaded_config = _load_config_or_exit(config)
    console.print(
        f"OK: backend={loaded_config.backend.value}, "
        f"sample_rate={loaded_config.sample_rate}, "
        f"commands={len(loaded_config.commands)}"
    )


@app.command("demo-text")
def demo_text(
    text: Annotated[str, typer.Option("--text", "-t", help="Text command to process")],
    config: Annotated[Path, typer.Option("--config", "-c", help="Path to YAML config")],
) -> None:
    loaded_config = _load_config_or_exit(config)
    matcher = build_matcher(loaded_config)
    backend = build_backend(loaded_config)
    if not process_text(text, matcher, backend):
        console.print("UNKNOWN")


def main() -> None:
    app()
