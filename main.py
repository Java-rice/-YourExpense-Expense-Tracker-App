#######Required Libraries########
#layout libraries
import kivy
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.core.text import LabelBase 
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.textfield import MDTextField
from kivymd.icon_definitions import md_icons
from kivy.properties import ListProperty
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.screenmanager import NoTransition
import re
#layout Libraries

##database libraries
import pymongo
from pymongo import MongoClient
##database libraries

##validation api
from kivyauth.google_auth import initialize_google, login_google, logout_google
#235651464495-v9qn51gb53394mig64avc51ijaf1q439.apps.googleusercontent.com
#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
##google and facebook acc api

Builder.load_file('layout.kv')
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

#Screens
class LogoScreen(Screen):
	#Start Screen
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def on_enter(self, *args):
		Clock.schedule_once(self.next_page, 4)

	def next_page(self, *args):
		self.manager.current = "Loading_Screen"

class LoadingScreen(Screen):
	#Loading Screen
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def on_enter(self, *args):
		Clock.schedule_once(self.login, 4)

	def login(self, *args):
		self.manager.current = "Login_Screen"

class LoginScreen(Screen):
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	#To make password visible
	def show_password(self, checkbox, value):
		if value:
			self.ids.password.password = False
		else:
			self.ids.password.password = True

	def loginverification(self, Luname, Lpass):

		self.ids.Lusername.helper_text = ""
		self.ids.Lpassword.helper_text = ""

		currentUsername = userprofile.find_one({})
		l = 0

		#username and email doesnt exist
		if len(Luname) == 0:
			self.ids.Lusername.helper_text = "Required"
			l += 1
		else:
			if (re.fullmatch(regex, Luname)):
				if currentUsername[Luname]["Email"] != Luname:
					self.ids.Lusername.helper_text = "Email doesn't exist"
					l += 1
				else:
					l += 0
			elif currentUsername is None:
				self.ids.Lusername.helper_text = "Username doesn't exist"
				l += 1	

		if len(Lpass) == 0:
			self.ids.Lpassword.helper_text = "Required"	
			l += 1
		else:
			if currentUsername[Luname]["Password"] != Lpass:
				self.ids.Lpassword.helper_text = "Wrong Password"
				l += 1

		if l > 0:
			self.manager.current = "Login_Screen"
			
		else:
			self.ids.Lusername.text = ""
			self.ids.Lpassword.text = ""

			User_name = Luname
			User_password = Lpass

			self.manager.current = "WelcomeBack_Screen"
			self.manager.get_screen("WelcomeBack_Screen").ids.name.text = str(currentUsername[Luname]["First_Name"])


class RegisterScreen(Screen):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	#To make password visible
	def show_Rpassword(self, checkbox, value):
		if value:
			self.ids.Rpassword.password = False
		else:
			self.ids.Rpassword.password = True

	#To make password visible
	def show_RCpassword(self, checkbox, value):
		if value:
			self.ids.RCpassword.password = False
		else:
			self.ids.RCpassword.password = True

	def regverification(self, Fname, Lname, Uname, Email, Rpass, RCpass):


		self.ids.Fname.helper_text = ""
		self.ids.Lname.helper_text = ""
		self.ids.Uname.helper_text = ""
		self.ids.Rpassword.helper_text = ""
		self.ids.RCpassword.helper_text = ""
		self.ids.Reg_Email.helper_text = ""

		collection = userprofile.find_one({Uname:{}})

		x = 0

		#No Input Error
		if len(Fname) == 0:
			self.ids.Fname.helper_text = "Required"
			x += 1
		if len(Lname) == 0:
			self.ids.Lname.helper_text = "Required"
			x += 1

		if len(Uname) == 0: 
			self.ids.Uname.helper_text = "Required"
			x += 1
		#else:
			#for x in listofuser:
				#if (x == Uname):
				#	self.ids.Uname.helper_text = "Username Already Exists"
				#	x += 1
				#	break

		if len(Rpass) == 0:
			self.ids.Rpassword.helper_text = "Required"
			x += 1
		if len(RCpass) == 0:
			self.ids.RCpassword.helper_text = "Required"
			x += 1

		#Confirm Password Checker Error
		if Rpass != RCpass:
			self.ids.Rpassword.helper_text = "Password do not match"
			self.ids.RCpassword.helper_text = "Password do not match"
			x += 1

		#Email Checker
		if (re.fullmatch(regex, Email)):
			x += 0
		else:
			self.ids.Reg_Email.helper_text = "Invalid Email"
			x += 1

		if x > 0:
			self.manager.current = "Register_Screen"
			
		else:
			user = { Uname : {"Uname": Uname, "Email": Email, "First_Name": Fname, "Last_Name": Lname, "Password": Rpass}}
			userprofile.insert_one(user)

			self.ids.Fname.text = ""
			self.ids.Lname.text = ""
			self.ids.Uname.text = ""
			self.ids.Reg_Email.text = ""
			self.ids.Rpassword.text = ""
			self.ids.RCpassword.text = ""

			self.manager.current = "Currency_Screen"


class CurrencyScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def currency(self, **kwargs):
		self.menu_list = [
			{
				"viewclass": "OneLineListItem",
				"text": "PHP",
				"on_release": lambda x = "PHP" : self.test1()
			},
			{
				"viewclass": "OneLineListItem",
				"text": "USD",
				"on_release": lambda x = "USD" : self.test2()
			}
		]
		self.menu = MDDropdownMenu(
			caller = self.ids.field,
			items = self.menu_list,
			position = "bottom",
			border_margin = dp(0),
		)
		self.menu.open()

class InitialAmount(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

class WelcomeScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

class WelcomeBackScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

class HomeScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

class Home(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)


#MAIN APPLICATION
class YourExpense(MDApp):
	def build(self):
		global sc_manager
		sc_manager = ScreenManager()
		sc_manager.add_widget(LogoScreen(name="Logo_Page"))
		sc_manager.add_widget(LoadingScreen(name="Loading_Screen"))
		sc_manager.add_widget(LoginScreen(name="Login_Screen"))
		sc_manager.add_widget(RegisterScreen(name="Register_Screen"))
		sc_manager.add_widget(CurrencyScreen(name="Currency_Screen"))
		sc_manager.add_widget(InitialAmount(name="InitialAmount_Screen"))
		sc_manager.add_widget(WelcomeScreen(name="Welcome_Screen"))
		sc_manager.add_widget(WelcomeBackScreen(name="WelcomeBack_Screen"))
		sc_manager.add_widget(HomeScreen(name="Home_Screen"))
		sc_manager.add_widget(Home(name="Home"))
		return sc_manager


#MAIN FUNCTION
if __name__ == '__main__':

	#WINDOW SIZE
	Window.size = (360, 640)

	#DataBase
	clusterdata = MongoClient("mongodb+srv://Java-rice:Fs6EMINE5Dm9YaFj@finalproject.p08n5.mongodb.net/?retryWrites=true&w=majority")
	db = clusterdata["Application"]
	userprofile = db["Profiles"]
	userbalance = db["Balance"]

	global User_name, User_password

	#Fonts Styles
	LabelBase.register(name = "LatoB", fn_regular= "assets/txt/Lato-Bold.ttf")
	LabelBase.register(name = "PoppinsB", fn_regular= "assets/txt/Poppins-Bold.ttf")
	LabelBase.register(name = "Montserrat", fn_regular= "assets/txt/MontserratC.ttf")
	LabelBase.register(name = "OpenSansR", fn_regular= "assets/txt/OpenSansR.ttf")

	#RUN THE MAIN APPLICATION
	YourExpense().run()