def classFactory(iface):
    # Load the plugin class from gpx_to_spacetime_cube.py
    from .gpx_to_spacetime_cube import GPXToSpaceTimeCube
    return GPXToSpaceTimeCube(iface)
