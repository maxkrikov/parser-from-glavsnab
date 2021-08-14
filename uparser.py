import requests
from bs4 import BeautifulSoup
import codecs
import sqlite3
from datetime import date
import re



def p():
	global db
	global sql
	db = sqlite3.connect('server.db')
	sql = db.cursor()


p()

sql.execute("""CREATE TABLE IF NOT EXISTS spis (
	nomer INTEGER,
	name TEXT,
	sulka TEXT
	
)""")

db.commit()


		




def start(link):
	global response
	global soup
	global kategr
	response = requests.get(link).text
	soup = BeautifulSoup(response, 'lxml')
	kategr = soup.find('div', class_="catalog_subsection_list")



def purser(link):
	global response
	global soup
	global starn
	global maxstr
	global ip0
	maxstr = 0

	response = requests.get(link).text
	soup = BeautifulSoup(response, 'lxml')
	stra = soup.find('nav', class_="paginator")
	ip0 = soup.find('div', class_="catalog_list")

	if stra == None:
		
		vuvod2()

		abc = int(input("Сохранить? (1/0)\n"))

		if abc == 0:
			print("Введите любой символ, что-бы выйти")
		if abc == 1:

			datetime_now = date.today()

			nazv = soup.find('h1', class_="title_h2").text

			nazv2 = f"{nazv}-{datetime_now}"

			nazv2 = re.sub(r"\s+", "", nazv2, flags=re.UNICODE)
			

			file = codecs.open(f"{nazv2}.txt", 'w', 'utf-8')
		
			for tag in ip0.find_all('div', class_='product-item-container'):
				ider = tag.get('id')

				ip1 = ip0.find('div', id=ider)

				listpo1 = ip1.find('div', class_='catalog_list_item')

				listpo2 = listpo1.find('div', class_='catalog_list_item_title').text

				prices0 = listpo1.find('div', class_="catalog_list_item_prices")

				prices = prices0.find('div', class_='price').text
				
				file.write(f"{listpo2} - {prices}\n")
			

			print("Сохранено успешно")
			file.close()

			aaaa = input("Введите любой символ, что-бы выйти\n")




	else:

		for starn in stra.find_all('li'):
			maxstr = starn.get_text()

		maxstr = int(maxstr)

		vuvod(maxstr)

		abc = int(input("Сохранить? (1/0)\n"))

		if abc == 0:
			print("Введите любой символ, что-бы выйти")
		if abc == 1:
			soxr(maxstr)

		aaaa = input("Введите любой символ, что-бы выйти\n")



			



def purser2(tekstr):
	global response
	global soup
	global ip0

	link = f"https://glavsnab.com{sulkao}?PAGEN_1={tekstr}&SIZEN_1=12"

	response = requests.get(link).text
	soup = BeautifulSoup(response, 'lxml')

	ip0 = soup.find('div', class_="catalog_list")

	


def soxr(maxstr2):
	datetime_now = date.today()

	nazv = soup.find('h1', class_="title_h2").text

	nazv2 = f"{nazv}-{datetime_now}"

	nazv2 = re.sub(r"\s+", "", nazv2, flags=re.UNICODE)
	
	file = codecs.open(f"{nazv2}.txt", 'w', 'utf-8')
	i = 1
	for abc in range(maxstr2):
		purser2(i)
		for tag in ip0.find_all('div', class_='product-item-container'):
			ider = tag.get('id')

			ip1 = ip0.find('div', id=ider)

			listpo1 = ip1.find('div', class_='catalog_list_item')

			listpo2 = listpo1.find('div', class_='catalog_list_item_title').text

			prices0 = listpo1.find('div', class_="catalog_list_item_prices")

			prices = prices0.find('div', class_='price').text
			
			file.write(f"{listpo2} - {prices}\n")
		i = i + 1

	print("Сохранено успешно")
	file.close()



def vuvod(maxstr2):
	print("Список выбранной категории:  \n")
	i = 1
	for abc in range(maxstr2):
		purser2(i)
		for tag in ip0.find_all('div', class_='product-item-container'):
			ider = tag.get('id')

			ip1 = ip0.find('div', id=ider)

			listpo1 = ip1.find('div', class_='catalog_list_item')

			listpo2 = listpo1.find('div', class_='catalog_list_item_title').text

			prices0 = listpo1.find('div', class_="catalog_list_item_prices")

			prices = prices0.find('div', class_='price').text

			print(f"{listpo2} - {prices}")
		i = i + 1




def vuvod2():
	
	print("Список выбранной категории:  \n")
	
	
	for tag in ip0.find_all('div', class_='product-item-container'):
		ider = tag.get('id')

		ip1 = ip0.find('div', id=ider)

		listpo1 = ip1.find('div', class_='catalog_list_item')

		listpo2 = listpo1.find('div', class_='catalog_list_item_title').text

		prices0 = listpo1.find('div', class_="catalog_list_item_prices")

		prices = prices0.find('div', class_='price').text

		print(f"{listpo2} - {prices}")
		












start("https://glavsnab.com/catalog/skobyanye_izdeliya/")
iop = 1
for vkategr in kategr.find_all('div', class_='catalog_subsection'):
	ider = vkategr.get('id')

	spiskatgr = kategr.find('div', id=ider)

	listpo1 = spiskatgr.find('div', class_='catalog_subsection_title').text

	listpo2 = spiskatgr.find('a').get('href')


	sql.execute(f"SELECT nomer FROM spis WHERE name = '{listpo1}'")
	data = sql.fetchone()
	if data is None:
		sql.execute(f"INSERT INTO spis VALUES ({iop}, '{listpo1}', '{listpo2}');")
		db.commit()

	print(f"{iop} - {listpo1}")

	iop = iop + 1


def start3():
	p()
	global aghs
	aghs = int(input("Введите число категории: "))
	sql.execute(f"SELECT nomer FROM spis WHERE nomer = {aghs}")
	data = sql.fetchone()
	if data is None:
		print("Категории с таким номером не найдено")
		start3()
	else:
		for b in sql.execute(f"SELECT sulka FROM spis WHERE nomer = {aghs}"):
			global sulkao
			sulkao = b[0]
	
start3()


linking = f"https://glavsnab.com{sulkao}?PAGEN_1=1&SIZEN_1=12"


purser(linking)