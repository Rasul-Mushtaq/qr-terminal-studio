from pathlib import Path
from typing import Optional
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.moduledrawers import CircleModuleDrawer, SquareModuleDrawer


def generate_qr(
    data: str,
    output_path: Path,
    fill_color: tuple[int, int, int] = (0, 0, 0),
    back_color: tuple[int, int, int] = (255, 255, 255),
    style: str = "square",
) -> Path:
    """
    Generates a styled QR code image from input data.

    Args:
        data: Payload string to encode.
        output_path: File system path where PNG should be saved.
        fill_color: RGB tuple for foreground modules.
        back_color: RGB tuple for background.
        style: Module design ('square' or 'circle').

    Returns:
        Path to the saved PNG image.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Select module shape
    drawer = CircleModuleDrawer() if style == "circle" else SquareModuleDrawer()

    # Generate styled image with custom color mask
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=drawer,
        color_mask=SolidFillColorMask(
            back_color=back_color, front_color=fill_color
        ),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
    return output_path