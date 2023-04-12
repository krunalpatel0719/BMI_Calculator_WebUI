import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="module")
def browser():
    service = Service(executable_path='/chrome_driver/chromedriver')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()

def test_bmi_calculation(browser):
    browser.get('http://localhost:5000/bmi')

    height_input = browser.find_element(By.ID, 'height')
    weight_input = browser.find_element(By.ID, 'weight')
    submit_button = browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

    height_input.send_keys('5 7')
    weight_input.send_keys('150')
    submit_button.click()

    result_text = browser.find_element(By.CSS_SELECTOR, '.result').text
    assert result_text == 'Your BMI is: 24.06 and you are of normal weight'
