# ============================================================
# Hands-On 5: Locators — ID, Name, XPath, CSS Selectors & Explicit Waits
# File: locators_waits.py
# Location: C:\DigitalNurture5\Module4_SeleniumBasics\automation_scripts\
#
# TARGET SITE: https://www.lambdatest.com/selenium-playground/
# ============================================================

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException
)
from webdriver_manager.chrome import ChromeDriverManager
import time

# ---- URLs ----
BASE_URL     = "https://www.lambdatest.com/selenium-playground/"
FORM_URL     = BASE_URL + "simple-form-demo/"
CHECKBOX_URL = BASE_URL + "checkbox-demo/"
ALERT_URL    = BASE_URL + "bootstrap-alert-messages-demo/"
DROPDOWN_URL = BASE_URL + "select-dropdown-demo/"


# ============================================================
# Helper: Create a Chrome WebDriver with safe options
# ============================================================
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Suppress "Chrome is being controlled" bar
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(10)
    return driver


# ============================================================
# Helper: Close any cookie/ad overlays that block clicking
# ============================================================
def close_overlays(driver):
    """Try to close any popups, cookie banners, or overlays."""
    overlay_selectors = [
        "button#onetrust-accept-btn-handler",
        "button.close",
        ".modal-close",
        "#cookie-accept",
    ]
    for sel in overlay_selectors:
        try:
            btn = driver.find_element(By.CSS_SELECTOR, sel)
            if btn.is_displayed():
                btn.click()
                time.sleep(0.5)
        except Exception:
            pass


# ============================================================
# TASK 1: Locator Strategies
# ============================================================

def task1_locator_strategies():
    """
    Practise all 6 locator strategies on the Simple Form Demo page.

    LOCATOR RANKING (best to worst for maintainable automation):
    1. By.ID              — unique, fast, readable. BEST when available.
    2. By.NAME            — usually unique within a form, fairly stable.
    3. By.CSS_SELECTOR    — fast, flexible, readable. Prefer over XPath.
    4. By.CLASS_NAME      — risky if multiple elements share the class.
    5. By.XPATH (relative) — powerful for text-based/parent traversal.
    6. By.TAG_NAME        — almost never unique; only for bulk collection.
    7. By.XPATH (absolute) — WORST. Breaks with any HTML structure change.
    """
    print("\n" + "="*60)
    print("TASK 1: Locator Strategies")
    print("="*60)

    driver = get_driver()

    try:
        # ---- Navigate to Simple Form Demo ----
        driver.get(FORM_URL)
        time.sleep(2)
        close_overlays(driver)

        wait = WebDriverWait(driver, 20)

        # Wait for page to fully load
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print(f"Page loaded: {driver.title}")

        # ---- Step 32: Six Locator Strategies ----

        # 1. By.ID — most preferred
        try:
            el1 = wait.until(EC.presence_of_element_located((By.ID, "user-message")))
            print(f"✓ By.ID found: tag={el1.tag_name}, id={el1.get_attribute('id')}")
        except TimeoutException:
            print("✗ By.ID failed — element not found")

        # 2. By.NAME
        try:
            el2 = driver.find_element(By.NAME, "user-message")
            print(f"✓ By.NAME found: name={el2.get_attribute('name')}")
        except NoSuchElementException:
            print("✗ By.NAME failed")

        # 3. By.CLASS_NAME
        try:
            # 'form-control' is the Bootstrap class on input fields
            el3 = driver.find_element(By.CLASS_NAME, "form-control")
            print(f"✓ By.CLASS_NAME found: tag={el3.tag_name}")
        except NoSuchElementException:
            print("✗ By.CLASS_NAME failed")

        # 4. By.TAG_NAME — finds first input tag on the page
        try:
            el4 = driver.find_element(By.TAG_NAME, "input")
            print(f"✓ By.TAG_NAME found: tag={el4.tag_name}")
        except NoSuchElementException:
            print("✗ By.TAG_NAME failed")

        # 5. By.XPATH — relative (GOOD — uses attributes)
        try:
            el5 = driver.find_element(By.XPATH, "//input[@id='user-message']")
            print(f"✓ By.XPATH relative found: id={el5.get_attribute('id')}")
        except NoSuchElementException:
            # Fallback XPath
            try:
                el5 = driver.find_element(By.XPATH, "//input[contains(@placeholder,'Message') or contains(@placeholder,'message') or contains(@id,'message')]")
                print(f"✓ By.XPATH fallback found: tag={el5.tag_name}")
            except NoSuchElementException:
                print("✗ By.XPATH failed")

        # ---- Step 33: Three CSS Selectors ----

        # CSS by ID
        try:
            css1 = driver.find_element(By.CSS_SELECTOR, "#user-message")
            print(f"✓ CSS by ID (#user-message): found")
        except NoSuchElementException:
            print("✗ CSS by ID failed")

        # CSS by attribute
        try:
            css2 = driver.find_element(By.CSS_SELECTOR, "[name='user-message']")
            print(f"✓ CSS by attribute ([name='user-message']): found")
        except NoSuchElementException:
            print("✗ CSS by attribute failed")

        # CSS by parent-child
        try:
            css3 = driver.find_element(By.CSS_SELECTOR, "form input")
            print(f"✓ CSS by parent-child (form input): found")
        except NoSuchElementException:
            print("✗ CSS by parent-child failed")

        # ---- Step 34: Checkbox Page — XPath text() and contains() ----
        driver.get(CHECKBOX_URL)
        time.sleep(2)
        close_overlays(driver)

        # XPath text() — exact match
        try:
            label1 = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//label[text()='Option 1']")
                )
            )
            print(f"\n✓ XPath text() found: '{label1.text}'")
        except TimeoutException:
            try:
                # Fallback — some versions use different label text
                label1 = driver.find_element(By.XPATH, "//input[@type='checkbox']/following-sibling::label")
                print(f"✓ XPath fallback found checkbox label: '{label1.text}'")
            except NoSuchElementException:
                print("✗ XPath text() not found — trying alternative")

        # XPath contains() — partial match — finds ALL option labels
        try:
            labels = driver.find_elements(By.XPATH, "//label[contains(text(),'Option')]")
            if labels:
                print(f"✓ XPath contains() found {len(labels)} labels:")
                for label in labels:
                    print(f"   - '{label.text}'")
            else:
                # Try alternative — checkboxes may have different structure
                checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
                print(f"✓ Found {len(checkboxes)} checkboxes on the page")
        except Exception as e:
            print(f"✗ XPath contains() failed: {e}")

        print("\n✅ Task 1 Complete!")

    except Exception as e:
        print(f"\n❌ Task 1 Error: {e}")

    finally:
        driver.quit()


