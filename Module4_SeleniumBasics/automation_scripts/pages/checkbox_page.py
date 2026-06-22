# ============================================================
# CheckboxPage — Page Object for Checkbox Demo
# File: pages/checkbox_page.py
# ============================================================

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckboxPage(BasePage):
    """Page Object for LambdaTest Checkbox Demo."""

    SINGLE_CHECKBOX = (
        By.XPATH,
        "//label[contains(.,'Click on check box')]/input"
    )

    def _get_checkbox(self):
        return self.wait_for_element(self.SINGLE_CHECKBOX)

    def click_checkbox(self):
        checkbox = self._get_checkbox()

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            checkbox
        )

        self.driver.execute_script(
            "arguments[0].click();",
            checkbox
        )

    def is_checked(self):
        return self._get_checkbox().is_selected()

    def ensure_unchecked(self):
        if self.is_checked():
            self.click_checkbox()

    def ensure_checked(self):
        if not self.is_checked():
            self.click_checkbox()