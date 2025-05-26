import tkinter as tk
from tkinter import ttk, filedialog
from events import bind_events

def setup_ui(app, width, height):
    # --- Frame setup ---
    app.frame = tk.Frame(app.root)
    app.frame.pack(fill="both", expand=True)

    # --- Canvas for image display ---
    app.canvas = tk.Canvas(app.frame, bg="black", width=width, height=height)
    app.canvas.grid(row=0, column=0, rowspan=12, columnspan=6, sticky="nsew", padx=5, pady=5)

    # --- Log textbox ---
    app.log_text = tk.Text(app.frame, height=8, width=60, wrap="word")
    app.log_text.grid(row=13, column=0, columnspan=6, sticky="ew", padx=5, pady=5)
    app.log_text.insert("end", "Welcome! Use the buttons to begin annotating.\n")

    # --- Progress/Status label ---
    app.progress_label = tk.Label(app.frame, text="Ready")
    app.progress_label.grid(row=14, column=0, columnspan=6, sticky="w", padx=5, pady=2)

    # --- Navigation Buttons ---
    btn_prev = tk.Button(app.frame, text="Previous Image", command=app.previous_image)
    btn_prev.grid(row=0, column=7, sticky="ew")
    btn_next = tk.Button(app.frame, text="Next Image", command=app.next_image)
    btn_next.grid(row=0, column=8, sticky="ew")

    # --- Crop/ROI Buttons ---
    btn_crop = tk.Button(app.frame, text="Crop", command=app.start_crop)
    btn_crop.grid(row=1, column=7, sticky="ew")
    btn_ecg = tk.Button(app.frame, text="ROI: ECG", command=lambda: app.start_roi_mode("ECG"))
    btn_ecg.grid(row=1, column=8, sticky="ew")
    btn_wave = tk.Button(app.frame, text="ROI: Waveform", command=lambda: app.start_roi_mode("Waveform"))
    btn_wave.grid(row=2, column=8, sticky="ew")

    # --- Tick mark buttons ---
    btn_h_tick = tk.Button(app.frame, text="Horizontal Tick", command=lambda: app.set_tick_mode("horizontal"))
    btn_h_tick.grid(row=3, column=7, sticky="ew")
    btn_v_tick = tk.Button(app.frame, text="Vertical Tick", command=lambda: app.set_tick_mode("vertical"))
    btn_v_tick.grid(row=3, column=8, sticky="ew")

    # --- Eraser and Undo/Redo Buttons ---
    btn_erase = tk.Button(app.frame, text="Eraser", command=app.start_erase)
    btn_erase.grid(row=4, column=7, sticky="ew")
    btn_undo = tk.Button(app.frame, text="Undo ROI", command=app.undo_last_roi)
    btn_undo.grid(row=4, column=8, sticky="ew")
    btn_redo = tk.Button(app.frame, text="Redo ROI", command=app.redo_last_roi)
    btn_redo.grid(row=5, column=8, sticky="ew")

    # --- Rotation Buttons ---
    btn_rotate_left = tk.Button(app.frame, text="Rotate Left", command=lambda: app.rotate_image(-5))
    btn_rotate_left.grid(row=5, column=7, sticky="ew")
    btn_rotate_right = tk.Button(app.frame, text="Rotate Right", command=lambda: app.rotate_image(5))
    btn_rotate_right.grid(row=6, column=7, sticky="ew")

    # --- Save Buttons and Excel ---
    btn_save_rois = tk.Button(app.frame, text="Save All ROIs", command=app.save_all_rois)
    btn_save_rois.grid(row=6, column=8, sticky="ew")
    btn_save_excel = tk.Button(app.frame, text="Save to Excel", command=app.save_to_excel)
    btn_save_excel.grid(row=7, column=8, sticky="ew")

    # --- Free text Entry: Location & Protocol ---
    tk.Label(app.frame, text="Location:").grid(row=7, column=6, sticky="e")
    app.location_entry = tk.Entry(app.frame, width=20)
    app.location_entry.grid(row=7, column=7, sticky="w")
    tk.Label(app.frame, text="Protocol (rest/exercise):").grid(row=8, column=6, sticky="e")
    app.protocol_entry = tk.Entry(app.frame, width=20)
    app.protocol_entry.grid(row=8, column=7, sticky="w")

    # --- Tick Entry Widgets ---
    tk.Label(app.frame, text="Horiz Tick 1:").grid(row=9, column=6, sticky="e")
    app.horz_tick1_entry = tk.Entry(app.frame, width=8)
    app.horz_tick1_entry.grid(row=9, column=7, sticky="w")
    tk.Label(app.frame, text="Horiz Tick 2:").grid(row=10, column=6, sticky="e")
    app.horz_tick2_entry = tk.Entry(app.frame, width=8)
    app.horz_tick2_entry.grid(row=10, column=7, sticky="w")
    tk.Label(app.frame, text="Horiz Units:").grid(row=11, column=6, sticky="e")
    app.horizontal_units_entry = tk.Entry(app.frame, width=8)
    app.horizontal_units_entry.grid(row=11, column=7, sticky="w")
    app.save_horizontal_ticks_btn = tk.Button(app.frame, text="Save Horiz Ticks", command=app.save_horizontal_ticks, state="disabled")
    app.save_horizontal_ticks_btn.grid(row=9, column=8, sticky="ew")
    app.clear_horizontal_ticks_btn = tk.Button(app.frame, text="Clear Horiz Ticks", command=app.clear_horizontal_ticks, state="disabled")
    app.clear_horizontal_ticks_btn.grid(row=10, column=8, sticky="ew")

    tk.Label(app.frame, text="Vert Tick 1:").grid(row=9, column=4, sticky="e")
    app.vert_tick1_entry = tk.Entry(app.frame, width=8)
    app.vert_tick1_entry.grid(row=9, column=5, sticky="w")
    tk.Label(app.frame, text="Vert Tick 2:").grid(row=10, column=4, sticky="e")
    app.vert_tick2_entry = tk.Entry(app.frame, width=8)
    app.vert_tick2_entry.grid(row=10, column=5, sticky="w")
    tk.Label(app.frame, text="Vert Units:").grid(row=11, column=4, sticky="e")
    app.vertical_units_entry = tk.Entry(app.frame, width=8)
    app.vertical_units_entry.grid(row=11, column=5, sticky="w")
    app.save_vertical_ticks_btn = tk.Button(app.frame, text="Save Vert Ticks", command=app.save_vertical_ticks, state="disabled")
    app.save_vertical_ticks_btn.grid(row=9, column=3, sticky="ew")
    app.clear_vertical_ticks_btn = tk.Button(app.frame, text="Clear Vert Ticks", command=app.clear_vertical_ticks, state="disabled")
    app.clear_vertical_ticks_btn.grid(row=10, column=3, sticky="ew")

    # Configure column/row weights for resizing
    for col in range(9):
        app.frame.grid_columnconfigure(col, weight=1)
    for row in range(15):
        app.frame.grid_rowconfigure(row, weight=1)

    # --- Bind events for interactivity (mouse, keys, etc.) ---
    bind_events(app)
