from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


path = "C:/Users/M/Desktop/chromedriver.exe"

driver = webdriver.Chrome(path)
driver.get('http://www.coupang.com/')