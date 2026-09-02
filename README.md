# QR Terminal Studio

A lightweight Python CLI tool for creating styled QR codes right from your terminal. It renders an instant ASCII preview directly in your terminal before saving the final image as a PNG.

> ### Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Typer](https://img.shields.io/badge/Typer-009688?style=for-the-badge&logo=python&logoColor=white)
![Rich](https://img.shields.io/badge/Rich-202020?style=for-the-badge&logo=python&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-00599C?style=for-the-badge&logo=python&logoColor=white)
![Git Bash](https://img.shields.io/badge/Git%20Bash-F05032?style=for-the-badge&logo=git&logoColor=white)
![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)

- **Language:** Python 3.10+
- **CLI Framework:** Typer (built on Click)
- **Terminal UI & Formatting:** Rich
- **Image Processing & QR Engine:** Pillow (PIL) and `qrcode`
- **Development Environment:** VS Code with Integrated Git Bash

## Features

- **Instant Terminal Preview:** Renders an ASCII QR code directly in terminal output before saving.
- **Custom Module Styles:** Choose between standard square modules or rounded circle modules.
- **Clean CLI Interface:** Built-in command handling, argument parsing, and error reporting.

## Setup Instructions

### 1. Open Project Directory

Navigate to your project directory in Git Bash or VS Code integrated terminal:

```bash
cd qr-terminal-studio
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv .venv
source .venv/Scripts/activate
```

### 3. Install Dependencies

```bash
pip install requirements.txt
```

## Usage & Examples

### Basic QR Code:

Generate a standard square QR code with terminal preview saved to `output.png`:

```bash
python main.py "https://github.com"
```

### Circle Module Style

Generate a QR code using circle modules and save it to a specific file path:

```bash
python main.py "https://github.com" -o github.png --style circle
```

### Disable Terminal Preview

Generate only the PNG file without printing the ASCII block preview:

```bash
python main.py "https://github.com" -o github.png --no-preview
```

### Check Available Options

```bash
python main.py --help
```

---

### Future Changes

As for later, I will try to implement the ability to add embedded logos/icons and colors to make it more customizable.
