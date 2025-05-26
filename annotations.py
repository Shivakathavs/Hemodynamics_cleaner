from PIL import ImageDraw

def draw_annotations(image_pil, app):
    draw = ImageDraw.Draw(image_pil)

    # Draw horizontal ticks
    if hasattr(app, "horizontal_ticks"):
        for idx, (x, y) in enumerate(app.horizontal_ticks):
            draw.ellipse((x-5, y-5, x+5, y+5), fill="blue", outline="black")
            draw.text((x+6, y-6), f"H{idx+1}", fill="blue")

    # Draw vertical ticks
    if hasattr(app, "vertical_ticks"):
        for idx, (x, y) in enumerate(app.vertical_ticks):
            draw.ellipse((x-5, y-5, x+5, y+5), fill="green", outline="black")
            draw.text((x+6, y-6), f"V{idx+1}", fill="green")

    # Draw ROI rectangles
    if hasattr(app, "roi_rectangles"):
        for rect in app.roi_rectangles:
            x0, y0, x1, y1, mode = rect
            color = "red" if mode == "ECG" else "blue"
            draw.rectangle([x0, y0, x1, y1], outline=color, width=2)
            draw.text((x0, y0-12), mode, fill=color)

    # Display free-text boxes if filled
    if hasattr(app, "location_entry") and hasattr(app, "type_entry"):
        loc = app.location_entry.get().strip()
        typ = app.type_entry.get().strip()
        draw.text((10, 10), f"Location: {loc}", fill="purple")
        draw.text((10, 30), f"Type: {typ}", fill="purple")

    return image_pil
