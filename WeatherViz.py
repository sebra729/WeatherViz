import sys
import maya.OpenMaya as OpenMaya;
import maya.OpenMayaMPx as OpenMayaMPx;
import maya.cmds as c;


def slider_drag_callback(*args):
	valueGravity = c.floatSliderGrp('testSlider', query=True, value=True);
	#print valueGravity;
	valueR = c.floatSliderGrp('slider', query=True, value=True);
	
	c.gravity('gravity', e=True, magnitude= valueGravity);
	c.collision('flore', e=True, r= valueR);
	#c.radioButton('rb1', e=True, enable= False);
	'''
	c.move(value,2.5,0,'shaft');
	c.move(2 + value,0,0,'ball1');
	c.move(-2 + value,0,0,'ball2');
	c.move(value,5,0,'glance');
	'''


kPluginCmdName = "WeatherViz"

# Command
class scriptedCommand(OpenMayaMPx.MPxCommand):
	def __init__(self):
		OpenMayaMPx.MPxCommand.__init__(self);
        
    # Invoked when the command is run.
	def doIt(self, argList):
		print 'Starting WeatherViz';
		
		self.spawn();
		
		weatherUI = WeatherUI();
		weatherUI.init();
		
	def spawn(self):
		'''
		c.polySphere(name='ball1');
		c.move(2,0,0);
		c.polySphere(name='ball2');
		c.move(-2,0,0);
		c.polyCylinder(name='shaft',h=5);
		c.move(0,2.5,0,'shaft');
		c.polySphere(name='glance');
		c.move(0,5,0);
		'''
		c.file('C:/Users/Sebastian/Documents/maya/projects/default/data/Cobblestones3/Files/untitled.fbx', type='FBX', ra=True, mergeNamespacesOnClash=False, namespace='Beach', options='fbx',  i=True);
		
		c.polyPlane(name = 'emmiterPlane', w=10, h=10);
		c.move(0, 10, 0);
		c.polyPlane(name = 'flore', w=15, h=15);
		
		c.emitter( dx=0, dy=-1, dz=0, sp=0.33, pos=(1, 1, 1), n='myEmitter', type='omni');
		c.particle( n='emittedParticles' );
		c.connectDynamic( 'emittedParticles', em='myEmitter' );
		c.addDynamic( 'emmiterPlane', 'myEmitter' );
		
		c.gravity(name = 'gravity');
		c.connectDynamic( 'emittedParticles', f = 'gravity' );
		
		c.collision('flore', f=0.05, r=0.3);
		c.connectDynamic('emittedParticles', c = 'flore');

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
		window = c.window(title='WeatherViz',widthHeight=(400,600));
		#form = c.formLayout(numberOfDivisions=10);
		c.rowColumnLayout(numberOfColumns=1);
		#c.textField();
		#c.intSlider(min=-100,max=100,value=0,step=1,width=200);
		c.floatSliderGrp('testSlider',label='Gravity', field=True, value=0, dc=slider_drag_callback, min=-10, max=10);
		c.floatSliderGrp('slider',label='Collision Resilience', field=True, value=0.3, dc=slider_drag_callback, min=0, max=1);
		c.radioCollection();
		c.radioButton('rb1', label='One', dpc=slider_drag_callback);
		c.radioButton('rb2', label='Two', dpc=slider_drag_callback);
		#c.formLayout(form, edit=True, attachForm=[(s1, 'top', 5), (s2, 5)]);
		c.showWindow(window);
		

