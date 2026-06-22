# ============================================================
# BasePage — common methods shared by all page objects
# File: pages/base_page.py
# ============================================================

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support    import expected_conditions as EC
from selenium.common.exceptions    import StaleElementReferenceException


class BasePage:
    """
    Base class for all Page Object classes.
    Contains common methods: navigate, get_title, wait_for_element.
    All page classes inherit from BasePage.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 15)

    def navigate_to(self, url: str):
        """Navigate the browser to a URL and wait for page to stabilize."""
        self.driver.get(url)
        time.sleep(3)  # Wait for LambdaTest ads/scripts to finish re-rendering

    def get_title(self) -> str:
        """Return the current page title."""
        return self.driver.title

    def wait_for_element(self, locator: tuple, timeout: int = 15):
        """
        Wait for an element to be present in DOM and return it.
        Uses presence_of_element_located (not visibility) to avoid
        issues with elements hidden behind overlays.
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_clickable(self, locator: tuple, timeout: int = 15):
        """Wait for an element to be clickable and return it."""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def js_set_value(self, locator: tuple, value: str):
        """
        Set input value via JavaScript — bypasses stale element issues.
        Re-finds the element each time so it never goes stale.
        """
        el = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].value = '';", el)
        self.driver.execute_script("arguments[0].value = arguments[1];", el, value)

    def js_click(self, locator: tuple):
        """
        Click element via JavaScript — bypasses overlay/stale issues.
        Re-finds the element each time.
        """
        el = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].click();", el)

    def js_get_text(self, locator: tuple) -> str:
        """Get element text via JavaScript — avoids stale reference."""
        try:
            el = self.driver.find_element(*locator)
            return self.driver.execute_script("return arguments[0].textContent;", el).strip()
        except Exception:
            return ""

    def js_is_checked(self, locator: tuple) -> bool:
        """Check checkbox state via JavaScript."""
        el = self.driver.find_element(*locator)
        return self.driver.execute_script("return arguments[0].checked;", el)