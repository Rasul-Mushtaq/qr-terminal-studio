import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox
from pathlib import Path
from qr_engine import generate_qr


class QRGui:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("QR Studio - Desktop Interface")
        self.root.geometry("460x480")
        self.root.resizable(False, False)

        self.fill_color = "#000000"
        self.bg_color = "#FFFFFF"
        self.logo_path = None

        self._build_ui()

    def _build_ui(self):
        padding = {'padx': 15, 'pady': 6}

        # Data Input
        ttk.Label(self.root, text="Data / URL Payload:", font=("Arial", 10, "bold")).pack(anchor="w", **padding)
        self.data_entry = ttk.Entry(self.root, width=50)
        self.data_entry.pack(fill="x", padx=15)
        self.data_entry.insert(0, "https://github.com")

        # Style Selection
        ttk.Label(self.root, text="Module Style:", font=("Arial", 10, "bold")).pack(anchor="w", **padding)
        self.style_var = tk.StringVar(value="square")
        style_frame = ttk.Frame(self.root)
        style_frame.pack(fill="x", padx=15)
        ttk.Radiobutton(style_frame, text="Square", value="square", variable=self.style_var).pack(side="left", padx=10)
        ttk.Radiobutton(style_frame, text="Circle", value="circle", variable=self.style_var).pack(side="left", padx=10)

        # Color Pickers
        ttk.Label(self.root, text="Custom Colors:", font=("Arial", 10, "bold")).pack(anchor="w", **padding)
        color_frame = ttk.Frame(self.root)
        color_frame.pack(fill="x", padx=15)
        ttk.Button(color_frame, text="Foreground Color", command=self._pick_fill_color).pack(side="left", padx=5)
        ttk.Button(color_frame, text="Background Color", command=self._pick_bg_color).pack(side="left", padx=5)

        # Logo Selection
        ttk.Label(self.root, text="Embedded Logo (Optional):", font=("Arial", 10, "bold")).pack(anchor="w", **padding)
        logo_frame = ttk.Frame(self.root)
        logo_frame.pack(fill="x", padx=15)
        self.logo_label = ttk.Label(logo_frame, text="No logo selected", foreground="gray")
        self.logo_label.pack(side="left", expand=True, fill="x")
        ttk.Button(logo_frame, text="Browse Image", command=self._pick_logo).pack(side="right")

        # Action Button
        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=15)
        gen_btn = ttk.Button(self.root, text="Generate & Save QR Code", command=self._generate_qr)
        gen_btn.pack(ipady=6, fill="x", padx=20)

    def _pick_fill_color(self):
        color = colorchooser.askcolor(title="Choose Foreground Color", initialcolor=self.fill_color)
        if color[1]:
            self.fill_color = color[1]

    def _pick_bg_color(self):
        color = colorchooser.askcolor(title="Choose Background Color", initialcolor=self.bg_color)
        if color[1]:
            self.bg_color = color[1]

    def _pick_logo(self):
        file_selected = filedialog.askopenfilename(
            title="Select Logo Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.webp")]
        )
        if file_selected:
            self.logo_path = Path(file_selected)
            self.logo_label.config(text=self.logo_path.name, foreground="black")

    def _generate_qr(self):
        data = self.data_entry.get().strip()
        if not data:
            messagebox.showerror("Error", "Please enter a payload or URL.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            initialfile="qr_output.png",
            title="Save QR Code As"
        )
        if not save_path:
            return

        try:
            generate_qr(
                data=data,
                output_path=Path(save_path),
                fill_color=self.fill_color,
                back_color=self.bg_color,
                style=self.style_var.get(),
                logo_path=self.logo_path,
            )
            messagebox.showinfo("Success", f"QR Code successfully saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def launch_gui():
    root = tk.Tk()
    app = QRGui(root)
    root.mainloop()