#Required Libraries
#Required Libraries
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
from kivy.clock import Clock
import pymongo
from pymongo import MongoClient

Builder.load_file('layout.kv')

#Screens
#Screens
class LogoScreen(Screen):
	#Start Screen
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def on_enter(self, *args):
		Clock.schedule_once(self.next_page, 1)
	
	def next_page(self, *args):
		self.manager.current = "Loading_Screen"

class LoadingScreen(Screen):
	#Loading Screen
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def on_enter(self, *args):
		Clock.schedule_once(self.login, 1)

	def login(self, *args):
		self.manager.current = "Login_Screen"

class LoginScreen(Screen):
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.username = MDTextField(
			hint_text = "Username/Email",
			font_name = "OpenSansR",
			font_size = "11dp",
			size_hint_x = .75,
			width = 200,
			pos_hint = {"center_x": .5, "center_y": .55},
			helper_text =  "Enter your Username",
			required = True,
			mode = "rectangle",
			)

		self.password = MDTextField(
			hint_text = "Password",
			font_name = "OpenSansR",
			font_size = "11dp",
			size_hint = (.75, .1),
			height = "2dp",
			width = 50,
			pos_hint = {"center_x": .5, "center_y": .40},
			helper_text =  "Enter your Username",
			required = True,
			mode = "rectangle",
			)

		self.add_widget(self.username)
		self.add_widget(self.password)

	def on_enter(self, *args):
		Clock.schedule_once(self.create, 2)

	def create(self, *args):
		self.manager.current = "Register_Screen"
	

class RegisterScreen(Screen):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.firstname = MDTextField(
			hint_text = "First Name",
			font_name = "OpenSansR",
			font_size = "11dp",
			size_hint = (.75, .1),
			height = "2dp",
			width = 50,
			pos_hint = {"center_x": .5, "center_y": .68},
			helper_text = "Enter your First Name",
			required = True,
			mode = "rectangle",
			)

		self.lastname = MDTextField(
			hint_text = "Last Name",
			font_name = "OpenSansR",
			font_size = "11dp",
			size_hint = (.75, .1),
			height = "2dp",
			width = 50,
			pos_hint = {"center_x": .5, "center_y": .60},
			helper_text = "Enter your Last Name",
			required = True,
			mode = "rectangle",
			)

		self.username = MDTextField(
			hint_text = "Username",
			font_name = "OpenSansR",
			font_size = "11dp",
			size_hint = (.75, .1),
			height = "2dp",
			width = 50,
			pos_hint = {"center_x": .5, "center_y": .52},
			helper_text = "Enter your Username",
			required = True,
			mode = "rectangle",
			)

		self.email = MDTextField(
			hint_text = "Email",
			font_name = "OpenSansR",
			font_size = "11dp",
			size_hint = (.75, .1),
			height = "2dp",
			width = 50,
			pos_hint = {"center_x": .5, "center_y": .44},
			helper_text = "Enter your Email",
			required = True,
			mode = "rectangle",
			)

		self.password = MDTextField(
			hint_text = "Password",
			font_name = "OpenSansR",
			font_size = "11dp",
			size_hint = (.75, .1),
			height = "2dp",
			width = 50,
			pos_hint = {"center_x": .5, "center_y": .36},
			helper_text = "Enter your Password",
			required = True,
			mode = "rectangle",
			)
		
		self.confirmpassword = MDTextField(
			hint_text = "Confirm Password",
			font_name = "OpenSansR",
			font_size = "11dp",
			size_hint = (.75, .1),
			height = "2dp",
			width = 50,
			pos_hint = {"center_x": .5, "center_y": .28},
			helper_text = "Enter your Password",
			required = True,
			mode = "rectangle",
			)


		self.add_widget(self.firstname)
		self.add_widget(self.lastname)
		self.add_widget(self.username)
		self.add_widget(self.email)
		self.add_widget(self.password)
		self.add_widget(self.confirmpassword)

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