from selenium.webdriver.common.by import By

from .base_page import BasePage


class InputFormPage(BasePage):
    INPUT_FORM_LINK = (By.LINK_TEXT, "Input Form Submit")
    NAME_INPUT = (By.NAME, "name")
    EMAIL_INPUT = (By.NAME, "email")
    PHONE_INPUT = (By.CSS_SELECTOR, "input[placeholder='Phone']")
    ADDRESS_INPUT = (By.NAME, "message")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success-msg, .alert-success")

    def open_from_home(self):
        self.wait_for_clickable(self.INPUT_FORM_LINK).click()

    def fill_form(self, name, email, phone, address):
        self.wait_for_element(self.NAME_INPUT).send_keys(name)
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(*self.PHONE_INPUT).send_keys(phone)
        self.driver.find_element(*self.ADDRESS_INPUT).send_keys(address)

    def submit_form(self):
        self.wait_for_clickable(self.SUBMIT_BUTTON).click()

    def get_success_message(self):
        return self.wait_for_element(self.SUCCESS_MESSAGE).text
