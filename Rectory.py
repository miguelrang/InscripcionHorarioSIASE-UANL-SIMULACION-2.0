from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, OptionProperty, NumericProperty, BooleanProperty, ColorProperty
from kivy.uix.button import Button
from kivy.clock import mainthread

from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextFieldRect, MDTextField#Round
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.menu import MDDropdownMenu
#from kivymd.uix.list import OneLineIconListItem

import threading
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

Builder.load_file('Classroom.kv')
class Classroom(MDFloatLayout, MDTabsBase):
	''''''

Builder.load_file('Schedule.kv')
class Schedule(MDFloatLayout, MDTabsBase):
	''''''

Builder.load_file("Form.kv")
"""
class RTextField(MDTextFieldRect):
	''''''

#class RLabel(MDLabel):
#	text = StringProperty()
#	name = StringProperty()
#	halign = OptionProperty("left", options=["left", "center", "right"])
#	valign = OptionProperty("left", options=["left", "center", "bottom", "top"])
#
#class RButtons(MDFloatLayout):
#	text = StringProperty()
#	disabled = BooleanProperty()
#	name = StringProperty()
#	disable = BooleanProperty()
class RCancelButton(MDFlatButton):
	''''''

class RActionButton(MDRaisedButton):
	''''''

class RSearch(MDBoxLayout):
	''''''

class RSearchClassroom(MDTextFieldRect):
	''''''

class RSearchSubject(MDTextFieldRect):
	''''''

class ROptions(MDTextFieldRect):
	''''''

class RKardexButton(Button):
	''''''

"""
class FBoxLayout(MDBoxLayout):
	''''''
class FFinder(MDTextField):
	''''''
class FLabel(MDLabel):
	''''''
class FTextField(MDTextFieldRect):
	def shortField(name:str) -> str:
		"""	We validate if the length of the text is longer than
			what is accepted.
		Args:
			name (str): Text field hint
		Returns:
			str: text shorted
		"""
		if len(text) > leng:
			app.showBanner(
				title='¡Atención!',
				text='La longitud de \'{}\' del aula no puede ser mayor de {}.'.format(name, leng)
			)
		return text[:leng]

class FSearcher(MDTextFieldRect):
	''''''
class FKardex(Button):
	''''''
class FCancelButton(MDFlatButton):
	''''''
class FActionButton(MDRaisedButton):
	''''''

