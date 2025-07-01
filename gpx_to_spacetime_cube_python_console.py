from qgis.core import QgsVectorLayer
from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import os

# ───── CONFIGURATION ───────────────────────────────────────────
TIME_UNIT = "minutes"  # Options: "minutes", "seconds"
MAX_TRACK_POINTS = 5000
# ───────────────────────────────────────────────────────────────

# Resolve relative GPX path
base_dir = os.path.dirname(__file__) if "__file__" in globals() else os.getcwd()
file_path = os.path.join(base_dir, "sample data", "AaseeLoop.gpx")

# Load track point layer from GPX
uri = f"{file_path}|layername=track_points"
layer = QgsVectorLayer(uri, "GPX Track Points", "ogr")

if not layer.isValid():
    raise RuntimeError("GPX file could not be loaded or is invalid.")

# Parse coordinates and timestamps
lons, lats, raw_times = [], [], []
for feat in layer.getFeatures():
    geom = feat.geometry()
    if geom.isEmpty():
        continue
    pt = geom.asPoint()
    lons.append(pt.x())
    lats.append(pt.y())
    qdt = feat.attribute("time")
    if qdt and hasattr(qdt, "toPyDateTime"):
        raw_times.append(qdt.toPyDateTime().timestamp())

# Basic validation
if not raw_times or len(raw_times) != len(lons):
    raise RuntimeError("No valid timestamped points found in GPX track.")

# Warn if the GPX is large
if len(raw_times) > MAX_TRACK_POINTS:
    QMessageBox.warning(
        None,
        "Large GPX Track",
        f"Track contains {len(raw_times)} points.\nThis may affect performance.",
    )

# Compute elapsed time (relative to start)
t0 = raw_times[0]
elapsed = [(t - t0) for t in raw_times]
if TIME_UNIT == "minutes":
    elapsed = [e / 60.0 for e in elapsed]
unit_label = TIME_UNIT

# Plot 3D trajectory
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.scatter(lons, lats, elapsed, c="blue", marker="o")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_zlabel(f"Time (elapsed {unit_label})")

# Show inside QDialog
canvas = FigureCanvas(fig)
dlg = QDialog(iface.mainWindow())
dlg.setWindowTitle("3D Space‑Time Cube")
layout = QVBoxLayout()
layout.addWidget(canvas)
dlg.setLayout(layout)
dlg.resize(800, 600)
dlg.exec_()

# Save plot
out_path = os.path.splitext(file_path)[0] + "_plot.png"
try:
    fig.savefig(out_path)
    print(f"Plot saved to: {out_path}")
except Exception as e:
    print(f"Error saving plot: {e}")

plt.close(fig)