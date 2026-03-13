# File: tests/test_login.py

import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ---------- Fixtures ----------

@pytest.fixture(scope="session")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def base_url():
    return "https://example.com/login"


@pytest.fixture(scope="session")
def valid_credentials():
    username = os.environ.get("TEST_USERNAME")
    password = os.environ.get("TEST_PASSWORD")

    assert username, "Environment variable TEST_USERNAME is required"
    assert password, "Environment variable TEST_PASSWORD is required"

    return username, password


@pytest.fixture(scope="function")
def open_login(driver, base_url):
    driver.get(base_url)


# ---------- Utility Function ----------

def login(driver, username, password):

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    ).send_keys(username)

    driver.find_element(By.ID, "password").send_keys(password)

    driver.find_element(By.ID, "loginBtn").click()


# ---------- Test Cases ----------

def test_login_with_valid_credentials(driver, open_login, valid_credentials):
    """
    Verify login with valid credentials
    """

    username, password = valid_credentials

    login(driver, username, password)

    landing_elem = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "landingPageMain"))
    )

    assert landing_elem.is_displayed(), "Landing page main element not visible after login"


def test_error_message_for_invalid_login(driver, open_login):
    """
    Verify error message for invalid login
    """

    login(driver, "invalid_user", "invalid_pass")

    error_elem = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "loginError"))
    )

    assert error_elem.is_displayed(), "Error message not displayed for invalid login"


def test_landing_page_loads_successfully(driver, open_login, valid_credentials):
    """
    Verify landing page loads successfully
    """

    username, password = valid_credentials

    login(driver, username, password)

    landing_elem = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "landingPageMain"))
    )

    assert landing_elem.is_displayed(), "Landing page main element not visible"


def test_navigation_menu_visible(driver, open_login, valid_credentials):
    """
    Verify navigation menu is visible
    """

    username, password = valid_credentials

    login(driver, username, password)

    nav_elem = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "navigationMenu"))
    )

    assert nav_elem.is_displayed(), "Navigation menu is not visible on the landing page"