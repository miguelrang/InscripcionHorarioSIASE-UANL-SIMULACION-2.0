from kivymd.app import MDApp

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from functools import partial

Builder.load_string(
'''
<Kardex>:
	MDLabel:
		text: root.text1
		markup: True
		halign: root.halign1
		valign: 'center'

		canvas.before:
			Color:
				rgba: root.color

			Rectangle:
				size: self.size
				pos: self.pos

	MDLabel:
		text: root.text2
		size_hint_x: 8
		markup: True
		halign: root.halign2
		valign: 'center'

		canvas.before:
			Color:
				rgba: root.color

			Rectangle:
				size: self.size
				pos: self.pos

	MDLabel:
		text: root.text3
		markup: True
		halign: root.halign1
		valign: 'center'
		
		canvas.before:
			Color:
				rgba: root.color

			Rectangle:
				size: self.size
				pos: self.pos

	MDLabel:
		text: root.text4
		markup: True
		halign: root.halign1
		valign: 'center'
		
		canvas.before:
			Color:
				rgba: root.color

			Rectangle:
				size: self.size
				pos: self.pos

	MDLabel:
		text: root.text5
		markup: True
		halign: root.halign1
		valign: 'center'
		
		canvas.before:
			Color:
				rgba: root.color

			Rectangle:
				size: self.size
				pos: self.pos

	MDLabel:
		text: root.text6
		markup: True
		halign: root.halign1
		valign: 'center'
		
		canvas.before:
			Color:
				rgba: root.color

			Rectangle:
				size: self.size
				pos: self.pos

	MDLabel:
		text: root.text7
		markup: True
		halign: root.halign1
		valign: 'center'
		
		canvas.before:
			Color:
				rgba: root.color

			Rectangle:
				size: self.size
				pos: self.pos

	MDLabel:
		text: root.text8
		markup: True
		halign: root.halign1
		valign: 'center'
		
		canvas.before:
			Color:
				rgba: root.color

			Rectangle:
				size: self.size
				pos: self.pos
'''
)
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.properties import ColorProperty, StringProperty, OptionProperty
from kivy.metrics import dp
class Kardex(MDGridLayout):
	color = ColorProperty()
	text1 = StringProperty()
	text2 = StringProperty()
	text3 = StringProperty()
	text4 = StringProperty()
	text5 = StringProperty()
	text6 = StringProperty()
	text7 = StringProperty()
	text8 = StringProperty()
	halign1 = OptionProperty("center", options=['left', 'center', 'right', 'justify', 'auto'])
	halign2 = OptionProperty("center", options=['left', 'center', 'right', 'justify', 'auto'])

Builder.load_string(
'''
<EnableSubjects>:
	MDTextButton:
		text: root.text1
		markup: True
		size_hint_x: 1.25
		pos_hint: {'center_x': .5, 'center_y': .5}
		halign: 'left'
		valign: 'center'
		on_press:
			if 'Materia' not in root.text2:\
			app.root.get_screen('siase').schedulesSubject(root.text1.replace('[color=#2979E9][u]', '').replace('[/u][/color]', ''), app.root.get_screen('siase').enrollment)

	MDLabel:
		text: root.text2
		markup: True
		size_hint_x: 8
		halign: 'left'
		valign: 'center'

	MDLabel:
		text: root.text3
		markup: True
		halign: 'center'
		valign: 'center'

	MDLabel:
		text: root.text4
		markup: True
		halign: 'center'
		valign: 'center'
'''
)
class EnableSubjects(MDBoxLayout):
	text1 = StringProperty()
	text2 = StringProperty()
	text3 = StringProperty()
	text4 = StringProperty()

