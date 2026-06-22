# ============================================================
# SimpleFormPage — Page Object for Simple Form Demo
# File: pages/simple_form_page.py
# ============================================================

import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SimpleFormPage(BasePage):

    MESSAGE_INPUT = (By.ID, "user-message")
    SUBMIT_BUTTON = (By.ID, "showInput")
    DISPLAYED_MSG = (By.ID, "message")

    def enter_message(self, text: str):
        """Type a message using JavaScript to avoid stale element issues."""
        self.wait_for_element(self.MESSAGE_INPUT)
        self.js_set_value(self.MESSAGE_INPUT, text)

    def click_submit(self):
        """Click submit via JavaScript to avoid overlay issues."""
        self.js_click(self.SUBMIT_BUTTON)
        time.sleep(1)

    def get_displayed_message(self) -> str:
        """Return the displayed message text after submission."""
        time.sleep(1)
        return self.js_get_text(self.DISPLAYED_MSG)