import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = "https://example.com/login"
DASHBOARD_URL = "https://example.com/dashboard"

@pytest.mark.usefixtures("driver")
def test_login_page_displays_username_and_password_fields(driver):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Wait for username field to be visible
    username = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "username"))
    )
    # Step 3: Wait for password field to be visible
    password = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    # Step 4: Assert both fields are displayed
    assert username.is_displayed(), "Username field is not displayed"
    assert password.is_displayed(), "Password field is not displayed"

@pytest.mark.usefixtures("driver")
def test_user_can_enter_username(driver):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Wait for username field
    username = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "username"))
    )
    # Step 3: Enter username
    username.clear()
    username.send_keys("testuser")
    # Step 4: Assert the value is entered
    assert username.get_attribute("value") == "testuser", "Username not entered correctly"

@pytest.mark.usefixtures("driver")
def test_user_can_enter_password(driver):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Wait for password field
    password = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    # Step 3: Enter password
    password.clear()
    password.send_keys("Secret123!")
    # Step 4: Assert the value is entered
    assert password.get_attribute("value") == "Secret123!", "Password not entered correctly"

@pytest.mark.usefixtures("driver")
def test_login_button_triggers_authentication(driver):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Wait for login button
    login_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "login-button"))
    )
    # Step 3: Enter username and password
    driver.find_element(By.ID, "username").send_keys("testuser")
    driver.find_element(By.ID, "password").send_keys("Secret123!")
    # Step 4: Click login button
    login_btn.click()
    # Step 5: Wait for either dashboard or error message
    WebDriverWait(driver, 10).until(
        EC.any_of(
            EC.url_contains("dashboard"),
            EC.visibility_of_element_located((By.ID, "error-message"))
        )
    )
    # Step 6: Assert authentication was attempted (url changed or error message shown)
    assert driver.current_url != LOGIN_URL, "Authentication did not trigger"

@pytest.mark.usefixtures("driver")
def test_valid_credentials_redirect_to_dashboard(driver):
    # Step 1: Navigate to login page
    driver.get(LOGIN_URL)
    # Step 2: Wait for fields
    username = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "username"))
    )
    password = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    # Step 3: Enter valid credentials from environment variables
    valid_username = os.getenv("LOGIN_USERNAME", "validuser")
    valid_password = os.getenv("LOGIN_PASSWORD", "ValidPass123!")
    username.send_keys(valid_username)
    password.send_keys(valid_password)
    # Step 4: Click login button
    driver.find_element(By.ID, "login-button").click()
    # Step 5: Wait for dashboard url
    WebDriverWait(driver, 10).until(
        EC.url_contains("dashboard")
    )
    # Step 6: Assert redirected to dashboard
    assert DASHBOARD_URL in driver.current_url, "User not redirected to dashboard after login"

@pytest.mark.usefixtures("driver")
def test_invalid_credentials_show_error_message(driver):
    # Step 1: Navigate to login page
    driver.get(LOGIN_URL)
    # Step 2: Wait for fields
    username = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "username"))
    )
    password = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    # Step 3: Enter invalid credentials
    username.send_keys("invaliduser")
    password.send_keys("wrongpass")
    # Step 4: Click login button
    driver.find_element(By.ID, "login-button").click()
    # Step 5: Wait for error message
    error_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "error-message"))
    )
    # Step 6: Assert error message is displayed
    assert error_msg.is_displayed(), "Error message not shown for invalid credentials"

@pytest.mark.usefixtures("driver")
def test_password_field_masks_characters(driver):
    # Step 1: Navigate to login page
    driver.get(LOGIN_URL)
    # Step 2: Wait for password field
    password = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    # Step 3: Assert password field type is 'password'
    field_type = password.get_attribute("type")
    assert field_type == "password", f"Password field is not masked, found type: {field_type}"