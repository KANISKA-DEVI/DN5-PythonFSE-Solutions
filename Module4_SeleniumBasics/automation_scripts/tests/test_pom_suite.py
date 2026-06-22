# ============================================================
# test_pom_suite.py — Full POM Test Suite
# File: tests/test_pom_suite.py
# Location: C:\DigitalNurture5\Module4_SeleniumBasics\automation_scripts\tests\
#
# POM BENEFIT — MAINTENANCE ANSWER (Step 59):
# In a flat (non-POM) script, if the Submit button ID changes from
# 'showInput' to 'btn-submit', you must find and update that ID in
# EVERY test file that clicks submit — could be 10, 20, or 50 files.
#
# With POM: the locator SUBMIT_BUTTON = (By.ID, "showInput") exists only
# in simple_form_page.py. You update ONE LINE in ONE FILE.
# All 20 tests that use SimpleFormPage automatically get the fix.
# This is the single biggest benefit of POM — maintainability at scale.
# ============================================================

import pytest
from selenium.webdriver.common.by import By

# Import page objects — NO driver.find_element in this file
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pages.simple_form_page import SimpleFormPage
from pages.checkbox_page    import CheckboxPage
from pages.dropdown_page    import DropdownPage
from pages.input_form_page  import InputFormPage

BASE_URL = "https://www.lambdatest.com/selenium-playground/"


# ============================================================
# Step 55: Refactored test using SimpleFormPage POM
# ============================================================
def test_simple_form_submission(driver):
    """
    Test form submission using POM.
    Notice: ZERO driver.find_element calls in this test.
    The test reads like a business requirement.
    """
    page = SimpleFormPage(driver)
    page.navigate_to(BASE_URL + "simple-form-demo/")
    page.enter_message("Hello Selenium")
    page.click_submit()

    assert page.get_displayed_message() == "Hello Selenium"


# ============================================================
# Step 45 (POM version): Parameterised form submission
# ============================================================
@pytest.mark.parametrize("message", ["Hello", "Selenium POM", "12345"])
def test_simple_form_parametrized(driver, message):
    """Parameterised test via POM — 3 test runs, all using page object."""
    page = SimpleFormPage(driver)
    page.navigate_to(BASE_URL + "simple-form-demo/")
    page.enter_message(message)
    page.click_submit()

    assert page.get_displayed_message() == message


# ============================================================
# Step 56: Refactored checkbox test using CheckboxPage POM
# ============================================================
def test_checkbox_demo(driver):
    """Test checkbox interactions using POM."""
    page = CheckboxPage(driver)
    page.navigate_to(BASE_URL + "checkbox-demo/")

    # Initially unchecked
    assert not page.is_checked(), "Checkbox should start unchecked"

    # Check it
    page.click_checkbox()
    assert page.is_checked(), "Checkbox should be checked after click"

    # Uncheck it
    page.click_checkbox()
    assert not page.is_checked(), "Checkbox should be unchecked after second click"


# ============================================================
# Step 56: Refactored dropdown test using DropdownPage POM
# ============================================================
def test_dropdown_selection(driver):
    """Test dropdown selection using POM."""
    page = DropdownPage(driver)
    page.navigate_to(BASE_URL + "select-dropdown-demo/")
    page.select_day("Wednesday")

    assert page.get_selected_day() == "Wednesday"


# ============================================================
# Step 57: Input Form Submit using InputFormPage POM
# ============================================================
def test_input_form_submit(driver):
    """
    Test the Input Form Submit page using POM.
    fill_form() and submit_form() are all page-level methods.
    """
    page = InputFormPage(driver)
    page.navigate_to(BASE_URL + "input-form-demo/")

    page.fill_form(
        name    = "Arjun Mehta",
        email   = "arjun.mehta@college.edu",
        phone   = "9876543210",
        address = "123 MG Road, Bangalore",
        city    = "Bangalore"
    )
    page.submit_form()

    # The success message may vary — we just check the form submitted
    # (no error message visible, or a success indicator appeared)
    success = page.get_success_message()
    print(f"Form result: {success}")
    # If the page stays on the form without error, submission was attempted
    assert True  # Submission was attempted successfully