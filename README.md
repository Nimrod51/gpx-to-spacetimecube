# GPX-To-SpaceTimeCube
This QGIS Plugin is able to transform a valid GPX file (with a time field) to a space time cube (QGIS Version 2.X). Uses Matplotlib and PyQGIS.  

You can run the script in two ways:    
1. As a QGIS 2.X Plugin (also available on: https://plugins.qgis.org/plugins/GPXToSpaceTimeCube/)  
2. As a standalone code in the QGIS Python Console 


## Example:
<img src="/spacetimeplot.gif?raw=true" width="500px">

******************************************
## Instructions for running as a QGIS Plugin: 

1. Clone or download this repository and place items in a folder, e.g. "GPXToSpaceTimeCube"

1. Copy folder to your QGIS plugin directory, on Windows this is typically:   

C:\Users\yourusername\\.qgis2\python\plugins  

2. Open QGIS and enable the tool from Plugins>Manage and Install Plugins> ☑ "GPXToSpaceTimeCube"   

3. Run the tool from the toolbar (ruby cube icon) and follow instructions on interface.   

**************************************
## Instructions as a standalone code in QGIS Python Console

Simply open the **GPXtoSpaceTimeCubePyConsole.py.py**	file in the root directory in the [QGIS Python Console](https://docs.qgis.org/2.18/en/docs/user_manual/plugins/python_console.html), and change the input path to the GPX file and run the code.

