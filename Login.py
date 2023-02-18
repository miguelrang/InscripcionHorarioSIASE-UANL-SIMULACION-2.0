from kivymd.app import MDApp

from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from datetime import datetime

import random
import re

class Login(Screen):
	#type_ids = ('touch',)
	def __init__(self, **kwargs):
		super(Login, self).__init__(**kwargs)
		global app
		app = MDApp.get_running_app()

		# 'Clock.schedule_interval' function calls the
		# function 'interval' (automatically add the var 'dt').
		# The second parameter says each seconds call the function. 
		Clock.schedule_interval(self.dateTime, 1)


	def dateTime(self, dt):
		dt = datetime.now()
		day = str(dt.day)
		if len(day) == 1:
			day = '0' + day
		month = str(dt.month)
		if len(month) == 1:
			month = '0' + month

		# We update the Labels
		self.ids.calendar.text = "[color=#ffffff]{}-{}-{}[/color]".format(day, month, dt.year)
		self.ids.clock.text = f"[color=#ffffff]{dt.strftime('%H:%M')}[/color]"


	def login(self, type:int, enrollment:str, passw:str):
		def emptyFields(enrollment:str, passw:str)-> bool:
			if enrollment == '' or passw == '':
				return True

		if not emptyFields(enrollment, passw):
			user = app.execute("Login '{}', '{}', '{}'".format(type, enrollment, passw))
			if user: # exist
				if type == 1:
					app.title = 'SIASE'
					app.root.current = 'siase'
					app.root.get_screen('siase').setData(
						enrollment=user[0][0],
						student=user[0][1],
						career=user[0][2]
					)

				else:
					app.title = 'Rectoria'
					app.root.current = 'rectory'
					app.root.get_screen('rectory').setData(
						id_rector=1000
					)
				app.resizeWindow(size=(1370, 700), left=0, top=30)

			else:
				app.openDialog(
					title='Inicio de Sesión Fallida',
					text='Matricula y/o contraseña incorrectos.'
				)
		else:
			app.openDialog(
				title='Campo(s) Vacio(s)',
				text='Debe llenar todos los campos.'
			)