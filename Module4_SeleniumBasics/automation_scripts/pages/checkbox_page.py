# ============================================================
# CheckboxPage — Page Object for Checkbox Demo
# File: pages/checkbox_page.py
# ============================================================

import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckboxPage(BasePage):

    # Use XPath to find any checkbox — ID may vary on LambdaTest
    SINGLE_CHECKBOX = (By.XPATH, "//input[@type='checkbox']")

    def click_checkbox(self):
        """Click the checkbox via JavaScript."""
        self.wait_for_element(self.SINGLE_CHECKBOX)
        self.js_click(self.SINGLE_CHECKBOX)
        time.sleep(1)

    def check_option(self):
        """Check the checkbox if not already checked."""
        if not self.is_checked():
            self.click_checkbox()

    def uncheck_option(self):
        """Uncheck the checkbox if currently checked."""
        if self.is_checked():
            self.click_checkbox()

    def is_checked(self) -> bool:
        """Return True if the checkbox is currently selected."""
        self.wait_for_element(self.SINGLE_CHECKBOX)
        return self.js_is_checked(self.SINGLE_CHECKBOX)