import sys
import os.path
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
		weatherUI.setUpCamera();
		

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
		
		
def _setUpIBL():
	
		if not c.objExists('myIbl') and not c.objExists('myIblShape'):
			mel.eval('miCreateDefaultNodes()');
			
			c.select(cl=True);
			mel.eval('setCurrentRenderer mentalRay;');
			ibl = c.createNode( 'mentalrayIblShape', n='myIbl' );
			c.rename('mentalrayIbl1', 'myIblShape');
			if(c.isConnected( 'myIbl.message', 'mentalrayGlobals.imageBasedLighting' ) != '0'):
				c.evalDeferred( "c.connectAttr(  'myIbl.message', 'mentalrayGlobals.imageBasedLighting', f=True)", lp=True);
			mel.eval('$path = `optionVar -q WeatherViz_HDR_Path`');
			#mel.eval('$path = optionVar -q "WeatherViz_HDR_Path"');
			mel.eval('AEassignFilenameCB  myIbl.texture $path "image"');
			c.setAttr('myIbl.colorGain', 14, 14, 14, type='double3');
			#sets render stats
			c.setAttr('myIbl.visibleInEnvironment', 1);
			c.setAttr('myIbl.visibleInReflections', 1);
			c.setAttr('myIbl.visibleInRefractions', 1);
			c.setAttr('myIbl.visibleInFinalGather', 1);

			c.setAttr('myIblShape.scaleX', 80);
			c.setAttr('myIblShape.scaleY', 80);
			c.setAttr('myIblShape.scaleZ', 80);
			c.select(cl=True);
		else:
			mel.eval('$path = `optionVar -q WeatherViz_HDR_Path`');
			mel.eval('AEassignFilenameCB  myIbl.texture $path "image"');
			
			

def _setHDRPathOptionVar():
	"""
	This definition sets **sIBL_GUI_loaderScriptPath** optionVar.
	"""
	
	_setOptionVar("WeatherViz_HDR_Path", c.textField("WeatherViz_HDR_Path_textField", query=True, text=True))
	
	
def _WeatherViz_HDR_Path_button__command(state=None):
	"""
	This definition is triggered by **Loader_Script_Path_button** widget.

	:param state: Button state. ( Boolean )
	"""

	fileName = c.fileDialog2(ds=2, fileFilter="All Files (*.*)", fm=4)
	fileName = fileName and fileName[0] or None
	if not fileName:
		print "noooo filenamaaa "
		return
		
	
	c.textField("WeatherViz_HDR_Path_textField", edit=True, text=fileName)
	print "ska satt text " + fileName;
	_setHDRPathOptionVar()
	_setUpIBL();
	
def _WeatherViz_HDR_Path_textField__changeCommand(value):
	"""
	This definition is triggered by **_Loader_Script_Path_textField** widget.

	:param value: Value. ( String )
	"""

	if os.path.exists(value):
		_setHDRPathOptionVar()
		setUpIBL();
	else:
		mel.eval("warning(\"WeatherViz | hdr path invalid!\");")
	
	
def _setOptionVar(name, value):
	"""
	This definition stores given optionVar with given value.
	
	:param name: OptionVar name. ( String )
	:param value: OptionVar value. ( Object )
	"""

	c.optionVar(sv=(name, value))
