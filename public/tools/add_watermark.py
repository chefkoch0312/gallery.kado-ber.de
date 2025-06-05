import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import threading

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wasserzeichen-Tool")
        self.root.geometry("600x500")
        
        self.supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp')
        
        self.directory_path = tk.StringVar()
        self.watermark_text = tk.StringVar(value="© Ihr Wasserzeichen")
        self.watermark_file = tk.StringVar()
        self.watermark_type = tk.StringVar(value="text")
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(main_frame, text="Arbeitsverzeichnis:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.directory_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Durchsuchen", command=self.select_directory).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(main_frame, text="Wasserzeichen-Typ:").grid(row=1, column=0, sticky=tk.W, pady=5)
        type_frame = ttk.Frame(main_frame)
        type_frame.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(type_frame, text="Text", variable=self.watermark_type, value="text").grid(row=0, column=0, padx=5)
        ttk.Radiobutton(type_frame, text="Bild", variable=self.watermark_type, value="image").grid(row=0, column=1, padx=5)
        
        ttk.Label(main_frame, text="Wasserzeichen-Text:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.watermark_text, width=50).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(main_frame, text="Wasserzeichen-Bild:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.watermark_file, width=50).grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Bild wählen", command=self.select_watermark_image).grid(row=3, column=2, padx=5, pady=5)
        
        settings_frame = ttk.LabelFrame(main_frame, text="Einstellungen", padding="5")
        settings_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(settings_frame, text="Transparenz:").grid(row=0, column=0, sticky=tk.W)
        self.transparency_var = tk.IntVar(value=50)
        transparency_scale = ttk.Scale(settings_frame, from_=10, to=100, variable=self.transparency_var, orient=tk.HORIZONTAL)
        transparency_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        self.transparency_label = ttk.Label(settings_frame, text="50%")
        self.transparency_label.grid(row=0, column=2)
        transparency_scale.configure(command=self.update_transparency_label)
        
        ttk.Label(settings_frame, text="Position:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.position_var = tk.StringVar(value="bottom_right")
        position_combo = ttk.Combobox(settings_frame, textvariable=self.position_var, 
                                    values=["top_left", "top_right", "bottom_left", "bottom_right", "center"],
                                    state="readonly")
        position_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Label(settings_frame, text="Schriftgröße:").grid(row=2, column=0, sticky=tk.W)
        self.font_size_var = tk.IntVar(value=36)
        font_size_spin = ttk.Spinbox(settings_frame, from_=12, to=100, textvariable=self.font_size_var, width=10)
        font_size_spin.grid(row=2, column=1, sticky=tk.W, padx=5)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Vorschau", command=self.preview_watermark).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Verarbeitung starten", command=self.start_processing).grid(row=0, column=1, padx=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.status_label = ttk.Label(main_frame, text="Bereit")
        self.status_label.grid(row=7, column=0, columnspan=3, pady=5)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        settings_frame.columnconfigure(1, weight=1)
        
    def update_transparency_label(self, value):
        self.transparency_label.config(text=f"{int(float(value))}%")
        
    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_path.set(directory)
            
    def select_watermark_image(self):
        file_path = filedialog.askopenfilename(
            title="Wasserzeichen-Bild auswählen",
            filetypes=[("Bilddateien", "*.png *.jpg *.jpeg *.bmp *.tiff *.tif")]
        )
        if file_path:
            self.watermark_file.set(file_path)
            
    def get_image_files(self, directory):
        image_files = []
        for file in os.listdir(directory):
            if file.lower().endswith(self.supported_formats):
                image_files.append(os.path.join(directory, file))
        return image_files
        
    def calculate_position(self, image_size, watermark_size, position):
        img_width, img_height = image_size
        wm_width, wm_height = watermark_size
        
        positions = {
            "top_left": (20, 20),
            "top_right": (img_width - wm_width - 20, 20),
            "bottom_left": (20, img_height - wm_height - 20),
            "bottom_right": (img_width - wm_width - 20, img_height - wm_height - 20),
            "center": ((img_width - wm_width) // 2, (img_height - wm_height) // 2)
        }
        
        return positions.get(position, positions["bottom_right"])
        
    def add_text_watermark(self, image, text, position, transparency, font_size):
        overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("DejaVuSans.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x, y = self.calculate_position(image.size, (text_width, text_height), position)
        
        alpha = int(255 * (transparency / 100))
        draw.text((x, y), text, font=font, fill=(255, 255, 255, alpha))
        
        return Image.alpha_composite(image.convert('RGBA'), overlay)
        
    def add_image_watermark(self, image, watermark_path, position, transparency):
        watermark = Image.open(watermark_path).convert('RGBA')
        
        max_size = min(image.size[0] // 4, image.size[1] // 4)
        if watermark.size[0] > max_size or watermark.size[1] > max_size:
            watermark.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        alpha = int(255 * (transparency / 100))
        watermark = watermark.copy()
        watermark.putalpha(alpha)
        
        x, y = self.calculate_position(image.size, watermark.size, position)
        
        overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))
        overlay.paste(watermark, (x, y), watermark)
        
        return Image.alpha_composite(image.convert('RGBA'), overlay)
        
    def process_image(self, image_path):
        try:
            image = Image.open(image_path)
            
            if self.watermark_type.get() == "text":
                watermarked = self.add_text_watermark(
                    image, 
                    self.watermark_text.get(),
                    self.position_var.get(),
                    self.transparency_var.get(),
                    self.font_size_var.get()
                )
            else:
                if not self.watermark_file.get():
                    raise ValueError("Bitte wählen Sie ein Wasserzeichen-Bild aus")
                watermarked = self.add_image_watermark(
                    image,
                    self.watermark_file.get(),
                    self.position_var.get(),
                    self.transparency_var.get()
                )
            
            base_name = os.path.splitext(image_path)[0]
            output_path = f"{base_name}_wm.jpg"
            
            if watermarked.mode == 'RGBA':
                background = Image.new('RGB', watermarked.size, (255, 255, 255))
                background.paste(watermarked, mask=watermarked.split()[-1])
                watermarked = background
            
            watermarked.save(output_path, 'JPEG', quality=95)
            return True, output_path
            
        except Exception as e:
            return False, str(e)
            
    def preview_watermark(self):
        if not self.directory_path.get():
            messagebox.showerror("Fehler", "Bitte wählen Sie ein Verzeichnis aus")
            return
            
        image_files = self.get_image_files(self.directory_path.get())
        if not image_files:
            messagebox.showinfo("Info", "Keine Bilddateien im gewählten Verzeichnis gefunden")
            return
            
        try:
            success, result = self.process_image(image_files[0])
            if success:
                self.show_preview(result)
            else:
                messagebox.showerror("Fehler", f"Fehler bei der Vorschau: {result}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der Vorschau: {str(e)}")
            
    def show_preview(self, image_path):
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Vorschau")
        preview_window.geometry("800x600")
        
        image = Image.open(image_path)
        image.thumbnail((750, 550), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        
        label = ttk.Label(preview_window, image=photo)
        label.image = photo  # Referenz behalten
        label.pack(expand=True)
        
        try:
            os.remove(image_path)
        except:
            pass
            
    def process_images(self):
        directory = self.directory_path.get()
        if not directory:
            messagebox.showerror("Fehler", "Bitte wählen Sie ein Verzeichnis aus")
            return
            
        image_files = self.get_image_files(directory)
        if not image_files:
            messagebox.showinfo("Info", "Keine Bilddateien im gewählten Verzeichnis gefunden")
            return
            
        total_files = len(image_files)
        processed = 0
        errors = []
        
        for i, image_path in enumerate(image_files):
            # Update Status
            self.status_label.config(text=f"Verarbeite: {os.path.basename(image_path)}")
            self.progress_var.set((i / total_files) * 100)
            self.root.update()
            
            success, result = self.process_image(image_path)
            if success:
                processed += 1
            else:
                errors.append(f"{os.path.basename(image_path)}: {result}")
                
        self.progress_var.set(100)
        self.status_label.config(text=f"Fertig! {processed} von {total_files} Bildern verarbeitet")
        
        if errors:
            error_msg = f"Fehler bei {len(errors)} Dateien:\n" + "\n".join(errors[:5])
            if len(errors) > 5:
                error_msg += f"\n... und {len(errors) - 5} weitere"
            messagebox.showwarning("Warnung", error_msg)
        else:
            messagebox.showinfo("Erfolg", f"Alle {processed} Bilder erfolgreich verarbeitet!")
            
    def start_processing(self):
        if not self.directory_path.get():
            messagebox.showerror("Fehler", "Bitte wählen Sie ein Verzeichnis aus")
            return
            
        if self.watermark_type.get() == "text" and not self.watermark_text.get().strip():
            messagebox.showerror("Fehler", "Bitte geben Sie einen Wasserzeichen-Text ein")
            return
            
        if self.watermark_type.get() == "image" and not self.watermark_file.get():
            messagebox.showerror("Fehler", "Bitte wählen Sie ein Wasserzeichen-Bild aus")
            return
            
        thread = threading.Thread(target=self.process_images)
        thread.daemon = True
        thread.start()

def main():
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()