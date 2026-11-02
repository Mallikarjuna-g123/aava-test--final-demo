import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

LOGIN_URL = 'http://your-app-url/login'  # Replace with actual login page URL
VALID_USERNAME = 'testuser'
VALID_PASSWORD = 'TestPass123!'
INVALID_USERNAME = 'invaliduser'
INVALID_PASSWORD = 'InvalidPass!'
SPECIAL_USERNAME = 'user!@#'
SPECIAL_PASSWORD = 'pass!@#'
INVALID_USERNAME_FORMAT = 'userexample.com'  # Missing '@'

@pytest.fixture(scope='function')
def driver():
    # Setup Chrome WebDriver
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

# TSG-001: Login Page Displays Username and Password Fields
def test_login_page_displays_fields(driver):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Assert: Username and password fields are visible
    username = driver.find_element(By.ID, 'username')
    password = driver.find_element(By.ID, 'password')
    assert username.is_displayed(), 'Username field is not visible'
    assert password.is_displayed(), 'Password field is not visible'

# TSG-002: User Can Enter Username
def test_user_can_enter_username(driver):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Click on the username input field
    username = driver.find_element(By.ID, 'username')
    username.click()
    # Step 3: Enter a valid username
    username.send_keys(VALID_USERNAME)
    # Assert: Username is entered and visible in the field
    assert username.get_attribute('value') == VALID_USERNAME

# TSG-003: User Can Enter Password
def test_user_can_enter_password(driver):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Click on the password input field
    password = driver.find_element(By.ID, 'password')
    password.click()
    # Step 3: Enter a valid password
    password.send_keys(VALID_PASSWORD)
    # Assert: Password is entered (masked, see next test for masking)
    assert password.get_attribute('value') == VALID_PASSWORD

# TSG-004: Password Field Masks Entered Characters
def test_password_field_masks_characters(driver):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Enter any value in the password field
    password = driver.find_element(By.ID, 'password')
    password.send_keys('secret')
    # Assert: Password field type is 'password' (masked)
    assert password.get_attribute('type') == 'password', 'Password field is not masked'

# TSG-005: Successful Login with Valid Credentials
def test_successful_login_with_valid_credentials(driver):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Enter a valid username
    driver.find_element(By.ID, 'username').send_keys(VALID_USERNAME)
    # Step 3: Enter a valid password
    driver.find_element(By.ID, 'password').send_keys(VALID_PASSWORD)
    # Step 4: Click the 'Login' button
    driver.find_element(By.ID, 'login-button').click()
    # Assert: Redirected to dashboard (check dashboard element)
    assert '/dashboard' in driver.current_url or driver.find_element(By.ID, 'dashboard').is_displayed(), 'User not redirected to dashboard'

# TSG-006: Login Failure with Invalid Credentials
def test_login_failure_with_invalid_credentials(driver):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Enter invalid username or password
    driver.find_element(By.ID, 'username').send_keys(INVALID_USERNAME)
    driver.find_element(By.ID, 'password').send_keys(INVALID_PASSWORD)
    # Step 3: Click the 'Login' button
    driver.find_element(By.ID, 'login-button').click()
    # Assert: Error message displayed and user remains on login page
    error = driver.find_element(By.ID, 'login-error')
    assert error.is_displayed(), 'Error message not displayed'
    assert LOGIN_URL in driver.current_url, 'User was redirected away from login page'

# TSG-007: Login Attempt with Blank Username
def test_login_attempt_blank_username(driver):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Leave username field blank
    # Step 3: Enter valid password
    driver.find_element(By.ID, 'password').send_keys(VALID_PASSWORD)
    # Step 4: Click the 'Login' button
    driver.find_element(By.ID, 'login-button').click()
    # Assert: Error message for username required
    error = driver.find_element(By.ID, 'username-error')
    assert error.is_displayed(), 'Username required error not displayed'
    assert LOGIN_URL in driver.current_url, 'User was redirected away from login page'

# TSG-008: Login Attempt with Blank Password
def test_login_attempt_blank_password(driver):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Enter valid username
    driver.find_element(By.ID, 'username').send_keys(VALID_USERNAME)
    # Step 3: Leave password field blank
    # Step 4: Click the 'Login' button
    driver.find_element(By.ID, 'login-button').click()
    # Assert: Error message for password required
    error = driver.find_element(By.ID, 'password-error')
    assert error.is_displayed(), 'Password required error not displayed'
    assert LOGIN_URL in driver.current_url, 'User was redirected away from login page'

# TSG-009: Login Attempt with Both Fields Blank
def test_login_attempt_both_fields_blank(driver):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Leave both fields blank
    # Step 3: Click the 'Login' button
    driver.find_element(By.ID, 'login-button').click()
    # Assert: Error messages for both fields required
    username_error = driver.find_element(By.ID, 'username-error')
    password_error = driver.find_element(By.ID, 'password-error')
    assert username_error.is_displayed(), 'Username required error not displayed'
    assert password_error.is_displayed(), 'Password required error not displayed'
    assert LOGIN_URL in driver.current_url, 'User was redirected away from login page'

# TSG-010: Error Message Does Not Leak Sensitive Information
def test_error_message_no_sensitive_info(driver):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Enter invalid username or password
    driver.find_element(By.ID, 'username').send_keys(INVALID_USERNAME)
    driver.find_element(By.ID, 'password').send_keys(INVALID_PASSWORD)
    # Step 3: Click the 'Login' button
    driver.find_element(By.ID, 'login-button').click()
    # Assert: Error message is generic (not specifying which field is incorrect)
    error = driver.find_element(By.ID, 'login-error')
    assert error.is_displayed(), 'Error message not displayed'
    error_text = error.text.lower()
    assert 'incorrect' in error_text or 'invalid' in error_text, 'Error message does not indicate generic failure'
    assert 'username' not in error_text and 'password' not in error_text, 'Error message leaks sensitive info'

# TSG-011: Login with Special Characters in Username and Password
def test_login_with_special_characters(driver):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Enter username with special characters
    driver.find_element(By.ID, 'username').send_keys(SPECIAL_USERNAME)
    # Step 3: Enter password with special characters
    driver.find_element(By.ID, 'password').send_keys(SPECIAL_PASSWORD)
    # Step 4: Click the 'Login' button
    driver.find_element(By.ID, 'login-button').click()
    # Assert: System processes input (either login or error message)
    try:
        dashboard = driver.find_element(By.ID, 'dashboard')
        assert dashboard.is_displayed(), 'Dashboard not displayed after login with special characters'
    except:
        error = driver.find_element(By.ID, 'login-error')
        assert error.is_displayed(), 'Error message not displayed for invalid credentials with special characters'

# TSG-012: Field Validation for Username Format
def test_field_validation_username_format(driver):
    # Step 1: Navigate to the login page
    driver.get(LOGIN_URL)
    # Step 2: Enter invalid username format
    driver.find_element(By.ID, 'username').send_keys(INVALID_USERNAME_FORMAT)
    # Step 3: Enter valid password
    driver.find_element(By.ID, 'password').send_keys(VALID_PASSWORD)
    # Step 4: Click the 'Login' button
    driver.find_element(By.ID, 'login-button').click()
    # Assert: Error message for invalid username format
    error = driver.find_element(By.ID, 'username-format-error')
    assert error.is_displayed(), 'Invalid username format error not displayed'
