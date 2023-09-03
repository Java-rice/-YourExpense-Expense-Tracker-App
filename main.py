#Required Libraries
#Required Libraries
from kivymd.app import MDApp
from kivy.core.window import Window	
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase 
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton, MDRaisedButton, MDRectangleFlatIconButton, MDIconButton
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView  					
from kivymd.uix.dialog import MDDialog
from kivy.uix.button import Button
from kivymd.icon_definitions import md_icons
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.label import MDIcon
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.datatables import MDDataTable
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout	
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivymd.icon_definitions import md_icons
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.selectioncontrol import MDSwitch
import json
#Required Libraries
#Required Libraries

Builder.load_file('layout.kv')

#Screens
#Screens
class LogoScreen(Screen):
	#Start Screen
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def on_enter(self, *args):
		Clock.schedule_once(self.next_page, 4)
	def next_page(self, *args):
		self.manager.current = "Name_Input"

class NameInput(Screen):
	pass
class WelcomePage(Screen):
	pass
class WelcomeBackPage(Screen):
	pass
class HomePage(Screen):
	pass
class TrackerPage(Screen):
	pass	
class AddPlanPage(Screen):
	pass
class AddPaidPage(Screen):
	pass
class NotifPage(Screen):
	pass
class ReportPage(Screen):
	pass
#Screens
#Screens

