from selenium import webdriver
from selenium.webdriver.common.by import By
import time 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

try:
    driver.get('https://www.saucedemo.com/')

    login = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID, 'user-name'))
    )
    login.send_keys('standard_user')
    
    password = driver.find_element(By.ID, 'password')
    password.send_keys('secret_sauce') 

    login_button = driver.find_element(By.ID, 'login-button')
    login_button.click()

finally: 
    time.sleep(2)
    driver.quit()































# try:
#     # Открытие страницы
#     driver.get('https://www.saucedemo.com/')

#     # Ожидание и заполнение поля "Username"
#     username_field = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, 'user-name'))
#     )
#     username_field.send_keys('standard_user')

#     # Заполнение поля "Password"
#     password_field = driver.find_element(By.ID, 'password')
#     password_field.send_keys('secret_sauce')

#     # Нажатие кнопки "Login"
#     login_button = driver.find_element(By.ID, 'login-button')
#     login_button.click()

#     # Ожидание загрузки следующей страницы (например, проверка наличия элемента на новой странице)
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CLASS_NAME, 'inventory_list'))
#     )

# finally:
#     time.sleep(2)
#     driver.quit()