class Rectory(Screen):
	def __init__(self, **kwargs):
		super(Rectory, self).__init__(**kwargs)
		global app
		app = MDApp.get_running_app()

		'''
		self.tab = {'rector':{}, 'teacher':{}, 'student':{}, 'classroom':{}, 'schedule':{}}
		self.setInititalData('rector', 'add')
		self.setInititalData('rector', 'upd')
		self.setInititalData('rector', 'del')

		self.setInititalData('teacher', 'add')
		self.setInititalData('teacher', 'upd')
		self.setInititalData('teacher', 'del')
		
		self.setInititalData('student', 'add')
		self.setInititalData('student', 'upd')
		self.setInititalData('student', 'del')

		self.setInititalData('classroom', 'add')
		self.setInititalData('classroom', 'upd')
		self.setInititalData('classroom', 'del')
		
		self.setInititalData('schedule', 'add')
		self.setInititalData('schedule', 'upd')
		self.setInititalData('schedule', 'del')
		'''

		global tclass
		tclass = {
			#'rlabel': type(RLabel()),
			#'rfield': type(RTextField()),
			#'rbuttons': type(RButtons()),
			#'rsearch': type(RSearch()),
			#'roptions': type(ROptions()),
			#'rkbutton': type(RKardexButton())
		}
		
		self.selected = {'upd': {'rector':{}, 'teacher':{}, 'student':{}, 'schedule':{}}}
		self.selected['del'] = self.selected['upd']

		self.field = None
		self.main_tab = 'rector'
		self.secondary_tab = 'add'

		self.menu = MDDropdownMenu(position='bottom')
		self.menu_items = []


	def setData(self, id_rector=int(), employee=str()) -> None:
		"""	Get the rectory employee id and name, we
			show this data and initialize the forms.
		Args:
			id_rector (int): employee id
			employee (str): employee name
		Returns: None
		"""
		
		self.ids["enrollment"].text = "[color=#ffffff][b]Matricula:[/b] {}[/color]".format(id_rector)
		self.ids["employee"].text = "[color=#ffffff][b]Empleado:[/b] {}[/color]".format(employee)


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

			elif 'Aula' in tab_text:
				tab = 'classroom'

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


	def text_validate(self, field:object, text:str, leng:int) -> None:
		""" Get a field, its name and text too. If text is not like is
			required in database, we modify it. Finally we update it.
		Args:
			field (object): Field we are writing.
			text (str): Text of field.
			leng (int): Maximum length for the field.
		Returns: None
		"""
		if field.active:
			if 'name' in field.name:
				text = text.title()
				
				nums = set('0123456789') & set(text)
				if nums:
					app.openDialog(
						title='Atención',
						text='No se permiten números en el nombre o apellido.'
					)
					for num in nums:
						text = text.replace(num, '')

			elif 'classroom' in field.name:
				text = text.upper()

			chars = '¬°!"#$%/()=\'?\\¿¡´¨*+~{^[]},;.-_'
			text_alert = 'Este campo no admite caracteres especiales'
			if 'classroom' not in field.name:
				chars += '|:'
				text_alert += ' (excepciones: \'|\', \':\')'
			text_alert += '.'
			
			chars = set(text) & set(chars)
			if chars:
				app.showBanner(
					title='¡Atención!',
					text=text_alert
				)
				for char in chars:
					text = text.replace(char, '')

			field.text = text
		else:
			field.text = ''

	'''
	def setWidget(self, wdg:object):
		recycle_grid = self.ids[self.main_tab].ids[self.secondary_tab].ids.recycle_grid
		for wdg_grid in recycle_grid.children:
			wdg_grid.disabled = True
				#break


	def search(self, field:object, text:str, length:int, tab:str, sub_tab:str) -> None:
		""" Get a textfield, its content and some parameters has to complete, so,
			we validate it. If is correct, we refill the restant fields for the user
			data.
		Params:
			field (object): Field
			text (str): field text
			length (int): maximum text length for field
			tab (str): user (rector(employee) | teacher | student)
			sub_tab (str): action (add | upd (update) | delete (del))
		Returns: None
		"""
		if field.text != "":
			if len(text) > length:
				# excedent...
				app.showBanner(
					title="Longitud Excedida",
					text='Este campo solo admite una longitud de {} caracteres'.format(length)
				)
			
			else: # all right
				data:tuple = app.execute("GetAccountData '{}', '{}'".format(tab, text))
				if data:
					i:int = len(data[0])-1
					#data = data[0]
					form:object = self.ids[tab].ids[sub_tab].ids.recycle_grid
					print('def SEARCH')
					print("DATA SELECT:", data)
					facus = set()
					careers = set()
					for d in data:
						for child in form.children:
							print(child.name.upper(), '*******************')
							if child.viewclass in [tclass['rsearch'], tclass['rfield'], tclass['roptions'], tclass['rbuttons']]:
								if child.viewclass != type(RButtons()):
									print("child:", child.name, "-", d[i])
									child.text = str(d[i])
		
									if child.name == 'faculty':
										facus.add(child.text)
										child.text = ', '.join(facus)
									elif child.name == 'career':
										careers.add(child.text)
										child.text = ', '.join(careers)
									self.tab[tab][sub_tab][child.name] = child.text
									
									i -= 1

								if sub_tab == "upd":
									#print(child.name)
									child.disabled = "enrollment" == child.name
									if child.viewclass == tclass['rbuttons']:
										child.disable = False

								elif sub_tab == 'del':
									child.disabled = child.viewclass != tclass['rbuttons'] # or class in ['rfield', 'rsearch']
									child.disable = child.disabled
								
								else: # add
									child.disabled = "enrollment" != child.name and child.name != "buttons"

						if self.secondary_tab in ['upd', 'del']:
							self.selected[sub_tab][tab] = self.tab[tab][sub_tab].copy()
				else:
					app.showBanner(
						title='Matricula Invalida o Iconrrecta',
						text="Lo sentimos, no se pudo encontrar ninguna cuenta con la matricula: {}.".format(text)
					)
					
		else:
			app.showBanner(
				title='¡Campo Vacío!',
				text='Debe de llenar el campo de busqueda.'
			)


	def text_validate(self, name:str, field:object, text:str)-> None:
		"""	Get a field and its text to set self text (some
			fields have different funtionalities)
		Args:
			name (str): row name (it helps us to know if the user is 
						in add, upd or del)
			field (object): field contains the full data 
							(text field, hint_text, etc.)
			text (str): content field (text)
			length (int): equivalent to max text length
		Returns: None
		"""
		if field.input_filter == 'int':
			self.tab[self.main_tab][self.secondary_tab][name] = text

		elif field.hint_text not in ['Matricula', 'Correo Universitario', 'Contraseña']:
			if field.focus == False:
				if field.input_filter != 'int' and set(text)&set("0123456789"):
					app.showBanner(
						title="Números Añadidos",
						text="Este campo no admite números."
					)
				
				for num in '0123456789': text = text.replace(num, '')

				field.text = text
				self.tab[self.main_tab][self.secondary_tab][name] = text
				
		else: # The field is the Enrollment, Email or Password
			if self.secondary_tab == "add" or "email" in name:
				app.openDialog(
					title='Campo Bloqueado',
					text='Este campo mostrara tu {} una vez guardados tus datos.'.format(field.hint_text)
				)

			else:
				self.tab[self.main_tab][self.secondary_tab][name] = text

	@mainthread
	def setClassrooms(self, seeker:object, options:list, text:str) -> None:
		"""	We get from database all classrooms and we save it in
			a list of dictionaries.
		Args:

			options (list): A list of tuples (each tuple contains 
							classroom data).
			text (str): Text for classroom option
		Returns: None
		"""
		def completeData(selected:str) -> None:
			seeker.text = selected
			#self.menu.dismiss()

		#options = app.execute("GetClassrooms")
		if options:
			self.menu_items = [{"text": data[0], "viewclass": "OneLineListItem", "on_press": lambda x=data[0]: completeData(x)} for data in options]
		else:
			app.showDialog(
				title='¡Sin {} para Mostrar!'.format(text),
				text='Actualmente no hay {} en la base de datos.'.format(text)
			)


	@mainthread
	def showClassrooms(self, caller:object, searching:str, widget=None) -> None:
		"""	We search coincidences from 'searching' variable and
			we shows them on screen.
		Args:
			caller (object): Widget for MDDropdownMenu widget.
			searching (str): Classroom to search or similars.
			id_classroom (object): Field where we shows the classroom id.
			classroom (object): Field where we show the classroom name/number.
			banches (object): Field where we show the enable banches in classroom.
			action (object): Action to do (Update / Delete).
		Returns: None
		"""
		def addFieldsContent(data:str) -> None:
			""" We show the classroom info in the fields.
			Args:
				data (str): Classroom we wrote in the seeker
			Returns: None
			"""
			data = app.execute("getClassroom '{}', '{}'".format(data.split(': ')[0], data.split(': ')[1]))[0]
			
			i = 0
			for wdg in widget.values():
				wdg.text = str(data[i]) if 'save' not in wdg.name else wdg.text # ignore button
				wdg.text = '' if self.main_tab == 'schedule' and 'subject' in wdg.name else wdg.text # clear schedule

				if 'upd' == self.secondary_tab and 'id_classroom' not in wdg.name:
					wdg.disabled = False
				elif 'del' == self.secondary_tab and 'del_save' == wdg.name:
					wdg.disabled = False

				i += 1

		def clearFieldsContent() -> None:
			""" We clear the content fields.
			Args: None
			Returns: None
			"""
			for wdg in widget.values():
				wdg.text = '' if 'save' not in wdg.name else wdg.text
				wdg.disabled = True


		if caller.text != '':
			coincidence = re.compile(r'(.?)*{}(.?)*'.format(searching))

			self.menu.caller = caller
			try:
				self.menu.dismiss()
			except:
				pass
			self.menu.items = []
			for option in self.menu_items:
				if coincidence.fullmatch(option['text']):
					self.menu.items.append(option)
					
					addFieldsContent(searching) if option['text'] == searching else clearFieldsContent()
						
			if self.menu.items == []:
				app.showBanner(
					title='¡Sin Coincidencias!',
					text='No pudimos encontrar ninguna coincidencia: {}'.format(searching)
				)

			elif len(self.menu.items) == 1 and self.menu.items[0]['text'] == searching:
				try:
					self.menu.dismiss()
				except:
					pass
			else:
				self.menu.width_mult=7.1
				self.menu.open()
		else:
			self.menu.dismiss()


	def showOptions(self, forms:object, field:object, enrollment:str, employee:str):
		if app.root.get_screen('options').setData(forms, field, enrollment, employee):
			app.root.current='options'


	def showKardex(self, forms:dict, button:object, enrollment:str, employee:str):
		if app.root.get_screen('options').setData(forms, button, enrollment, employee, self.secondary_tab):
			app.root.current='options'
				

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
					'faculty': [], # facutlty or faculties + career or careers (strings)
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
					'faculty': [], # facutlty or faculties + career or careers (strings)
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
					'status': '', # int
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
					'status': '', # int
					'kardex': {}, # dict with cursed subjects in the before career
				},
				'del':{
					'enrollment': ''
				}
			},
			'classroom': {
				'add': {
					'faculty': '', # str
					'classroom': '', # str
					'banches': '' # str
				},
				'upd':{
					'id_classroom': '', # str
					'faculty': '', # str
					'classroom': '', # str
					'banches': '' # str
				},
				'del':{
					'id_classroom': '' #str
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
		print('alterTable', data)
		

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

			if viewclass in [tclass['rsearch'], tclass['rfield'], tclass['roptions']]:
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

	'''