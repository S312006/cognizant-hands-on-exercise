from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from .base_page import BasePage


class DropdownPage(BasePage):
    DROPDOWN_LINK = (By.LINK_TEXT, "Select Dropdown List")
    DAY_DROPDOWN = (By.ID, "select-demo")

    def open_from_home(self):
        self.wait_for_clickable(self.DROPDOWN_LINK).click()

    def select_day(self, day_name):
        dropdown_el = self.wait_for_element(self.DAY_DROPDOWN)
        Select(dropdown_el).select_by_visible_text(day_name)

    def get_selected_day(self):
        dropdown_el = self.wait_for_element(self.DAY_DROPDOWN)
        return Select(dropdown_el).first_selected_option.text
