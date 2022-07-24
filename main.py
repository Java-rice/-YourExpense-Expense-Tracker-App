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
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.datatables import MDDataTable
from kivy.uix.boxlayout import BoxLayout
from datetime import datetime
from babel import numbers
import uuid 
import re
#layout Libraries

#graph
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import numpy as np
import matplotlib.pyplot as plt

##database libraries
import pymongo
from pymongo import MongoClient
##database libraries

##validation api
from kivyauth.google_auth import initialize_google, login_google, logout_google


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

#Login Screen
class LoginScreen(Screen):
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		#Current User Variable
		global CurrentUser
		CurrentUser = {}

		#Initialize what we see on screen
		self.ids.Lusername.text = ""
		self.ids.Lpassword.text = ""
		client_id = open("client_id.txt")
		client_secret = open("client_secret.txt")
		initialize_google(self.after_login, self.error_listener, client_id.read(), client_secret.read())

		#Google Login
	def after_login(self, name, email, photo_uri):
		print(name)
		print(email)
		self.manager.transition.direction = "left"
		logout_google()


	def error_listener(self):
		print("Login Failed!")

	def google_log(self):
		login_google()

	def logout(self):
		logout_google()

	def after_logout(self):
		self.root.current = "WelcomeBack_Screen"


	#To make password visible
	def show_password(self, checkbox, value):
		if value:
			self.ids.Lpassword.password = False
		else:
			self.ids.Lpassword.password = True

	#Verify login including input formats
	def loginverification(self, Luname, Lpass):

		self.ids.Lusername.helper_text = ""
		self.ids.Lpassword.helper_text = ""

		l = 0
		n = 0
		i = 0

		#username and email doesnt exist
		if len(Luname) == 0:
			self.ids.Lusername.helper_text = "Required"
			l += 1
		else:
			if (re.fullmatch(regex, Luname)):
				data = userprofile.find({"Email": Luname})
				if userprofile.find_one({"Email": Luname}) is None:
					self.ids.Lusername.helper_text = "Email doesn't exist"
					l += 1
				else:
					l += 0
					n += 1

			else:
				if userprofile.find_one({"Uname": Luname}) is None:
					self.ids.Lusername.helper_text = "Username doesn't exist"
					l += 1	
				else:
					data = userprofile.find({"Uname": Luname})
					n += 1
					l += 0


		if len(Lpass) == 0:
			self.ids.Lpassword.helper_text = "Required"	
			l += 1
		elif n > 0:
			for x in data:
				if x["Password"] == Lpass:
					l += 0
				else:
					self.ids.Lpassword.helper_text = "Incorrect Password"
					l += 1

		if l > 0:
			self.manager.current = "Login_Screen"
			
		else:
			self.ids.Lusername.text = ""
			self.ids.Lpassword.text = ""


			global CurrentUser

			if (re.fullmatch(regex, Luname)):
				for x in userprofile.find({"Email": Luname}):
					CurrentUser = x
			else:
				for x in userprofile.find({"Uname": Luname}):
					CurrentUser = x

			self.manager.get_screen("Welcome_Screen").ids.namecurrent.text = CurrentUser["First_Name"]
			self.manager.get_screen("Home_Screen").ids.Myname.text = CurrentUser["Uname"]

			self.manager.get_screen("Home_Screen").update(CurrentUser)

