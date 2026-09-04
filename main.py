from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
import qrcode

from qr_engine import generate_qr

app = typer.Typer(help="Secure Dynamic QR Terminal Studio CLI")
console = Console()


def print_ascii_preview(data: str) -> None:
    """Renders a quick ASCII QR preview directly inside the terminal."""
    qr = qrcode.QRCode(border=1)
    qr.add_data(data)
    qr.make(fit=True)
    
    console.print("\n[bold cyan]Terminal ASCII Preview:[/bold cyan]")
    matrix = qr.get_matrix()
    for row in matrix:
        line = "".join("██" if cell else "  " for cell in row)
        console.print(f"[bold white]{line}[/bold white]")
    console.print()


@app.command()
def create(
    data: str = typer.Argument(..., help="Text, URL, or data payload to encode"),
    output: Path = typer.Option(
        Path("output.png"), "--output", "-o", help="Output PNG file path"
    ),
    style: str = typer.Option(
        "square", "--style", "-s", help="Module design style: 'square' or 'circle'"
    ),
    fill_color: str = typer.Option(
        "#000000", "--fill", "-f", help="Foreground color in hex (e.g. '#1E1E2E') or name"
    ),
    bg_color: str = typer.Option(
        "#FFFFFF", "--bg", "-b", help="Background color in hex (e.g. '#89B4FA') or name"
    ),
    logo: Optional[Path] = typer.Option(
        None, "--logo", "-l", help="Path to an image file (PNG/JPG) to embed in the center"
    ),
    logo_size: float = typer.Option(
        0.2, "--logo-size", help="Logo scale factor (0.1 to 0.3)"
    ),
    preview: bool = typer.Option(
        True, "--preview/--no-preview", help="Render ASCII preview in terminal"
    ),
) -> None:
    """Generate a customized QR code image with custom styling, colors, and embedded logos."""
    try:
        if preview:
            print_ascii_preview(data)

        saved_path = generate_qr(
            data=data,
            output_path=output,
            fill_color=fill_color,
            back_color=bg_color,
            style=style,
            logo_path=logo,
            logo_scale=logo_size,
        )
        console.print(
            f"[bold green]✔ Success![/bold green] QR code saved to [yellow]{saved_path}[/yellow]"
        )
    except Exception as err:
        console.print(f"[bold red]Error generating QR code:[/bold red] {err}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()