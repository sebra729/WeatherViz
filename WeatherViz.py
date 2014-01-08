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
		self.rain = Rain();
	
	def init(self):
		window = c.window(title='WeatherViz',widthHeight=(400,600));
		form = c.formLayout(numberOfDivisions=100);
		c.checkBoxGrp('weatherPanel', label='Weather');
		c.checkBox('snowCheck', label='Snow', onc=self.snow.init, ofc=self.snow.remove, p='weatherPanel');
		c.checkBox('rainCheck', label='Rain', onc=self.rain.init, ofc=self.rain.remove, p='weatherPanel');
		c.button('collButton', label='Add collision', c=self.addCollision);
		tempSlider = c.floatSliderGrp('tempSilder',label='Temperature', field=True, value=0, dc=self.slider_drag_callback, min=-1, max=1);
		
		c.formLayout(form, edit=True, attachPosition=[(tempSlider, 'top', 20, 1)]);
		
		c.showWindow(window);
		
	def setupSky(self):
		c.polyPlane(h=30,w=30,n='emitPlane');
		c.polyNormal('emitPlane', nm=3 , n='polynormalReversed');
		c.move(0,20,0,'emitPlane');
		c.select(cl=True);
		
	def addCollision(self,*args):
		if c.particleExists('snowParticle'):
			self.snow.addCollision();
		if c.particleExists('rainParticle'):
			self.rain.addCollision();
			
			
	def slider_drag_callback(self,*args):
		value = c.floatSliderGrp('tempSilder', query=True, value=True);
		print value;
		#c.move(value,2.5,0,'lll');


class Snow():
	
	def __init__(self):
		pass;
	
	def init(WeatherUI,self):
		c.select('emitPlane');
		c.emitter(n='snowEmitter',type='surf',r=100,sro=0,nuv=0,cye='none',cyi=1,spd=1,srn=0,nsp=1,tsp=0,mxd=0,mnd=0,dx=0,dy=-1,dz=0,sp=1);
		c.particle(n='snowParticle');

		c.select(cl=True);
		c.setAttr( "snowParticle|snowParticleShape.particleRenderType", 8); # 1 ist for 8
		c.gravity(n='snowGravity',m=0.5);
		c.select(cl=True);
		c.turbulence(n='snowTurb',m=1);
		c.connectDynamic('snowParticle',em='snowEmitter');
		c.connectDynamic('snowParticle',f='snowGravity');
		c.connectDynamic('snowParticle',f='snowTurb');
		c.addAttr('snowParticleShape', ln='rgbPP', dt='vectorArray' );
		c.dynExpression('snowParticleShape', s='snowParticleShape.rgbPP = <<1.0, 1.0, 1.0>>', c=1);

		c.select(cl=True);
		
	def remove(WeatherUI,self):
		c.delete('snowEmitter','snowGravity','snowTurb','snowParticle');
		
	def addCollision(WeatherUI):
		objects = c.ls(sl=True);
		for i in range(0,len(objects)):
			c.collision(objects[i], f=1, r=0);
			c.connectDynamic('snowParticle', c=objects[i]);
			print objects[i];

class Rain():
	
	def __init__(self):
		pass;
		
	def init(WeatherUI,self):
		c.select('emitPlane');
		c.emitter(n='rainEmitter',type='surf',r=100,sro=0,nuv=0,cye='none',cyi=1,spd=1,srn=0,nsp=1,tsp=0,mxd=0,mnd=0,dx=0,dy=-1,dz=0,sp=1);
		c.particle(n='rainParticle');
		c.select(cl=True);
		c.gravity(n='rainGravity');
		c.select(cl=True);
		c.connectDynamic('rainParticle',em='rainEmitter');
		c.connectDynamic('rainParticle',f='rainGravity');
		c.select(cl=True);
		
	def remove(WeatherUI,self):
		c.delete('rainEmitter','rainGravity','rainParticle');
		
	def addCollision(WeatherUI):
		objects = c.ls(sl=True);
		for i in range(0,len(objects)):
			c.collision(objects[i], f=0.3, r=0.5);
			c.connectDynamic('rainParticle', c=objects[i]);
			print objects[i];