##end global

	
class WeatherUI():
		
	

		
	def __init__(self):
		self.snow = Snow();
		self.rain = Rain();
		self.wind = Wind();
	
	def init(self):
		window = c.window(title='WeatherViz',widthHeight=(400,600));
		#form = c.formLayout(numberOfDivisions=100);
		c.rowColumnLayout(numberOfColumns=1);
		c.checkBoxGrp('weatherPanel', label='Weather');
		c.checkBox('snowCheck', label='Snow', onc=self.snow.init, ofc=self.snow.remove, p='weatherPanel');
		c.checkBox('rainCheck', label='Rain', onc=self.rain.init, ofc=self.rain.remove, p='weatherPanel');
		c.checkBox('windCheck', label='Wind', onc=self.wind.init, ofc=self.wind.remove, p='weatherPanel');
		c.button('collButton', label='Add collision', c=self.addCollision);


		#s1 = c.floatSliderGrp('snowTurb',label='Snow turbulence', field=True, value=5, dc=self.slider_drag_callback, min=0, max=10);
		c.floatSliderGrp('snowIntens',label='Snow Intencity', field=True, value=200, dc=self.slider_drag_callback, min=0, max=1000, en=False);
		c.floatSliderGrp('rainIntens',label='Rain Intencity', field=True, value=200, dc=self.slider_drag_callback, min=0, max=1000, en=False);
		c.floatSliderGrp('snowTurbSlider',label='Turbulence', field=True, value=1, dc=self.slider_drag_callback, min=0, max=100, en=False);
		c.floatSliderGrp('airMSlider',label='Wind Magnitude', field=True, value=30, dc=self.slider_drag_callback, min=0, max=100, en=False);
		c.floatSliderGrp('airMxdSlider',label='Wind Distance', field=True, value=20, dc=self.slider_drag_callback, min=0, max=100, en=False);
		#c.formLayout(form, edit=True, attachPosition=[(s1, 'top', 20, 1)]);
		#c.formLayout(form, edit=True, attachPosition=[(s2, 'top', 20, 1)]);
		
		c.textField("WeatherViz_HDR_Path_textField", cc=_WeatherViz_HDR_Path_textField__changeCommand)
		c.button("WeatherViz_HDR_Path_button", label="...", al="center", command=_WeatherViz_HDR_Path_button__command)
		
		WeatherViz_HDR_Path = c.optionVar(q="WeatherViz_HDR_Path")
		if WeatherViz_HDR_Path:
			c.textField("WeatherViz_HDR_Path_textField", edit=True, text=WeatherViz_HDR_Path)
			
		c.showWindow(window);
		c.windowPref(enableAll=True)
		
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
		
		#ground = c.polyPlane(h=100,w=100, n='groundPlane');
		#c.move(0,-13, 0, 'groundPlane');
		
		#C:/Users/Sebastian/Documents/maya/projects/default/sourceimages/exr/Location_1_1_hdr.exr
		#
		if not (c.pluginInfo("Mayatomr",q=True,loaded=True)):
			c.loadPlugin("Mayatomr")
		else:
			pass
		
		"""
			To load the hdr image from path
		"""
		HDR_Path = c.optionVar(q="WeatherViz_HDR_Path")
		if HDR_Path:
			if os.path.exists(HDR_Path):
				print HDR_Path;
				_setUpIBL();

				return True
			else:
				mel.eval("error(\"WeatherViz | hdr image doesnt exist!\");")
		else:
			mel.eval("warning(\"WeatherViz | No hdr image found!\");")
			#c.confirmDialog(title="sIBL_GUI | Warning", message="No Loader Script found!\nPlease define one in preferences!", button=["Ok"], defaultButton="Ok")
		
		
		
		
		
		ground = c.polyPlane(h=100,w=120, n='groundPlane');
		c.move(37,-13, -15, 'groundPlane');
		c.rotate(0, -20, -5,'groundPlane');
		
		
		alphaShader = c.shadingNode('lambert', asShader=True, n='alphaShader');
		SG2 = c.sets(empty=True, renderable=True, noSurfaceShader=True, name=alphaShader+"SG2");
		c.setAttr(alphaShader+'.transparency', 1, 1, 1, type="double3");
		c.select( 'groundPlane' );
		c.hyperShade( assign=alphaShader);
		
	
	
	
	
	def setUpCamera(self):
		c.camera(p=[-16,10, -33], rot=[-10,255,0], fl=20);
		
	def setUpSky(self):
		c.polyPlane( h=120,w=120,n='emitPlane');
		c.polyNormal('emitPlane', nm=3 , n='polynormalReversed');
		c.move(0,100,0,'emitPlane');
		c.select(cl=True);
		
	def addCollision(self,*args):
		if c.particleExists('snowParticle'):
			self.snow.addCollision();
		if c.particleExists('rainParticle'):
			self.rain.addCollision();
			
	def slider_drag_callback(*args):
		if c.objExists('turb'):
			valueTurb = c.floatSliderGrp('snowTurbSlider', query=True, value=True);
			c.turbulence('turb', e=True, m=valueTurb);
		
		if c.objExists('snowEmitter'):
			valueSnowInt = c.floatSliderGrp('snowIntens', query=True, value=True);
			c.emitter('snowEmitter', e=True, r=valueSnowInt);
		
		if c.objExists('rainEmitter'):
			valueRainInt = c.floatSliderGrp('rainIntens', query=True, value=True);
			c.emitter('rainEmitter', e=True, r=valueRainInt);
			
		if c.objExists('air'):
			value2 = c.floatSliderGrp('airMSlider', query=True, value=True);
			value3 = c.floatSliderGrp('airMxdSlider', query=True, value=True);
			c.air('air', e=True, m=value2, mxd=value3);
		
		

			
