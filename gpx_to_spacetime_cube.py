from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox, QDialog, QVBoxLayout
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsVectorLayer, QgsProject
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import os

class GPXToSpaceTimeCube:
    def __init__(self, iface):
        self.iface = iface
        self.action = None

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), "logo.png")
        icon = QIcon(icon_path)
        self.action = QAction(icon, "GPX → Space-Time Cube", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&GPX Tools", self.action)


    def unload(self):
        self.iface.removePluginMenu("&GPX Tools", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        # ───── CONFIGURATION ──────────────────────────────────────
        TIME_UNIT = "minutes"  # "minutes" or "seconds"
        MAX_TRACK_POINTS = 5000
        # ──────────────────────────────────────────────────────────

        # Ask user for GPX file
        file_path, _ = QFileDialog.getOpenFileName(
            self.iface.mainWindow(),
            "Select GPX file",
            "",
            "GPX Files (*.gpx)"
        )
        if not file_path:
            return

        uri = f"{file_path}|layername=track_points"
        layer = QgsVectorLayer(uri, "GPX Track Points", "ogr")
        if not layer.isValid():
            QMessageBox.critical(self.iface.mainWindow(), "Error", "Failed to load GPX track points.")
            return

        QgsProject.instance().addMapLayer(layer)

        lons, lats, raw_times = [], [], []
        for feat in layer.getFeatures():
            geom = feat.geometry()
            if geom.isEmpty():
                continue
            pt = geom.asPoint()
            lons.append(pt.x())
            lats.append(pt.y())
            qdt = feat.attribute('time')
            if qdt and hasattr(qdt, 'toPyDateTime'):
                raw_times.append(qdt.toPyDateTime().timestamp())

        # Basic validation
        if not raw_times or len(raw_times) != len(lons):
            QMessageBox.warning(self.iface.mainWindow(), "Data Error", "No valid timestamped points found.")
            return

        # Warn for very large tracks
        if len(raw_times) > MAX_TRACK_POINTS:
            QMessageBox.warning(
                self.iface.mainWindow(),
                "Large GPX Track",
                f"Track contains {len(raw_times)} points.\nThis may affect performance."
            )

        # Compute elapsed time
        t0 = raw_times[0]
        elapsed = [(t - t0) for t in raw_times]
        if TIME_UNIT == "minutes":
            elapsed = [e / 60.0 for e in elapsed]
        unit_label = TIME_UNIT

        # Create 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(lons, lats, elapsed, c='blue', marker='o')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_zlabel(f'Time (elapsed {unit_label})')

        # Save plot
        out_path = os.path.splitext(file_path)[0] + "_plot.png"
        try:
            fig.savefig(out_path)
            QMessageBox.information(self.iface.mainWindow(), "Plot Saved", f"Saved to:\n{out_path}")
        except Exception as e:
            QMessageBox.critical(self.iface.mainWindow(), "Save Error", f"Failed to save plot:\n{e}")

        # Show in dialog
        canvas = FigureCanvas(fig)
        dlg = QDialog(self.iface.mainWindow())
        dlg.setWindowTitle("3D Space‑Time Cube")
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        dlg.setLayout(layout)
        dlg.resize(800, 600)
        dlg.exec_()

        plt.close(fig)
