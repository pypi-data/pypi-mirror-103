from getpass import getuser
from selenium import webdriver
from random import randint
import time, selenium, os

chrome = 'C:\\Users\\' + getuser() + '\\AppData\\Local\\Google\\Chrome'

def init(headless):
	global options
	options = webdriver.ChromeOptions()
	options.add_argument('--log-level=3')
	options.add_argument("--mute-audio")
	if(headless == 'show'):
		pass
	elif(headless == 'hide'):
		options.add_argument("headless")
	else:
		print('Unexpected Error')
	options.add_experimental_option("excludeSwitches", ["enable-automation"])
	options.add_experimental_option('useAutomationExtension', False)

	global driver
	driver = webdriver.Chrome(executable_path=chrome + "\\chromedriver.exe", chrome_options=options)
	os.system("cls")
	driver.get("https://vk.com/login")

def authorization(login, password):
	username = driver.find_element_by_id("email")
	username.send_keys(login)
	sign = driver.find_element_by_id("pass")
	sign.send_keys(password)
	button = driver.find_element_by_id("login_button")
	button.click()

def check():
	while True:
		try:
			driver.find_element_by_xpath('/html/body/div[12]/div/div/div[2]/div[1]/div/nav/ol/li[1]/a/span[1]')
			return True
		except:
			pass
		try:
			driver.find_element_by_xpath('/html/body/div[10]/div/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div')
			return False
		except:
			pass

def loop(album, delay):
	driver.get(album)

	while True:
		try:
			text = driver.find_element_by_xpath('/html/body/div[12]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div/div[2]/div/div[1]/div[2]').text
			i = int(text.split(' а')[0].split('\n')[1])
			break
		except:
			pass

	while True:
		try:
			track = driver.find_element_by_xpath('/html/body/div[12]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div/div[2]/div/div[2]/div[2]/div/div[{}]/div/button'.format(randint(0, i)))
			play = webdriver.common.action_chains.ActionChains(driver)
			play.move_to_element_with_offset(track, 0, 0)
			play.click()
			play.perform()
			time.sleep(delay)
		except:
			pass