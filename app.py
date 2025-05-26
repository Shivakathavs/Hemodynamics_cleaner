import tkinter as tk
from tkinter import filedialog, messagebox
from image_logic import MedicalImageProcessor

def main():
    root = tk.Tk()
    root.title("Medical Image Split and Calibration Tool")

    # Prompt user for image directory
    image_dir = filedialog.askdirectory(title="Select image directory")
    if not image_dir:
        messagebox.showerror("No folder selected", "You must select a folder to continue.")
        root.destroy()
        return

    app = MedicalImageProcessor(root, image_dir=image_dir)
    app.log_images_found()  # Log total and remaining images at startup
    root.mainloop()

if __name__ == "__main__":
    main()
    
