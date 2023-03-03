import time
from selenium import webdriver
with open ("profile.txt") as f:
    path_profile = f.readline()

option = webdriver.ChromeOptions()
option.add_argument('--user-data-dir=D:\\Myprograms\\profile\\User Data')

browser = webdriver.Chrome(chrome_options=option)
browser.get('https://funpay.com/chips/50/trade')

input_price_path = "/html/body/div[1]/div[1]/section/div[2]/div/div/div[2]/div/form/div/div[2]/div/div[3]/div[4]/div/input"
button_path = "/html/body/div[1]/div[1]/section/div[2]/div/div/div[2]/div/form/div/div[1]/div/div/div/div[2]/button"
on_off_path = "/html/body/div[1]/div[1]/section/div[2]/div/div/div[2]/div/form/div/div[2]/div/div[3]/div[1]/div[1]/label/i"
#browser.find_element_by_xpath(input_price_path).clear()
#browser.find_element_by_xpath(input_price_path).send_keys("33")
#browser.find_element_by_xpath(button_path).click()
#browser.find_element_by_xpath(on_off_path).click()