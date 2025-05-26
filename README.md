# Medical Image Processor

A modular, Tkinter-based application for visualizing, annotating, and splitting medical images.

## 📂 Project Structure

```
medical_image_processor/
├── app.py              # Main entry point
├── config.json         # Configuration settings (paths, UI, etc.)
├── image_logic.py      # Image loading, splitting, rotation, crop logic
├── events.py           # Mouse/keyboard events and operations
├── ui.py               # UI layout, styles, and control bindings
├── annotations.py      # Drawing lines, ticks, overlays
├── file_utils.py       # Logging, progress update, image search
```

## ✅ Features

- Click to place horizontal red split lines.
- Full-width overlays exactly where clicked.
- Crop, rotate, erase, and annotate images.
- Export split parts and log activity.
- Save data to Excel automatically.

## ▶️ How to Run

```bash
# From command line
python app.py
```

or from JupyterLab:

```python
!python app.py
```

> Make sure your environment has Tkinter GUI support.

## 💾 Requirements

- Python 3.8+
- Packages:
  - `opencv-python`
  - `Pillow`
  - `pandas`

Install dependencies via pip:

```bash
pip install opencv-python Pillow pandas
```

## 🛠 Configuration

Edit `config.json` to change:

- Base image directory
- Output folder
- Default window size, title
- Eraser size

## 📑 License

This project is provided for academic and internal medical image processing use.

