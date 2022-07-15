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
from kivy.clock import Clock
#layout Libraries

##database libraries
import pymongo
from pymongo import MongoClient
##database libraries

##google and facebook acc api
from kivyauth.google_auth import initialize_google, login_google, logout_google
#235651464495-v9qn51gb53394mig64avc51ijaf1q439.apps.googleusercontent.com
#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
##google and facebook acc api

Builder.load_file('layout.kv')


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

class RegisterScreen(Screen):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

class CurrencyScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

class InitialAmount(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

class WelcomeScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

class WekcomeBackScreen(Screen):
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
		sc_manager.add_widget(CurrencyScreen(name="InitialAmount_Screen"))
		sc_manager.add_widget(CurrencyScreen(name="Welcome_Screen"))
		sc_manager.add_widget(CurrencyScreen(name="WelcomeBack_Screen"))
		return sc_manager

	def show_password(self, checkbox, value):
		pass



#MAIN FUNCTION
if __name__ == '__main__':

	#WINDOW SIZE
	Window.size = (360, 640)

	#DataBase
	clusterdata = MongoClient("mongodb+srv://Java-rice:Fs6EMINE5Dm9YaFj@finalproject.p08n5.mongodb.net/?retryWrites=true&w=majority")
	db = clusterdata["Application"]
	collection = db["Profiles"]

	#Fonts Styles
	LabelBase.register(name = "LatoB", fn_regular= "assets/txt/Lato-Bold.ttf")
	LabelBase.register(name = "PoppinsB", fn_regular= "assets/txt/Poppins-Bold.ttf")
	LabelBase.register(name = "Montserrat", fn_regular= "assets/txt/MontserratC.ttf")
	LabelBase.register(name = "OpenSansR", fn_regular= "assets/txt/OpenSansR.ttf")

	#RUN THE MAIN APPLICATION
	YourExpense().run()