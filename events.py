from file_utils import log_to_console, update_progress

def bind_events(app):
    """Bind all canvas and window events to their handlers"""
    app.canvas.bind("<Button-1>", lambda e: on_image_click(app, e))
    app.canvas.bind("<B1-Motion>", lambda e: on_image_drag(app, e))
    app.canvas.bind("<ButtonRelease-1>", lambda e: on_image_release(app, e))
    app.root.bind("<Configure>", lambda e: on_window_resize(app, e))
    app.root.bind("<Escape>", lambda e: cancel_operations(app))

def _canvas_to_image_coords(app, canvas_x, canvas_y):
    """Convert canvas coordinates to image coordinates"""
    if not hasattr(app, "rotated_image") or app.rotated_image is None:
        return 0, 0
    img_w = app.rotated_image.shape[1]
    img_h = app.rotated_image.shape[0]
    scale_x = app.displayed_image_width / img_w
    img_x = int(canvas_x / scale_x)
    img_y = int(canvas_y / scale_x)
    return img_x, img_y

def on_image_click(app, event):
    """Handle mouse click events on the image"""
    canvas_x = int(app.canvas.canvasx(event.x))
    canvas_y = int(app.canvas.canvasy(event.y))
    img_x, img_y = _canvas_to_image_coords(app, canvas_x, canvas_y)

    if app.drawing_mode == "erase":
        import cv2
        cv2.circle(app.cv_image, (img_x, img_y), 10, (255, 255, 255), -1)
        app.last_erase_point = (img_x, img_y)
    elif app.crop_mode and app.roi_mode:
        app.crop_start = (img_x, img_y)
        app.crop_rect = (img_x, img_y, img_x, img_y)
    
    if app.drawing_mode == "tick_horizontal":
        if len(app.horizontal_ticks) < 2:
            app.horizontal_ticks.append((img_x, img_y))
            log_to_console(app, f"Added horizontal tick at ({img_x}, {img_y})")
            app.update_display()
        if len(app.horizontal_ticks) == 2:
            app.drawing_mode = None
            app.horz_tick1_entry.config(state='normal')
            app.horz_tick2_entry.config(state='normal')
            app.horizontal_units_entry.config(state='normal')
            app.save_horizontal_ticks_btn.config(state='normal')
            app.clear_horizontal_ticks_btn.config(state='normal')

    elif app.drawing_mode == "tick_vertical":
        if len(app.vertical_ticks) < 2:
            app.vertical_ticks.append((img_x, img_y))
            log_to_console(app, f"Added vertical tick at ({img_x}, {img_y})")
            app.update_display()
        if len(app.vertical_ticks) == 2:
            app.drawing_mode = None
            app.vert_tick1_entry.config(state='normal')
            app.vert_tick2_entry.config(state='normal')
            app.vertical_units_entry.config(state='normal')
            app.save_vertical_ticks_btn.config(state='normal')
            app.clear_vertical_ticks_btn.config(state='normal')

    app.update_display()

def on_image_drag(app, event):
    """Handle mouse drag events on the image"""
    if not hasattr(app, "rotated_image") or app.rotated_image is None:
        return
    
    canvas_x = int(app.canvas.canvasx(event.x))
    canvas_y = int(app.canvas.canvasy(event.y))
    img_x, img_y = _canvas_to_image_coords(app, canvas_x, canvas_y)

    if app.drawing_mode == "erase" and hasattr(app, 'last_erase_point'):
        x1, y1 = app.last_erase_point
        x2, y2 = img_x, img_y
        app.last_erase_point = (x2, y2)
        import cv2
        cv2.line(app.cv_image, (x1, y1), (x2, y2), (255, 255, 255), 10)
    elif app.crop_mode and app.crop_start:
        x0, y0 = app.crop_start
        app.crop_rect = (x0, y0, img_x, img_y)

    app.update_display()

def on_image_release(app, event):
    """Handle mouse release events on the image"""
    if app.crop_mode and app.crop_start and app.crop_rect:
        x0, y0, x1, y1 = map(int, app.crop_rect)
        x0, x1 = sorted([x0, x1])
        y0, y1 = sorted([y0, y1])
        app.roi_rectangles.append((x0, y0, x1, y1, app.roi_mode))
        app.undo_stack.append((x0, y0, x1, y1, app.roi_mode))
        log_to_console(app, f"Added ROI ({app.roi_mode}): ({x0},{y0}) to ({x1},{y1})")
        app.crop_start = None
        app.crop_rect = None
        app.crop_mode = False
        app.roi_mode = None
        app.update_display()
        update_progress(app)

def on_window_resize(app, event):
    """Handle window resize events"""
    if app.cv_image is not None:
        app.update_display()

def cancel_operations(app):
    """Cancel all current operations"""
    app.crop_mode = False
    app.drawing_mode = None
    app.crop_start = None
    app.crop_rect = None
    app.roi_mode = None
    app.update_display()
