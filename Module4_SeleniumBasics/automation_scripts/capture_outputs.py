# ============================================================
# capture_outputs.py — Fixed Version
# Takes organized screenshots for Module 4 Selenium exercises
# Run: python capture_outputs.py
# Location: C:\DigitalNurture5\Module4_SeleniumBasics\automation_scripts\
# ============================================================

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

BASE_URL = "https://www.lambdatest.com/selenium-playground/"
OUTPUT_FOLDER = "../written_exercises/output"


# ============================================================
# Helper: Create driver
# ============================================================
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(15)
    driver.set_page_load_timeout(30)
    return driver


# ============================================================
# Helper: Save screenshot
# ============================================================
def save_screenshot(driver, filename):
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    path = os.path.join(OUTPUT_FOLDER, filename)
    driver.save_screenshot(path)
    print(f"  ✓ Screenshot saved: {path}")


# ============================================================
# Helper: Close cookie/ad overlays
# ============================================================
def close_overlays(driver):
    selectors = [
        "button#onetrust-accept-btn-handler",
        ".ReactModal__Content button.close",
        "button.close",
        "#cookie-accept",
    ]
    for sel in selectors:
        try:
            btn = driver.find_element(By.CSS_SELECTOR, sel)
            if btn.is_displayed():
                btn.click()
                time.sleep(0.5)
        except Exception:
            pass


# ============================================================
# Helper: Safe send_keys with explicit wait
# ============================================================
def safe_send_keys(driver, locator, text, timeout=15):
    """Wait for element to be visible AND interactable, then type."""
    wait = WebDriverWait(driver, timeout)
    element = wait.until(EC.visibility_of_element_located(locator))
    # Scroll element into view
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.5)
    # Click first to focus
    try:
        element.click()
    except Exception:
        driver.execute_script("arguments[0].click();", element)
    time.sleep(0.3)
    element.clear()
    element.send_keys(text)
    return element


# ============================================================
# Helper: Safe click with explicit wait
# ============================================================
def safe_click(driver, locator, timeout=15):
    """Wait for element to be clickable, scroll to it, then click."""
    wait   = WebDriverWait(driver, timeout)
    element = wait.until(EC.element_to_be_clickable(locator))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.5)
    try:
        element.click()
    except Exception:
        driver.execute_script("arguments[0].click();", element)
    return element


# ============================================================
# HO4 — Selenium Setup & Navigation Screenshots
# ============================================================
def capture_ho4():
    print("\n📸 Capturing HO4 screenshots...")
    driver = get_driver()
    try:
        # Screenshot 1: Playground home page
        driver.get(BASE_URL)
        time.sleep(3)
        close_overlays(driver)
        save_screenshot(driver, "ho4_playground_home.png")

        # Screenshot 2: Simple Form Demo page
        driver.get(BASE_URL + "simple-form-demo/")
        time.sleep(2)
        close_overlays(driver)
        save_screenshot(driver, "ho4_simple_form_page.png")

        # Screenshot 3: Google tab demo (window handling)
        driver.execute_script('window.open("https://www.google.com");')
        time.sleep(2)
        tabs = driver.window_handles
        driver.switch_to.window(tabs[1])
        time.sleep(2)
        save_screenshot(driver, "ho4_google_tab.png")
        driver.switch_to.window(tabs[0])

        print("  ✅ HO4 complete")
    except Exception as e:
        print(f"  ⚠️ HO4 error: {e}")
        save_screenshot(driver, "ho4_error.png")
    finally:
        driver.quit()


