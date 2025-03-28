import json
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions


options = ChromeOptions()
options.set_capability("sessionName", "BrowserStack S20+ Test")
driver = webdriver.Chrome(options=options)


# Helper function for scrolling element into view (useful for mobile)
def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(0.5)  # Small pause after scroll can sometimes help


try:
    # User Login
    driver.get("https://bstackdemo.com/")
    WebDriverWait(driver, 20).until(
        EC.title_contains("StackDemo")
    )  # Increased wait time for mobile potentially

    # Click Sign In button
    signin_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "signin"))
    )
    scroll_to_element(driver, signin_button)  # Scroll just in case
    signin_button.click()

    # --- Login Form ---
    # Select username 'demouser'
    # Note: On mobile, the username/password might be directly typed,
    # but this site uses divs for selection.

    # Click username dropdown area (optional, but might help reveal options)
    username_field = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#username input")
        )  # Target input inside
    )
    scroll_to_element(driver, username_field)
    # username_field.click() # Clicking the input might not be needed if the div below works

    # Select the actual 'demouser' option
    demouser_option = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[@id='username']//div[text()='demouser']")
        )
    )
    scroll_to_element(driver, demouser_option)  # Scroll to the option
    demouser_option.click()

    # Click password dropdown area (optional)
    password_field = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#password input")
        )  # Target input inside
    )
    scroll_to_element(driver, password_field)
    # password_field.click() # Clicking the input might not be needed

    # Select the actual password option
    password_option = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[@id='password']//div[text()='testingisfun99']")
        )
    )
    scroll_to_element(driver, password_option)  # Scroll to the option
    password_option.click()

    # Click login button
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "login-btn"))
    )
    scroll_to_element(driver, login_button)  # Scroll if needed
    login_button.click()

    # --- Filter and Favorite ---
    # Wait for products page to load (check for a known element)
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "shelf-container"))
    )

    # Filter for Samsung device
    # Ensure the filter sidebar is visible/clickable
    samsung_filter = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            # Corrected locator: target the input/label or the span robustly
            (
                By.XPATH,
                "//span[text()='Samsung']/preceding-sibling::input[@type='checkbox']",
            )
            # (By.XPATH, "//span[normalize-space()='Samsung']") # Alternative if checkbox click fails
        )
    )
    scroll_to_element(driver, samsung_filter)
    # Sometimes a JS click is more reliable on mobile checkboxes
    driver.execute_script("arguments[0].click();", samsung_filter)
    # samsung_filter.click() # Standard click - try JS click if this fails

    # Allow time for filter results to apply
    time.sleep(2)  # Add a small static wait after filtering

    # Find and favorite the Galaxy S20+
    # CORRECTED LOCATOR: The favorite button is not 'delete'
    # It's usually a button within the item's div, maybe containing a heart icon.
    # Inspect the element on the actual page to confirm the best locator.
    # Assuming it's a button sibling to the price or inside a 'buy-btn' div:
    favorite_button_locator = (
        By.XPATH,
        "//p[normalize-space(text())='Galaxy S20 Plus']/ancestor::div[contains(@class, 'shelf-item')]//div[contains(@class, 'shelf-item__buy-btn')]",
        # Alternative: "//p[normalize-space(text())='Galaxy S20 Plus']/following-sibling::div[@class='shelf-item__buy-btn']"
    )

    favorite_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(favorite_button_locator)
    )
    scroll_to_element(driver, favorite_button)
    favorite_button.click()

    # --- Verify in Favorites ---
    # Navigate to favorites page
    favorites_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "favourites"))
    )
    # On mobile, the favorites link might be in a collapsed menu or need scrolling
    scroll_to_element(driver, favorites_link)
    favorites_link.click()

    # Verify Galaxy S20+ is in favorites
    # Wait for the favorites page items to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "shelf-item")
        )  # Wait for at least one item
    )

    # SIMPLIFIED and more robust locator for the title in favorites
    favorite_item_locator = (
        By.XPATH,
        "//div[contains(@class, 'shelf-item')]//p[normalize-space(text())='Galaxy S20 Plus']",
    )

    # Use visibility_of_element_located for verification
    favorite_item_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(favorite_item_locator)
    )
    scroll_to_element(
        driver, favorite_item_element
    )  # Scroll to make sure it's fully visible
    favorite_item_text = favorite_item_element.text

    if "Galaxy S20 Plus" in favorite_item_text:  # Check against the exact text
        print("Verification PASSED: Galaxy S20 Plus found in favorites.")
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Successfully favorited Galaxy S20+"}}'
        )
    else:
        print(
            f"Verification FAILED: Expected 'Galaxy S20 Plus', but found '{favorite_item_text}'"
        )
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Galaxy S20+ not found or text mismatch in favorites"}}'
        )

except (NoSuchElementException, TimeoutException) as err:
    message = f"Exception: {err.__class__.__name__} - {str(err)}"
    print(message)  # Print error locally for debugging
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": '
        + json.dumps(message)
        + "}}"
    )
except Exception as err:
    message = f"An unexpected error occurred: {err.__class__.__name__} - {str(err)}"
    print(message)  # Print error locally for debugging
    # Capture stack trace if needed for complex errors
    # import traceback
    # message += "\n" + traceback.format_exc()
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": '
        + json.dumps(message)
        + "}}"
    )
finally:
    # Always quit the driver session to release resources on BrowserStack
    if driver:
        driver.quit()
