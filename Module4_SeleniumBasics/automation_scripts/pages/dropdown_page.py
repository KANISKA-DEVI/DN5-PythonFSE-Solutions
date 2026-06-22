# ============================================================
# DropdownPage — Page Object for Select Dropdown Demo
# File: pages/dropdown_page.py
# ============================================================

from selenium.webdriver.common.by  import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class DropdownPage(BasePage):
    """Page Object for .../selenium-playground/select-dropdown-demo/"""

    DROPDOWN = (By.ID, "select-demo")

    def select_day(self, day_name: str):
        """Select a day from the dropdown by visible text."""
        el     = self.wait_for_element(self.DROPDOWN)
        select = Select(el)
        select.select_by_visible_text(day_name)

    def get_selected_day(self) -> str:
        """Return the currently selected option text."""
        el     = self.wait_for_element(self.DROPDOWN)
        select = Select(el)
        return select.first_selected_option.text.strip()