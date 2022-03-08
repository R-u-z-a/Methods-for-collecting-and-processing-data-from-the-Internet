# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172#

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient

chrome_options = Options()
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)

driver.get("https://www.mvideo.ru/")

while True:
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)

    try:
        button_trend = driver.find_element(By.XPATH, "//button[@class='tab-button ng-star-inserted']")
        button_trend.click()

        names_el = driver.find_elements(By.XPATH,
                                        "//mvid-shelf-group//div[@class='product-mini-card__name ng-star-inserted']")
        prices_el = driver.find_elements(By.XPATH,
                                         "//mvid-shelf-group//div[@class='product-mini-card__price ng-star-inserted']")
        links_el = driver.find_elements(By.XPATH,
                                        "//mvid-shelf-group//div[@class='product-mini-card__name ng-star-inserted']//a")
    except NoSuchElementException:
        continue
    else:
        break

names = []
prices = []
links = []

for name in names_el:
    names.append(name.text)

for price in prices_el:
    prices.append(price.text)

for link in links_el:
    links.append(link.get_attribute("href"))

for i in range(len(prices)):
    prices[i] = int("".join(prices[i].split()[:2]))

client = MongoClient("localhost", 27017)
db = client["mvideo"]
trends = db.trends

for i in range(len(names)):
    trends.insert_one({
        "Название": names[i],
        "Цена": prices[i],
        "Ссылка": links[i]
    })

list(trends.find({}))
