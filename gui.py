from pathlib import Path
import customtkinter as ctk
from tkinter import colorchooser, filedialog, messagebox
from qr_engine import generate_qr

# Global theme setup
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class QRGui(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("QR Studio - Desktop Interface")
        self.geometry("480x540")
        self.resizable(False, False)

        self.fill_color = "#000000"
        self.bg_color = "#FFFFFF"
        self.logo_path = None

        self._build_ui()

    def _build_ui(self):
        # Title Header
        self.title_label = ctk.CTkLabel(
            self, 
            text="QR Terminal Studio", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.title_label.pack(pady=(20, 10))

        # Main Card Frame
        self.card = ctk.CTkFrame(self, corner_radius=12)
        self.card.pack(fill="both", expand=True, padx=20, pady=10)

        # Data Input
        ctk.CTkLabel(
            self.card, text="Data / URL Payload:", font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.data_entry = ctk.CTkEntry(
            self.card, placeholder_text="https://github.com", height=38, corner_radius=8
        )
        self.data_entry.pack(fill="x", padx=20)
        self.data_entry.insert(0, "https://github.com")

        # Style Selection
        ctk.CTkLabel(
            self.card, text="Module Style:", font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.style_segmented = ctk.CTkSegmentedButton(
            self.card, values=["Square", "Circle"]
        )
        self.style_segmented.set("Square")
        self.style_segmented.pack(fill="x", padx=20)

        # Custom Colors
        ctk.CTkLabel(
            self.card, text="Custom Colors:", font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        color_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        color_frame.pack(fill="x", padx=20)

        self.fg_btn = ctk.CTkButton(
            color_frame,
            text="Foreground Color",
            fg_color="#1f538d",
            hover_color="#14375e",
            corner_radius=8,
            command=self._pick_fill_color,
        )
        self.fg_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.bg_btn = ctk.CTkButton(
            color_frame,
            text="Background Color",
            fg_color="#333333",
            hover_color="#444444",
            corner_radius=8,
            command=self._pick_bg_color,
        )
        self.bg_btn.pack(side="left", expand=True, fill="x", padx=(5, 0))

        # Logo Selection
        ctk.CTkLabel(
            self.card, text="Embedded Logo (Optional):", font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        logo_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20)

        self.logo_label = ctk.CTkLabel(
            logo_frame, text="No logo selected", text_color="gray"
        )
        self.logo_label.pack(side="left")

        self.logo_btn = ctk.CTkButton(
            logo_frame,
            text="Browse Image",
            width=110,
            fg_color="#2b2b2b",
            hover_color="#3a3a3a",
            corner_radius=8,
            command=self._pick_logo,
        )
        self.logo_btn.pack(side="right")

        # Action Button
        self.gen_btn = ctk.CTkButton(
            self,
            text="Generate & Save QR Code",
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#2FA572",
            hover_color="#218057",
            corner_radius=10,
            command=self._generate_qr,
        )
        self.gen_btn.pack(fill="x", padx=20, pady=(10, 20))

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
            self.logo_label.configure(text=self.logo_path.name, text_color="white")

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
            style = self.style_segmented.get().lower()
            generate_qr(
                data=data,
                output_path=Path(save_path),
                fill_color=self.fill_color,
                back_color=self.bg_color,
                style=style,
                logo_path=self.logo_path,
            )
            messagebox.showinfo("Success", f"QR Code successfully saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def launch_gui():
    app = QRGui()
    app.mainloop()