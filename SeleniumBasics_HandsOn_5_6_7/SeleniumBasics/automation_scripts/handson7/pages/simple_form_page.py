from selenium.webdriver.common.by import By

from .base_page import BasePage


class SimpleFormPage(BasePage):
    # Locators as class-level tuples - update the ID here once if the app
    # changes, instead of hunting through every test file.
    SIMPLE_FORM_LINK = (By.LINK_TEXT, "Simple Form Demo")
    MESSAGE_INPUT = (By.ID, "user-message")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "#get-input .btn")
    DISPLAYED_MESSAGE = (By.ID, "message")

    def open_from_home(self):
        self.wait_for_clickable(self.SIMPLE_FORM_LINK).click()

    def enter_message(self, text):
        field = self.wait_for_element(self.MESSAGE_INPUT)
        field.clear()
        field.send_keys(text)

    def click_submit(self):
        self.wait_for_clickable(self.SUBMIT_BUTTON).click()

    def get_displayed_message(self):
        return self.wait_for_element(self.DISPLAYED_MESSAGE).text
