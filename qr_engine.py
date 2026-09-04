from pathlib import Path
from typing import Optional
from PIL import Image, ImageColor
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.moduledrawers import CircleModuleDrawer, SquareModuleDrawer


def _parse_color(color_val: str) -> tuple[int, int, int]:
    """Converts hex strings or named colors to RGB tuples."""
    try:
        return ImageColor.getcolor(color_val, "RGB")
    except ValueError:
        raise ValueError(f"Invalid color format: '{color_val}'. Use hex (e.g. '#FF0000') or named colors.")


def generate_qr(
    data: str,
    output_path: Path,
    fill_color: str = "#000000",
    back_color: str = "#FFFFFF",
    style: str = "square",
    logo_path: Optional[Path] = None,
    logo_scale: float = 0.2,
) -> Path:
    """Generates a styled QR code with custom colors and optional embedded logo.

    Args:
        data: Text or URL payload.
        output_path: File system path for the PNG.
        fill_color: Foreground hex/named color.
        back_color: Background hex/named color.
        style: Module design ('square' or 'circle').
        logo_path: Optional path to an icon or logo image.
        logo_scale: Logo width percentage relative to total QR width (0.1 to 0.3).

    Returns:
        Path to the saved PNG image.
    """
    fg_rgb = _parse_color(fill_color)
    bg_rgb = _parse_color(back_color)

    # Use High Error Correction when embedding logos to ensure scannability
    qr = qrcode.QRCode(
        version=None,  # Auto-fit version based on data size
        error_correction=qrcode.constants.ERROR_CORRECT_H if logo_path else qrcode.constants.ERROR_CORRECT_M,
        box_size=12,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    drawer = CircleModuleDrawer() if style == "circle" else SquareModuleDrawer()

    # Generate base QR code
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=drawer,
        color_mask=SolidFillColorMask(back_color=bg_rgb, front_color=fg_rgb),
    ).convert("RGBA")

    # Embed center logo if provided
    if logo_path and logo_path.exists():
        logo = Image.open(logo_path).convert("RGBA")
        
        # Calculate maximum logo box dimensions
        qr_w, qr_h = img.size
        target_size = int(qr_w * max(0.05, min(logo_scale, 0.3)))  # Cap between 5% and 30%
        logo.thumbnail((target_size, target_size), Image.Resampling.LANCZOS)

        # Center position calculation
        logo_w, logo_h = logo.size
        pos_x = (qr_w - logo_w) // 2
        pos_y = (qr_h - logo_h) // 2

        # Paste logo using alpha channel mask
        img.paste(logo, (pos_x, pos_y), logo)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
    return output_path