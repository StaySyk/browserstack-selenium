import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions

# BrowserStack configuration for Samsung Galaxy S22
options = ChromeOptions()
options.set_capability("browserName", "chrome")
options.set_capability("deviceName", "Samsung Galaxy S22")
options.set_capability("realMobile", "true")
options.set_capability("os_version", "12.0")
options.set_capability("sessionName", "Samsung S22 Test")

# Initialize the WebDriver (BrowserStack)
driver = webdriver.Remote(options=options)

try:
    # Navigate to the website
    driver.get("https://bstackdemo.com/")

    # Wait for login button and click it
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, "signin"))
    ).click()

    # Enter credentials and log in
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "username"))
    ).send_keys("demouser")
    driver.find_element(By.ID, "password").send_keys("testingisfun99")
    driver.find_element(By.ID, "login-btn").click()

    # Apply Samsung filter
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[@class='checkmark' and text()='Samsung']")
        )
    ).click()

    # Scroll down slightly for mobile view adjustments
    driver.execute_script("window.scrollBy(0, 300);")
    time.sleep(2)  # Allow UI to stabilize

    # Click the favorite button for Galaxy S20+
    fav_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//p[contains(text(), 'Galaxy S20+')]/ancestor::div[contains(@class, 'shelf-item')]//button[@aria-label='delete']",
            )
        )
    )
    fav_button.click()

    # Navigate to favorites page
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "favourites"))
    ).click()

    # Verify if Galaxy S20+ is in favorites
    favorite_item = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//p[contains(@class, 'shelf-item__title') and contains(text(),'Galaxy S20+')]",
            )
        )
    )

    if favorite_item:
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Successfully favorited Galaxy S20+ on S22."}}'
        )
    else:
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Galaxy S20+ not found in favorites on S22."}}'
        )

except Exception as err:
    message = f"Exception: {str(err.__class__)} - {str(err)}"
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": '
        + json.dumps(message)
        + "}}"
    )

finally:
    driver.quit()
