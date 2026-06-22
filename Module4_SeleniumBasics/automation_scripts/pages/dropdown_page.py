# ============================================================
# DropdownPage — Page Object for Select Dropdown Demo
# File: pages/dropdown_page.py
# ============================================================

import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class DropdownPage(BasePage):

    DROPDOWN = (By.ID, "select-demo")

    def select_day(self, day_name: str):
        """
        Select a day using JavaScript — avoids stale element issues
        with Selenium's Select class on re-rendering pages.
        """
        self.wait_for_element(self.DROPDOWN)
        # Use JS to set the dropdown value directly
        self.driver.execute_script(
            """
            var select = arguments[0];
            var options = select.options;
            for (var i = 0; i < options.length; i++) {
                if (options[i].text === arguments[1]) {
                    select.selectedIndex = i;
                    break;
                }
            }
            """,
            self.driver.find_element(*self.DROPDOWN),
            day_name
        )
        time.sleep(1)

    def get_selected_day(self) -> str:
        """Return the currently selected option text."""
        el = self.driver.find_element(*self.DROPDOWN)
        return self.driver.execute_script(
            "return arguments[0].options[arguments[0].selectedIndex].text;", el
        )