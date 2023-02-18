from kivymd.app import MDApp
from kivymd.uix.list import IRightBodyTouch, OneLineIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty


class RightCheckBox(MDCheckbox):
	''''''

class ROption(OneLineIconListItem):
	label = StringProperty()
	#grp = StringProperty()

class Options(Screen):
	def __init__(self, **kwargs):
		super(Options, self).__init__(**kwargs)

		global app
		app = MDApp.get_running_app()

		self.field:object = None
		self.forms:object = None
		self.option:int = 0
		self.selected = []


	def setData(self, forms:object, field:object, enrollment:str, employee:str):
		self.forms = forms
		self.selected = field.text.split(', ')
		if self.selected == ['']:
			self.selected = []

		self.field = field
		recycle = self.ids.recycle
		recycle.data = []
		if 'Facultad' in field.hint_text:
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
			
		else: # career
			self.option = 2
			for child in forms.ids.recycle_grid.children:
				if child.name == 'faculty':
					#careers = []
					for facu in child.text.split(', '):
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
						else:
							app.openDialog(
								title='¡No hay Carreras para Mostrar!',
								text='Primero debes elegir una facultad.'
							)
					break

		self.ids['enrollment'].text = enrollment
		self.ids['employee'].text = employee


	def addSelected(self, forms:object, option:int, field:object, selected:list):
		if option == 1: # faculties
			field.text = ''
			allowed_careers = []
			for facu in selected:
				field.text += facu + ', '

				careers = app.execute("GetCareers '{}'".format(field.text.split(': ')[0]))
				for career in careers:
					allowed_careers.append(career[1])

			field.text = field.text[:len(field.text)-2]
			for child in forms.ids.recycle_grid.children:
				if child.name == 'career':
					old_careers = child.text.split(', ')
					child.text = ''
					for career in old_careers.copy():
						if career in allowed_careers:
							child.text = career + ', '
					child.text = child.text[:len(child.text)-2]

					break

	
	def exit(self, recycle:object):
		recycle.data = []
		app.root.current='rectory'