""" AUN FALTA MODIFICAR EN RECTORIA
Builder.load_string(
'''
<EnableSchedules>:
	MDTextButton:
		text: root.text1
		markup: True
		size_hint_x: 1.25
		pos_hint: {'center_x': .5, 'center_y': .5}
		halign: 'left'
		valign: 'center'
		on_press:
			if 'Materia' not in root.text2:\
			app.root.get_screen('siase').schedulesSubject(root.text1.replace('[color=#2979E9][u]', '').replace('[/u][/color]', ''), app.root.get_screen('siase').enrollment)

	MDLabel:
		text: root.text2
		markup: True
		size_hint_x: 8
		halign: 'left'
		valign: 'center'

	MDLabel:
		text: root.text3
		markup: True
		halign: 'center'
		valign: 'center'

	MDLabel:
		text: root.text4
		markup: True
		halign: 'center'
		valign: 'center'
'''
)
class EnableSchedules(MDBoxLayout):
	text1 = StringProperty()
	text2 = StringProperty()
	text3 = StringProperty()
	text4 = StringProperty()
AUN FALTA MODIFICAR EN RECTORIA"""
class SIASE(Screen):
	def __init__(self, **kwargs):
		super(SIASE, self).__init__(**kwargs)
		global app
		app = MDApp.get_running_app()


	def setData(self, enrollment:str, student:str, career:str):
		def setCareer(c:str):
			c = c.replace('LICENCIADO', 'LIC.')
			c = c.replace('LICENCIATURA', 'LIC.')
			c = c.replace('INGENIERO', 'ING.')
			c = c.replace('INGENIERIA', 'ING.')

			return c
			
		self.ids.recycle.data = []
		self.enrollment = enrollment
		self.student = student # PUEDE QUE NO SE USE
		self.career = career # PUEDE QUE NO SE USE

		self.ids.enrollment.text = '[b]Matricula:[/b] {}'.format(enrollment)
		self.ids.full_name.text = '[b]Nombre:[/b] {}'.format(student)
		self.ids.career.text = '[b]Carrera:[/b] {}'.format(setCareer(career))


	def showKardex(self, enrollment:str):
		subjects = app.execute("GetKardex '{}'".format(enrollment))
		self.ids.recycle.data = []
		self.ids.recycle.data.append(
			{
				"viewclass": "Kardex",
				"cols": 8,
				"color": (1, 234/255, 150/255, 1),
				"spacing": dp(1),
				"padding": (dp(5), dp(5), dp(300), dp(5)),
				"text1": '[color=#000000][b]Sem[/b][/color]',
				"text2": '[color=#000000][b]Materia[/b][/color]',
				"text3": '[color=#000000][b]1\nOpo.[/b][/color]',
				"text4": '[color=#000000][b]2\nOpo.[/b][/color]',
				"text5": '[color=#000000][b]3\nOpo.[/b][/color]',
				"text6": '[color=#000000][b]4\nOpo.[/b][/color]',
				"text7": '[color=#000000][b]5\nOpo.[/b][/color]',
				"text8": '[color=#000000][b]6\nOpo.[/b][/color]',
				"halign1": 'center',
				"halign2": 'center'
			}
		)
		
		n = 1
		for subject in subjects:
			sem = subject[0]
			subj = subject[1]
			op1 = subject[2]
			op2 = subject[3]
			op3 = subject[4]
			op4 = subject[5]
			op5 = subject[6]
			op6 = subject[7]
			
			if n % 2 == 0:
				color = (.9, .9, .9, 1)
			else:
				color = (1, 1, 1, 1)

			self.ids.recycle.data.append(
				{
					"viewclass": "Kardex",
					"cols": 8,
					"color": color,
					"spacing": dp(1),
					"padding": (dp(5), dp(5), dp(300), dp(5)),
					"text1": '[color=#05396E]{}[/color]'.format(sem),
					"text2": '[color=#05396E]{}[/color]'.format(subj),
					"text3": '[color=#05396E]{}[/color]'.format(op1),
					"text4": '[color=#05396E]{}[/color]'.format(op2),
					"text5": '[color=#05396E]{}[/color]'.format(op3),
					"text6": '[color=#05396E]{}[/color]'.format(op4),
					"text7": '[color=#05396E]{}[/color]'.format(op5),
					"text8": '[color=#05396E]{}[/color]'.format(op6),
					"halign1": 'center',
					"halign2": 'left'
				}
			)

			n += 1


	def inscription(self, enrollment:str) -> None:
		"""	Get the enrollment or student ID and set the enable
			subjects for the inscription
		Args:
			enrollment (str): student ID to show the subjects and 
							  schedules he/she has not course
		Returns: None
		"""
		def reprobed(subjects:list)-> bool:
			"""	Get a list of tuples with data from which we take the note 
				and return a boolean to know if the student is expulsed or not
			Args:
				subjects (list): Subjects with the note

			Returns:
				bool: Where True means the student has been expulsed
			"""
			expulsed = False
			for subject in subjects:
				if subject[2] == 'NONE':
					expulsed = True
					break

			return expulsed

		def idInscriptedSubjects(student_schedule:tuple) -> list:
			"""	Get a tuple with the student's current schedule 
				data and return only the schedule id/key
			Args:
				student_schedule (tuple): schedule data

			Returns:
				list: The key of each schedule
			"""
			inscripted = []
			for subject in student_schedule:
				inscripted.append(subject[0])

			return inscripted

		subjects = app.execute("GetEnableSubject '{}'".format(enrollment))
		inscripted:list = idInscriptedSubjects(app.execute("GetStudentSchedules '{}'".format(enrollment)))
		if not reprobed(subjects):
			self.ids.recycle.data = [] # We empty the data showed in the recycle view
			# We begin to fill the 'data table'
			self.ids.recycle.data.append(
				{
					"viewclass": "EnableSubjects",
					"orientation": 'horizontal',
					"md_bg_color": (1, 234/255, 150/255, 1),
					"padding": (dp(50), dp(0), dp(50), dp(0)),
					"text1": '[color=#000000][b]Clave[/b][/color]',
					"text2": '[color=#000000][b]Materia[/b][/color]',
					"text3": '[color=#000000][b]Sem[/b][/color]',
					"text4": '[color=#000000][b]Opo[/b][/color]',
				}
			)

			n = 1
			for s in subjects:
				id:int = s[0]
				subject:str = s[1]
				sem:int = s[2]
				op:str = s[3]

				if op != 'N/A' and not id in inscripted:
					# Set bg color of the line
					if n % 2 == 0:
						color = (.9, .9, .9, 1)
					else:
						color = (1, 1, 1, 1)

					# Set the minimum & maximum semester
					if n == 1:
						minimum = sem
						maximum = sem+2

					# Verify we are in range
					if sem >= minimum and sem <= maximum:
						self.ids.recycle.data.append(
							{
								"viewclass": "EnableSubjects",
								"orientation": 'horizontal',
								"md_bg_color": color,
								"padding": (dp(50), dp(0), dp(50), dp(0)),
								"text1": '[color=#2979E9][u]{}[/u][/color]'.format(id),
								"text2": '[color=#05396E]{}[/color]'.format(subject),
								"text3": '[color=#05396E]{}[/color]'.format(sem),
								"text4": '[color=#05396E]{}[/color]'.format(op),
							}
						)

						n += 1

					else:
						break
		else:
			app.openDialog(
				title='Lo sentimos',
				text='Usted ha quedado fuera de su carrera.'
			)


	def schedulesSubject(self, id_subject:str, enrollment:str) -> None:
		""" Get the subject id and the student id to inscribe and
			show in the 'data table'
		Args:
			id_subject (str): Subject key to show the available
							  schedule of this
			enrollment: (str): Student key to show the schedules
							   subject for the student career
		Returns: None
		"""
		
		""" AUN FALTA MODIFICAR EN RECTORIA
		self.ids.recycle.data = [] # We empty the 'data table'
		# We begin to fill the 'data table'
		self.ids.recycle.data.append(
			{
				"viewclass": "",
				"orientation": 'horizontal',
				"md_bg_color": (1, 234/255, 150/255, 1),
				"padding": (dp(50), dp(0), dp(50), dp(0)),
				"text1": '[color=#000000][b]Clave[/b][/color]',
				"text2": '[color=#000000][b]Materia[/b][/color]',
				"text3": '[color=#000000][b]Sem[/b][/color]',
				"text4": '[color=#000000][b]Opo[/b][/color]',
			}
		)

		n = 1
		schedules = app.execute("GetScheduleSubject '{}', '{}'".format(id_subject, enrollment))
		for s in schedules:
			sem = s[0]
			teacher = s[1]
			group = s[2]
			schedule = s[3]
		AUN FALTA MODIFICAR EN RECTORIA"""