# ============================================================
# TASK 2: WebDriverWait and Expected Conditions
# ============================================================

def task2_explicit_waits():
    """
    Demonstrate Explicit Waits vs time.sleep().

    WAIT TYPES:
    - time.sleep(N):         Always waits N seconds. Wasteful on fast machines.
    - implicitly_wait(N):    Global. Waits up to N seconds per find_element call.
    - WebDriverWait + EC:    Waits up to N seconds, checks every 500ms.
                             Stops AS SOON as condition is met. BEST approach.
    - FluentWait:            Like WebDriverWait but configurable poll interval
                             and ignorable exceptions during polling.
    """
    print("\n" + "="*60)
    print("TASK 2: Explicit Waits vs time.sleep()")
    print("="*60)

    driver = get_driver()

    try:
        # ---- Navigate to Bootstrap Alerts page ----
        driver.get(ALERT_URL)
        time.sleep(2)
        close_overlays(driver)

        wait = WebDriverWait(driver, 20)

        # ---- Step 37: VERSION 1 — time.sleep (BAD approach) ----
        print("\n--- Version 1: time.sleep() (BAD) ---")
        start_sleep = time.time()

        try:
            # Find and click a button that shows an alert
            # Try multiple possible button selectors
            btn = None
            button_selectors = [
                (By.XPATH, "//button[contains(text(),'Success')]"),
                (By.XPATH, "//button[contains(@class,'success')]"),
                (By.CSS_SELECTOR, ".btn-success"),
                (By.XPATH, "//button[contains(text(),'success') or contains(text(),'Success') or contains(text(),'Show')]"),
            ]

            for selector in button_selectors:
                try:
                    btn = driver.find_element(*selector)
                    if btn.is_displayed():
                        break
                except NoSuchElementException:
                    continue

            if btn:
                # Scroll to button and click
                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                time.sleep(0.5)
                try:
                    btn.click()
                except ElementClickInterceptedException:
                    driver.execute_script("arguments[0].click();", btn)

                time.sleep(3)  # Hard wait — BAD practice

                # Try to find the alert
                alert_selectors = [
                    ".alert-success",
                    ".alert.alert-success",
                    "[class*='alert'][class*='success']",
                    ".alert",
                ]
                for sel in alert_selectors:
                    try:
                        alert = driver.find_element(By.CSS_SELECTOR, sel)
                        if alert.is_displayed():
                            print(f"sleep() version found alert: '{alert.text[:50]}...'")
                            break
                    except NoSuchElementException:
                        continue
            else:
                print("No success button found — skipping sleep demo")

        except Exception as e:
            print(f"sleep() version note: {e}")

        elapsed_sleep = time.time() - start_sleep
        print(f"sleep() version took: {elapsed_sleep:.2f}s")

        # ---- Step 36 & 38: VERSION 2 — Explicit Wait (GOOD approach) ----
        print("\n--- Version 2: Explicit Wait (GOOD) ---")
        driver.get(ALERT_URL)
        time.sleep(2)
        close_overlays(driver)

        start_explicit = time.time()

        try:
            # Step 38: Wait for element to be CLICKABLE before clicking
            # element_to_be_clickable = visible AND enabled AND not obscured
            # visibility_of_element_located = just visible in DOM (may be disabled)
            btn = None
            button_selectors = [
                (By.XPATH, "//button[contains(text(),'Success')]"),
                (By.CSS_SELECTOR, ".btn-success"),
                (By.XPATH, "//button[contains(@class,'success')]"),
            ]

            for selector in button_selectors:
                try:
                    btn = wait.until(EC.element_to_be_clickable(selector))
                    if btn:
                        break
                except TimeoutException:
                    continue

            if btn:
                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                time.sleep(0.3)
                try:
                    btn.click()
                except ElementClickInterceptedException:
                    driver.execute_script("arguments[0].click();", btn)

                # Step 36: Wait for success alert to become VISIBLE
                alert = None
                alert_selectors = [
                    (By.CSS_SELECTOR, ".alert-success"),
                    (By.CSS_SELECTOR, ".alert.alert-success"),
                    (By.CSS_SELECTOR, ".alert"),
                ]
                for sel in alert_selectors:
                    try:
                        alert = wait.until(EC.visibility_of_element_located(sel))
                        if alert:
                            break
                    except TimeoutException:
                        continue

                if alert:
                    print(f"explicit wait found alert: '{alert.text[:50]}'")
                    assert len(alert.text) > 0, "Alert has no text"
                    print("✓ Alert text assertion passed")
                else:
                    print("Alert appeared but could not be captured")
            else:
                print("No clickable button found — page structure may have changed")

        except Exception as e:
            print(f"Explicit wait note: {e}")

        elapsed_explicit = time.time() - start_explicit
        print(f"explicit wait version took: {elapsed_explicit:.2f}s")
        print(f"Explicit wait is faster: {elapsed_sleep > elapsed_explicit}")

        # ---- Step 39: FluentWait ----
        print("\n--- FluentWait Demo ---")
        driver.get(ALERT_URL)
        time.sleep(2)
        close_overlays(driver)

        # FluentWait: poll every 500ms, ignore NoSuchElementException during polling
        fluent_wait = WebDriverWait(
            driver,
            timeout=20,
            poll_frequency=0.5,
        )

        try:
            btn = None
            for selector in [
                (By.XPATH, "//button[contains(text(),'Success')]"),
                (By.CSS_SELECTOR, ".btn-success"),
            ]:
                try:
                    btn = fluent_wait.until(EC.element_to_be_clickable(selector))
                    if btn:
                        break
                except TimeoutException:
                    continue

            if btn:
                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                time.sleep(0.3)
                try:
                    btn.click()
                except ElementClickInterceptedException:
                    driver.execute_script("arguments[0].click();", btn)

                for sel in [
                    (By.CSS_SELECTOR, ".alert-success"),
                    (By.CSS_SELECTOR, ".alert"),
                ]:
                    try:
                        result = fluent_wait.until(EC.visibility_of_element_located(sel))
                        if result:
                            print(f"✓ FluentWait found element: '{result.text[:50]}'")
                            break
                    except TimeoutException:
                        continue
            else:
                print("FluentWait: No button found to click")

        except Exception as e:
            print(f"FluentWait note: {e}")

        print("\n✅ Task 2 Complete!")

    except Exception as e:
        print(f"\n❌ Task 2 Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        driver.quit()


# ============================================================
# Run all tasks
# ============================================================
if __name__ == "__main__":
    print("Starting Hands-On 5: Locators & Explicit Waits")
    print("Target: https://www.lambdatest.com/selenium-playground/")

    task1_locator_strategies()
    task2_explicit_waits()

    print("\n" + "="*60)
    print("✅ All Hands-On 5 tasks completed!")
    print("="*60)