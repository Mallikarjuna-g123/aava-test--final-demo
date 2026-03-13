import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = "https://example.com/login"
DASHBOARD_URL = "https://example.com/dashboard"
MAX_USERNAME_LENGTH = 50  # Adjust as per app config
MAX_PASSWORD_LENGTH = 50  # Adjust as per app config

@pytest.fixture
def valid_username():
    return os.environ.get("VALID_USERNAME", "testuser")

@pytest.fixture
def valid_password():
    return os.environ.get("VALID_PASSWORD", "TestPassword123!")

@pytest.fixture
def invalid_username():
    return "invaliduser"

@pytest.fixture
def invalid_password():
    return "WrongPass!"

@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 10)

# TSG-001: Login Page Displays Username and Password Fields
def test_login_page_fields_visible(driver, wait):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Wait for username and password fields to be visible
    username = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    password = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    # Step 3: Assert both fields are displayed
    assert username.is_displayed(), "Username field is not visible"
    assert password.is_displayed(), "Password field is not visible"

# TSG-002: User Can Enter Username
def test_username_field_accepts_input(driver, wait, valid_username):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Find and click on the username input field
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.click()
    # Step 3: Enter a valid username
    username.send_keys(valid_username)
    # Step 4: Assert the username field displays the entered text
    assert username.get_attribute("value") == valid_username

# TSG-003: User Can Enter Password
def test_password_field_accepts_input(driver, wait, valid_password):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Find and click on the password input field
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.click()
    # Step 3: Enter a valid password
    password.send_keys(valid_password)
    # Step 4: Assert password field accepts input and masks characters
    assert password.get_attribute("value") == valid_password
    assert password.get_attribute("type") == "password", "Password field is not masked"

# TSG-004: Password Field Masks Entered Characters
def test_password_field_masks_input(driver, wait):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Enter any text into the password field
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys("Secret123!")
    # Step 3: Assert entered characters are masked
    assert password.get_attribute("type") == "password", "Password field does not mask input"

# TSG-005: Successful Login with Valid Credentials
def test_successful_login_redirects_to_dashboard(driver, wait, valid_username, valid_password):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Enter valid username
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(valid_username)
    # Step 3: Enter valid password
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(valid_password)
    # Step 4: Click the 'Login' button
    login_btn = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
    login_btn.click()
    # Step 5: Assert redirection to dashboard
    wait.until(EC.url_to_be(DASHBOARD_URL))
    assert driver.current_url == DASHBOARD_URL

# TSG-006: Login Fails with Invalid Credentials
def test_login_fails_with_invalid_credentials(driver, wait, invalid_username, invalid_password):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Enter invalid username or password
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    username.send_keys(invalid_username)
    password.send_keys(invalid_password)
    # Step 3: Click the 'Login' button
    login_btn = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
    login_btn.click()
    # Step 4: Assert error message is displayed and user remains on login page
    error_msg = wait.until(EC.visibility_of_element_located((By.ID, "login-error")))
    assert error_msg.is_displayed(), "Error message not displayed"
    assert driver.current_url == LOGIN_URL

# TSG-007: Login Fails with Empty Username
def test_login_fails_with_empty_username(driver, wait, valid_password):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Leave username field empty
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.clear()
    # Step 3: Enter valid password
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(valid_password)
    # Step 4: Click the 'Login' button
    login_btn = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
    login_btn.click()
    # Step 5: Assert validation error for username
    error_msg = wait.until(EC.visibility_of_element_located((By.ID, "username-error")))
    assert error_msg.is_displayed(), "Username required error not displayed"

# TSG-008: Login Fails with Empty Password
def test_login_fails_with_empty_password(driver, wait, valid_username):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Enter valid username
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(valid_username)
    # Step 3: Leave password field empty
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.clear()
    # Step 4: Click the 'Login' button
    login_btn = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
    login_btn.click()
    # Step 5: Assert validation error for password
    error_msg = wait.until(EC.visibility_of_element_located((By.ID, "password-error")))
    assert error_msg.is_displayed(), "Password required error not displayed"

# TSG-009: Login Fails with Both Fields Empty
def test_login_fails_with_empty_fields(driver, wait):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Leave both username and password fields empty
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.clear()
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.clear()
    # Step 3: Click the 'Login' button
    login_btn = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
    login_btn.click()
    # Step 4: Assert validation errors for both fields
    username_error = wait.until(EC.visibility_of_element_located((By.ID, "username-error")))
    password_error = wait.until(EC.visibility_of_element_located((By.ID, "password-error")))
    assert username_error.is_displayed(), "Username required error not displayed"
    assert password_error.is_displayed(), "Password required error not displayed"

# TSG-010: Username Field Accepts Maximum Allowed Characters
def test_username_field_max_length(driver, wait):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Enter maximum allowed characters into username field
    max_username = "a" * MAX_USERNAME_LENGTH
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(max_username)
    # Step 3: Assert field accepts input up to max limit
    assert len(username.get_attribute("value")) == MAX_USERNAME_LENGTH

# TSG-011: Password Field Accepts Maximum Allowed Characters
def test_password_field_max_length(driver, wait):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Enter maximum allowed characters into password field
    max_password = "p" * MAX_PASSWORD_LENGTH
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(max_password)
    # Step 3: Assert field accepts input up to max limit and masks input
    assert len(password.get_attribute("value")) == MAX_PASSWORD_LENGTH
    assert password.get_attribute("type") == "password"

# TSG-012: Username Field Trims Leading and Trailing Spaces
def test_username_field_trims_spaces(driver, wait, valid_password):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Enter username with leading and trailing spaces
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    test_username = "  testuser  "
    username.send_keys(test_username)
    # Step 3: Enter valid password
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(valid_password)
    # Step 4: Click the 'Login' button
    login_btn = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
    login_btn.click()
    # Step 5: Assert system trims spaces and processes username correctly by redirecting to dashboard
    wait.until(EC.url_to_be(DASHBOARD_URL))
    assert driver.current_url == DASHBOARD_URL

# TSG-013: Error Message Disappears on Retry
def test_error_message_disappears_on_retry(driver, wait, invalid_username, invalid_password, valid_username, valid_password):
    # Step 1: Attempt login with invalid credentials
    driver.get(LOGIN_URL)
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    username.send_keys(invalid_username)
    password.send_keys(invalid_password)
    login_btn = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
    login_btn.click()
    # Step 2: Observe error message
    error_msg = wait.until(EC.visibility_of_element_located((By.ID, "login-error")))
    assert error_msg.is_displayed(), "Error message not displayed after invalid login"
    # Step 3: Enter valid credentials
    username.clear()
    password.clear()
    username.send_keys(valid_username)
    password.send_keys(valid_password)
    # Step 4: Click the 'Login' button
    login_btn.click()
    # Step 5: Assert error message disappears and user is redirected to dashboard
    wait.until(EC.url_to_be(DASHBOARD_URL))
    assert driver.current_url == DASHBOARD_URL
    # Optionally check that error message is no longer visible
    assert not error_msg.is_displayed(), "Error message did not disappear after successful login"
