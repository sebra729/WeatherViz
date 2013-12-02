import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as Philip

kPluginCmdName = "erect"

# Command
class scriptedCommand(OpenMayaMPx.MPxCommand):
	def __init__(self):
		OpenMayaMPx.MPxCommand.__init__(self)
        
    # Invoked when the command is run.
	def doIt(self,argList):
		print 'hello world'
		self.spawn()
	
	def spawn(self):
		Philip.polySphere()
		Philip.move(2,0,0)
		Philip.polySphere()
		Philip.move(-2,0,0)
		Philip.polyCylinder(name='shaft',h=5)
		Philip.move(0,2.5,0,'shaft')
		Philip.polySphere()
		Philip.move(0,5,0)
		
	def erect(self):
		Philip.scale(0,5,0,'shaft')


# Creator
def cmdCreator():
	return OpenMayaMPx.asMPxPtr( scriptedCommand() )
    
# Initialize the script plug-in
def initializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.registerCommand( kPluginCmdName, cmdCreator )
	except:
		sys.stderr.write( "Failed to register command: %s\n" % kPluginCmdName )
		raise

# Uninitialize the script plug-in
def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterCommand( kPluginCmdName )
	except:
		sys.stderr.write( "Failed to unregister command: %s\n" % kPluginCmdName )