import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.upload import VkUpload
from vk_api.utils import get_random_id
import time
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from PIL import ImageGrab

with open ("profile.txt") as f:
    path_profile = f.readline()

inputfile = "logvk.txt"
with open(inputfile) as file:
    my_list = [row.strip().split()[1] for row in file]

def makescreen():
    image = ImageGrab.grab()
    return image.save('screen.png')

def upload_photo(upload, photo):
    response = upload.photo_messages(photo)[0]
    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']
    return owner_id, photo_id, access_key

def send_photo(vk, peer_id, owner_id, photo_id, access_key):
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    vk.messages.send(
        random_id=get_random_id(),
        peer_id=peer_id,
        attachment=attachment)

def read_page():
    page = requests.get(URL)
    if page.status_code == 200:
        page_html = bs(page.text, 'html.parser')
        reference_user = page_html.find_all('a', class_='tc-item')
        for i in reference_user:
            if i.find('div', class_='media media-user mt0 online style-circle'):
                name_user = i.find('div', class_='media-user-name')
                amount_user = i.find('div', class_='tc-amount')
                price_user = i.find('div', class_='tc-price')
                users.append([name_user.text.strip(), amount_user.text.strip()[:-3], price_user.text.strip()[:-2]])
        print(users)
    else:
        print("Ошибка при получении ответа от сервера")
    time.sleep(3)

# const variables
input_price_path = "/html/body/div[1]/div[1]/section/div[2]/div/div/div[2]/div/form/div/div[2]/div/div[3]/div[4]/div/input"
button_path = "/html/body/div[1]/div[1]/section/div[2]/div/div/div[2]/div/form/div/div[1]/div/div/div/div[2]/button"
on_off_path = "/html/body/div[1]/div[1]/section/div[2]/div/div/div[2]/div/form/div/div[2]/div/div[3]/div[1]/div[1]/label/i"
URL = "https://funpay.com/chips/50/"
URL_SELENIUM = 'https://funpay.com/chips/50/trade'
users = []

#start work code
vk_session = vk_api.VkApi(token=str(my_list[0]))
PEER_ID = int(my_list[1])
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
upload = VkUpload(vk)
place = int(input("Введите ваше место \n"))-1
while (True):
    try:
        read_page()
        total = 0
        for name in users:
            total += 1
            if 'range' in name:
                my_price = name[2]
                if users[place][0] != 'range' and total > place:
                    raznica = float(users[place][2])-float(my_price)
                    if raznica != float(users[place][2]) and round(float(users[place][2])*float(my_list[2])-0.01, 3) > 20:
                        vk.messages.send(  # Отправляем сообщение
                            user_id=PEER_ID,
                            random_id=0,
                            message=f"Тебя перебил {users[place][0]} на {round(abs(raznica), 3)} \n ставлю: {round(float(users[place][2])*float(my_list[2])-0.01, 3)})")
                        option = webdriver.ChromeOptions()
                        option.add_argument('--user-data-dir=' + path_profile)
                        browser = webdriver.Chrome(chrome_options=option)
                        browser.get(URL_SELENIUM)
                        browser.find_element_by_xpath(input_price_path).clear()
                        browser.find_element_by_xpath(input_price_path).send_keys(str(round(float(users[place][2])*float(my_list[2])-0.01, 3)))
                        browser.find_element_by_xpath(button_path).click()
                        time.sleep(5)
                        browser.get(URL)
                        browser.execute_script("window.scrollTo(0, 400)")
                        time.sleep(2)
                        browser.quit()
                elif float(users[place+1][2]) - float(my_price) > 0.02:
                    vk.messages.send(  # Отправляем сообщение
                        user_id=PEER_ID,
                        random_id=0,
                        message=f"Подправляю цену \n ставлю: {round(float(users[place+1][2]) * float(my_list[2]) - 0.01, 3)})")
                    option = webdriver.ChromeOptions()
                    option.add_argument('--user-data-dir=' + path_profile)
                    browser = webdriver.Chrome(chrome_options=option)
                    browser.get(URL_SELENIUM)
                    browser.find_element_by_xpath(input_price_path).clear()
                    browser.find_element_by_xpath(input_price_path).send_keys(
                        str(round(float(users[place+1][2]) * float(my_list[2]) - 0.01, 3)))
                    browser.find_element_by_xpath(button_path).click()
                    time.sleep(5)
                    browser.get(URL)
                    browser.execute_script("window.scrollTo(0, 400)")
                    time.sleep(2)
                    browser.quit()
                users.clear()
                time.sleep(5)
                break
    except Exception as e:
        continue



