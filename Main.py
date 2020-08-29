from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QDialog
import smtplib
import random
from email.mime.multipart import MIMEMultipart     
from email.mime.text import MIMEText           
from email.mime.image import MIMEImage 
import parsing_scripts as p_s
import analys_scripts as a_s
import sqlite3
from waitingspinnerwidget import QtWaitingSpinner
class MainWindow(QtWidgets.QWidget):
	def __init__(self,parent = None):
		QtWidgets.QWidget.__init__(self,parent)
		self.vbox = QtWidgets.QVBoxLayout()
		self.reg_name = QtWidgets.QLineEdit('Введите Имя')
		self.post_auth_label = QtWidgets.QLabel("Вы успешно авторизованы,Вам доступны все функции")
		self.reg_password = QtWidgets.QLineEdit('введите пароль')
		self.reg_code = QtWidgets.QLineEdit('введите код')
		self.reg_mail = QtWidgets.QLineEdit('введите почту')
		self.log_name = QtWidgets.QLineEdit('Введите Имя')
		self.log_password = QtWidgets.QLineEdit('введите пароль')
		self.reg_code_accept_button = QtWidgets.QPushButton('Подтвердить код')
		self.reg_button = QtWidgets.QPushButton('зарегистрироваться')
		self.log_button = QtWidgets.QPushButton('авторизоваться')
		self.test_button = QtWidgets.QPushButton('test')
		self.log_button.clicked.connect(self.log_in)
		self.reg_button.clicked.connect(self.register)
		self.auth_flag = False
		self.work_file = ''
		
		"""блок анализа"""
		self.analys_box = QtWidgets.QGroupBox()
		self.analys_grid = QtWidgets.QGridLayout()
		"""кнопочки"""
		self.backward_button =  QtWidgets.QPushButton('назад к выбору файла')
		self.backward_button.clicked.connect(self.go_back)
		
		
		self.avito_high_low_button  = QtWidgets.QPushButton ("найти самое дешевое и дорогое обьявление")
		self.avito_high_low_button.clicked.connect(lambda: a_s.high_low_ad(self.work_file))
		self.avito_button_1 =  QtWidgets.QPushButton("посчитать кол-во обьявлений")
		self.avito_button_1.clicked.connect(lambda: a_s.count_ads(self.work_file))
		self.avito_button_2 =  QtWidgets.QPushButton("выбрать обявления по введенному ключевому слову")
		self.avito_button_2.clicked.connect(lambda: a_s.search_ads(self.work_file))
		self.avito_button_3 =  QtWidgets.QPushButton("выгрузить все ссылки c адресами")
		self.avito_button_3.clicked.connect(lambda: a_s.get_urls(self.work_file))
		self.avito_buttons = [self.avito_high_low_button,self.avito_button_1,self.avito_button_2,self.avito_button_3]
		
		self.picabu_high_low_button = QtWidgets.QPushButton ("найти самую высоко и низко оцененную статью")
		self.picabu_high_low_button.clicked.connect(lambda: a_s.high_low_art(self.work_file))
		self.picabu_button_1  = QtWidgets.QPushButton ("найти статью по тегам")
		self.picabu_button_1.clicked.connect(lambda: a_s.tags_search(self.work_file))
		self.picabu_button_2  = QtWidgets.QPushButton ("найти статью по автору")
		self.picabu_button_2.clicked.connect(lambda: a_s.author_search(self.work_file))
		self.picabu_button_3  = QtWidgets.QPushButton ("посчитать статьи с тегом моё")
		self.picabu_button_3.clicked.connect(lambda: a_s.count_my(self.work_file))
		self.picabu_button_4  = QtWidgets.QPushButton ("найти партнерские посты")
		self.picabu_button_4.clicked.connect(lambda: a_s.search_partner(self.work_file))
		self.picabu_buttons = [self.picabu_high_low_button,self.picabu_button_1,self.picabu_button_2,self.picabu_button_3,self.picabu_button_4]
		"""кнопочки"""
		
		
		self.file_choose_button = QtWidgets.QPushButton('выбрать файл')
		self.file_choose_button.clicked.connect(self.set_analyse_layout)
		self.analys_grid.addWidget(self.file_choose_button)

		
		self.analys_box.setLayout(self.analys_grid)
		
		"""блок анализа"""
		
		"""список сайтов"""
		self.list = QtWidgets.QComboBox(parent = None)
		self.grid  = QtWidgets.QGridLayout()
		self.site_choice_button = QtWidgets.QPushButton("Спарсить")
		self.list.addItem("АвитоМотоциклыиМототехника")
		self.list.addItem("АвитоАвтомобили")
		self.list.addItem("АвитоТелефоны")
		self.list.addItem("АвитоКвартиры")
		self.list.addItem("АвитоНоутбуки")
		self.list.addItem("АвитоВелосипеды")
		self.list.addItem("АвитоКошки")
		self.list.addItem("АвитоСобаки")
		self.list.addItem("АвитоРастения")
		self.list.addItem("ПикабуГорячее")
		self.list.addItem("ПикабуСвежее")
		self.list.addItem("ПикабуЛучшее")
		
		
		# ~ self.list.addItem("")
		# ~ self.list.addItem("")
		self.list_box = QtWidgets.QGroupBox()
		self.grid.addWidget(self.list,0,0, alignment = QtCore.Qt.AlignTop)
		self.grid.addWidget(self.site_choice_button,1,0,alignment =QtCore.Qt.AlignBottom)
		self.list_box.setLayout(self.grid)
		self.site_choice_button.clicked.connect(self.parse_site)
		"""список сайтов"""
		
	
		"""группировка в тулбар"""
		self.reg_box =  QtWidgets.QGroupBox()
		self.reg_group = QtWidgets.QHBoxLayout()
		
		self.log_box =  QtWidgets.QGroupBox()
		self.log_group = QtWidgets.QHBoxLayout()
		
		self.reg_group.addWidget(self.reg_name)
		self.reg_group.addWidget(self.reg_password)
		self.reg_group.addWidget(self.reg_mail)
		self.reg_group.addWidget(self.reg_button,alignment=QtCore.Qt.AlignBottom)
		
		
		self.log_group.addWidget(self.log_name)
		self.log_group.addWidget(self.log_password)
		self.log_group.addWidget(self.log_button,alignment=QtCore.Qt.AlignBottom)
		
		self.reg_box.setLayout(self.reg_group)
		self.log_box.setLayout(self.log_group)
		
		self.reg_toolbox = QtWidgets.QToolBox()
		self.login_toolbox = QtWidgets.QToolBox()
		
		self.reg_toolbox.addItem(self.reg_box,'Регистрация')
		self.login_toolbox.addItem(self.log_box,'Авторизация')
		
		self.toolbar_group = QtWidgets.QHBoxLayout()
		
		self.toolbar_group.addWidget(self.reg_toolbox)
		self.toolbar_group.addWidget(self.login_toolbox)
		
		self.toolbar_box = QtWidgets.QGroupBox()
		self.toolbar_box.setLayout(self.toolbar_group)
		"""группировка в тулбар"""
		
		
		"""группировка во вкладки"""
		self.tab =  QtWidgets.QTabWidget()
		self.tab.addTab(self.toolbar_box,'Идентификация')
		
		
		
		
		"""группировка во вкладки"""
		self.vbox.addWidget(self.tab)
		

		
	def go_back(self):
		for i in range(self.analys_grid.count()): 
			 self.analys_grid.itemAt(i).widget().hide() 
		self.file_choose_button.show()
	
	def register(self):
		reg_name =  self.reg_name.text()
		reg_password = self.reg_password.text()
		reg_mail = self.reg_mail.text()
		msg = 'Введите код присланный вам на почту'
		code = self.register_code(reg_mail)
		self.reg_group.addWidget(self.reg_code)
		self.reg_group.addWidget(self.reg_code_accept_button,alignment=QtCore.Qt.AlignBottom)
		self.reg_code_accept_button.clicked.connect(lambda: self.check_code(reg_name,reg_password,reg_mail,code))
		self.reg_button.setEnabled(False)
		window = DialogWindow(msg)
		
	def check_code(self,name,password,mail,code):
		name = name
		password = password
		mail = mail
		code = code
		print(code)
		print(self.reg_code.text())
		if self.reg_code.text() != str(code):
			msg = 'Вы ввели неверный код'
			window = DialogWindow(msg)
		else:
			msg = 'Вы успешно зарегистрировались и Можете авторизоваться'
			window = DialogWindow(msg)
			self.add_user(name,password,mail)
			
	def add_user(self,name,password,mail):
		name = name
		password = password
		mail = mail
		self.reg_code_accept_button.setEnabled(False)
		conn = sqlite3.connect('users.sqlite')
		c = conn.cursor()
		c.execute("INSERT INTO USERS(Name,Password,Mail) VALUES ('%s','%s','%s')"%(name,password,mail))
		conn.commit()
		
	def log_in(self):
		name = self.log_name.text()
		password = self.log_password.text()
		all_users = 'SELECT * FROM USERS'
		conn = sqlite3.connect('users.sqlite')
		c = conn.cursor()
		c.execute(all_users)
		all_users = {}
		user = {}
		rows = c.fetchall()
		x = 5
		while(x == 5):
			auth = False
			for row in rows:
				user['имя'] = row[1]
				user['пароль'] = row[2]
				print(user)
				if name == user['имя'] and password == user['пароль']:
					auth = True
				elif name != user['имя'] and password != user['пароль'] and auth == False:
					auth = False
			if auth == True:
				msg = 'Вы Успешно авторизованы'
				window = DialogWindow(msg)
				self.tab.addTab(self.list_box,'список сайтов/парсинг')
				self.tab.addTab(self.analys_box,'анализ данных')
				self.reg_button.setEnabled(False)
				self.log_button.setEnabled(False)
			elif auth == False:
				msg = 'Неверное имя пользователя или пароль'
				window = DialogWindow(msg)
			x = 6
	
	
			
		
	def register_code(self,reg_mail):
		code = random.randint(15678,93789)
		addr_from = 'benjaminhlebnikov@yandex.ru'
		password = 'dragon6587'    
		addr_to = reg_mail
		msg = MIMEMultipart()                              
		msg['From']    = addr_from       
		msg['To']      = addr_to                            
		msg['Subject'] = 'Код подтверждения'
		body = str(code)
		msg.attach(MIMEText(body, 'plain'))  
		server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)  
		server.ehlo()
		server.login(addr_from, password)  
		server.send_message(msg)                 
		server.quit()                                                            
		print(code)
		return code
		
	def parse_site(self):
		site = self.list.currentText()
		if 'Кинопоиск' in site:
			p_s.parse_kinopoisk(site)
		elif 'Авито' in site:
			p_s.parse_avito(site)
		elif 'Пикабу' in site:
			p_s.parse_picabu(site)
			
	def set_analyse_layout(self,key):
		file_dialog = FileChooseDialog()
		self.work_file = file_dialog.file 
		if 'avito' in str(self.work_file):
			self.file_choose_button.hide()
			for button in self.avito_buttons:
				self.analys_grid.addWidget(button)
				self.analys_grid.addWidget(self.backward_button)
				self.backward_button.show()
				button.show()
		elif  'пикабу'  in str(self.work_file):
			self.file_choose_button.hide()
			for button in self.picabu_buttons:
				self.analys_grid.addWidget(button)
				self.analys_grid.addWidget(self.backward_button)
				self.backward_button.show()
				button.show()
			
				
		
class DialogWindow(QtWidgets.QWidget):
	def __init__(self,msg,parent = None):
		QtWidgets.QWidget.__init__(self,parent)
		self.dialog = QtWidgets.QMessageBox.information(None,"Регистрация",msg,buttons=QtWidgets.QMessageBox.Close,defaultButton=QtWidgets.QMessageBox.Close)


class SearchDialog(QtWidgets.QWidget):
	def __init__(self,parent = None):
		self.s,self.ok = QtWidgets.QInputDialog.getText(None,"Поиск","Введите ключевое слово")
		
class FileChooseDialog(QtWidgets.QWidget):
	def __init__(self,parent = None):
		QtWidgets.QWidget.__init__(self,parent)
		self.file = QtWidgets.QFileDialog.getOpenFileName()
		
		
if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	app.setStyleSheet(open("styles.qss","r").read())
	window = MainWindow()
	window.setWindowTitle("ультра парсер")
	window.setLayout(window.vbox)
	window.resize(1200,420)
	window.show()
	sys.exit(app.exec_())



