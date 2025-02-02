import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
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

@pytest.fixture(scope="function")
def failed_login_driver(driver):
    driver.get('https://www.saucedemo.com/')
    login = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID, 'user-name'))
    )
    login.send_keys('wrong_login')

    password = driver.find_element(By.ID, 'password')
    password.send_keys('wrong_password')

    button = driver.find_element(By.ID, 'login-button')
    button.click()

    return driver

def test_login(logged_in_driver):
    assert logged_in_driver.current_url.endswith("inventory.html")

def test_add_to_card(logged_in_driver):
    add_to_card = WebDriverWait(logged_in_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'add-to-cart-sauce-labs-backpack'))
    )
    add_to_card.click()
    
    cart_badge = logged_in_driver.find_element(By.CLASS_NAME, 'shopping_cart_badge')
    assert cart_badge.text == "1", "Товар не добавлен в корзину"

def test_remove_from_card(logged_in_driver):
    remove_button = WebDriverWait(logged_in_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'remove-sauce-labs-backpack'))
    )
    remove_button.click()
    
    cart_badge = logged_in_driver.find_elements(By.CLASS_NAME, 'shopping_cart_badge')
    assert len(cart_badge) == 0, "Товар не удалён из корзины"

def test_price_filter_low_to_high(logged_in_driver):
    filter_dropdown = WebDriverWait(logged_in_driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'product_sort_container'))
    )
    Select(filter_dropdown).select_by_visible_text("Price (low to high)")

    WebDriverWait(logged_in_driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'inventory_item_price'))
    )

    prices = logged_in_driver.find_elements(By.CLASS_NAME, 'inventory_item_price')
    price_list = []

    for price in prices:
        price_text = price.text.replace("$", "")
        price_list.append(float(price_text))

    assert price_list == sorted(price_list), "Товары не отсортированы по возрастанию цены"

def test_price_filter_high_to_low(logged_in_driver):
    filter_high = WebDriverWait(logged_in_driver,10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "product_sort_container"))
    )
    Select(filter_high).select_by_visible_text("Price (high to low)")


    prices = WebDriverWait(logged_in_driver,10).until(
        EC.presence_of_all_elements_located ((By.CLASS_NAME, "inventory_item_price"))
    )
    price_list = []

    for price in prices:
        price_text = price.text.replace('$', '')
        price_list.append(float(price_text))

    assert price_list == sorted(price_list, reverse=True)
    
def test_failed_login(failed_login_driver):
    error_message = WebDriverWait(failed_login_driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'h3[data-test="error"]'))
    )
    assert "Epic sadface: Username and password do not match any user in this service" in error_message.text, "Неверное сообщение об ошибке"


























