import os

def find_all_images(directory=".", exts=None):
    if exts is None:
        exts = [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]
    image_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in exts):
                image_files.append(os.path.join(root, file))
    return sorted(image_files)

def log_to_console(app, msg):
    if hasattr(app, "log_text") and app.log_text:
        app.log_text.insert("end", str(msg) + "\n")
        app.log_text.see("end")
    print(msg)

def update_progress(app):
    if hasattr(app, "progress_label") and app.progress_label:
        status = []
        if hasattr(app, "split_points"):
            status.append(f"Splits: {len(app.split_points)}")
        if hasattr(app, "horizontal_ticks"):
            status.append(f"HorizTicks: {len(app.horizontal_ticks)}")
        if hasattr(app, "vertical_ticks"):
            status.append(f"VertTicks: {len(app.vertical_ticks)}")
        # Add images remaining
        if hasattr(app, "image_files") and hasattr(app, "current_index"):
            remaining = len(app.image_files) - app.current_index
            status.append(f"Images left: {remaining}")
        app.progress_label.config(text=" | ".join(status))

def log_images_remaining(app):
    remaining = len(app.image_files) - app.current_index
    msg = f"{remaining} images remaining to be analyzed."
    log_to_console(app, msg)
    # Also update the progress label
    update_progress(app)

def log_images_found(app):
    total = len(app.image_files)
    log_to_console(app, f"{total} images found in the directory: {app.image_dir}")
    log_images_remaining(app)
