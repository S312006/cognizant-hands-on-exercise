from selenium.webdriver.common.by import By

from .base_page import BasePage


class CheckboxPage(BasePage):
    CHECKBOX_LINK = (By.LINK_TEXT, "Checkbox Demo")

    @staticmethod
    def _checkbox_locator(index):
        # Playground checkboxes are option1, option2, ... under #colorbox
        return (By.CSS_SELECTOR, f"#colorbox li:nth-child({index}) input[type='checkbox']")

    def open_from_home(self):
        self.wait_for_clickable(self.CHECKBOX_LINK).click()

    def check_option(self, index):
        box = self.wait_for_element(self._checkbox_locator(index))
        if not box.is_selected():
            box.click()

    def uncheck_option(self, index):
        box = self.wait_for_element(self._checkbox_locator(index))
        if box.is_selected():
            box.click()

    def is_option_checked(self, index):
        return self.wait_for_element(self._checkbox_locator(index)).is_selected()
