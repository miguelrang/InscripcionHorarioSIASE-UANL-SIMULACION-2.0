from kivymd.app import MDApp
from kivymd.uix.list import IRightBodyTouch, OneLineIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.boxlayout import MDBoxLayout

from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivy.properties import StringProperty, ColorProperty


class RightCheckBox(MDCheckbox):
	''''''

class ROption(OneLineIconListItem):
	label = StringProperty()
	#grp = StringProperty()

class RKardexSubject(MDBoxLayout):
	orientation='horizontal'
	spacing=dp(1)
	subject = StringProperty()
	rgba = ColorProperty()

class Options(Screen):
	def __init__(self, **kwargs):
		super(Options, self).__init__(**kwargs)

		global app
		app = MDApp.get_running_app()

		self.field:object = None
		self.forms:object = None
		self.option:int = 0
		self.selected = []


	def setData(self, forms:object, field:object, enrollment:str, employee:str, sub_tab=str()) -> bool:
		""" Get 4 params (
			, 4th: Rectory Employee is adding,
			updating the user data).
		Args:
			forms (object): the forms we are editing.
			field (object): text field where we will save the options selected.
			enrollment (str/int): Enrollment of rectory employe is adding or 
								  updating the user data.
			employee (str): Rectory Employee is adding or updating the user data.
		Returns: 
			None
			bool: True = the student has kardex & False no
		"""
		self.ids['enrollment'].text = enrollment
		self.ids['employee'].text = employee

		self.forms = forms
		self.selected = field.text.split(', ')
		if self.selected == ['']:
			self.selected = []

		self.field = field
		recycle = self.ids.recycle
		recycle.data = []
		if field.text == 'Kardex': # field = button
			if forms['career']:
				for career in forms['career'].split(', '):
					id_career = career.split(': ')[0]
					recycle.data.append(
						{
							"viewclass": "RLabel",
							"text": "[b]Kardex - {}[/b]".format(career.split(': ')[1]),
							"md_bg_color": (255/255, 234/255, 150/255, 1),
							"halign": "left",
							"valign": "center"
						}
					)

					n = 1
					subjects = app.execute("GetRectoryKardex '{}', '{}', ''".format(sub_tab, id_career))
					print(subjects)
					for subject in subjects:
						if n % 2 == 0:
							color = (.9, .9, .9, 1)
						else:
							color = (1, 1, 1, 1)
						
						recycle.data.append(
							{
								"viewclass": "RKardexSubject",
								"subject": subject[0],
								"rgba": color
							}
						)
						n += 1
				return True
			else:
				app.showBanner(
					title='¡Kardex Deshabilitado!',
					text='Por favor, asegurese de que este cursando una carrera.'
				)
				return False
			
		elif 'Facultad' in field.hint_text:
			self.option = 1
			faculties = app.execute("GetFaculties")
			for facu in faculties:
				recycle.data.append(
					{
						'viewclass': 'ROption',
						#'grp': '1',
						'label': '{}: {}'.format(facu[0], facu[1])
					}
				)

			return True
			
		elif 'Carrera' in field.hint_text:
			self.option = 2
			for child in forms.ids.recycle_grid.children:
				if child.name == 'faculty':
					#careers = []
					for facu in child.text.split(', '):
						print('SHOW MISTAKE')
						print(facu)
						if facu != '':
							fac_car = app.execute("GetCareers '{}'".format(facu.split(': ')[0]))
							for career in fac_car:
								#careers.append(career)
								recycle.data.append(
									{
										'viewclass': 'ROption',
										'label': '{}: {}'.format(career[0], career[1])
									}
								)

							return True
						else:
							app.openDialog(
								title='¡No hay Carreras para Mostrar!',
								text='Primero debes elegir una facultad.'
							)
							return False
					break


	def addSelected(self, forms:object, option:int, field:object, selected:list) -> None:
		"""	Get the selected faculties/careers for the text field. If we choose 
			the faculties field, we remove the careers from the career field if 
			not correspond to the chosen faculties.
		Args:
			forms (object): Forms where we have our field.
			option (int): 1 = Faculties, 2 = Careers.
			field (object): TextField where we will show the chosen
							faculties/careers.
			selected (list): List with the chosen faculties/careers.
		Returns: None
		"""
		rectory = app.root.get_screen('rectory')
		if option == 1 : # faculties
			if selected != []: # faculties selected
				field.text:str = ', '.join(selected) # saving faculties in fields
				allowed_careers:list = [] # here we will save the careers corresponds to the chosen faculties
				for facu in selected: # facu in selected faculties
					f:str = facu.split(': ')[0] # 'id_faculty: faculty'.split(': ')[0] -> id_faculty
					careers = app.execute("GetCareers '{}'".format(f)) # Where ID_faculty='f' -> ((id_career1, career1,),...)
					for career in careers: # (id_careerN, careerN,) in ((id_career1, career1,),..., (id_careerN, careerN,),)
						allowed_careers.append('{}: {}'.format(career[0], career[1]))

				for child in forms.ids.recycle_grid.children: # for object in objects (fields / labels / buttons)
					if child.name == 'career': # object is the career textfield
						old_careers:list = child.text.split(', ') # Get ['id_career1: career1',..., 'id_careerN: careerN']
						career_field:object = child
						break

				removed:list = [] # careers to remove from the career field (we do this because this careers not correspond to the selected faculties)
				for c in old_careers.copy(): # 'id_careerN: careerN' in ['id_career1: career1',..., 'id_careerN: careerN']
					if c not in allowed_careers: # career not allowed
						removed.append(c)
						old_careers.remove(c)
				career_field.text = ', '.join(old_careers) # we save the enable & chosen careers
				rectory.tab[rectory.main_tab][rectory.secondary_tab]['career'] = career_field.text

				title = text = ''
				if removed != []: # if we removed any career from the career field
					title = ' & Carreras Eliminadas'
					text = '\nCarrera(s): ' + ', '.join(removed)

				app.showBanner(
					title='Facultad(es) Seleccionadas'.format(title),
					text='Facultad(es): {}{}'.format(field.text, text)
				)

			else: # NO faculties selected, so, we remove all careers from career field
				field.text = ''
				rectory.tab[rectory.main_tab][rectory.secondary_tab]['career'] = ''
				for child in forms.ids.recycle_grid.children:
					if child.name == 'career':
						child.text = ''
						break

				app.showBanner(
					title='¡Facultades sin Marcar!',
					text='Debes de marcar al menos una facultad.'
				)

			rectory.tab[rectory.main_tab][rectory.secondary_tab]['faculty'] = field.text

		else: # option 2 -> careers
			field.text = ', '.join(selected) # we save the selected careers
			rectory.tab[rectory.main_tab][rectory.secondary_tab]['career'] = field.text # we repeat the before step for the dict.
			
			if field.text != '': # Careers selected
				app.showBanner(
					title='Carrera(s) Seleccionadas',
					text=field.text
				)
			else: # NO Careers selected
				app.showBanner(
					title='¡Carreras sin Marcar!',
					text='Debes de marcar al menos una carrera.'
				)
	
	def exit(self, recycle:object):
		recycle.data = []
		app.root.current='rectory'



