import sys
import maya.OpenMaya as OpenMaya;
import maya.OpenMayaMPx as OpenMayaMPx;
import maya.cmds as c;

kPluginCmdName = "WeatherViz"

# Command
class scriptedCommand(OpenMayaMPx.MPxCommand):
	def __init__(self):
		OpenMayaMPx.MPxCommand.__init__(self);
        
    # Invoked when the command is run.
	def doIt(self, argList):
		print 'Starting WeatherViz';
		
		
		weatherUI = WeatherUI();
		weatherUI.init();


# Creator
def cmdCreator():
	return OpenMayaMPx.asMPxPtr(scriptedCommand());
    
# Initialize the script plug-in
def initializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject);
	try:
		mplugin.registerCommand(kPluginCmdName,cmdCreator);
	except:
		sys.stderr.write( 'Failed to register command: %s\n' % kPluginCmdName );
		raise

# Uninitialize the script plug-in
def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject);
	try:
		mplugin.deregisterCommand(kPluginCmdName);
	except:
		sys.stderr.write( 'Failed to unregister command: %s\n' % kPluginCmdName );
		
		
		
class WeatherUI():
	
	def __init__(self):
		pass;
	
	def init(self):
		window = c.window('weatherWindow',title='WeatherViz',widthHeight=(400,600));
		c.formLayout(numberOfDivisions=10);
		c.textField();
		c.intSlider(min=-100,max=100,value=0,step=1,width=200);
		c.showWindow(window);