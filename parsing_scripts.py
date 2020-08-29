import Main
from PyQt5 import QtCore, QtGui, QtWidgets  
from PyQt5.QtWidgets import  QDialog,QVBoxLayout
from PyQt5.QtGui import QColor
import requests
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions 
import time	
from waitingspinnerwidget import QtWaitingSpinner
from bs4 import BeautifulSoup

# ~ class Indicator(QDialog):
	# ~ def __init__(self,parent = None):
		# ~ QDialog.__init__(self,parent)
		# ~ self.setLayout(QVBoxLayout())
		# ~ self.spinner = QtWaitingSpinner(self)
	# ~ def show_indicator(self):
		# ~ self.spinner.start()
		

'''Настройка индикатора'''



	
def parse_picabu(site):
	ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
	site_key = ''
	if site == 'ПикабуГорячее':
		site_key = 'пикабугорячее'
		url = 'https://pikabu.ru/'
		
	elif site == 'ПикабуСвежее':
		site_key = 'пикабусвежее'
		url = 'https://pikabu.ru/new'
		
	elif site == 'ПикабуЛучшее':
		site_key = 'пикабулучшее'
		url = 'https://pikabu.ru/best'
	# ~ spinner = Indicator()
	driver = webdriver.Chrome()
	driver.get(url)
	ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
	i = 1
	while(True):
		time.sleep(1)
		# ~ spinner.show_indicator()
		driver.execute_script("window.scrollTo(0, window.scrollY + 200)")
		results = (driver.find_elements_by_xpath('//article[@class="story"]'))
		print(results)
		for result in results:
			try:
				
				rating = result.find_element_by_xpath('.//div[@class="story__rating-count"]').text
				print(rating)

				title = result.find_element_by_xpath('.//h2[@class="story__title"]').text
				print(title)
			
				if i <= 1:
					art_url = result.find_element_by_xpath('.//a[@class="story__title-link story__title-link_visited"]').get_attribute('href')
					print(art_url)
				else:
					art_url = result.find_element_by_xpath('.//a[@class="story__title-link"]').get_attribute('href')
					print(art_url)
					
				author = result.find_element_by_xpath('.//div[@class="user__info-item"]').text
				print(author)
				
				try:
					tags = result.find_element_by_xpath('.//div[@class="story__tags tags"]').text
				except:
					tags = 'нет тегов'
				print(tags)
			except:
				msg = "Кому нужны партнерские посты?(НИКОМУ)"
				window = Main.DialogWindow(msg)
				rating = 0
		
				title = WebDriverWait(driver, 0.1,ignored_exceptions=ignored_exceptions)\
                        .until(expected_conditions.presence_of_element_located((By.XPATH, './/a[@class="story__title-link"]'))).text
                        
				
				art_url = WebDriverWait(driver, 0.1,ignored_exceptions=ignored_exceptions)\
                        .until(expected_conditions.presence_of_element_located((By.XPATH, './/a[@class="story__title-link"]'))).get_attribute('href')
                        
			

                
				author = 'какой-то партнер'
				tags = 'партнерский'
				
			data = {'rating':rating,'title':title,'url':art_url,'author':author,'tags':tags}
			write_csv_picabu(data,site_key)
			i += 1
			
		time.sleep(5)
		i = 1
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		
		
	
		
	
def parse_kinopoisk(site):
	site_key = ''
	if site == 'КинопоискЛюбовь':
		site_key = 'любовь'
		url = 'https://www.kinopoisk.ru/top/lists/295/filtr/all/sort/order/page/1/'
		base_url = 'https://www.kinopoisk.ru/top/lists/295/filtr/all/sort/order/'
	elif site == "КинопоискВампиры":
		site_key = 'вампиры'
		url  = 'https://www.kinopoisk.ru/top/lists/294/filtr/all/sort/order/page/1/' 
		base_url = 'https://www.kinopoisk.ru/top/lists/294/filtr/all/sort/order/'
	elif site == "КинопоискЗомби":
		site_key = 'зомби'
		url = 'https://www.kinopoisk.ru/top/lists/296/filtr/all/sort/order/page/1/'
		base_url = 'https://www.kinopoisk.ru/top/lists/296/filtr/all/sort/order/'
	elif site == "КинопоискКосмос":
		site_key = 'космос'
		url = 'https://www.kinopoisk.ru/top/lists/297/filtr/all/sort/order/page/1/'
		base_url = 'https://www.kinopoisk.ru/top/lists/297/filtr/all/sort/order/'

		'''скрипт'''
	html = get_html_kinopoisk(url)
	total_pages = get_total_pages_kinopoisk(html)
	print(total_pages)
	for i in range(1,total_pages):
		url_gen = base_url + 'page/'+str(i)+'/' 
		print(url_gen)
		html = get_html_kinopoisk(url_gen)
		get_page_data_kinopoisk(html,site_key)
		time.sleep(15)
	'''скрипт'''
	
	

