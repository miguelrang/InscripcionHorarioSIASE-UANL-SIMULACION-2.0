import pyodbc as SQLServer

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.banner import MDBanner

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
Config.set('graphics', 'position', 'custom')
from kivy.utils import platform
#from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
#from kivy.clock import Clock

from Login import Login
from SIASE import SIASE
from Rectory import Rectory
from Options import Options
#from Mod import Mod
#from Delete import Delete 

"""
from PIL import Image
img = Image.open("images/wallpaper-rectory2.png")
img = img.resize((1370, 700), Image.ANTIALIAS)
img.save("images/wallpaper-rectory.png")
"""

class WindowManager(ScreenManager):
	def __init__(self, **kwargs):
		super(WindowManager, self).__init__(**kwargs)


class main(MDApp):
	def build(self):
		if platform == 'win':
			self.icon = "images/icon.png"

		self.title = "Servicios en Linea"
		Window.size = (700, 450)
		
		wm = WindowManager()
		wm.add_widget(Builder.load_file('Login.kv'))
		wm.add_widget(Builder.load_file('SIASE.kv'))
		wm.add_widget(Builder.load_file('Rectory.kv'))
		wm.add_widget(Builder.load_file('Options.kv'))
		
		return wm

	def on_start(self):
		app = MDApp.get_running_app()

		app.title='Rectoria'
		app.root.current='rectory'
		app.root.get_screen('rectory').setData('1000', 'Emerson David Rangel Gómez')
		app.resizeWindow(size=(1370, 700), left=0, top=30)

	def openDialog(self, title:str, text:str):
		def closeDialog(*args):
			self.dialog.dismiss()

		self.dialog = MDDialog(
			title=title,
			text=text,
			buttons=[
				MDRectangleFlatButton(
					text='Aceptar',
					on_press=closeDialog
				)
			]
		)
		self.dialog.open()


	def showBanner(self, title:str, text:str, sc='rectory'):
		banner = self.root.get_screen(sc).ids.banner
		banner.text = [title, text]
		banner.show()


	def resizeWindow(self, size:tuple, left:float, top:float):
		Window.size = size
		Window.left = left
		Window.top = top

	def execute(self, procedure:str):
		def server():
			server = ('Driver={ODBC Driver 17 for SQL Server};'
				'Server=LAPTOP-CF0NC87S;'
				'Database=UANL;'
				'Trusted_Connection=yes'
			)

			return server
	
		with SQLServer.connect(server()) as connect:
			sql = connect.cursor()
			#print('EXECUTE', procedure + ';')
			sql.execute('EXECUTE {};'.format(procedure))

			if 'Get' in procedure:
				return sql.fetchall()
		

if __name__ == "__main__":
	#sql = sqlCONNECTION()
	main().run()
