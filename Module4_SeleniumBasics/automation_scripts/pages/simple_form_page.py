# ============================================================
# SimpleFormPage — Page Object for Simple Form Demo
# File: pages/simple_form_page.py
# ============================================================

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SimpleFormPage(BasePage):
    """Page Object for .../selenium-playground/simple-form-demo/"""

    # Locators — single source of truth
    MESSAGE_INPUT = (By.ID, "user-message")
    SUBMIT_BUTTON = (By.ID, "showInput")
    DISPLAYED_MSG = (By.ID, "message")

    def enter_message(self, text: str):
        """Type a message into the input field."""
        el = self.wait_for_clickable(self.MESSAGE_INPUT)
        el.clear()
        el.send_keys(text)

    def click_submit(self):
        """Click the Submit button via JS to bypass any overlay."""
        self.js_click(self.SUBMIT_BUTTON)

    def get_displayed_message(self) -> str:
        """Return the text of the displayed message after submission."""
        return self.wait_for_element(self.DISPLAYED_MSG).text.strip()