class WeatherUI():
	
	def __init__(self):
		print 'Weather yaaoo';
	
	def create(self):
		window = c.window('ar_optionsWindow',title='WeatherViz',widthHeight=(400,600));
		c.showWindow(window);
		