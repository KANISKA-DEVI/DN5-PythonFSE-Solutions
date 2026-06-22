# ============================================================
# BasePage — common methods shared by all page objects
# File: pages/base_page.py
# ============================================================

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    """
    Base class for all Page Object classes.
    Contains shared helpers: navigate, wait, cookie dismissal.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def navigate_to(self, url: str):
        """Navigate to a URL and dismiss any cookie banner."""
        self.driver.get(url)

        self._dismiss_cookie_banner()

        # Remove floating chat widgets that may block elements
        try:
            self.driver.execute_script("""
                let widgets = document.querySelectorAll(
                    'iframe,[id*="chat"],[class*="chat"],[class*="widget"]'
                );
                widgets.forEach(el => el.remove());
            """)
        except Exception:
            pass

    def get_title(self) -> str:
        return self.driver.title

    def wait_for_element(self, locator: tuple, timeout: int = 15):
        """Wait for an element to be visible and return it."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator: tuple, timeout: int = 15):
        """Wait for an element to be clickable and return it."""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def js_click(self, locator: tuple, timeout: int = 15):
        """Wait for element then click via JavaScript."""
        element = self.wait_for_clickable(locator, timeout)

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

    def _dismiss_cookie_banner(self):
        """Silently dismiss any cookie-consent overlay if present."""
        try:
            button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//*[contains(translate(text(),'ACCEPT ALL','accept all'),'accept all') "
                        "or @id='cookie-accept' "
                        "or (contains(@class,'cookie') and @role='button')]"
                    )
                )
            )

            button.click()
            time.sleep(0.5)

        except Exception:
            pass