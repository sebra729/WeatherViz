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
		
		#self.penis();
		
		weatherUI = WeatherUI();
		weatherUI.init();
		weatherUI.setupSky();
		
	def penis(self):
		c.polySphere(name='ball1');
		c.move(2,0,0);
		c.polySphere(name='ball2');
		c.move(-2,0,0);
		c.polyCylinder(name='shaft',h=5);
		c.move(0,2.5,0,'shaft');
		c.polySphere(name='glance');
		c.move(0,5,0);
		c.select(cl=True);
		c.emitter(n='emit',type='dir',r=100,sro=0,nuv=0,cye='none',cyi=1,spd=1,srn=0,nsp=1,tsp=0,mxd=0,mnd=0,dx=0,dy=1,dz=0,sp=0.2);
		c.particle(n='particle');
		c.connectDynamic('particle',em='emit');
		c.move(0,5.5,0,'emit');
		c.select(cl=True);
		
		#-pos 0 0 0 -type omni -r 100 -sro 0 -nuv 0 -cye none -cyi 1 -spd 1 -srn 0 -nsp 1 -tsp 0 -mxd 0 -mnd 0 -dx 1 -dy 0 -dz 0 -sp 0 ;
		
		

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
		self.snow = Snow();
	
	def init(self):
		window = c.window(title='WeatherViz',widthHeight=(400,600));
		c.formLayout(numberOfDivisions=10);
		#c.textField();
		#c.intSlider(min=-100,max=100,value=0,step=1,width=200);
		c.checkBox('snowCheck',label='Snow', onc=self.snowOn, ofc=self.snowOff);
		c.showWindow(window);
		
	def setupSky(self):
		c.polyPlane(h=30,w=30,n='emitPlane');
		c.move(0,20,0,'emitPlane');
		
	def snowOn(self,*args):
		self.snow.init();
		
	def snowOff(self,*args):
		print 'remove';	
	

class Snow():
	
	def __init__(self):
		pass;
	
	def init(self):
		c.select('emitPlane');
		c.emitter(n='snowEmitter',type='surf',r=100,sro=0,nuv=0,cye='none',cyi=1,spd=1,srn=0,nsp=1,tsp=0,mxd=0,mnd=0,dx=0,dy=-1,dz=0,sp=1);
		c.particle(n='snowParticle');
		c.select(cl=True);
		c.gravity(n='gravity',m=0.5);
		c.select(cl=True);
		c.turbulence(n='turb',m=5);
		c.connectDynamic('snowParticle',em='snowEmitter');
		c.connectDynamic('snowParticle',f='gravity');
		c.connectDynamic('snowParticle',f='turb');
		c.select(cl=True);

class Rain():
	
	def __init__(self):
		pass;
		
	def init(self):
		pass;
