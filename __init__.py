# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GPXtoSpaceTimeCube
                                 A QGIS plugin
 This tool transformes a GPX to a space Time Cube
                             -------------------
        begin                : 2017-08-12
        copyright            : (C) 2017 by Nimrod Gavish
        email                : n_gavi01@wwu.de
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load GPXtoSpaceTimeCube class from file GPXtoSpaceTimeCube.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .GPX_SpaceTimeCube import GPXtoSpaceTimeCube
    return GPXtoSpaceTimeCube(iface)
