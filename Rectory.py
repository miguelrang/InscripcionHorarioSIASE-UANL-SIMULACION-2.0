from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, OptionProperty, NumericProperty, BooleanProperty

from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.uix.boxlayout import MDBoxLayout
#from kivymd.uix.list import OneLineIconListItem

import random
import re


class Add(MDFloatLayout, MDTabsBase):
	''''''
class Update(MDFloatLayout, MDTabsBase):
	''''''
class Delete(MDFloatLayout, MDTabsBase):
	''''''
Builder.load_file('Rector.kv')
class Rector(MDFloatLayout, MDTabsBase):
	''''''

Builder.load_file('Teacher.kv')
class Teacher(MDFloatLayout, MDTabsBase):
	''''''

Builder.load_file('Student.kv')
class Student(MDFloatLayout, MDTabsBase):
	''''''

Builder.load_file('Schedule.kv')
class Schedule(MDFloatLayout, MDTabsBase):
	''''''

Builder.load_file("Form.kv")
class RTextField(MDTextFieldRect):
	hint = StringProperty()
	length = NumericProperty()
	spaces = BooleanProperty()
	boolean = BooleanProperty()

class RLabel(MDLabel):
	text = StringProperty()
	name = StringProperty()
	halign = OptionProperty("left", options=["left", "center", "right"])
	valign = OptionProperty("left", options=["left", "center", "bottom", "top"])

class RButtons(MDFloatLayout):
	text = StringProperty()
	disabled = BooleanProperty()
	name = StringProperty()
	disable = BooleanProperty()

class RSearch(MDBoxLayout):
	orientation = 'horizontal'
	spacing = dp(5)
	padding = dp(1), dp(0), dp(1), dp(0)
	name = StringProperty()
	text = StringProperty()
	disabled = BooleanProperty()

class ROptions(MDTextFieldRect):
	hint = StringProperty()

