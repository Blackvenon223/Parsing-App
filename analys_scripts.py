import Main
from PyQt5 import QtCore, QtGui, QtWidgets  
from PyQt5.QtWidgets import  QDialog,QVBoxLayout
from PyQt5.QtGui import QColor
import csv



def high_low_art(filename):
	low_rating = 999999999
	high_rating = 0
	low_url = ''
	high_url = ''
	filename = filename[0].split('/')[5]
	with open(filename,'r',encoding='utf8') as f:
		reader = csv.reader(f)
		for row in reader:
			if row != []:
				if row[0] != '':
					rating =  int(row[0])
					print(rating)
					url = row[2]
					if rating <  low_rating:
						low_rating = rating
						low_url = url
					elif rating >  high_rating:
						high_rating = rating
						high_url = url
		msg = "Cамое низкая оценка составляет " + str(low_rating) + " ссылка на нее " + str(low_url) + "Самая  высокая оценка составляет  "  + str(high_rating) + " ссылка на нее " + str(high_url)
		window = Main.DialogWindow(msg)		
		
		
		
def count_my(filename):
	arts = 0
	filename = filename[0].split('/')[5]
	with open(filename,'r',encoding='utf8') as f:
		reader = csv.reader(f)
		for row in reader:
			if row != []:	
				if 'моё' in row[4]:
					arts += 1
		msg = "Всего " +str(arts)+ " Статей с тегом моё"
		window = Main.DialogWindow(msg)		
		
def search_partner(filename):
	filename = filename[0].split('/')[5]
	with open(filename,'r',encoding='utf8') as f:
		reader = csv.reader(f)
		for row in reader:
			if row != []:	
				if 'партнерский' in row[4]:
					url = row[2].split('\n')
					title = row[1].split('\n')
					partner_csv_write(title,url)
							
		
		
		
					
def tags_search(filename):
	search_window = Main.SearchDialog()
	if search_window.ok:
		tag = search_window.s
	filename = filename[0].split('/')[5]
	with open(filename,'r',encoding='utf8') as f:
		reader = csv.reader(f)
		for row in reader:
			if row != []:	
				url = row[2].split('\n')
				if tag in row[4]:
					print(type(url))
					search_csv_write(url,tag)
					
def author_search(filename):
	search_window = Main.SearchDialog()
	if search_window.ok:
		author = search_window.s
	filename = filename[0].split('/')[5]
	with open(filename,'r',encoding='utf8') as f:
		reader = csv.reader(f)
		for row in reader:
			if row != []:	
				url = row[2].split('\n')
				if author in row[3]:
					print(type(url))
					search_csv_write(url,author)
				
				
def count_ads(filename):
	print (filename)
	filename = filename[0].split('/')[5]
	print (filename)
	with open(filename,'r',encoding='utf8') as f:
		ads = []
		reader = csv.reader(f)
		for row in reader:
			if row != []:
				ads.append(row)
		ads = len(ads)
		print(ads)
		msg = "Всего " + str(ads) + " Обьявлений!"
		window = Main.DialogWindow(msg)		
		
				
def high_low_ad(filename):
	filename = filename[0].split('/')[5]
	with open(filename,'r',encoding='utf8') as f:
		ads = []
		reader = csv.reader(f)
		low = 99999999
		high = 0
		low_url = ''
		high_url = ''
		for row in reader:
			if row != []:
				print(row[1])
				try:
					if  'Цена не' in row[1]:
						print("without price")
					elif 'Бесплатно' in row[1]:
						print("free")
					elif 'Договорная'  in row[1]:
						print("dogovor")
					else:
						pre_num = row[1].split('\n')[2].split('  ')[0].split(' ')
						print(pre_num)
						first_num = pre_num[1]
						second_num = pre_num[2]
						num = int((first_num) + (second_num))
						print(num)
						print(type(num))
				except: 
					num = row[1].split('\n')[2].split('  ')[0].split(' ')
					num = int(num[1])
					print(num)
					print(type(num))
				if num < low:
					low = num
					low_url = row[3]
				elif num > high:
					high = num
					high_url = row[3]
		msg = "Cамое дешевое обьявление стоит " + str(low) + " ссылка на него " + str(low_url) + "Самое дорогое стоит "  + str(high) + " ссылка на него " + str(high_url)
		window = Main.DialogWindow(msg)	
				
def search_ads(filename):
	keyword = ''
	flen = 0
	words = []
	search_window = Main.SearchDialog()
	if search_window.ok:
		keyword = search_window.s
		print(keyword)
		print(type(keyword))
		l = len(keyword) + 1
		keyword_half_1 = [keyword[0:l//2]]
		keyword_half_2 = [keyword[l//2:]]
	filename = filename[0].split('/')[5]
	with open(filename,'r',encoding='utf8') as f:
		ads = []
		reader = csv.reader(f)
		for row in reader:
			if row != []:
				url = row[3].split('\n')
				print(url)
				row = row[0].split('\n')[1].split(',')
				print(row)
				if len(row) == 1:
					row = row[0]
					if keyword in row.lower():
						search_csv_write(url,keyword)
				else:
					i = 0
					length = len(row)
					for i in range(i,length):
						print(length)
						print(i)
						print(row[i])
						word = row[i]
						words.append(word.lower())
						i +=1 
					if keyword in  words:
						search_csv_write(url,keyword)
				print(row)
	# ~ print()
	
	
def get_urls(filename):
	filename = filename[0].split('/')[5]
	with open(filename,'r',encoding='utf8') as f:
		ads = []
		reader = csv.reader(f)
		for row in reader:
			if row != []:
				adress = row[2].split('\n')[1]
				url = row[3].split('\n')[0]
				print(url)
				print(adress)
				urls_adress_csv_write(adress,url)
				
def urls_adress_csv_write(adress,url):
	with open('Выгрузка ссылок с адресами.csv','a',encoding='utf8') as f:
		writer = csv.writer(f)
		writer.writerow((adress,url))

	

def search_csv_write(url,keyword):
	with open('Поиск по '+keyword+'.csv','a',encoding='utf8') as f:
		writer = csv.writer(f)
		writer.writerow(url)	
		
def partner_csv_write(title,url):
	with open('выгрузкапартнескихпостов.csv','a',encoding='utf8') as f:
		writer = csv.writer(f)
		writer.writerow((title,url))	
			
			
