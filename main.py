from selenium import webdriver
import time

chrome_driver_path = 'DRIVER PATH'
driver = webdriver.Chrome(chrome_driver_path)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

#Ищем печеньку
cookie = driver.find_element_by_id("cookie")

#Элементы прокачки
items = driver.find_elements_by_css_selector("#store div")
item_ids = [item.get_attribute("id") for item in items]

timeout = time.time() + 5
five_min = time.time() + 60*5 # 5minutes

while True:
    cookie.click()

    #Каждые 5 сек
    if time.time() > timeout:

        #Получаем все улучшения
        all_prices = driver.find_elements_by_css_selector("#store b")
        item_prices = []

        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        #Создаем словарь с предметами и ценами
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]

        #Получаем текущее число печенек
        money_element = driver.find_element_by_id("money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        #Ищем улучшение которое можем применить
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                 affordable_upgrades[cost] = id

        #Покупаем самое дорогое улучшение
        highest_price_affordable_upgrade = max(affordable_upgrades)
        print(highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

        driver.find_element_by_id(to_purchase_id).click()
        
        #Добавляем 5 сек ожидание перед следующей проверкой
        timeout = time.time() + 5

    #Через 5 минут останавливаем бот и проверяем кол-во печенек в секунду
    if time.time() > five_min:
        cookie_per_s = driver.find_element_by_id("cps").text
        break