class Rectory(Screen):
	def __init__(self, **kwargs):
		super(Rectory, self).__init__(**kwargs)
		global app
		app = MDApp.get_running_app()

		self.tab = {'rector':{}, 'teacher':{}, 'student':{}, 'schedule':{}}
		self.setInititalData('rector', 'add')
		self.setInititalData('rector', 'upd')
		self.setInititalData('rector', 'del')

		self.setInititalData('teacher', 'add')
		self.setInititalData('teacher', 'upd')
		self.setInititalData('teacher', 'del')
		
		self.setInititalData('student', 'add')
		self.setInititalData('student', 'upd')
		self.setInititalData('student', 'del')
		
		self.setInititalData('schedule', 'add')
		self.setInititalData('schedule', 'upd')
		self.setInititalData('schedule', 'del')
		
		global tclass
		tclass = {
			'rlabel': type(RLabel()),
			'rfield': type(RTextField()),
			'rbuttons': type(RButtons()),
			'rsearch': type(RSearch()),
			'roptions': type(ROptions())
		}
		
		self.selected = {'upd': {'rector':{}, 'teacher':{}, 'student':{}, 'schedule':{}}}
		self.selected['del'] = self.selected['upd']

		self.field = None
		self.main_tab = 'rector'
		self.secondary_tab = 'add'


	def setTab(self, main_tab:bool, instance_tabs:object, instance_tab:object, instance_tab_label:object, tab_text:str)-> None:
		"""	Get some parameters(objects and string) with the name tab or icon
			and we set the main tab or the secondary tab
		Args:
			instance_tabs (object)
			instance_tab (object)
			instance_tab_label (object)
			tab_text (str): text or name icon of tab
		Returns: None
		"""
		def removeTrash(tab_text:object) -> str:
			"""	Get the name tab with trash and returns only the name
			Args:
				tab_text (str): text with trash
			Returns:
				str: name
			"""
			if 'Rectoria' in tab_text:
				tab = 'rector'

			elif 'Profesor' in tab_text:
				tab = 'teacher'

			elif 'Estudiante' in tab_text:
				tab = 'student'

			elif 'Horario' in tab_text:
				tab = 'schedule'

			elif 'Agregar' in tab_text:
				tab = 'add'

			elif 'Actualizar' in tab_text:
				tab = 'upd'

			else:
				tab = 'del'

			return tab

		tab = removeTrash(tab_text)
		if main_tab:
			self.main_tab = tab

		else:
			self.secondary_tab = tab


	def setWidget(self, wdg:object):
		recycle_grid = self.ids[self.main_tab].ids[self.secondary_tab].ids.recycle_grid
		for wdg_grid in recycle_grid.children:
			wdg_grid.disabled = True
				#break


	def text_validate(self, name:str, field:object, text:str, length:int, spaces:bool)-> None:
		"""	Get a field and its text to set self text (some
			fields have different funtionalities)
		Args:
			name (str): row name (it helps us to know if the user is 
						in add, upd or del)
			field (object): field contains the full data 
							(text field, hint_text, etc.)
			text (str): content field (text)
			length (int): equivalent to max text length
			spaces (bool): spaces allowed (Yes = True & No = False)
		Returns: None
		"""
		if name == "": # search field (intentionality, we send an empty name)
			if field.text != "":
				# excedent...
				if len(text) > length:
					# excedent + multiline
					if text.count("\n") > 0:
						app.showBanner(
							title="Longitud Excedida, Saltos de Linea y Números Añadidos",
							text='Este campo solo admite una longitud de {} caracteres y no permite saltos de linea ni números.'.format(length)
						)
					# excedent
					else:
						app.showBanner(
							title="Longitud Excedida",
							text='Este campo solo admite una longitud de {} caracteres'.format(length)
						)
				elif text.count("n") > 0: # multiline
					app.showBanner(
						title='Saltos de linea',
						text="Este campo no permite los saltos de linea."
					)
				else: # all right
					data:tuple = app.execute("GetAccountData '{}', '{}'".format(self.main_tab, text))
					if data:
						i:int = len(data[0])-1
						data = data[0]
						form:object = self.ids[self.main_tab].ids[self.secondary_tab].ids.recycle_grid
						for child in form.children:
							if child.viewclass in [tclass['rsearch'], tclass['rfield'], tclass['rbuttons']]:
								if child.viewclass != type(RButtons()):
									#print("child:", child.name, "-", data[i])
									child.text = str(data[i])
									self.tab[self.main_tab][self.secondary_tab][child.name] = child.text
									i -= 1

								if self.secondary_tab == "upd":
									child.disabled = "enrollment" == child.name
									if child.viewclass == tclass['rbuttons']:
										child.disable = False

								elif self.secondary_tab == 'del':
									child.disabled = child.viewclass != tclass['rbuttons'] # or class in ['rfield', 'rsearch']
									child.disable = child.disabled
								
								else: # add
									child.disabled = "enrollment" != child.name and child.name != "buttons"

						if self.secondary_tab in ['upd', 'del']:
							self.selected[self.secondary_tab][self.main_tab] = self.tab[self.main_tab][self.secondary_tab].copy()
					else:
						app.showBanner(
							title='Matricula Invalida o Iconrrecta',
							text="Lo sentimos, no se pudo encontrar ninguna cuenta con la matricula: {}.".format(text)
						)
						
				text = text[:length]
				text = text.replace("\n", "")

		elif field.hint_text not in ['Matricula', 'Correo Universitario', 'Contraseña']:
			if field.focus == False:
				# excedent + ...
				if len(text) > length:
					# excedent + multiline + ...
					if text.count('\n') > 0:
						# excedent + multilines + numbers
						if field.input_filter != 'int' and set(text)&set("0123456789"):
							app.showBanner(
								title="Longitud Excedida, Saltos de Linea y Números Añadidos",
								text='Este campo solo admite una longitud de {} caracteres y no permite saltos de linea ni números.'.format(length)
							)
						# excent + multilines
						else:
							app.showBanner(
								title="Longitud Excedida y Saltos de Linea",
								text='Este campo solo admite una longitud de {} caracteres y no permite saltos de linea.'.format(length)
							)
					# excedent
					else:
						app.showBanner(
							title="Longitud Excedida",
							text='Este campo solo admite una longitud de {} caracteres'.format(length)
						)

				# multiline + ...
				elif text.count('\n') > 0:
					# multiline + numbers
					if field.input_filter != 'int' and set(text)&set("0123456789"):
						app.showBanner(
							title="Saltos de Linea y Números Añadidos",
							text='Este campo no permite saltos de linea ni números.'
						)
					# multiline
					else:
						app.showBanner(
							title='Saltos de linea',
							text="Este campo no permite los saltos de linea."
						)
				# numbers
				elif field.input_filter != 'int' and set(text)&set("0123456789"):
					app.showBanner(
						title="Números Añadidos",
						text="Este campo no admite números."
					)
				text = text.replace('\n', '')
				text = text[:length]
				text = text.replace("0", "")
				text = text.replace("1", "")
				text = text.replace("2", "")
				text = text.replace("3", "")
				text = text.replace("4", "")
				text = text.replace("5", "")
				text = text.replace("6", "")
				text = text.replace("7", "")
				text = text.replace("8", "")
				text = text.replace("9", "")
				

				text = text[:length]
				if spaces == False:
					text = text.replace(' ', '')

				field.text = text
				self.tab[self.main_tab][self.secondary_tab][name] = text
				
		else: # The field is the Enrollment, Email or Password
			if self.secondary_tab == "add" or name == "email":
				app.openDialog(
					title='Campo Bloqueado',
					text='Este campo mostrara tu {} una vez guardados tus datos.'.format(field.hint_text)
				)
				

	def showOptions(self, forms:object, field:object, enrollment:str, employee:str):
		app.root.get_screen('options').setData(forms, field, enrollment, employee)
		app.root.current='options'


	def setData(self, id_rector=int(), employee=str()) -> None:
		"""	Get the rectory employee id and name, we
			show this data and initialize the forms.
		Args:
			id_rector (int): employee id
			employee (str): employee name
		Returns: None
		"""
		def setDataRectory(recycle:id, sub_tab:str)-> None:
			"""	Get the recycle view where we will show the forms
				for rectory employee.
			Args:
				recycle (object): This show an scroller box layout
								  with the forms
				sub_tab (str): It specifics the sub tab where we are
							   adding the fields, buttons or labels.
			Returns: None
			"""

			# Label sub title
			recycle.data.append(
				{
					"viewclass": "RLabel",
					"text": "[b][size=20][color=#05396E]Datos del Empleado[/color][/size][/b]",
					"halign": "left",
					"valign": "center"
				}
			)

			# Label string
			text = "[size=14][color=#EDA216]Las cuentas de rectoria tienen los "
			text += "permisos para agregas mas cuentas de la misma, además de "
			text += "cuentas para profesores, alumnos y agregar horarios.[/color][/size]"
			recycle.data.append(
				{
					"viewclass": "RLabel",
					"text": text,
					"halign": "left",
					"valign": "center"
				}
			)
			disabled:bool = False
			action = "Registrar"
			if sub_tab in ['upd', 'del']:
				# Enrollment
				recycle.data.append({"viewclass": "RSearch", "name":"enrollment", "text": "", "disabled": False})
				recycle.data.append({"viewclass": "RLabel", 'text': "", "size_hint_y": 1})
				if sub_tab == "upd":
					action = "Actualizar"
				else:
					action = "Eliminar"

				disabled = True

			# Name
			recycle.data.append(
				{
					"viewclass": "RTextField",
					"name": "name",
					"text": "",
					"hint": "Nombre",
					"length": 30,
					"spaces": True,
					"boolean": False,
					"multiline": False,
					"disabled": disabled
				}
			)

			# Middle Name
			recycle.data.append(
				{
					"viewclass": "RTextField",
					"name": "middle_name",
					"text": "",
					"hint": "Primer Apellido",
					"length": 20,
					"spaces": False,
					"boolean": False,
					"multiline": False,
					"disabled": disabled
				}
			)

			# Last Name
			recycle.data.append(
				{
					"viewclass": "RTextField",
					"name": "last_name",
					"text": "",
					"hint": "Segundo Apellido",
					"length": 20,
					"spaces": False,
					"boolean": False,
					"multiline": False,
					"disabled": disabled
				}
			)

			if sub_tab == 'add':
				# Enrollment
				recycle.data.append(
					{
						"viewclass": "RTextField",
						"name": "enrollment",
						"text": "",
						"boolean": True,
						"hint": "Matricula"
					}
				)

			# Email
			recycle.data.append(
				{
					"viewclass": "RTextField",
					"name": "email",
					"text": "",
					"hint": "Correo Universitario",
					"boolean": True,
					"disabled": disabled
				}
			)

			# Password
			recycle.data.append(
				{
					"viewclass": "RTextField",
					"name": "pass",
					"text": "",
					"hint": "Contraseña",
					"boolean": sub_tab == "add",
					"disabled": disabled
				}
			)

			# Buttons
			recycle.data.append(
				{
					"viewclass": "RButtons",
					"name": "buttons",
					"text": action,
					"disabled": disabled,
					"disable": disabled
				}
			)
			
		def setDataTeacher(recycle:id, sub_tab:str)-> None:
			"""	Get the recycle view where we will show the forms
				for teacher.
			Args:
				recycle (object): This show an scroller box layout
								  with the forms
				sub_tab (str): It specifics the sub tab where we are
							   adding the fields, buttons or labels.
			Returns: None
			"""

			# Label sub title
			recycle.data.append(
				{
					"viewclass": "RLabel",
					"text": "[b][size=20][color=#05396E]Datos del Profesor[/color][/size][/b]",
					"halign": "left",
					"valign": "center"
				}
			)

			# Label string
			text = "[size=14][color=#EDA216]Los profesores en conjunto con "
			text += "nuestros empleados de rectoria se póndrán de acuerdo para "
			text += "definir los horarios, considerando que muchos profesores "
			text += "cuentan con dos empleos.[/color][/size]"
			recycle.data.append(
				{
					"viewclass": "RLabel",
					"text": text,
					"halign": "left",
					"valign": "center"
				}
			)

			action = "Registrar"
			if sub_tab in ['upd', 'del']:
				# Enrollment
				recycle.data.append({"viewclass": "RSearch", "name":"enrollment", "text": "", "disabled": False})
				recycle.data.append({"viewclass": "RLabel", 'text': "", "size_hint_y": 1})
				if sub_tab == "upd":
					action = "Actualizar"
				else:
					action = "Eliminar"

				disabled = True

			# Name
			recycle.data.append(
				{
					"viewclass": "RTextField",
					"name": "name",
					"text": "",
					"hint": "Nombre",
					"length": 30,
					"spaces": True,
					"boolean": False,
					"multiline": False
				}
			)

			# Middle Name
			recycle.data.append(
				{
					"viewclass": "RTextField",
					"name": "middle_name",
					"text": "",
					"hint": "Primer Apellido",
					"length": 20,
					"spaces": False,
					"multiline": False
				}
			)

			# Last Name
			recycle.data.append(
				{
					"viewclass": "RTextField",
					"name": "last_name",
					"text": "",
					"hint": "Segundo Apellido",
					"length": 20,
					"spaces": False,
					"multiline": False
				}
			)

			# Faculty
			recycle.data.append(
				{
					"viewclass": "ROptions",
					"name": "faculty",
					"hint_text": "Facultad(es)"
				}
			)

			# Career
			recycle.data.append(
				{
					"viewclass": "ROptions",
					"name": "career",
					"hint_text": "Carrera(s)"
				}
			)

			if sub_tab == 'add':
				# Enrollment
				recycle.data.append(
					{
						"viewclass": "RTextField",
						"name": "enrollment",
						"hint": "Matricula",
						"boolean": True,
						"text": ""
					}
				)

			# Email
			recycle.data.append(
				{
					"viewclass": "RTextField",
					"name": "email",
					"hint": "Correo Universitario",
					"boolean": True,
					"text": ""
				}
			)

			# Password
			recycle.data.append(
				{
					"viewclass": "RTextField",
					"name": "pass",
					"text": "",
					"boolean": sub_tab == 'add',
					"hint": "Contraseña"
				}
			)

			# Buttons
			recycle.data.append(
				{
					"viewclass": "RButtons",
					"name": "buttons",
					"text": "Registrar",
					"disabled": False,
					"disable": False
				}
			)

			# Empty label
			recycle.data.append(
				{
					"viewclass": "RLabel",
					"text": ""
				}
			)

		def setDataStudent(recycle:id, sub_tab:str)-> None:
			"""	Get the recycle view where we will show the forms
				for student.
			Args:
				recycle (object): This show an scroller box layout
								  with the forms
				sub_tab (str): It specifics the sub tab where we are
							   adding the fields, buttons or labels.
			Returns: None
			"""
			pass

		def setDataSchedule(recycle:id, sub_tab:str)-> None:
			"""	Get the recycle view where we will show the forms
				for schedule.
			Args:
				recycle (object): This show an scroller box layout
								  with the forms
				sub_tab (str): It specifics the sub tab where we are
							   adding the fields, buttons or labels.
			Returns: None
			"""
			pass

		if id_rector != int() and employee != str():
			self.ids["enrollment"].text = "[color=#ffffff][b]Matricula:[/b] {}[/color]".format(id_rector)
			self.ids["employee"].text = "[color=#ffffff][b]Empleado:[/b] {}[/color]".format(employee)

		for tab in self.tab.keys():
			# tab['rector']
			# tab['teacher']
			# tab['student']
			# tab['schedule']
			for sub_tab in ['add', 'upd', 'del']:
				recycle=self.ids[tab].ids[sub_tab].ids.recycle
				recycle.data = []
				if tab == 'rector':
					setDataRectory(
						recycle=recycle,
						sub_tab=sub_tab
					)
				elif tab == 'teacher':
					setDataTeacher(
						recycle=recycle,
						sub_tab=sub_tab
					)
				elif tab == 'student':
					setDataStudent(
						recycle=recycle,
						sub_tab=sub_tab
					)
				else: # schedule
					setDataSchedule(
						recycle=recycle,
						sub_tab=sub_tab
					)
				

	def setInititalData(self, tab:str, sub_tab:str)-> None:
		"""	Get the dictionary keys to know which ones to leave blank
		Args:
			tab (str): It's the 'type' or main tab ('rector', 'teacher', 'student' or 'schedule')
			sub_tab (str) It's the secondary tab and it contains the action ('add', 'upd' or 'del')
		Returns: None
		"""
		
		initial_data:dict = {
			'rector': {
				'add': {
					'name': '', # str
					'middle_name': '', # str
					'last_name': '', # str
					'enrollment': '', # int
					'email': '', # str
					'pass': '' # str
				},
				'upd':{
					'enrollment': '', # int
					'name': '', # str
					'middle_name': '', # str
					'last_name': '', # str
					'email': '',
					'pass': ''
				},
				'del':{
					'enrollment': '' # int
				}
			},
			'teacher': {
				'add': {
					'name': '', # str
					'middle_name': '', # str
					'last_name': '', # str
					'faculty': {}, # facutlty or faculties + career or careers (strings)
					'career': [], # career or careers (strings)
					'enrollment': '', # int
					'email': '', # str
					'pass': '', # str
				},
				'upd':{
					'enrollment': '', # int
					'name': '', # str
					'middle_name': '', # str
					'last_name': '', # str
					'faculty': {}, # facutlty or faculties + career or careers (strings)
					'career': [], # career or careers (strings)
					'email': '', # str
					'pass': '', # str			
				},
				'del':{
					'enrollment': '' # int
				}
			},
			'student': {
				'add': {
					'name': '', # str
					'middle_name': '', # str
					'last_name': '', # str
					'enrollment': '', # int
					'email': '', # str
					'pass': '', # str
					'faculty': '', # str
					'career': '', # str
					'try': 1, # int
					'kardex': {}, # dict with cursed subjects in the before career
				},
				'upd':{
					'enrollment': '', # int
					'name': '', # str
					'middle_name': '', # str
					'last_name': '', # str
					'email': '', # str
					'pass': '', # str
					'faculty': '', # str
					'career': '', # str
					'try': 1, # int
					'kardex': {}, # dict with cursed subjects in the before career
				},
				'del':{
					'enrollment': ''
				}
			},
			'schedule': {
				'add': {
					
				},
				'upd':{
					
				},
				'del':{

				}
			}
		}

		self.tab[tab][sub_tab] = initial_data[tab][sub_tab]


	def alterTable(self, tab:str, sub_tab:str, data:dict) -> None:
		"""	Get the data of an employee, teacher, student or a new schedule
			and we save it in the database.
		Args:
			tab (str): It specific the 'type' ('rector', 'teacher', 'student' or 'schedule')
			sub_tab (str): It specific the action ('add', 'upd' or 'del')
			data (dict): Data to save
		Returns: None
		"""
		def isCorrect(data:dict, sub_tab:str) -> bool:
			""" Get the data of an employee, teacher, student or a new schedule
				and it validates all the fields are filled.
			Args:
				data (dict): Data to validate.
			Returns:
				bool: True = is correct & False = is not correct. 
			"""
			correct = True
			for key in data:
				if not data[key] and sub_tab == 'upd':
					correct = False
					break

			return correct

		def userExist(tab:str, sub_tab:str, data:dict) -> bool:
			""" Get the data, main tab, secondary tab and then
				validate it account exist.
			Args:
				tab (str): type account ('rector', 'teacher', 'student')
				sub_tab (str): action ('add', 'upd', 'del')
				data (dict): data of account
			Returns:
				bool: True = user exist & False = user not exist
			"""
			if tab == 'rector':
				typ = 1

			elif tab == 'teacher':
				typ = 2

			else:
				typ = 3

			if app.execute("GetAccount '{}', '{}', '{}', '{}', '{}'".format(typ, data["enrollment"], data["middle_name"], data["last_name"], data["name"])):
				return True

			else:
				return False

		def isModified(d1:dict):
			"""	Get the selected data before modifying and the 'modified',
				and we validate if it was modified.
			Agrs:
				d1 (dict):
			Returns:
				tuple (bool, bool): (True = is modified & False = is not modified), 
									(True = name is modified & False = is not modified).
			"""
			modified = False
			if self.secondary_tab == 'upd':
				d2 = self.selected[self.secondary_tab][self.main_tab]
				if d1['name'] != d2['name'] or d1['middle_name'] != d2['middle_name'] or d1['last_name'] != d2['last_name']:
					modified = True

				return d1 != d2, modified
			else:
				return None, None
		

		def getEmail(typ:int, name:str, middle_name:str, last_name:str) -> str:
			"""	Generate the email for the user taking de args 
				and then returns it.
			Args:
				typ (int): type is the main tab (rector, teacher or student)
				name (str): first name (and second name)
				middle_name (str): father's 'name'
				last_name (str): mother's 'name'
			Returns:
				str: nonexistent email
			"""
			def nonexistenEmail(typ:int, email:str) -> str:
				"""	Get the email, validate it exist and returns it
					a nonexistent version.
				Args:
					typ (int): type is the main tab (rector, teacher or student)
					email (str): user email
				Returns:
					str: email 'modified'
				"""
				splited = email.split('@')
				max_email = app.execute("GetMaxEmail '{}', '{}'".format(typ, '{}%'.format(splited[0])))
				if max_email[0][0] != None:
					n:str = max_email[0][0].split('@')[0].replace(splited[0], '')
					if n != '':
						n = int(n) + 1
					email:str = splited[0] + '{}@'.format(n) + splited[1]
				
				return email

			shortened = last_name[0] + last_name[len(last_name)-1]
			email = '{}.{}{}@uanl.edu.mx'.format(name, middle_name, shortened)
			email = email.lower()

			return nonexistenEmail(typ, email)


		def getPassword() -> str:
			"""	Gen the random password and then returns it.
			Agrs: None
			Returns:
				str: random password
			"""
			chars = 'abcdefghijklmnñopqrstuvwxyz'
			chars += chars.upper()
			chars += '0123456789'
			password = ''
			for i in range(8):
				password += random.choice(chars)

			return password

		def fillEmptyFields(tab:str, sub_tab:str, data:dict) -> None:
			"""	Get data and fill the empty fields
			Args:
				tab (str): main tab
				sub_tab (str): secondary tab
				data (dict): data of recory employee, teacher
							 or student
			Returns: None
			"""
			keys = data.keys()
			for child in self.ids[tab].ids[sub_tab].ids.recycle_grid.children:
				if child.viewclass != tclass['rlabel'] and child.viewclass != tclass['rbuttons']:
					child.disabled = True

				elif child.viewclass == tclass['rsearch']:
					child.disable = True

				if child.name in keys:
					child.text = data[child.name]
				

		if isCorrect(data, sub_tab):
			user_exist:bool = userExist(tab, sub_tab, data)
			# user shuld not exist for adding & shuld exist for upd or del
			if (user_exist and sub_tab != 'add') or (not user_exist and sub_tab == 'add'):
				is_modified:bool = isModified(data) # tuple (is modified, is name modified)
				# is data modified for update? if sub tab == 'upd' or sub tab == 'del' is no important
				if (is_modified[0] and self.secondary_tab == 'upd') or (self.secondary_tab in ['add', 'del']):
					if tab == 'rector':
						n = 1
					elif tab == 'teacher':
						n = 2
					else:
						n = 3

					if sub_tab in ['add', 'upd'] and tab in ['rector', 'teacher', 'student']:
						data["email"] = getEmail(n, data["name"], data["middle_name"], data["last_name"])
						if sub_tab == 'add':
							data["pass"] = getPassword()

						else: # sub_tab == 'upd'
							# user name exist?
							if app.execute("GetAccount '{}', '', '{}', '{}', '{}'".format(n, data["middle_name"], data["last_name"], data["name"])):
								tab = ''

					if tab == "rector":
						app.execute(
							"AlterRectoryTable '{}', '{}', '{}', '{}', '{}', '{}', '{}'".format(
								data["enrollment"],
								data["name"], 
								data["middle_name"],
								data["last_name"],
								data["email"], 
								data["pass"], 
								sub_tab
							)
						)

						if sub_tab in ['add', 'upd']:
							if sub_tab == 'add':
								data["enrollment"] = str(
									app.execute(
										"GetIDEmployee '{}', '{}', '{}', '{}', '{}'".format(
											data["middle_name"],
											data["last_name"],
											data["name"],
											data["email"],
											data["pass"]
										)
									)[0][0]
								)
								text = 'El Empleado se a Guardado Correctamente.'
							else:
								text = 'Los Datos del Empleado se Actualizaron con éxito.'
							fillEmptyFields(tab, sub_tab, data)
						
						else: # del
							text = 'Los Datos del Empleado han sido Eliminados Eorrectamente.'
						
					elif tab == "teacher":
						for f in data["faculty"]:
							# f = faculty name
							# data["faculty"][f] = list of career(s)
							for c in data["faculty"][f]:
								app.execute(
									"AlterTeacherTable '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'".format(
										data["enrollment"],
										data["name"], 
										data["middle_name"],
										data["last_name"],
										f,
										c,
										data["email"],
										data["pass"], 
										sub_tab
									)
								)

						if sub_tab == 'add':
							data["enrollment"] = app.execute(
								"GetIDTeacher '{}', '{}', '{}', '{}', '{}'".format(
									data["middle_name"],
									data["last_name"],
									data["name"],
									data["email"],
									data["pass"]
								)
							)[0][0]

							fillEmptyFields(tab, sub_tab, data)
							text = 'El Profesor se a Guardado Correctamente.'
						elif sub_tab == 'upd':
							text = 'Los Datos del Profesor se Actualizaron con Éxito.'
						else: # del
							text = 'El datos del Profesor han sido Eliminados Correctamente.'

					elif tab == "student":
						app.execute(
							"AlterStudentTable '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'".format(
								data["enrollment"],
								data["name"], 
								data["middle_name"],
								data["last_name"],
								data["faculty"],
								data["career"],
								data["pass"],
								data["try"], 
								sub_tab
							)
						)

					elif tab == 'schedule':
						app.execute()

					if tab == '':
						app.showBanner(
							title='¡No se pudieron hacer las modificaciones!',
							text='El usuario ya existe.'
						)

					else:
						app.showBanner(
							title='¡Excelente!',
							text=text
						)

				else:
					app.showBanner(
						title='Sin Modificaciones',
						text='Aún no se modifica ningún dato.'
					)
			else:
				if user_exist and sub_tab == 'add':
					app.showBanner(
						title="¡Error de Almacenamiento!",
						text="Lo sentimos, no se ha podido guardar este usuario porque ya existe."
					)

				elif not user_exist and sub_tab != 'add': 
					app.showBanner(
						title="¡No se ha Ecnontrado el Usuario!",
						text="Lo sentimos, no hemos podido encontrar al usuario en nuestra base de datos."
					)
		else:
			app.showBanner(
				title="Aún hay campos por llenar",
				text="Por favor, llene todos los campos."
			)


	def setInitialStateForm(self, tab:str, sub_tab:str) -> None:
		""" Get the parent and child tab, and then set 
			the initial shape of the form
		Args:
			tab (str): main tab
			sub_tab (str): secondary tab
		Returns: None
		"""
		keys = self.tab[tab][sub_tab].keys()
		form:object = self.ids[tab].ids[sub_tab].ids.recycle_grid
		for child in form.children:
			if child.name in keys:
				child.disabled = sub_tab != 'add' # if sub tab == add - disabled = FALSE else TRUE

			if child.name == 'enrollment' and child.viewclass == tclass['rsearch']:
				child.disabled = False


	def clearWidgets(self, tab:str, sub_tab:str) -> None:
		keys = self.tab[tab][sub_tab].keys()
		form:object = self.ids[tab].ids[sub_tab].ids.recycle_grid
		#print('tab::', tab)
		#print('sub_tab::', sub_tab)
		for child in form.children:
			viewclass = child.viewclass

			if viewclass == tclass['rsearch'] or viewclass == tclass['rfield']:
				#print('viewclass::', viewclass, 'child name', child.name, 'child text::', child.text)
				child.text = ''

			#if sub_tab != 'add': # sub_tab = 'upd' or 'del'
			#	child.disabled = viewclass != tclass['rsearch']
			if child.name in keys:
				child.disabled = sub_tab != 'add' # if sub tab == add - disabled = FALSE else TRUE

			if child.name == 'enrollment' and child.viewclass == tclass['rsearch']:
				child.disabled = False

				
	def exit(self):
		pass

	