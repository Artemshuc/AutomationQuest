import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def logged_in_driver(driver):
    driver.get('https://www.saucedemo.com/')
    
    login = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'user-name'))
    )
    login.send_keys('standard_user')
    
    password = driver.find_element(By.ID, 'password')
    password.send_keys('secret_sauce')
    
    button = driver.find_element(By.ID, 'login-button')
    button.click()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'inventory_item'))
    )
    
    return driver

def test_login(logged_in_driver):
    assert logged_in_driver.current_url.endswith("inventory.html")
    time.sleep(2)

def test_add_to_card(logged_in_driver):
    add_to_card = WebDriverWait(logged_in_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'add-to-cart-sauce-labs-backpack'))
    )
    add_to_card.click()
    
    cart_badge = logged_in_driver.find_element(By.CLASS_NAME, 'shopping_cart_badge')
    assert cart_badge.text == "1", "Товар не добавлен в корзину"
    time.sleep(2)

def test_remove_from_card(logged_in_driver):
    remove_button = WebDriverWait(logged_in_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'remove-sauce-labs-backpack'))
    )
    remove_button.click()
    
    cart_badge = logged_in_driver.find_elements(By.CLASS_NAME, 'shopping_cart_badge')
    assert len(cart_badge) == 0, "Товар не удалён из корзины"
    time.sleep(2)














# def test_add_to_card(logged_in_driver):
#     add_to_card = WebDriverWait(logged_in_driver, 10).until(
#         EC.presence_of_element_located((By.ID, 'add-to-cart-sauce-labs-backpack'))
#     )
#     add_to_card.click()
    
#     cart_badge = logged_in_driver.find_element(By.CLASS_NAME, 'shopping_cart_badge')
#     assert cart_badge.text == "1", "Товар не добавлен в корзину"
#     time.sleep(2)

# def test_remove_from_card(logged_in_driver):
#     remove_button = WebDriverWait(logged_in_driver, 10).until(
#         EC.presence_of_element_located((By.ID, 'remove-sauce-labs-backpack'))
#     )
#     remove_button.click()
    
#     cart_badge = logged_in_driver.find_elements(By.CLASS_NAME, 'shopping_cart_badge')
#     assert len(cart_badge) == 0, "Товар не удалён из корзины"
#     time.sleep(2)
























