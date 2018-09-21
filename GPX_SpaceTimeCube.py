# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GPXtoSpaceTimeCube
                                 A QGIS plugin
 This tool transformes a GPX to a space Time Cube
                              -------------------
        begin                : 2017-08-12
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Nimrod Gavish
        email                : n_gavi01@wwu.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from GPX_SpaceTimeCube_dialog import GPXtoSpaceTimeCubeDialog
import os.path


class GPXtoSpaceTimeCube:
    """QGIS Plugin Implementation."""
    gpx_path=""
    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'GPXtoSpaceTimeCube_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&GPXtoSpaceTimeCube')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'GPXtoSpaceTimeCube')
        self.toolbar.setObjectName(u'GPXtoSpaceTimeCube')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('GPXtoSpaceTimeCube', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = GPXtoSpaceTimeCubeDialog()

        self.dlg.toolButton.clicked.connect(self.getGPXPath)
        self.dlg.pushButton.clicked.connect(self.RunAllCode)

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/GPXtoSpaceTimeCube/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Transforms GPX to Space Time Cube'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&GPXtoSpaceTimeCube'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def getGPXPath(self):
        from PyQt4.QtGui import QAction, QIcon, QFileDialog
        self.gpx_path = QFileDialog.getOpenFileName(self.dlg, "select","",'*.gpx')
        self.dlg.lineEdit.setText(self.gpx_path)

    def RunAllCode(self):
        import ogr, os
        import time, datetime
        import matplotlib as mpl
        from mpl_toolkits.mplot3d import Axes3D
        #import numpy as np
        import matplotlib.pyplot as plt

        if os.path.exists(self.gpx_path):
            gpx_path=self.gpx_path
        else:
            print "GPX path is not selected"
            self.dlg.status.setText("No file selected")
            self.dlg.status.setStyleSheet('background-color: red;')
            return
        
        #Open GPX
        in_path = os.path.join (gpx_path)
        in_driver= ogr.GetDriverByName("GPX")
        data_source = in_driver.Open(in_path,0)

        #Plot parameters
        mpl.rcParams ['legend.fontsize'] = 10
        fig = plt.figure()
        ax = fig.gca(projection='3d')

        #Create layer from data source
        if data_source is None:
            #print "Could not open %s" % (in_path)
            self.dlg.status.setText("Data source is invalid")
            self.dlg.status.setStyleSheet('background-color: red;')
        else:
            #print "Opened %s" % (in_path)
            layer = data_source.GetLayer(4) # 0 - waypoints, 1 - routes, 2 - tracks, 3 - route points, 4 - track points 
                    
        #Get time and spatial data from GPX dynamically and plot
        x=[] #Latitude
        y=[] #Latitude
        z=[] ##Time in minutes since start 
        elapsedTime=[] #Time in seconds since epoch
        DTArray=[] ##Array of python strings
        DateTimeArray=[] #Python datetime object of each point
        schema=[] #All field names

        ldefn = layer.GetLayerDefn()
        for n in range(ldefn.GetFieldCount()):
            fdefn = ldefn.GetFieldDefn(n)
            schema.append(fdefn.name)
        try:
            timeIndex=schema.index('time')
        except ValueError:
            #print "No time field found"
            self.dlg.status.setText("No time field found")
            self.dlg.status.setStyleSheet('background-color: red;')

        try:
            for feat in layer:
                pt = feat.geometry()
                x.append(pt.GetX())
                y.append(pt.GetY())
                dateTime=feat.GetField(timeIndex)
                try:
                    DT=datetime.datetime.strptime(dateTime, "%Y/%m/%d %H:%M:%S+00" )
                except ValueError:
                    DT=datetime.datetime.strptime(dateTime, "%Y/%m/%d %H:%M:%S.%f+00" )
                DateTimeArray.append(DT)
                SSE= time.mktime(DT.timetuple()) #Seconds since epoch
                elapsedTime.append(SSE)
                DTArray.append(DT.strftime("%H:%M:%S"))
        except TypeError:
            print "Time field does contain none or invalid dates"
            self.dlg.status.setText("Time field does contain none or invalid dates")
            self.dlg.status.setStyleSheet('background-color: red;')

        #Create sub title for plot
        title=DateTimeArray[0].strftime("%Y/%m/%d")+" " +DTArray[0]+" to " + DateTimeArray[-1].strftime("%Y/%m/%d")+" "+DTArray[-1]

        #Extract elapsed time in minutes 
        z.append(0) #First item in elapsedTime array should be 0 
        for i in range(1,len(elapsedTime)):
            z.append((elapsedTime[i]-elapsedTime[0])/60)

        #Plot X,Y,Z
        ax.plot(x,y,z)

        #Labels & Plot
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_zlabel('Time (Minutes)')
        ax.legend()
        plt.axis("equal")
        fig.suptitle('Space Time Cube', fontsize=12, fontweight='bold')
        plt.title(title,loc='center')
        plt.show()
        #Optionally save the image
        #plt.savefig("C:/Output/SpaceTime.jpg", dpi=100, format="jpg")
        #print "SUCCESS"
        self.dlg.status.setText("SUCCESS")
        self.dlg.status.setStyleSheet('background-color: green;')
                 

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
