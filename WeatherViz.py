import sys
import maya.OpenMaya as OpenMaya;
import maya.OpenMayaMPx as OpenMayaMPx;
import maya.cmds as c;
import maya.mel as mel;

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
		weatherUI.setUpSky();
		weatherUI.setUpModel();
		

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

		s1 = c.floatSliderGrp('snowTurb',label='Snow turbulence', field=True, value=5, dc=self.slider_drag_callback, min=0, max=10);
		c.formLayout(form, edit=True, attachPosition=[(s1, 'top', 20, 1)]);
		c.showWindow(window);
		
	def setUpModel(self):
		#c.file('C:/Users/Sebastian/Documents/maya/projects/default/data/Cobblestones3/Files/untitled.fbx', type='FBX', ra=True, mergeNamespacesOnClash=False, namespace='untitled', options='fbx',  i=True);	
		#name = 'C:\Users\Sebastian\Documents\maya\projects\default\sourceimages\exr\Location_1_1_hdr.exr';
		#sphere = c.polySphere(n='worldSphere', ax=[0, 0, 0], r=80);
		#shader = c.shadingNode('surfaceShader', asShader=True);
		#SG = c.sets(empty=True, renderable=True, noSurfaceShader=True, name=shader+"SG");
		#c.connectAttr(shader+'.outColor', SG+".surfaceShader", force=True);
		#img = c.shadingNode('file', asTexture=True);
		#c.setAttr(img+'.fileTextureName', name, type='string');
		#c.connectAttr(img+'.outColor', shader+'.outColor', force=True);
		#c.sets(sphere[0], edit=True, forceElement=SG);
		#c.setAttr(img+'.hdrMapping', 2);
		#c.setAttr(img+'.hdrExposure', 3);
		
		
		
		
		mel.eval('setCurrentRenderer mentalRay;');
		lbl = c.createNode( 'mentalrayIblShape', n='myIbl' );
		c.rename('mentalrayIbl1', 'myIblShape');
		c.evalDeferred( "c.connectAttr(  ibl+'.message', 'mentalrayGlobals.imageBasedLighting', f=True)", lp=True);
		mel.eval('$path = "C:/Users/Philip/Desktop/SKOLA/TNCG14/projekt/sIBL/Location_1_1_hdr.exr"');
		mel.eval('AEassignFilenameCB  myIbl.texture $path "image"');
		c.setAttr('myIbl.colorGain', 14, 14, 14, type='double3');
		#sets render stats
		c.setAttr('myIbl.visibleInEnvironment', 1);
		c.setAttr('myIbl.visibleInReflections', 1);
		c.setAttr('myIbl.visibleInRefractions', 1);
		c.setAttr('myIbl.visibleInFinalGather', 1);

		c.setAttr('myIblShape.scaleX', 100);
		c.setAttr('myIblShape.scaleY', 100);
		c.setAttr('myIblShape.scaleZ', 100);
		
		ground = c.polyPlane(h=100,w=100, n='groundPlane');
		
		alphaShader = c.shadingNode('lambert', asShader=True, n='alphaShader');
		SG2 = c.sets(empty=True, renderable=True, noSurfaceShader=True, name=alphaShader+"SG2");
		c.setAttr(alphaShader+'.transparency', 1, 1, 1, type="double3");
		c.select( 'groundPlane' );
		c.hyperShade( assign=alphaShader);
		
	def setUpSky(self):
		c.polyPlane( h=100,w=100,n='emitPlane');
		c.polyNormal('emitPlane', nm=3 , n='polynormalReversed');
		c.move(0,100,0,'emitPlane');
		c.select(cl=True);
		
	def addCollision(self,*args):
		if c.particleExists('snowParticle'):
			self.snow.addCollision();
		if c.particleExists('rainParticle'):
			self.rain.addCollision();
			
	def slider_drag_callback(*args):
		valueTurb = c.floatSliderGrp('snowTurb', query=True, value=True);
		print valueTurb;
		c.turbulence('snowTurb', e=True, m=valueTurb);

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
 		c.air(n='snowAir', m=5.0, mxd=20.0, pos=[0, 30, 0], vco=True);
		c.connectDynamic('snowParticle',f='snowAir');
		c.setAttr("particleCloud1.color", 1, 1, 1, type="double3");
		
		
	def remove(WeatherUI,self):
		c.delete('snowEmitter','snowGravity','snowTurb','snowParticle');
		
	def addCollision(WeatherUI):
		
		objects = c.ls(sl=True);
		for i in range(0,len(objects)):
			c.collision(objects[i], f=0.05, r=0);
			c.connectDynamic('snowParticle', c=objects[i]);
			print objects[i];

class Rain():
	
	def __init__(self):
		pass;
		
	def init(WeatherUI,self):
		c.select('emitPlane');
		c.emitter(n='rainEmitter',type='surf',r=300,sro=0,nuv=0,cye='none',cyi=1,spd=1,srn=0,nsp=1,tsp=0,mxd=0,mnd=0,dx=0,dy=-1,dz=0,sp=1);
		c.particle(n='rainParticle');
		
		c.select(cl=True);
		c.setAttr( "rainParticle|rainParticleShape.particleRenderType", 6); # rainParticleShape/render Attributes
		c.gravity(n='rainGravity');
		c.select(cl=True);
		c.connectDynamic('rainParticle',em='rainEmitter');
		c.connectDynamic('rainParticle',f='rainGravity');
		c.addAttr('rainParticleShape', ln='rgbPP', dt='vectorArray' );
		c.dynExpression('rainParticleShape', s='rainParticleShape.rgbPP = <<0, 0, 1.0>>', c=1);
		c.select(cl=True);
		c.setAttr("particleCloud1.color", 1, 1, 1, type="double3"); #instead of particleCloud1?
		#sets the collision event and particle spawning
		c.particle( name='rainCollisionParticle' , inherit=True);
		c.connectDynamic('rainCollisionParticle',f='rainGravity');
		c.select(cl=True);
		c.setAttr( "rainCollisionParticle|rainCollisionParticleShape.particleRenderType", 6); # rainParticleShape/render Attributes
		c.setAttr('rainCollisionParticle.inheritFactor', 1);
		c.event( 'rainParticle', em=2, die=True, target='rainCollisionParticle', spread=0.5, random=True, count=0, name='rainParticleCollideEvent' );
		
	def remove(WeatherUI,self):
		c.delete('rainEmitter','rainGravity','rainParticle');
		
	def addCollision(WeatherUI):
		
		objects = c.ls(sl=True);
		for i in range(0,len(objects)):
			c.collision(objects[i], f=0.05, r=0.2);
			c.connectDynamic('rainParticle', c=objects[i]);
			print objects[i];
