# ============================================================
# test_playground.py — pytest Test Suite for LambdaTest Playground
# File: test_playground.py
# Location: automation_scripts/test_playground.py
# ============================================================

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


# ── Helpers ───────────────────────────────────────────────────────────────────

def _dismiss_cookie_banner(driver):
    """Dismiss any cookie / consent overlay that blocks clicks."""
    try:
        btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//*[contains(translate(text(),'ACCEPT ALL','accept all'),'accept all') "
                 "or @id='cookie-accept' or contains(@class,'cookie') and @role='button']")
            )
        )
        btn.click()
        time.sleep(0.5)
    except Exception:
        pass  # No banner — carry on


# ── Task 1: Basic Tests ───────────────────────────────────────────────────────

def test_simple_form_submission(driver, base_url):
    """
    Step 42: Submit a message in the Simple Form Demo and verify it appears.
    """
    driver.get(base_url + "simple-form-demo/")
    _dismiss_cookie_banner(driver)
    wait = WebDriverWait(driver, 20)

    msg_input = wait.until(EC.element_to_be_clickable((By.ID, "user-message")))
    msg_input.clear()
    msg_input.send_keys("Hello Selenium")

    # The button id is 'showInput' on the LambdaTest playground
    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "showInput")))
    driver.execute_script("arguments[0].click();", submit_btn)

    displayed = wait.until(EC.visibility_of_element_located((By.ID, "message")))
    assert displayed.text.strip() == "Hello Selenium", \
        f"Expected 'Hello Selenium' but got '{displayed.text}'"


def test_checkbox_demo(driver, base_url):
    """
    Step 43: Check and uncheck the single checkbox; verify state each time.
    """
    driver.get(base_url + "checkbox-demo/")
    _dismiss_cookie_banner(driver)

    wait = WebDriverWait(driver, 20)

    # Try several possible locators because LambdaTest changes its HTML
    checkbox = None

    locators = [
        (By.ID, "isAgeSelected"),
        (By.CSS_SELECTOR, "input[type='checkbox']"),
        (By.XPATH, "(//input[@type='checkbox'])[1]"),
    ]

    for locator in locators:
        try:
            checkbox = wait.until(
                EC.presence_of_element_located(locator)
            )
            break
        except:
            pass

    assert checkbox is not None, "Could not find checkbox"

    # Ensure unchecked
    if checkbox.is_selected():
        driver.execute_script("arguments[0].click();", checkbox)

    assert not checkbox.is_selected()

    # Check
    driver.execute_script("arguments[0].click();", checkbox)
    assert checkbox.is_selected()

    # Uncheck
    driver.execute_script("arguments[0].click();", checkbox)
    assert not checkbox.is_selected()


# ── Task 2: Parameterised Tests ───────────────────────────────────────────────

@pytest.mark.parametrize("message", ["Hello", "Selenium Automation", "12345"])
def test_simple_form_submission_parametrized(driver, base_url, message):
    """
    Step 45: Run the simple-form test with 3 different input values.
    Each value creates a separate test entry in the report.
    """
    driver.get(base_url + "simple-form-demo/")
    _dismiss_cookie_banner(driver)
    wait = WebDriverWait(driver, 20)

    msg_input = wait.until(EC.element_to_be_clickable((By.ID, "user-message")))
    msg_input.clear()
    msg_input.send_keys(message)

    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "showInput")))
    driver.execute_script("arguments[0].click();", submit_btn)

    displayed = wait.until(EC.visibility_of_element_located((By.ID, "message")))
    assert displayed.text.strip() == message, \
        f"Expected '{message}' but got '{displayed.text}'"


def test_dropdown_selection(driver, base_url):
    """
    Step 49: Select 'Wednesday' from the Select Dropdown List and verify.
    """
    driver.get(base_url + "select-dropdown-demo/")
    _dismiss_cookie_banner(driver)
    wait = WebDriverWait(driver, 20)

    dropdown_el = wait.until(
        EC.presence_of_element_located((By.ID, "select-demo"))
    )
    dropdown = Select(dropdown_el)
    dropdown.select_by_visible_text("Wednesday")

    selected = dropdown.first_selected_option
    assert selected.text.strip() == "Wednesday", \
        f"Expected 'Wednesday' but got '{selected.text}'"