# ============================================================
# HO5 — Locators & Explicit Waits Screenshots
# ============================================================
def capture_ho5():
    print("\n📸 Capturing HO5 screenshots...")
    driver = get_driver()
    try:
        wait = WebDriverWait(driver, 20)

        # Screenshot 1: Simple Form Demo — locators
        driver.get(BASE_URL + "simple-form-demo/")
        time.sleep(2)
        close_overlays(driver)

        # Highlight the input element
        el = wait.until(EC.presence_of_element_located((By.ID, "user-message")))
        driver.execute_script(
            "arguments[0].style.border='3px solid red'; arguments[0].style.backgroundColor='#fffacd';",
            el
        )
        save_screenshot(driver, "ho5_locator_id_highlighted.png")

        # Screenshot 2: Checkbox Demo
        driver.get(BASE_URL + "checkbox-demo/")
        time.sleep(2)
        close_overlays(driver)
        save_screenshot(driver, "ho5_checkbox_demo.png")

        # Screenshot 3: Checkbox clicked
        try:
            cb = wait.until(EC.element_to_be_clickable((By.ID, "isAgeSelected")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", cb)
            time.sleep(0.5)
            cb.click()
            time.sleep(1)
            save_screenshot(driver, "ho5_checkbox_checked.png")
        except Exception as e:
            print(f"  ⚠️ Checkbox click: {e}")

        # Screenshot 4: Bootstrap Alert
        driver.get(BASE_URL + "bootstrap-alert-messages-demo/")
        time.sleep(2)
        close_overlays(driver)
        save_screenshot(driver, "ho5_alert_page.png")

        # Try clicking a button and capturing the alert
        try:
            btn_selectors = [
                (By.XPATH, "//button[contains(text(),'Success')]"),
                (By.CSS_SELECTOR, ".btn-success"),
                (By.XPATH, "//button[contains(@class,'btn') and contains(text(),'Success')]"),
            ]
            for sel in btn_selectors:
                try:
                    btn = wait.until(EC.element_to_be_clickable(sel))
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(2)
                    save_screenshot(driver, "ho5_alert_shown.png")
                    break
                except TimeoutException:
                    continue
        except Exception as e:
            print(f"  ⚠️ Alert button: {e}")

        print("  ✅ HO5 complete")
    except Exception as e:
        print(f"  ⚠️ HO5 error: {e}")
        save_screenshot(driver, "ho5_error.png")
    finally:
        driver.quit()


# ============================================================
# HO6 — pytest Test Results Screenshots
# ============================================================
def capture_ho6():
    print("\n📸 Capturing HO6 screenshots...")
    driver = get_driver()
    try:
        wait = WebDriverWait(driver, 20)

        # Screenshot 1: Form submission test passing
        driver.get(BASE_URL + "simple-form-demo/")
        time.sleep(3)
        close_overlays(driver)

        # Use safe_send_keys helper
        safe_send_keys(driver, (By.ID, "user-message"), "Hello Selenium")
        time.sleep(0.5)

        safe_click(driver, (By.ID, "showInput"))
        time.sleep(2)

        # Wait for the result to appear
        try:
            result = wait.until(EC.visibility_of_element_located((By.ID, "message")))
            print(f"  Form result: '{result.text}'")
        except TimeoutException:
            print("  ⚠️ Result element not found")

        save_screenshot(driver, "ho6_form_submission_pass.png")

        # Screenshot 2: Checkbox test
        driver.get(BASE_URL + "checkbox-demo/")
        time.sleep(2)
        close_overlays(driver)

        try:
            cb = wait.until(EC.element_to_be_clickable((By.ID, "isAgeSelected")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", cb)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", cb)
            time.sleep(1)
            save_screenshot(driver, "ho6_checkbox_pass.png")
        except Exception as e:
            print(f"  ⚠️ Checkbox: {e}")

        # Screenshot 3: Dropdown test
        driver.get(BASE_URL + "select-dropdown-demo/")
        time.sleep(2)
        close_overlays(driver)

        try:
            dropdown_el = wait.until(
                EC.element_to_be_clickable((By.ID, "select-demo"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", dropdown_el)
            time.sleep(0.5)
            select = Select(dropdown_el)
            select.select_by_visible_text("Wednesday")
            time.sleep(1)
            save_screenshot(driver, "ho6_dropdown_pass.png")
        except Exception as e:
            print(f"  ⚠️ Dropdown: {e}")

        print("  ✅ HO6 complete")
    except Exception as e:
        print(f"  ⚠️ HO6 error: {e}")
        save_screenshot(driver, "ho6_error.png")
    finally:
        driver.quit()


# ============================================================
# HO7 — Page Object Model Screenshots
# ============================================================
def capture_ho7():
    print("\n📸 Capturing HO7 screenshots...")
    driver = get_driver()
    try:
        wait = WebDriverWait(driver, 20)

        # Screenshot 1: POM Simple Form
        driver.get(BASE_URL + "simple-form-demo/")
        time.sleep(3)
        close_overlays(driver)

        # Wait for page to fully load then find input
        try:
            inp = wait.until(EC.element_to_be_clickable((By.ID, "user-message")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", inp)
            time.sleep(0.5)
            inp.click()
            time.sleep(0.3)
            inp.clear()
            inp.send_keys("POM Test")
            time.sleep(0.5)

            submit = wait.until(EC.element_to_be_clickable((By.ID, "showInput")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit)
            time.sleep(0.3)
            driver.execute_script("arguments[0].click();", submit)
            time.sleep(2)

            save_screenshot(driver, "ho7_pom_simple_form.png")
        except Exception as e:
            print(f"  ⚠️ Simple form: {e}")
            save_screenshot(driver, "ho7_pom_simple_form.png")

        # Screenshot 2: POM Checkbox
        driver.get(BASE_URL + "checkbox-demo/")
        time.sleep(2)
        close_overlays(driver)

        try:
            cb = wait.until(EC.element_to_be_clickable((By.ID, "isAgeSelected")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", cb)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", cb)
            time.sleep(1)
            save_screenshot(driver, "ho7_pom_checkbox.png")
        except Exception as e:
            print(f"  ⚠️ Checkbox: {e}")

        # Screenshot 3: POM Dropdown
        driver.get(BASE_URL + "select-dropdown-demo/")
        time.sleep(2)
        close_overlays(driver)

        try:
            dropdown_el = wait.until(
                EC.element_to_be_clickable((By.ID, "select-demo"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", dropdown_el)
            time.sleep(0.5)
            select = Select(dropdown_el)
            select.select_by_visible_text("Wednesday")
            time.sleep(1)
            save_screenshot(driver, "ho7_pom_dropdown.png")
        except Exception as e:
            print(f"  ⚠️ Dropdown: {e}")

        # Screenshot 4: Input Form
        driver.get(BASE_URL + "input-form-demo/")
        time.sleep(3)
        close_overlays(driver)
        save_screenshot(driver, "ho7_pom_input_form.png")

        print("  ✅ HO7 complete")
    except Exception as e:
        print(f"  ⚠️ HO7 error: {e}")
        save_screenshot(driver, "ho7_error.png")
    finally:
        driver.quit()


# ============================================================
# Run all captures
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Capturing screenshots for Module 4 outputs...")
    print("=" * 60)

    capture_ho4()
    capture_ho5()
    capture_ho6()
    capture_ho7()

    print("\n" + "=" * 60)
    print("✅ All output screenshots saved!")
    print(f"📁 Location: automation_scripts/{OUTPUT_FOLDER}/")
    print("=" * 60)