class Snow():
	
	def __init__(self):
		pass;
	
	def init(WeatherUI,self):
		c.select('emitPlane');
		c.emitter(n='snowEmitter',type='surf',r=300,sro=0,nuv=0,cye='none',cyi=1,spd=1,srn=0,nsp=1,tsp=0,mxd=0,mnd=0,dx=0,dy=-1,dz=0,sp=1);
		c.particle(n='snowParticle');

		c.select(cl=True);
		c.setAttr( "snowParticle|snowParticleShape.particleRenderType", 8); # 1 ist for 8
		c.gravity(n='snowGravity',m=0.5);
		c.select(cl=True);
		
		c.connectDynamic('snowParticle',em='snowEmitter');
		c.connectDynamic('snowParticle',f='snowGravity');
		
		c.addAttr('snowParticleShape', ln='rgbPP', dt='vectorArray' );
		c.dynExpression('snowParticleShape', s='snowParticleShape.rgbPP = <<1.0, 1.0, 1.0>>', c=1);
		c.addAttr('snowParticleShape', ln='radius', at='float', min=0, max=20, dv=1);
		c.setAttr('snowParticleShape.radius', 0.3);
		c.setAttr("particleCloud1.color", 1, 1, 1, type="double3");
		c.setAttr('snowParticleShape.lifespanMode', 2);
		c.setAttr('snowParticleShape.lifespan', 30)
		
		c.select(cl=True);
		
		c.floatSliderGrp('snowIntens', en=True, e=True);
		
		
	def remove(WeatherUI,self):
		c.delete('snowEmitter','snowGravity','snowParticle');
		c.floatSliderGrp('snowTurbSlider',en=False, e=True);
		c.floatSliderGrp('snowIntens',en=False, e=True);
		
	def addCollision(WeatherUI):
		
		objects = c.ls(sl=True);
		for i in range(0,len(objects)):
			c.collision(objects[i], f=0.3, r=0);
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
		
		c.floatSliderGrp('rainIntens',en=True, e=True);
		
	def remove(WeatherUI,self):
		c.delete('rainEmitter','rainGravity','rainParticle', 'rainCollisionParticle');
		c.floatSliderGrp('rainIntens',en=False, e=True);
		
	def addCollision(WeatherUI):
		
		objects = c.ls(sl=True);
		for i in range(0,len(objects)):
			c.collision(objects[i], f=0.05, r=0.2);
			c.connectDynamic('rainParticle', c=objects[i]);
			print objects[i];
			
class Wind():
	
	def __init__(self):
		pass;
		
	def init(WeatherUI,self):
		c.select(cl=True);
		c.turbulence(n='turb',m=1);
		c.air(n='air', m=30.0, mxd=20.0, pos=[20, 15, -40], vco=True);
		c.floatSliderGrp('snowTurbSlider', en=True, e=True);
		c.floatSliderGrp('airMSlider', en=True, e=True);
		c.floatSliderGrp('airMxdSlider', en=True, e=True);
		
		if c.objExists('snowParticle'):
			c.connectDynamic('snowParticle',f='turb');
		
		if c.objExists('snowParticle'):
			c.connectDynamic('snowParticle',f='air');
			
		if c.objExists('rainParticle'):
			c.connectDynamic('rainParticle',f='turb');
			
		if c.objExists('rainParticle'):
			c.connectDynamic('rainParticle',f='air');

	def remove(WeatherUI,self):
		c.delete('turb', 'air');
		c.floatSliderGrp('snowTurbSlider', en=False, e=True);
		c.floatSliderGrp('airMSlider', en=False, e=True);
		c.floatSliderGrp('airMxdSlider', en=False, e=True);
		
	def addCollision(WeatherUI):
		pass;
		