#MAIN APPLICATION
class YourExpense(MDApp):
	def build(self):
		global sc_manager
		sc_manager = ScreenManager()
		sc_manager.add_widget(LogoScreen(name="Logo_Page"))
		sc_manager.add_widget(NameInput(name="Name_Input"))
		sc_manager.add_widget(WelcomePage(name="Welcome_Page"))
		sc_manager.add_widget(WelcomeBackPage(name="WelcomeBack_Page"))
		sc_manager.add_widget(HomePage(name="Home_Page"))
		sc_manager.add_widget(TrackerPage(name="Tracker_Page"))
		sc_manager.add_widget(AddPlanPage(name="AddPlan_Page"))
		sc_manager.add_widget(AddPaidPage(name="AddPaid_Page"))
		sc_manager.add_widget(ReportPage(name="Report_Page"))
		sc_manager.add_widget(NotifPage(name="Notif_Page"))
		return sc_manager

	#PROFILE CHECKER
	def get_data(self, name):
		global profile
		profile = name
		if len(name) == 0:
			invalid_but = MDRectangleFlatButton(text = 'Return', padding = [35, 0], on_release = self.cancel)
			self.dialogue = MDDialog(title = "Invalid Name", size_hint = (.9, 1), buttons = [invalid_but])
			self.dialogue.open()
		else:
			i = 0
			j = 0
			stckuser = {name: list()}
			stck = {name: {"Plan_Transaction": {}, "Paid_Transaction": {}}}
			for i in data.keys():
				if profile == i:
					j += 1
			if j < 1:
				data.update(stck)
				with open(database, "w") as f:
					json.dump(data,f,indent=2)
				info.update(stckuser)
				with open(user_reports, "w") as user:
					json.dump(info,user,indent=2)
				sc_manager.current = "Welcome_Page"
				self.root.get_screen("Welcome_Page").ids.Username_new.text = profile
				
				
			else:
				Proc_but = MDRectangleFlatButton(text = 'Proceed', padding = [23.8, 0], on_release = self.proceed_welcome)
				Ovrr_but = MDRectangleFlatButton(text = 'Override', padding = [23.8, 0], on_release = self.overide_welcome)
				Cancel_but = MDRectangleFlatButton(text = 'Cancel', padding = [23.8, 0], on_release = self.cancel)
				self.dialogue = MDDialog(title = "Account Already Exists", size_hint = (.9, 1), buttons = [Proc_but, Ovrr_but, Cancel_but])
				self.dialogue.open()


	def cancel(self, obj):
		self.dialogue.dismiss()	

	#PROCEED AS EXISTING ACCOUNT
	def proceed_welcome(self, obj):
		sc_manager.current = "WelcomeBack_Page"
		self.root.get_screen("WelcomeBack_Page").ids.Username.text = profile
		self.dialogue.dismiss()

	#DELETE AND REPLACE EXISTING ACCOUNT
	def overide_welcome(self, obj):
		del data[profile], info[profile]
		data.update({profile: {"Plan_Transaction": {}, "Paid_Transaction": {}}})
		with open(database, "w") as f:
			json.dump(data,f,indent=2)
		info.update({profile: list()})
		with open(user_reports, "w") as user:
			json.dump(info,user,indent=2)
		sc_manager.current = "Welcome_Page"
		self.root.get_screen("Welcome_Page").ids.Username_new.text = profile
		self.dialogue.dismiss()

	#PLAN TRANSACTION DATA
	def planrec(self, NTitle, NAmount, Ndate):
		NTransac = {NTitle: {"Amount": NAmount, "Date": Ndate, "Status":"Pending"}}
		TRecords = [f'You started a transaction entitled "{NTitle}"\namounting to {NAmount}' , Ndate]

		data[profile]["Plan_Transaction"].update(NTransac)
		with open(database, "w") as f:
			json.dump(data,f, indent = 3)
		info[profile].append(TRecords)
		with open(user_reports, "w") as user:
			json.dump(info,user, indent = 3)

	#PAID TRANSACTION DATA
	def paidrec(self, DTitle, DAmount, DDate):
		DTransac = {DTitle: {"Amount": DAmount, "Date": DDate , "Status": "Paid"}}
		DRecords = [f'You have done a transaction entitled "{DTitle}"\namounting to {DAmount}', DDate]
		data[profile]["Paid_Transaction"].update(DTransac)
		with open(database, "w") as f:
			json.dump(data,f, indent = 3)
		info[profile].append(DRecords)
		with open(user_reports, "w") as user:
			json.dump(info,user, indent = 3)

	#DATEPICKER
	def show_date(self):
		date_dialog = MDDatePicker()
		date_dialog.bind(on_save = self.on_ok, on_cancel = self.on_cancel)
		date_dialog.open()

	#OK BUTTON - DATE
	def on_ok(self, instance, value, data_range):
		wdate = f'{value.day}/{value.month}/{value.year}'
		if sc_manager.current == "AddPlan_Page":
			self.root.get_screen("AddPlan_Page").ids.date.text = str(wdate)
		elif sc_manager.current == "AddPaid_Page":
			self.root.get_screen("AddPaid_Page").ids.date.text = str(wdate)

	#CANCEL BUTTON - DATE	
	def on_cancel(self, instance, value):
		pass

	#LOGOUT BUTTON
	def logout(self):
		Yes_but = MDRectangleFlatButton(text = 'Yes', padding = [35, 0], on_release = self.YES_choice)
		No_but = MDRectangleFlatButton(text = 'No', padding = [35, 0], on_release = self.NO_choice)
		self.Y_N = MDDialog(title = "Are you sure, you want to exit?", size_hint = (.9, 1), buttons = [Yes_but, No_but])
		self.Y_N.open()

	#CONFIRM LOGOUT
	def YES_choice(self, obj):
		self.Y_N.dismiss()
		sc_manager.current = "Name_Input"

	#CANCEL LOGOUT
	def NO_choice(self, obj):
		self.Y_N.dismiss()

	#REPORT PAGE CONTENT
	def ReportsBox(self):
		Reportslen = len(info[profile])
		for i in range(Reportslen):
			boxmain = RelativeLayout(size_hint=(1, 1))
			box = Image(source="assets/Notifbox.png", size_hint = (1, 1))
			Rtext = Label(text = info[profile][i][0], pos_hint = {'center_x': 0.55, 'center_y': 0.4},
				font_size = "10sp", 
				font_name= "Poppins", 
				halign= 'center', 
				color= (255, 255, 255)
				)
			datetext = Label(text = info[profile][i][1], pos_hint = {'center_x': 0.33, 'center_y': 0.69},
				font_size = "10sp", 
				font_name= "Poppins", 
				halign= 'center', 
				color= (255, 255, 255)
				)
			boxmain.add_widget(box)
			boxmain.add_widget(datetext)
			boxmain.add_widget(Rtext)
			self.root.get_screen("Report_Page").ids.report_container.add_widget(boxmain)

		sc_manager.current = "Report_Page"

	#TRACKER BOX CONTENT
	def TrackerBoxes(self):
		NTrackerlen = len(data[profile]["Plan_Transaction"])
		DTrackerlen = len(data[profile]["Paid_Transaction"])
		Plankeys = list(data[profile]["Plan_Transaction"].keys())
		Paidkeys = list(data[profile]["Paid_Transaction"].keys())

		#PLAN TRACKER COLUMN
		for i in range(NTrackerlen):
			NMbox = RelativeLayout(size_hint=(1, .8))
			Nbox = Image(source="assets/row.png", size_hint = (1, 1))
			Ngrid_box = GridLayout(size_hint= (.98, 1), cols = 4)
			NNLabel = Label(text = str(Plankeys[i]),
				font_size = "11sp", 
				font_name= "Poppins", 
				halign= 'center', 
				color= (255, 255, 255),
				size_hint_x=None, 
				width=120)
			NALabel = Label(text = str(data[profile]["Plan_Transaction"][Plankeys[i]]["Amount"]),
				font_size = "11sp", 
				font_name= "Poppins", 
				halign= 'center', 
				color= (255, 255, 255),
				size_hint_x = None,
				width = 85)
			NDLabel = Label(text = str(data[profile]["Plan_Transaction"][Plankeys[i]]["Date"]),
				font_size = "11sp", 
				font_name= "Poppins", 
				halign= 'center', 
				color= (255, 255, 255),
				size_hint_x = None, 
				width = 90)
			if str(data[profile]["Plan_Transaction"][Plankeys[i]]["Status"]) == "Pending":
				NSLabel = Label(text = "Ongoing",
					font_size = "10sp", 
					font_name= "Poppins", 
					halign= 'center', 
					color= (255, 255, 255),
					size_hint_x = None, 
					width = 63)
			else:
				NSLabel = Label(text = "Paid",
					font_size = "10sp", 
					font_name = "Poppins", 
					halign = 'center', 
					color = (255, 255, 255),
					size_hint_x = None, 
					width = 63)

			NMbox.add_widget(Nbox)
			Ngrid_box.add_widget(NNLabel)
			Ngrid_box.add_widget(NALabel)
			Ngrid_box.add_widget(NDLabel)
			Ngrid_box.add_widget(NSLabel)
			NMbox.add_widget(Ngrid_box)

			self.root.get_screen("Tracker_Page").ids.plan_container.add_widget(NMbox)

		#PAID TRACKER COLUMN
		for i in range(DTrackerlen):
			DMbox = RelativeLayout(size_hint=(1, .8))
			Dbox = Image(source="assets/row.png", size_hint = (1, 1))
			Dgrid_box = GridLayout(size_hint= (.98, 1), cols = 4)
			DNLabel = Label(text = str(Paidkeys[i]),
				font_size = "11sp", 
				font_name= "Poppins", 
				halign= 'center', 
				color= (255, 255, 255),
				size_hint_x=None, 
				width= 120)
			DALabel = Label(text = str(data[profile]["Paid_Transaction"][Paidkeys[i]]["Amount"]),
				font_size = "11sp", 
				font_name= "Poppins", 
				halign= 'center', 
				color= (255, 255, 255),
				size_hint_x=None, 
				width= 85)
			DDLabel = Label(text = str(data[profile]["Paid_Transaction"][Paidkeys[i]]["Date"]),
				font_size = "11sp", 
				font_name= "Poppins", 
				halign= 'center', 
				color= (255, 255, 255),
				size_hint_x=None, 
				width= 90)
			if str(data[profile]["Paid_Transaction"][Paidkeys[i]]["Status"]) == "Pending":
				DSLabel = Label(text = "Ongoing",
					font_size = "10sp", 
					font_name= "Poppins", 
					halign= 'center', 
					color= (255, 255, 255),
					size_hint_x = None, 
					width = 63)
			else:
				DSLabel = Label(text = "Paid",
					font_size = "10sp", 
					font_name= "Poppins", 
					halign= 'center', 
					color= (255, 255, 255),
					size_hint_x = None, 
					width = 63)
			DMbox.add_widget(Dbox)
			Dgrid_box.add_widget(DNLabel)
			Dgrid_box.add_widget(DALabel)
			Dgrid_box.add_widget(DDLabel)
			Dgrid_box.add_widget(DSLabel)
			DMbox.add_widget(Dgrid_box)

			self.root.get_screen("Tracker_Page").ids.paid_container.add_widget(DMbox)

		sc_manager.current = "Tracker_Page"

	#CLEAR WIDGETS IN TRACKER PAGE
	def clearwidg(self):
		self.root.get_screen("Tracker_Page").ids.plan_container.clear_widgets()
		self.root.get_screen("Tracker_Page").ids.paid_container.clear_widgets()

	#CLEAR WIDGETS IN REPORT PAGE
	def reportsclear(self):
		self.root.get_screen("Report_Page").ids.report_container.clear_widgets()

	#CLEAR WIDGETS IN STATUS PAGE
	def Notifclear(self):
		self.root.get_screen("Notif_Page").ids.Notif_container.clear_widgets()

	#STATUS PAGE CONTENT
	def NotifBoxes(self):
		
		global stockd
		Notiflen = len(data[profile]["Plan_Transaction"])
		Notifnames = list(data[profile]["Plan_Transaction"].keys())
		for i in range(Notiflen):
			stockd = Notifnames[i]
			Noboxmain = RelativeLayout(size_hint=(1, 1))
			picbox = Image(source="assets/Notifboxes.png", size_hint = (.9, 1), pos_hint = {'center_x': 0.5, 'center_y': 0.5})
			Nicon = MDIcon(icon = "calendar", pos_hint = {'center_x': 0.1, 'center_y': 0.5})
			Notiftext = Label(text = str(Notifnames[i]), pos_hint = {'center_x': .5, 'center_y': 0.69},
				font_size = "13sp", 
				font_name= "Poppins", 
				color= (255, 255, 255)
				)
			NotifA = Label(text = str(data[profile]["Plan_Transaction"][Notifnames[i]]["Amount"]), pos_hint = {'center_x': 0.5, 'center_y': 0.35},
				font_size = "13sp", 
				font_name= "Poppins", 
				halign= 'center', 
				color= (255, 255, 255)
				)
			Notifdatetext = Label(text = str(data[profile]["Plan_Transaction"][Notifnames[i]]["Date"]), pos_hint = {'center_x': 0.85, 'center_y': 0.5},
				font_size = "13sp", 
				font_name= "Poppins", 
				halign= 'center', 
				color= (255, 255, 255)
				)
			Noboxmain.add_widget(picbox)
			Noboxmain.add_widget(Notiftext)
			Noboxmain.add_widget(NotifA)
			Noboxmain.add_widget(Notifdatetext)
			Noboxmain.add_widget(Nicon)
			self.root.get_screen("Notif_Page").ids.Notif_container.add_widget(Noboxmain)

		
		sc_manager.current = "Notif_Page"

#MAIN FUNCTION
if __name__ == '__main__':

	#WINDOW SIZE
	Window.size = (360, 640)

	#FONT REGISTER
	LabelBase.register(name = "Poppins", fn_regular= "assets/Poppins.ttf")

	global profile
	#json file - data storage
	database = "datastorage.json"
	user_reports = "user_reports.json"

	#TRACKER INFO
	with open( database, "r") as f:
		data = json.loads(f.read())

	#USER RECORDS INFO
	with open( user_reports, "r") as user:
		info = json.loads(user.read())

	#RUN THE MAIN APPLICATION
	YourExpense().run()