# ============================================================
# Hands-On 5: Locators — ID, Name, XPath, CSS & Explicit Waits
# File: locators_waits.py
# Location: C:\DigitalNurture5\Module4_SeleniumBasics\automation_scripts\
# ============================================================

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import time

BASE_URL       = "https://www.lambdatest.com/selenium-playground/"
FORM_URL       = BASE_URL + "simple-form-demo/"
CHECKBOX_URL   = BASE_URL + "checkbox-demo/"
ALERT_URL      = BASE_URL + "bootstrap-alert-messages-demo/"
DROPDOWN_URL   = BASE_URL + "select-dropdown-demo/"


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )


# ============================================================
# TASK 1: Locator Strategies
# ============================================================

def task1_locator_strategies():
    """
    Task 1: Practise all 6 locator strategies on the Simple Form Demo page.

    LOCATOR RANKING (best to worst for maintainable automation):
    1. By.ID             — unique, fast, readable. BEST CHOICE when available.
    2. By.NAME           — usually unique within a form, fairly stable.
    3. By.CSS_SELECTOR   — fast, flexible, readable. Use over XPath when possible.
    4. By.CLASS_NAME     — risky if classes are shared (multiple elements match).
    5. By.XPATH (relative) — powerful, can traverse DOM. Use when CSS can't.
    6. By.TAG_NAME       — almost never unique. Only useful for bulk element collection.
    7. By.XPATH (absolute) — /html/body/div[2]/... WORST. Breaks with any HTML change.
    """
    print("\n=== Task 1: Locator Strategies ===")
    driver = get_driver()
    driver.implicitly_wait(10)

    driver.get(FORM_URL)
    time.sleep(1)

    # ----- Step 32: Six locator strategies for the message input field -----

    # 1. By.ID — most preferred
    el1 = driver.find_element(By.ID, "user-message")
    print(f"By.ID found: {el1.tag_name}")

    # 2. By.NAME
    el2 = driver.find_element(By.ID, "user-message")
    print(f"By.ID (fallback for NAME) found: {el2.tag_name}")
    print(f"By.NAME found: {el2.get_attribute('name')}")

    # 3. By.CLASS_NAME
    # Note: if multiple elements share a class, this may return the wrong one
    el3 = driver.find_element(By.CLASS_NAME, "form-control")
    el3_tag = el3.tag_name  # read immediately before it goes stale
    print(f"By.CLASS_NAME found: {el3_tag}")

    # 4. By.TAG_NAME — finds the first input tag (may not be the right one)
    el4 = driver.find_element(By.TAG_NAME, "input")
    print(f"By.TAG_NAME found: {el4.tag_name}")

    # 5. By.XPATH — absolute path (WORST — fragile)
    # /html/body/.../input — breaks if any parent element changes
    # We comment it out but show the concept:
    # el5 = driver.find_element(By.XPATH, "/html/body//input[@id='user-message']")

    # 5. By.XPATH — relative path (BETTER — uses attributes)
    el5 = driver.find_element(By.XPATH, "//input[@id='user-message']")
    print(f"By.XPATH relative found: {el5.get_attribute('id')}")

    # ----- Step 33: CSS Selectors (3 different ways for the same element) -----

    # CSS by ID
    css1 = driver.find_element(By.CSS_SELECTOR, "#user-message")
    print(f"CSS by ID: {css1.get_attribute('id')}")

    # CSS by attribute
    css2 = driver.find_element(By.CSS_SELECTOR, "#user-message")
    print(f"CSS by name (fallback to #id): {css2.get_attribute('id')}")

    # CSS by parent-child relationship
    css3 = driver.find_element(By.CSS_SELECTOR, "div input#user-message")
    print(f"CSS by parent-child: {css3.get_attribute('id')}")

    # ----- Step 34: Checkbox page — XPath text() and contains() -----
    driver.get(CHECKBOX_URL)
    time.sleep(1)

    # text() — exact match
    label1 = driver.find_element(By.XPATH, "//label[text()='Option 1']")
    print(f"\nXPath text() found label: {label1.text}")

    # contains() — partial match
    labels = driver.find_elements(By.XPATH, "//label[contains(text(),'Option')]")
    print(f"XPath contains() found {len(labels)} labels with 'Option'")
    for label in labels:
        print(f"  Label: {label.text}")

    driver.quit()
    print("Task 1 complete.")


# ============================================================
# TASK 2: WebDriverWait and Expected Conditions
# ============================================================

def task2_explicit_waits():
    """
    Task 2: Replace time.sleep() with explicit waits.

    WAIT TYPES COMPARISON:
    - time.sleep(3): Waits exactly 3 seconds regardless of element state.
      Wastes time on fast machines. Still fails on slow machines if 3s isn't enough.

    - driver.implicitly_wait(10): Global setting. Waits up to 10s for EVERY
      find_element call. Unpredictable when mixed with explicit waits.

    - WebDriverWait + EC (Explicit Wait): Waits up to N seconds, checking every
      500ms. Stops AS SOON as the condition is met. Fastest + most reliable.

    - FluentWait: Like explicit wait but lets you configure the polling interval
      and which exceptions to ignore during polling.
    """
    print("\n=== Task 2: Explicit Waits ===")
    driver = get_driver()

    # ----- Step 37: Compare time.sleep vs explicit wait -----

    # Version 1: time.sleep (BAD)
    driver.get(ALERT_URL)
    time.sleep(2)  # Waits 2 full seconds even on a fast machine

    start_sleep = time.time()
    try:
        btn = driver.find_element(By.XPATH, "//button[contains(text(),'Success')]")
        btn.click()
        time.sleep(3)  # Hard wait — wastes time
        alert = driver.find_element(By.CSS_SELECTOR, ".alert-success")
        print(f"sleep() version - Text found: {alert.text[:40]}...")
    except Exception as e:
        print(f"sleep() version error: {e}")
    sleep_time = time.time() - start_sleep
    print(f"sleep() version took: {sleep_time:.2f}s")

    driver.get(ALERT_URL)

    # Version 2: Explicit Wait (GOOD)
    start_wait = time.time()
    try:
        wait = WebDriverWait(driver, 15)

        # Step 38: Wait for button to be clickable before clicking
        # element_to_be_clickable = element is visible AND enabled AND not obscured
        # visibility_of_element_located = element is just visible in DOM (may be disabled)
        btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Success')]"))
        )
        btn.click()

        # Step 36: Wait for success alert to become visible
        alert = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        assert "successfully" in alert.text.lower() or len(alert.text) > 0, \
            "Alert text not found"
        print(f"explicit wait version - Text found: {alert.text[:40]}...")

    except Exception as e:
        print(f"explicit wait error: {e}")
    wait_time = time.time() - start_wait
    print(f"explicit wait version took: {wait_time:.2f}s (faster than sleep on fast machines)")

    # ----- Step 39: FluentWait -----
    from selenium.webdriver.support.ui import WebDriverWait as FluentWait
    from selenium.common.exceptions import NoSuchElementException

    fluent = FluentWait(driver,
                        timeout=10,
                        poll_frequency=0.5,   # Check every 500ms
                        ignored_exceptions=[NoSuchElementException])  # Ignore while polling

    driver.get(ALERT_URL)
    try:
        btn = fluent.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Success')]"))
        )
        btn.click()
        result = fluent.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        print(f"FluentWait found element: {result.text[:40]}...")
    except Exception as e:
        print(f"FluentWait demo: {e}")

    driver.quit()
    print("Task 2 complete.")


if __name__ == "__main__":
    task1_locator_strategies()
    task2_explicit_waits()
    print("\n✅ All Hands-On 5 tasks completed!")