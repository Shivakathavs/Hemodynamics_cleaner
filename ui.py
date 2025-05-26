import tkinter as tk
from tkinter import ttk, Text, Scrollbar, WORD, BOTH, RIGHT, Y, LEFT, X, VERTICAL, HORIZONTAL, Canvas, Frame, TOP

def setup_ui(app, img_width=1200, img_height=900):
    app.display_width = img_width
    app.display_height = img_height

    app.root.geometry(f"{img_width+100}x{img_height+300}")
    app.root.minsize(img_width, img_height)

    app.main_paned = ttk.PanedWindow(app.root, orient=VERTICAL)
    app.main_paned.pack(fill=BOTH, expand=True)

    app.image_panel = Frame(app.main_paned)
    app.main_paned.add(app.image_panel, weight=4)

    app.canvas = Canvas(app.image_panel, width=img_width, height=img_height, bg="gray")
    app.canvas.grid(row=0, column=0, sticky="nsew")
    app.h_scroll = Scrollbar(app.image_panel, orient=HORIZONTAL, command=app.canvas.xview)
    app.h_scroll.grid(row=1, column=0, sticky="ew")
    app.v_scroll = Scrollbar(app.image_panel, orient=VERTICAL, command=app.canvas.yview)
    app.v_scroll.grid(row=0, column=1, sticky="ns")
    app.canvas.configure(xscrollcommand=app.h_scroll.set, yscrollcommand=app.v_scroll.set)

    app.image_panel.grid_rowconfigure(0, weight=1)
    app.image_panel.grid_columnconfigure(0, weight=1)

    app.control_panel = ttk.Frame(app.main_paned)
    app.main_paned.add(app.control_panel, weight=1)

    button_canvas = Canvas(app.control_panel, height=80)
    button_scroll = Scrollbar(app.control_panel, orient=HORIZONTAL, command=button_canvas.xview)
    button_frame = ttk.Frame(button_canvas)

    button_frame.bind("<Configure>", lambda e: button_canvas.configure(scrollregion=button_canvas.bbox("all")))
    button_canvas.create_window((0, 0), window=button_frame, anchor="nw")
    button_canvas.configure(xscrollcommand=button_scroll.set)
    button_canvas.pack(fill=X, expand=False, side=TOP)
    button_scroll.pack(fill=X, side=TOP)

    ttk.Button(button_frame, text="Add Horizontal Ticks", command=lambda: app.set_tick_mode("horizontal")).pack(side=LEFT, padx=2)
    ttk.Button(button_frame, text="Add Vertical Ticks", command=lambda: app.set_tick_mode("vertical")).pack(side=LEFT, padx=2)

    ttk.Button(button_frame, text="ECG ROI", command=lambda: app.start_roi_mode("ECG")).pack(side=LEFT, padx=2)
    ttk.Button(button_frame, text="Waveform ROI", command=lambda: app.start_roi_mode("Waveform")).pack(side=LEFT, padx=2)
    ttk.Button(button_frame, text="Save All ROIs", command=app.save_all_rois).pack(side=LEFT, padx=2)
    ttk.Button(button_frame, text="Undo ROI", command=app.undo_last_roi).pack(side=LEFT, padx=2)
    ttk.Button(button_frame, text="Redo ROI", command=app.redo_last_roi).pack(side=LEFT, padx=2)

    app.save_horizontal_ticks_btn = ttk.Button(button_frame, text="Save Horizontal Ticks", command=app.save_horizontal_ticks, state='disabled')
    app.save_horizontal_ticks_btn.pack(side=LEFT, padx=2)
    app.clear_horizontal_ticks_btn = ttk.Button(button_frame, text="Clear Horizontal Ticks", command=app.clear_horizontal_ticks, state='disabled')
    app.clear_horizontal_ticks_btn.pack(side=LEFT, padx=2)
    ttk.Label(button_frame, text="First Horz Tick:").pack(side=LEFT, padx=2)
    app.horz_tick1_entry = ttk.Entry(button_frame, width=5, state='disabled')
    app.horz_tick1_entry.pack(side=LEFT, padx=2)
    ttk.Label(button_frame, text="Second Horz Tick:").pack(side=LEFT, padx=2)
    app.horz_tick2_entry = ttk.Entry(button_frame, width=5, state='disabled')
    app.horz_tick2_entry.pack(side=LEFT, padx=2)
    ttk.Label(button_frame, text="Horizontal Units:").pack(side=LEFT, padx=2)
    app.horizontal_units_entry = ttk.Entry(button_frame, width=5, state='disabled')
    app.horizontal_units_entry.pack(side=LEFT, padx=2)

    app.save_vertical_ticks_btn = ttk.Button(button_frame, text="Save Vertical Ticks", command=app.save_vertical_ticks, state='disabled')
    app.save_vertical_ticks_btn.pack(side=LEFT, padx=2)
    app.clear_vertical_ticks_btn = ttk.Button(button_frame, text="Clear Vertical Ticks", command=app.clear_vertical_ticks, state='disabled')
    app.clear_vertical_ticks_btn.pack(side=LEFT, padx=2)
    ttk.Label(button_frame, text="First Vert Tick:").pack(side=LEFT, padx=2)
    app.vert_tick1_entry = ttk.Entry(button_frame, width=5, state='disabled')
    app.vert_tick1_entry.pack(side=LEFT, padx=2)
    ttk.Label(button_frame, text="Second Vert Tick:").pack(side=LEFT, padx=2)
    app.vert_tick2_entry = ttk.Entry(button_frame, width=5, state='disabled')
    app.vert_tick2_entry.pack(side=LEFT, padx=2)
    ttk.Label(button_frame, text="Vertical Units:").pack(side=LEFT, padx=2)
    app.vertical_units_entry = ttk.Entry(button_frame, width=5, state='disabled')
    app.vertical_units_entry.pack(side=LEFT, padx=2)

    ttk.Button(button_frame, text="Crop Region", command=app.start_crop).pack(side=LEFT, padx=2)
    ttk.Button(button_frame, text="Rotate +90°", command=lambda: app.rotate_image(90)).pack(side=LEFT, padx=2)
    ttk.Button(button_frame, text="Rotate -90°", command=lambda: app.rotate_image(-90)).pack(side=LEFT, padx=2)
    ttk.Button(button_frame, text="Rotate +0.5°", command=lambda: app.rotate_image(0.5)).pack(side=LEFT, padx=2)
    ttk.Button(button_frame, text="Rotate -0.5°", command=lambda: app.rotate_image(-0.5)).pack(side=LEFT, padx=2)
    ttk.Button(button_frame, text="Eraser", command=app.start_erase).pack(side=LEFT, padx=2)

    nav_frame = ttk.Frame(app.control_panel)
    nav_frame.pack(fill=X, pady=5)
    ttk.Button(nav_frame, text="Previous", command=app.previous_image).pack(side=LEFT, padx=2)
    ttk.Button(nav_frame, text="Next", command=app.next_image).pack(side=LEFT, padx=2)

    app.progress_label = ttk.Label(app.control_panel, text="Ready to start")
    app.progress_label.pack(fill=X, padx=5, pady=2)

    app.console_paned = ttk.PanedWindow(app.control_panel, orient=VERTICAL)
    app.console_paned.pack(fill=BOTH, expand=True)
    app.log_frame = ttk.Frame(app.console_paned)
    app.console_paned.add(app.log_frame, weight=1)

    app.log_text = Text(app.log_frame, height=10, width=80, wrap=WORD)
    app.log_scroll = Scrollbar(app.log_frame, command=app.log_text.yview)
    app.log_text.configure(yscrollcommand=app.log_scroll.set)
    app.log_scroll.pack(side=RIGHT, fill=Y)
    app.log_text.pack(side=LEFT, fill=BOTH, expand=True)

    # Location and Type metadata inputs
    meta_frame = ttk.Frame(app.control_panel)
    meta_frame.pack(fill=X, padx=5, pady=5)
    ttk.Label(meta_frame, text="Location:").pack(side=LEFT, padx=2)
    app.location_entry = ttk.Entry(meta_frame, width=20)
    app.location_entry.pack(side=LEFT, padx=2)
    ttk.Label(meta_frame, text="Type:").pack(side=LEFT, padx=2)
    app.type_entry = ttk.Entry(meta_frame, width=20)
    app.type_entry.pack(side=LEFT, padx=2)

    # Save location/type values to app attributes
    app.get_location = lambda: app.location_entry.get().strip()
    app.get_type = lambda: app.type_entry.get().strip()

    from events import bind_events
    bind_events(app)
    setup_styles(app)

def setup_styles(app):
    style = ttk.Style()
    style.configure('Split.TButton', foreground='red')
    style.configure('Horizontal.TButton', foreground='blue')
    style.configure('Vertical.TButton', foreground='green')
