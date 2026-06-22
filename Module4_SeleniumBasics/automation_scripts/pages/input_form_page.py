# ============================================================
# InputFormPage — Page Object for Input Form Submit Demo
# File: pages/input_form_page.py
# ============================================================

import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InputFormPage(BasePage):

    NAME_INPUT    = (By.XPATH, "//input[@name='name']")
    EMAIL_INPUT   = (By.XPATH, "//input[@name='email']")
    PHONE_INPUT   = (By.XPATH, "//input[@name='phone']")
    ADDRESS_INPUT = (By.XPATH, "//input[@name='address']")
    CITY_INPUT    = (By.XPATH, "//input[@name='city']")
    SUBMIT_BTN    = (By.XPATH, "//button[@type='submit']")
    SUCCESS_MSG   = (By.XPATH, "//*[contains(text(),'Thanks') or contains(text(),'success') or contains(@class,'success')]")

    def fill_form(self, name: str, email: str, phone: str, address: str, city: str = "Chennai"):
        """Fill all form fields using JavaScript to avoid interactability issues."""
        self.wait_for_element(self.NAME_INPUT)
        time.sleep(1)  # Let form fully render

        self.js_set_value(self.NAME_INPUT, name)
        self.js_set_value(self.EMAIL_INPUT, email)
        self.js_set_value(self.PHONE_INPUT, phone)
        self.js_set_value(self.ADDRESS_INPUT, address)
        try:
            self.js_set_value(self.CITY_INPUT, city)
        except Exception:
            pass  # City field may not be present on all form variants

    def submit_form(self):
        """Click the Submit button via JavaScript."""
        self.js_click(self.SUBMIT_BTN)
        time.sleep(2)

    def get_success_message(self) -> str:
        """Return the success/confirmation message text after form submission."""
        try:
            return self.js_get_text(self.SUCCESS_MSG)
        except Exception:
            return ""