WeatherViz
==========

1. Run script below in Maya script editor

import maya.cmds as cmds
maya.cmds.unloadPlugin("WeatherViz.py")
cmds.loadPlugin( 'WeatherViz.py' )
cmds.WeatherViz()

OBS! If maya fails to run the scipt, run the script below, clean the scene and
rerun the script in 1.

import maya.mel as mel;
mel.eval('setCurrentRenderer mentalRay;');
ibl = c.createNode( 'mentalrayIblShape', n='myIbl' );
c.rename('mentalrayIbl1', 'myIblShape');
c.evalDeferred( "c.connectAttr(  ibl+'.message', 'mentalrayGlobals.imageBasedLighting', f=True)", lp=True);
mel.eval('$path = "C:/path_to_IBL_scene/image.exr"');