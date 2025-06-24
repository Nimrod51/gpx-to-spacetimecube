from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsVectorLayer
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import datetime
from qgis.core import QgsWkbTypes

# Path to input GPX file
file_path = '/home/ngavish/Downloads/10km_waldheim.gpx'

# Load GPX track points as a QgsVectorLayer
uri = f"{file_path}|layername=track_points"
layer = QgsVectorLayer(uri, "GPX Track Points", "ogr")
if not layer.isValid():
    print("invalid gpx file!")


lons, lats, times = [], [], []

for feat in layer.getFeatures():
    geom = feat.geometry()
    if not geom.isEmpty():
        point = geom.asPoint()
        lons.append(point.x())
        lats.append(point.y())

        qdatetime = feat.attribute('time')
        if qdatetime and hasattr(qdatetime, 'toPyDateTime'):
            dt = qdatetime.toPyDateTime()
            times.append(dt.timestamp())



# Create 3D scatter plot with Matplotlib
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(lons, lats, times, c='blue', marker='o')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Time (seconds since epoch)')

# Save plot image
out_path = os.path.splitext(file_path)[0] + "_plot.png"
try:
    fig.savefig(out_path)
except Exception as e:
    QMessageBox.critical(self.iface.mainWindow(),
                         "Error",
                         f"Failed to save plot: {e}")
plt.close(fig)
