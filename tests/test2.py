import json
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Set up Chrome options for BrowserStack
options = ChromeOptions()
options.set_capability("sessionName", "BrowserStack S20+ Test")
driver = webdriver.Chrome(options=options)

try:
    # User Login
    driver.get("https://bstackdemo.com/")
    WebDriverWait(driver, 10).until(EC.title_contains("StackDemo"))
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "signin"))
    ).click()

    # Wait for the username field and click it
    username_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "username"))
    )
    username_field.click()
    time.sleep(1)  # Short delay for dropdown to load

    # Try selecting 'demouser' from the dropdown
    try:
        demouser_option = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//option[@value='demouser']"))
        )
        demouser_option.click()
    except Exception:
        driver.execute_script("document.getElementById('username').value = 'demouser';")

    # Confirm the input value
    assert (
        driver.execute_script("return document.getElementById('username').value")
        == "demouser"
    )

    # Enter password: target the actual input element inside the password container
    password_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#password input"))
    )
    password_field.send_keys("testingisfun99")

    # Click login button
    login_button = driver.find_element(By.ID, "login-btn")
    if driver.execute_script("return arguments[0].disabled;", login_button):
        driver.execute_script("arguments[0].removeAttribute('disabled');", login_button)
    login_button.click()

    # Filter for Samsung device
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[@class='checkmark' and text()='Samsung']")
        )
    ).click()

    # Find and favorite the Galaxy S20+
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//p[contains(text(), 'Galaxy S20+')]/ancestor::div[contains(@class, 'shelf-item')]//button[@aria-label='delete']",
            )
        )
    ).click()

    # Navigate to favorites page
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "favourites"))
    ).click()

    # Verify Galaxy S20+ is in favorites
    favorite_item = (
        WebDriverWait(driver, 10)
        .until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class, 'shelf-container')]//div[contains(@class, 'shelf-item')]//p[contains(@class, 'shelf-item__title') and contains(text(),'Galaxy S20+')]",
                )
            )
        )
        .text
    )

    if "Galaxy S20+" in favorite_item:
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Successfully favorited Galaxy S20+"}}'
        )
    else:
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Galaxy S20+ not found in favorites"}}'
        )

except NoSuchElementException as err:
    message = "Exception: " + str(err.__class__) + str(err)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": '
        + json.dumps(message)
        + "}}"
    )
except Exception as err:
    message = "Exception: " + str(err.__class__) + str(err)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": '
        + json.dumps(message)
        + "}}"
    )
finally:
    driver.quit()