def parse_avito(site):
	page_part = 'p='
	site_key = ''
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
	if site == "АвитоМотоциклыиМототехника":
		site_key = 'мото'
		url = 'https://www.avito.ru/omsk/mototsikly_i_mototehnika?p=1'
		base_url = 'https://www.avito.ru/omsk/mototsikly_i_mototehnika?'
	elif site == "АвитоАвтомобили":
		site_key = 'Автомобили'
		url = 'https://www.avito.ru/omsk/avtomobili?p=1'
		base_url = 'https://www.avito.ru/omsk/avtomobili?'
		
	elif site == "АвитоТелефоны":
		url = 'https://www.avito.ru/omsk/telefony?p=1'
		base_url = 'https://www.avito.ru/omsk/telefony?'
		site_key = 'Телефоны'
	elif site == "АвитоКвартиры":
		site_key = 'Квартиры'
		url = 'https://www.avito.ru/omsk/kvartiry?p=1'
		base_url = 'https://www.avito.ru/omsk/kvartiry?'
	elif site == "АвитоНоутбуки":
		site_key = 'Ноутбуки'
		url = 'https://www.avito.ru/omsk/noutbuki?p=1'
		base_url = 'https://www.avito.ru/omsk/noutbuki?'
	elif site == "АвитоВелосипеды":
		site_key = 'Велосипеды'
		url = 'https://www.avito.ru/omsk/velosipedy?p=1'
		base_url = 'https://www.avito.ru/omsk/velosipedy?'
	elif site == "АвитоКошки":
		site_key = 'Кошки'
		url = 'https://www.avito.ru/omsk/koshki?p=1'
		base_url = 'https://www.avito.ru/omsk/koshki?'
	elif site == "АвитоСобаки":
		site_key = 'Собаки'
		url = 'https://www.avito.ru/omsk/sobaki?p=1'
		base_url = 'https://www.avito.ru/omsk/sobaki?'
	elif site == "АвитоРастения":
		site_key = 'Растения'
		url = 'https://www.avito.ru/omsk/rasteniya?p=1'
		base_url = 'https://www.avito.ru/omsk/rasteniya?'
		
	'''скрипт'''
	html = get_html_avito(url)
	total_pages = get_total_pages(html)
	print(total_pages)
	for i in range(1,total_pages):
		url_gen = base_url + page_part + str(i)
		print(url_gen)
		html = get_html_avito(url_gen)
		get_page_data_avito(html,site_key)
	'''скрипт'''
	
def get_page_data_avito(html,key):
	key = key
	soup = BeautifulSoup(html,'lxml')
	try:
		ads = soup.find('div',class_='js-catalog_serp').find_all('div',class_='snippet-horizontal item item_table clearfix js-catalog-item-enum item-with-contact js-item-extended')
		for ad in ads:
			try:
				title = ad.find('div',class_='item__line').find('div',class_='item_table-wrapper').find('h3').text
			except:
				title = ''
			try:
				url = 'https://www.avito.ru' + ad.find('div',class_='description item_table-description').find('h3').find('a').get('href')
			except:
				url = ''
			try:
				price = ad.find('div',class_='about').text
			except:
				price = ''
			try:
				adress = ad.find('div',class_='description item_table-description').find('div',class_='data').find('div',class_='item-address').text
			except:
				adress = ''
			data = {'title':title,'price':price,'adress':adress,'url':url}
			write_csv_avito(data,key)		
	except:
		msg = "Авито не дают спарсить данную страницу(А может и мой косяк)"
		window = Main.DialogWindow(msg)
	
	
def get_page_data_kinopoisk(html,key):
	key = key
	soup = BeautifulSoup(html,'lxml')
	try:
		films = soup.find('tr').find('div',class_='block_left_pad').find('table',class_='ten_items js-rum-hero').find_all('tr')
		for film in films:
			try:
				title = film.find('td',class_='news').find('a').text
			except:
				title = ''
			try:
				description = film.find('td',class_='news').find('span',class_='gray_text').text
			except:
				description = ''
			try:
				rating = film.find('td').find('div',class_='ratingBlock').find('span',class_='all').text
			except:
				rating = ''
			data = {'title':title,'description':description,'rating':rating}
			write_csv_kinopoisk(data,key)
	except:
		msg = "Кинопоиск видит во мне злого бота(А может и мой косяк)"
		window = Main.DialogWindow(msg)

		
def write_csv_avito(data,key):
	key = key
	with open('avito'+key+'.csv','a',encoding='utf8') as f:
		writer = csv.writer(f)
		writer.writerow((data['title'],data['price'],data['adress'],data['url']))	
def write_csv_kinopoisk(data,key):
	key = key
	with open('Кинопоиск'+key+'.csv','a',encoding='utf8') as f:
		writer = csv.writer(f)
		writer.writerow((data['title'],data['description'],data['rating']))
		
def write_csv_picabu(data,key):
	key = key
	with open(key+'.csv','a',encoding='utf8') as f:
		
		writer = csv.writer(f)
		writer.writerow((data['rating'],data['title'],data['url'],data['author'],data['tags']))
			
def get_html_avito(url):
	try:
		headers = {
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
		}
		r = requests.get(url)
		print(r)
		return r.text
	except:
		msg = "Авито видит во мне злого бота(А может и мой косяк)"
		window = Main.DialogWindow(msg)
	
def get_html_kinopoisk(url):
	headers = {
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
		}
	r = requests.get(url,headers)
	print(r)
	return r.text
	
def get_total_pages(html):
	soup = BeautifulSoup(html,'lxml')
	pages = soup.find('div',class_="pagination-pages").find_all('a',class_='pagination-page')[-1].get('href')
	total_pages = pages.split('=')[1].split('&')[0]
	print(total_pages)
	return(int(total_pages))
	
def get_total_pages_kinopoisk(html):
	soup = BeautifulSoup(html,'lxml')
	pages = soup.find('div',class_='block_left_pad').find('div',class_='navigator').find('div',class_='pagesFromTo').text
	print(pages) 
	total_pages = pages.split('из')[1]
	print(total_pages)
	return int(total_pages)
	

