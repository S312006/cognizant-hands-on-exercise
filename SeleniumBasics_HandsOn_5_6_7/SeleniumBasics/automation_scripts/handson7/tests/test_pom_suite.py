"""
Hands-On 7 [Advanced]
Page Object Model - full suite refactored so test files contain ONLY
assertions (what should happen); all interactions (how to make it happen)
live in the pages/ classes. Zero driver.find_element calls below.

Run with:
    pytest tests/ -v --html=report.html --self-contained-html
"""

import sys
from pathlib import Path

import pytest

# Allow `from pages...` imports when running pytest from the handson7/ folder
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pages.checkbox_page import CheckboxPage
from pages.dropdown_page import DropdownPage
from pages.input_form_page import InputFormPage
from pages.simple_form_page import SimpleFormPage


@pytest.mark.parametrize("message", ["Hello Selenium", "POM Refactor", "12345"])
def test_simple_form_submission(driver, base_url, message):
    page = SimpleFormPage(driver)
    page.navigate_to(base_url)
    page.open_from_home()
    page.enter_message(message)
    page.click_submit()

    assert page.get_displayed_message() == message


def test_checkbox_demo(driver, base_url):
    page = CheckboxPage(driver)
    page.navigate_to(base_url)
    page.open_from_home()

    page.check_option(1)
    assert page.is_option_checked(1) is True

    page.uncheck_option(1)
    assert page.is_option_checked(1) is False


def test_dropdown_selection(driver, base_url):
    page = DropdownPage(driver)
    page.navigate_to(base_url)
    page.open_from_home()

    page.select_day("Wednesday")
    assert page.get_selected_day() == "Wednesday"


def test_input_form_submit(driver, base_url):
    page = InputFormPage(driver)
    page.navigate_to(base_url)
    page.open_from_home()

    page.fill_form(
        name="Jane Doe",
        email="jane.doe@example.com",
        phone="9876543210",
        address="221B Baker Street",
    )
    page.submit_form()

    assert "success" in page.get_success_message().lower()


# ---------------------------------------------------------------------------
# Step 59: Why POM matters - the maintenance argument
# ---------------------------------------------------------------------------
#
# Suppose the Submit button's ID changes from 'submit' to 'btn-submit'.
#
# In a FLAT script, driver.find_element(By.ID, 'submit') is likely copy-
# pasted into every test that submits a form: test_simple_form_submission,
# test_input_form_submit, any regression test that touches a form, etc.
# The change breaks all of them simultaneously, and fixing it means
# grep-ing through every test file, updating N occurrences, and re-running
# the whole suite to make sure none were missed.
#
# With POM, the locator exists in exactly ONE place: the SUBMIT_BUTTON
# class-level tuple inside the relevant page class (e.g. SimpleFormPage).
# Updating that single tuple fixes every test that calls page.click_submit()
# or page.submit_form(), because the test files never reference the raw
# locator at all - they only call the page's methods. One line changes,
# the whole suite is green again.
