"""
import pytest
from selenium.webdriver.common.by import By

def test_login_page_load(driver):
    driver.get("https://example.com/login")

    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")

    assert username.is_displayed()
    assert password.is_displayed()
"""