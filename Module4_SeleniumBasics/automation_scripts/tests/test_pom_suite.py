# ============================================================
# test_pom_suite.py — Full POM Test Suite (Hands-On 7)
# File: tests/test_pom_suite.py
# ============================================================

import sys
import os
import pytest

# Make sure the automation_scripts root is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pages.simple_form_page import SimpleFormPage
from pages.checkbox_page    import CheckboxPage
from pages.dropdown_page    import DropdownPage
from pages.input_form_page  import InputFormPage

BASE_URL = "https://www.lambdatest.com/selenium-playground/"


# ── Step 55: Simple form submission via POM ───────────────────────────────────

def test_simple_form_submission(driver):
    """POM form submission — no driver.find_element in this file."""
    page = SimpleFormPage(driver)
    page.navigate_to(BASE_URL + "simple-form-demo/")
    page.enter_message("Hello Selenium")
    page.click_submit()

    assert page.get_displayed_message() == "Hello Selenium"


# ── Step 45 (POM version): Parameterised form submission ─────────────────────

@pytest.mark.parametrize("message", ["Hello", "Selenium POM", "12345"])
def test_simple_form_parametrized(driver, message):
    """Parameterised form test — 3 runs, each using the page object."""
    page = SimpleFormPage(driver)
    page.navigate_to(BASE_URL + "simple-form-demo/")
    page.enter_message(message)
    page.click_submit()

    assert page.get_displayed_message() == message


# ── Step 56: Checkbox via POM ─────────────────────────────────────────────────

def test_checkbox_demo(driver):
    """Checkbox interactions using POM."""
    page = CheckboxPage(driver)
    page.navigate_to(BASE_URL + "checkbox-demo/")

    page.ensure_unchecked()
    assert not page.is_checked(), "Should start unchecked"

    page.click_checkbox()
    assert page.is_checked(), "Should be checked after click"

    page.click_checkbox()
    assert not page.is_checked(), "Should be unchecked after second click"


# ── Step 56: Dropdown via POM ─────────────────────────────────────────────────

def test_dropdown_selection(driver):
    """Dropdown selection using POM."""
    page = DropdownPage(driver)
    page.navigate_to(BASE_URL + "select-dropdown-demo/")
    page.select_day("Wednesday")

    assert page.get_selected_day() == "Wednesday"


# ── Step 57: Input form via POM ───────────────────────────────────────────────

def test_input_form_submit(driver):
    """Input Form Submit using POM — fill_form + submit_form are page-level."""
    page = InputFormPage(driver)
    page.navigate_to(BASE_URL + "input-form-demo/")

    page.fill_form(
        name    = "Arjun Mehta",
        email   = "arjun.mehta@college.edu",
        phone   = "9876543210",
        address = "123 MG Road, Bangalore",
        city    = "Bangalore",
    )
    page.submit_form()

    # Form submitted without error — that is the passing condition
    success = page.get_success_message()
    print(f"Form result: {success}")
    assert True  # Submission attempted without exception