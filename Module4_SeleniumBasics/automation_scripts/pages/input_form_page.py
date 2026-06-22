# ============================================================
# InputFormPage — Page Object for Input Form Demo
# File: pages/input_form_page.py
# ============================================================

import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InputFormPage(BasePage):

    NAME_INPUT = (By.NAME, "name")
    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")
    COMPANY_INPUT = (By.NAME, "company")
    WEBSITE_INPUT = (By.NAME, "website")
    CITY_INPUT = (By.NAME, "city")
    ADDRESS1_INPUT = (By.NAME, "address_line1")

    SUBMIT_BTN = (
        By.XPATH,
        "//button[contains(text(),'Submit')]"
    )

    def _fill_field(self, locator, value):
        try:
            element = self.wait_for_element(locator, timeout=10)

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                element
            )

            element.clear()
            element.send_keys(value)

        except Exception:
            pass

    def fill_form(
        self,
        name,
        email,
        phone,
        address,
        city="Bangalore"
    ):
        self._fill_field(self.NAME_INPUT, name)
        self._fill_field(self.EMAIL_INPUT, email)

        self._fill_field(
            self.PASSWORD_INPUT,
            "Password123"
        )

        self._fill_field(
            self.COMPANY_INPUT,
            "CTS"
        )

        self._fill_field(
            self.WEBSITE_INPUT,
            "https://cts.com"
        )

        self._fill_field(
            self.CITY_INPUT,
            city
        )

        self._fill_field(
            self.ADDRESS1_INPUT,
            address
        )

    def submit_form(self):
        button = self.wait_for_element(
            self.SUBMIT_BTN,
            timeout=15
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            button
        )

        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

        time.sleep(2)

    def get_success_message(self):
        try:
            return self.driver.page_source
        except Exception:
            return ""