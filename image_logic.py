import os
import cv2
import numpy as np
import pandas as pd
from PIL import Image, ImageTk
from file_utils import find_all_images, log_to_console, update_progress
from annotations import draw_annotations
from ui import setup_ui

try:
    resample = Image.Resampling.LANCZOS
except AttributeError:
    resample = Image.LANCZOS

class MedicalImageProcessor:
    def __init__(self, root, image_dir="."):
        self.root = root
        self.image_dir = image_dir
        self.initialize_variables()

        self.display_width = 1200
        self.display_height = 900

        self.image_files = find_all_images(directory=self.image_dir)
        log_to_console(self, f"Total images to process: {len(self.image_files)}")

        setup_ui(self, self.display_width, self.display_height)

        if self.image_files:
            self.load_current_image()
        else:
            log_to_console(self, f"No images found in the directory: {self.image_dir}")

    def initialize_variables(self):
        self.current_index = 0
        self.rotation_angle = 0.0
        self.cv_image = None
        self.tk_image = None
        self.original_image = None
        self.crop_rect = None
        self.crop_mode = False
        self.drawing_mode = None
        self.canvas = None
        self.progress_label = None
        self.log_text = None
        self.crop_start = None
        self.roi_mode = None
        self.roi_rectangles = []
        self.undo_stack = []
        self.redo_stack = []
        self.horizontal_ticks = []
        self.vertical_ticks = []
        self.tick_values = {"horizontal": [], "vertical": []}
        self.tick_units = {"horizontal": "", "vertical": ""}

    def set_tick_mode(self, mode):
        if mode == "horizontal":
            self.drawing_mode = "tick_horizontal"
            log_to_console(self, "Click two points to define horizontal ticks.")
        elif mode == "vertical":
            self.drawing_mode = "tick_vertical"
            log_to_console(self, "Click two points to define vertical ticks.")

    def load_current_image(self):
        if not self.image_files:
            log_to_console(self, "No images to load.")
            return
        self.current_file = self.image_files[self.current_index]
        self.cv_image = cv2.imread(self.current_file)
        self.original_image = self.cv_image.copy()
        self.crop_rect = None
        self.crop_mode = False
        self.roi_rectangles = []
        self.undo_stack = []
        self.redo_stack = []
        self.rotation_angle = 0.0
        self.horizontal_ticks = []
        self.vertical_ticks = []
        self.tick_values = {"horizontal": [], "vertical": []}
        self.tick_units = {"horizontal": "", "vertical": ""}

        log_to_console(self, f"Image {self.current_index + 1} of {len(self.image_files)}")
        log_to_console(self, f"Images left to process: {len(self.image_files) - self.current_index - 1}")

        self.update_display()
        log_to_console(self, f"Loaded image: {self.current_file}")
    
    def log_images_found(self):
        total = len(self.image_files)
        remaining = total - self.current_index - 1
        log_to_console(self, f"Total images to process: {total}")
        log_to_console(self, f"Currently viewing image {self.current_index + 1}")
        log_to_console(self, f"Images left to process: {remaining}")

    def update_display(self):
        img = self.cv_image if self.cv_image is not None else self.original_image
        if img is None:
            return
        self.rotated_image = img.copy()
        pil_img = Image.fromarray(cv2.cvtColor(self.rotated_image, cv2.COLOR_BGR2RGB))
        pil_img = draw_annotations(pil_img, self)
        w, h = pil_img.size
        self.displayed_image_width = w
        self.displayed_image_height = h
        max_w, max_h = self.display_width, self.display_height

        scale = min(max_w / w, max_h / h, 1.0)
        if scale < 1.0:
            new_w, new_h = int(w * scale), int(h * scale)
            pil_img = pil_img.resize((new_w, new_h), resample)
            self.displayed_image_width = new_w
            self.displayed_image_height = new_h
        else:
            new_w, new_h = w, h

        self.tk_image = ImageTk.PhotoImage(pil_img)
        self.canvas.delete("all")
        self.canvas.config(width=min(new_w, max_w), height=min(new_h, max_h))
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)
        self.canvas.config(scrollregion=(0, 0, new_w, new_h))
        update_progress(self)

    def clear_horizontal_ticks(self):
        self.horizontal_ticks = []
        self.tick_values["horizontal"] = []
        self.horz_tick1_entry.delete(0, 'end')
        self.horz_tick2_entry.delete(0, 'end')
        self.horizontal_units_entry.delete(0, 'end')
        self.update_display()
        log_to_console(self, "Cleared horizontal ticks.")

    def clear_vertical_ticks(self):
        self.vertical_ticks = []
        self.tick_values["vertical"] = []
        self.vert_tick1_entry.delete(0, 'end')
        self.vert_tick2_entry.delete(0, 'end')
        self.vertical_units_entry.delete(0, 'end')
        self.update_display()
        log_to_console(self, "Cleared vertical ticks.")

    def save_horizontal_ticks(self):
        if len(self.horizontal_ticks) < 2:
            log_to_console(self, "Select two points for horizontal ticks before saving.")
            return
        try:
            v1 = float(self.horz_tick1_entry.get())
            v2 = float(self.horz_tick2_entry.get())
            self.tick_values["horizontal"] = [v1, v2]
        except Exception:
            self.tick_values["horizontal"] = ["", ""]
        self.tick_units["horizontal"] = self.horizontal_units_entry.get().strip()
        log_to_console(self, "Saved horizontal tick calibration.")

    def save_vertical_ticks(self):
        if len(self.vertical_ticks) < 2:
            log_to_console(self, "Select two points for vertical ticks before saving.")
            return
        try:
            v1 = float(self.vert_tick1_entry.get())
            v2 = float(self.vert_tick2_entry.get())
            self.tick_values["vertical"] = [v1, v2]
        except Exception:
            self.tick_values["vertical"] = ["", ""]
        self.tick_units["vertical"] = self.vertical_units_entry.get().strip()
        log_to_console(self, "Saved vertical tick calibration.")

    def start_crop(self):
        self.crop_mode = True
        log_to_console(self, "Draw a rectangle to crop the image.")
        self.update_display()

    def start_roi_mode(self, mode):
        self.roi_mode = mode
        self.crop_mode = True
        self.crop_start = None
        self.crop_rect = None
        log_to_console(self, f"ROI mode: {mode} - click and drag to select area")
        self.update_display()

    def crop_image(self):
        if not self.crop_rect:
            return
        x0, y0, x1, y1 = map(int, self.crop_rect)
        x0, x1 = max(0, min(x0, x1)), min(self.cv_image.shape[1], max(x0, x1))
        y0, y1 = max(0, min(y0, y1)), min(self.cv_image.shape[0], max(y0, y1))
        self.cv_image = self.cv_image[y0:y1, x0:x1]
        self.original_image = self.cv_image.copy()
        self.crop_rect = None
        self.crop_mode = False
        log_to_console(self, f"Cropped image to: ({x0}, {y0}), ({x1}, {y1})")
        self.update_display()

    def rotate_image(self, angle):
        self.rotation_angle += angle
        img = self.cv_image if self.cv_image is not None else self.original_image
        if img is None:
            return

        (h, w) = img.shape[:2]
        center = (w / 2, h / 2)
        M = cv2.getRotationMatrix2D(center, self.rotation_angle, 1.0)
        abs_cos = abs(M[0, 0])
        abs_sin = abs(M[0, 1])
        new_w = int(h * abs_sin + w * abs_cos)
        new_h = int(h * abs_cos + w * abs_sin)
        M[0, 2] += (new_w / 2) - center[0]
        M[1, 2] += (new_h / 2) - center[1]
        rotated = cv2.warpAffine(img, M, (new_w, new_h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        self.cv_image = rotated
        self.update_display()
        log_to_console(self, f"Rotated image by {angle} degrees (total: {self.rotation_angle}).")

    def start_erase(self):
        self.drawing_mode = "erase"
        log_to_console(self, "Eraser mode: drag mouse to erase parts of the image.")

    def previous_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_current_image()
        else:
            log_to_console(self, "Already at the first image.")

    def next_image(self):
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.load_current_image()
        else:
            log_to_console(self, "Already at the last image.")

    def save_all_rois(self):
        if not self.roi_rectangles:
            log_to_console(self, "No ROIs to save.")
            return

        base_filename = os.path.splitext(os.path.basename(self.current_file))[0]
        parent_dir = os.path.dirname(self.current_file)
        subfolder_path = os.path.join(parent_dir, base_filename)
        os.makedirs(subfolder_path, exist_ok=True)

        for idx, (x0, y0, x1, y1, mode) in enumerate(self.roi_rectangles):
            roi = self.cv_image[y0:y1, x0:x1]
            suffix = f"_{mode.lower()}_{idx+1}"
            roi_path = os.path.join(subfolder_path, f"{base_filename}{suffix}.png")
            cv2.imwrite(roi_path, roi)
            log_to_console(self, f"Saved ROI: {roi_path}")

    def undo_last_roi(self):
        if self.roi_rectangles:
            self.redo_stack.append(self.roi_rectangles.pop())
            self.update_display()
            log_to_console(self, "Undid last ROI")

    def redo_last_roi(self):
        if self.redo_stack:
            self.roi_rectangles.append(self.redo_stack.pop())
            self.update_display()
            log_to_console(self, "Redid last ROI")

    def save_to_excel(self):
        if not self.get_location() or not self.get_type():
            log_to_console(self, "Location and Type fields cannot be empty.")
            return

        hticks = self.horizontal_ticks
        vticks = self.vertical_ticks

        horizontal_tick_values = self.tick_values.get("horizontal", ["", ""])
        vertical_tick_values = self.tick_values.get("vertical", ["", ""])
        horizontal_units = self.tick_units.get("horizontal", "")
        vertical_units = self.tick_units.get("vertical", "")
        waveform_type = self.get_type()
        waveform_location = self.get_location()
        protocol = self.get_protocol()

        data = {
            "horizontal_tick1_px": [hticks[0][0] if len(hticks) > 0 else ""],
            "horizontal_tick1_py": [hticks[0][1] if len(hticks) > 0 else ""],
            "horizontal_tick2_px": [hticks[1][0] if len(hticks) > 1 else ""],
            "horizontal_tick2_py": [hticks[1][1] if len(hticks) > 1 else ""],
            "horizontal_tick1_value": [horizontal_tick_values[0]],
            "horizontal_tick2_value": [horizontal_tick_values[1]],
            "horizontal_units": [horizontal_units],

            "vertical_tick1_px": [vticks[0][0] if len(vticks) > 0 else ""],
            "vertical_tick1_py": [vticks[0][1] if len(vticks) > 0 else ""],
            "vertical_tick2_px": [vticks[1][0] if len(vticks) > 1 else ""],
            "vertical_tick2_py": [vticks[1][1] if len(vticks) > 1 else ""],
            "vertical_tick1_value": [vertical_tick_values[0]],
            "vertical_tick2_value": [vertical_tick_values[1]],
            "vertical_units": [vertical_units],

            "waveform_type": [waveform_type],
            "waveform_location": [waveform_location],
            "co_present": [self.co_present_var.get() if hasattr(self, "co_present_var") else ""],

            "location_free_text": [self.get_location()],
            "protocol_free_text": [self.get_protocol()],
        }

        df = pd.DataFrame(data)
        base_filename = os.path.splitext(os.path.basename(self.current_file))[0]
        output_dir = os.path.dirname(self.current_file)
        excel_path = os.path.join(output_dir, f"{base_filename}.xlsx")
        df.to_excel(excel_path, index=False)
        log_to_console(self, f"Saved calibration and metadata to: {excel_path}")