class RegisterScreen(Screen):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.ids.Fname.text = ""
		self.ids.Lname.text = ""
		self.ids.Uname.text = ""
		self.ids.Reg_Email.text = ""
		self.ids.Rpassword.text = ""
		self.ids.RCpassword.text = ""

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

		x = 0
		p = 0

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
		elif userprofile.find_one({"Uname": Uname}):
			self.ids.Uname.helper_text = "Account already Exists"
			x += 1
		else:
			x += 0

		if len(Rpass) == 0:
			self.ids.Rpassword.helper_text = "Required"
			x += 1
		elif len(Rpass)	< 6:
			self.ids.Rpassword.helper_text = "Min Password Length : 6"
			x += 1
		else:
			p += 1

		if len(RCpass) == 0:
			self.ids.RCpassword.helper_text = "Required"
			x += 1

		#Confirm Password Checker Error
		if (p < 1) & (Rpass != RCpass):
			self.ids.Rpassword.helper_text = "Password do not match"
			self.ids.RCpassword.helper_text = "Password do not match"
			x += 1

		#Email Checker
		if (re.fullmatch(regex, Email)):
			if userprofile.find_one({"Email": Email}):
				self.ids.Reg_Email.helper_text = "Account already Exists"
				x += 1
			else:
				x += 0
		else:
			self.ids.Reg_Email.helper_text = "Invalid Email"
			x += 1

		if x > 0:
			self.manager.current = "Register_Screen"
			
		else:
			global user

			user = { 
			"_id": uuid.uuid4().hex,
			"Uname": Uname, 
			"Email": Email, 
			"First_Name": Fname, 
			"Last_Name": Lname, 
			"Password": Rpass
			}

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
		self.menu_list = [{
				"viewclass": "OneLineListItem",
				"text": "PHP",
				"height": dp(56),
				"on_release": 
					lambda x = "PHP" : self.PHP()
			},{
				"viewclass": "OneLineListItem",
				"text": "USD",
				"height": dp(56),
				"on_release": 
					lambda x = "USD" : self.USD()
			},{
				"viewclass": "OneLineListItem",
				"text": "EURO",
				"height": dp(56),
				"on_release": 
					lambda x = "USD" : self.EURO()
			}
		]
		self.menu = MDDropdownMenu(
			caller = self.ids.field,
			items = self.menu_list,
			position =  "center",
			width_mult = 4,
		)


	def PHP(self):
		self.menu.dismiss()
		self.ids.field.text = "PHP"
		

	def USD(self):
		self.menu.dismiss()
		self.ids.field.text = "USD"
		

	def EURO(self):
		self.menu.dismiss()
		self.ids.field.text = "EURO"

	def confirmcurrency(self, currency):
		user["Currency"] = currency

		self.manager.transition.direction = "left"
		self.manager.current = "InitialAmount_Screen"

class InitialAmount(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def amountchecking(self, amount):

		if amount.isnumeric(): 
			user["Money"] = amount
			today = datetime.now()
			userprofile.insert_one(user)
			#main user and balance flow
			userbalance.insert_one({"_id": user["_id"],"Uname": user["Uname"], "Email": user["Email"], "BalanceFlow": [user["Money"]]} )
			#string history with current date
			userhistory.insert_one({"_id": user["_id"],"Uname": user["Uname"], "Email": user["Email"], "History": [["You Have Created Your Account", today.strftime("%B %d, %Y" )]]})
			#list for add money and subtracted money
			userstat.insert_one({"_id": user["_id"],"Uname": user["Uname"], "Email": user["Email"], "Add_Money" : [user["Money"]], "Subtracted_Money" : []})
			#list for total expenses in categories
			usercat.insert_one({"_id": user["_id"],"Uname": user["Uname"], "Email": user["Email"]})
			#Current table for Add Categories
			usermain.insert_one({"_id": user["_id"],"Uname": user["Uname"], "Email": user["Email"], "Categories":{}})
			#usercommunityinformation
			usercommunity.insert_one({"_id": user["_id"],"Uname": user["Uname"], "Email": user["Email"], "AboutMe" : None, "Age" : None, "Sex": None, "Occupation": None, "Birthday": None, "Posts" : []})

			self.manager.current = "ThankYou_Screen"

		else:
			if len(amount) == 0:
				self.ids.Iamount.helper_text = "Required"
				self.manager.current = "InitialAmount_Screen"
			else:
				self.ids.Iamount.helper_text = "Must be a number"
				self.manager.current = "InitialAmount_Screen"


class WelcomeScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

class ThankYouScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)


class HomeScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def update(self, data):
		if data["Currency"] == "PHP":
			self.manager.get_screen("Home_Screen").ids.balance.text = numbers.format_currency(data["Money"], 'PHP ', locale='en_US')
		elif data["Currency"] == "USD":
			self.manager.get_screen("Home_Screen").ids.balance.text = numbers.format_currency(data["Money"], 'USD ', locale='en')
		else:
			self.manager.get_screen("Home_Screen").ids.balance.text = numbers.format_currency(data["Money"], 'EUR ', locale='en')

		self.allocation_table = MDDataTable(
			padding="15dp",
			size_hint = (0.95, .65),
			pos_hint =  {'center_x': .5, 'center_y': .35},

			column_data = [
				("[size=12]Categories[/size]", dp(20)),
                ("[size=12]Budget[/size]", dp(20)),
                ("[size=12]Expenses[/size]", dp(20)),
                ("[size=12]Remaining[/size]", dp(20))
			],row_data=[])

		y = usermain.find_one({"Uname": self.ids.Myname.text })

		for i in y["Categories"]:
			self.allocation_table.add_row([ y["Categories"][i] , "", ""])

		
		#Update the portfolio email and username
		pfolio = userprofile.find_one({"Uname": self.ids.Myname.text })
		self.ids.portfolio_name.text = pfolio["First_Name"] + " " + pfolio["Last_Name"]
		self.ids.portfolio_email.text = pfolio["Email"]	

		self.manager.get_screen("Home_Screen").ids.allocationfloat.add_widget(self.allocation_table)
		self.ids.About.set_state("close")
		self.manager.current = "Welcome_Screen"
	
	def modifybalance(self, *args):

		x = userprofile.find_one({"Uname": self.ids.Myname.text })

		global userdata
		userdata = x

		self.bal = MDTextField(
			hint_text= "Enter Amount",
			font_name= "OpenSansR",
			font_size= "12dp",
			size_hint_x= None,
			line_color_normal= (0, 0, 0, 1),
			width = 200,
			helper_text_mode= "persistent",
			pos_hint= {"center_x": .5, "center_y": .225},
			helper_text=  "",
			)
		self.mbalance = MDDialog(
			title = "Edit Balance",
			buttons = [
				MDFlatButton(text="ADD", padding = [10, 0],theme_text_color="Custom", on_release = self.Add),
            	MDFlatButton(text="SUBTRACT", theme_text_color="Custom", on_release = self.Subtract),
            	MDFlatButton(text="DISCARD", theme_text_color="Custom", on_release = self.Discard)]
            )
		self.mbalance.add_widget(self.bal)
		self.mbalance.open()

	def addcategories(self, *args):
		self.Box = FloatLayout(
			pos_hint= {"center_x": .5, "center_y": .5})
		self.CategoryField = MDTextField(
			hint_text= "Enter Category",
			font_name= "OpenSansR",
			font_size= "10dp",
			size_hint_x= None,
			line_color_normal= (0, 0, 0, 1),
			width = 150,
			helper_text_mode= "persistent",
			pos_hint= {"center_x": .3, "center_y": .58},
			helper_text=  "Note: Category musn't exists",
			)

		self.BudgetField = MDTextField(
			hint_text= "Add Budget",
			font_name= "OpenSansR",
			font_size= "10dp",
			size_hint_x= None,
			line_color_normal= (0, 0, 0, 1),
			width = 120,
			helper_text_mode= "persistent",
			pos_hint= {"center_x": .3, "center_y": .2},
			helper_text=  "",
			)

		self.Box.add_widget(self.CategoryField)
		self.Box.add_widget(self.BudgetField)

		self.AddCategories = MDDialog(
			title = "Add Categories",
			buttons = [
				MDFlatButton(text="ADD", padding = [10, 0],theme_text_color="Custom", on_release = self.AddC),
            	MDFlatButton(text="CANCEL", theme_text_color="Custom", on_release = self.Cancel)]
            )
		self.AddCategories.add_widget(self.Box)
		self.AddCategories.open()

	def Add(self, obj):
		#Store the money you added
		userstat.update_one({"Uname": self.ids.Myname.text }, { "$push" : {"Add_Money": self.bal.text }})
		#Store changes in balance for balance flow
		userbalance.update_one({"Uname": self.ids.Myname.text }, {"$push": {"BalanceFlow" : (int(userdata["Money"]) + int(self.bal.text))}})

		#store the new money to userdata balance money and change the label
		self.stock = int(userdata["Money"]) + int(self.bal.text)
		userdata["Money"] = self.stock
		userprofile.update_one({"Uname": userdata["Uname"]}, {"$set" :{"Money": userdata["Money"]}})
		self.displaynewbalance()
		self.mbalance.dismiss()

	def Subtract(self, obj):
		#store the new money to userdata balance money and change the label
		self.stock = int(userdata["Money"]) - int(self.bal.text)
		userdata["Money"] = self.stock
		userprofile.update_one({"Uname": userdata["Uname"]}, {"$push" :{"Data": {"Subtracted_Money": userdata["Money"]}}})
		self.displaynewbalance()
		self.mbalance.dismiss()

	def Discard(self, obj):
		self.mbalance.dismiss()

	def displaynewbalance(self):
		if userdata["Currency"] == "PHP":
			print(userdata["First_Name"])
			self.ids.balance.text = numbers.format_currency(userdata["Money"], 'PHP ', locale='en_US')
		elif userdata["Currency"] == "USD":
			self.ids.balance.text = numbers.format_currency(userdata["Money"], 'EUR ', locale='en')
		else:
			self.ids.balance.text = numbers.format_currency(userdata["Money"], 'USD ', locale='en')

	def AddC(self, obj):

		y = usermain.find_one({"Uname": self.ids.Myname.text })
		dictcat = y["Categories"]

		z = 0
		stk = 0

		if len(self.CategoryField.text) == 0:
			self.BudgetField.helper_text = "Required"
			z += 1
		if len(self.BudgetField.text) == 0:
			self.BudgetField.helper_text = "Required"
			z += 1
		if self.BudgetField.text.isnumeric() == False:
			self.BudgetField.helper_text = "Must Be a Number"
			z += 1

		for stk in dictcat.keys():
			if stk == self.CategoryField.text:
				z += 1	

		if z < 1:
			if usercat.find_one({"Uname": self.ids.Myname.text, self.CategoryField.text : []}) is None:
				usercat.insert_one({self.CategoryField.text : []})

			y["Categories"][self.CategoryField.text] = self.BudgetField.text
			usermain.update_one({"Uname": self.ids.Myname.text }, { "$set" : y})
			self.AddCategories.dismiss()


		self.allocation_table.add_row((self.CategoryField.text, self.BudgetField.text , 0, self.BudgetField.text))

	def Cancel(self, obj):
		self.AddCategories.dismiss()

	def updatePortfolio(self):
		z = userstat.find_one({"Email": self.ids.portfolio_email.text})
		i = 0 
		j = 0
		k = 0
		for i in z["Add_Money"]:
			j += int(i)
		for h in z["Subtracted_Money"]:
			k += int(h)
		
		x = np.array(["Expenses", "Income"])
		y = np.array([k,j])

		plt.barh(x,y)
		plt.ylabel("Expenses vs. Income")
		plt.xlabel("Total")

		cont = self.ids.Boxinvsout
		cont.add_widget(FigureCanvasKivyAgg(plt.gcf()))


class AddTransaction(Screen):
	pass


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
		sc_manager.add_widget(ThankYouScreen(name="ThankYou_Screen"))
		sc_manager.add_widget(HomeScreen(name="Home_Screen"))
		sc_manager.add_widget(AddTransaction(name="AddTransaction_Screen"))
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
	userhistory = db["History"]
	usermain = db["Transactions"]
	usercommunity = db["Community"]
	communityinteractions = db["Posts"]
	userstat = db["Statistics"]
	usercat = db["CategoryExpenses"]

	global user
	global username

	#Fonts Styles
	LabelBase.register(name = "LatoB", fn_regular= "assets/txt/Lato-Bold.ttf")
	LabelBase.register(name = "PoppinsB", fn_regular= "assets/txt/Poppins-Bold.ttf")
	LabelBase.register(name = "Montserrat", fn_regular= "assets/txt/MontserratC.ttf")
	LabelBase.register(name = "OpenSansR", fn_regular= "assets/txt/OpenSansR.ttf")

	#RUN THE MAIN APPLICATION
	YourExpense().run()