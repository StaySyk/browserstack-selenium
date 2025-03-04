import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as E
from selenium.common.exceptions import NoSuchElementException

# Minimal ChromeOptions setup
opts = Options()
opts.set_capability("sessionName", "BrowserStack Minimal Test")
driver = webdriver.Remote(options=opts)

# Quick shorthand for WebDriverWait
wait = lambda timeout=10: W(driver, timeout)

try:
    # 1. Go to site & click "Sign in"
    driver.get("https://bstackdemo.com/")
    wait().until(E.title_contains("StackDemo"))
    wait().until(E.element_to_be_clickable((By.ID, "signin"))).click()

    # 2. Set username & password via JavaScript (bypasses dropdown issues)
    driver.execute_script("document.getElementById('username').value = 'demouser';")
    driver.execute_script(
        "document.getElementById('password').value = 'testingisfun99';"
    )

    # 3. Remove 'disabled' if needed & click login
    login_btn = driver.find_element(By.ID, "login-btn")
    if driver.execute_script("return arguments[0].disabled;", login_btn):
        driver.execute_script("arguments[0].removeAttribute('disabled');", login_btn)
    login_btn.click()

    # 4. Filter for Samsung & favorite Galaxy S20+
    wait().until(
        E.element_to_be_clickable(
            (By.XPATH, "//span[@class='checkmark' and text()='Samsung']")
        )
    ).click()
    wait().until(
        E.element_to_be_clickable(
            (
                By.XPATH,
                "//p[contains(text(),'Galaxy S20+')]/ancestor::div[contains(@class,'shelf-item')]//button[@aria-label='delete']",
            )
        )
    ).click()

    # 5. Go to favorites & verify Galaxy S20+
    wait().until(E.element_to_be_clickable((By.ID, "favourites"))).click()
    item_text = (
        wait()
        .until(
            E.visibility_of_element_located(
                (
                    By.XPATH,
                    "//p[contains(@class,'shelf-item__title') and contains(text(),'Galaxy S20+')]",
                )
            )
        )
        .text
    )

    # 6. Mark test as passed/failed on BrowserStack
    if "Galaxy S20+" in item_text:
        driver.execute_script(
            'browserstack_executor: {"action":"setSessionStatus","arguments":{"status":"passed","reason":"Successfully favorited Galaxy S20+"}}'
        )
    else:
        driver.execute_script(
            'browserstack_executor: {"action":"setSessionStatus","arguments":{"status":"failed","reason":"Galaxy S20+ not found in favorites"}}'
        )

except NoSuchElementException as err:
    msg = f"Exception: {err.__class__} {err}"
    driver.execute_script(
        f'browserstack_executor: {{"action":"setSessionStatus","arguments":{{"status":"failed","reason":{json.dumps(msg)}}}}}'
    )
except Exception as err:
    msg = f"Exception: {err.__class__} {err}"
    driver.execute_script(
        f'browserstack_executor: {{"action":"setSessionStatus","arguments":{{"status":"failed","reason":{json.dumps(msg)}}}}}'
    )
finally:
    driver.quit()
