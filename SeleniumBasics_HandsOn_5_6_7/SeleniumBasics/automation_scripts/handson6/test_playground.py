"""
Hands-On 6 [Advanced]
Running Selenium Tests with pytest - Fixtures, Assertions & Reporting

Run with:
    pytest test_playground.py -v
    pytest test_playground.py --html=report.html --self-contained-html
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


# ---------------------------------------------------------------------------
# Step 45: parameterised form submission test - 3 separate runs generated.
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("message", ["Hello", "Selenium Automation", "12345"])
def test_simple_form_submission(driver, base_url, message):
    driver.get(base_url)
    driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()

    wait = WebDriverWait(driver, 10)
    message_input = wait.until(EC.presence_of_element_located((By.ID, "user-message")))
    message_input.clear()
    message_input.send_keys(message)

    driver.find_element(By.CSS_SELECTOR, "#get-input .btn").click()

    displayed = wait.until(EC.visibility_of_element_located((By.ID, "message")))
    assert displayed.text == message


# ---------------------------------------------------------------------------
# Step 43: checkbox interaction test.
# ---------------------------------------------------------------------------
def test_checkbox_demo(driver, base_url):
    driver.get(base_url)
    driver.find_element(By.LINK_TEXT, "Checkbox Demo").click()

    wait = WebDriverWait(driver, 10)
    checkbox = wait.until(EC.presence_of_element_located((By.ID, "isAgeSelected")))

    checkbox.click()
    assert checkbox.is_selected(), "Checkbox should be selected after first click"

    checkbox.click()
    assert not checkbox.is_selected(), "Checkbox should be deselected after second click"


# ---------------------------------------------------------------------------
# Step 49: dropdown selection test using the Select helper class.
# ---------------------------------------------------------------------------
def test_dropdown_selection(driver, base_url):
    driver.get(base_url)
    driver.find_element(By.LINK_TEXT, "Select Dropdown List").click()

    wait = WebDriverWait(driver, 10)
    dropdown_el = wait.until(EC.presence_of_element_located((By.ID, "select-demo")))

    select = Select(dropdown_el)
    select.select_by_visible_text("Wednesday")

    selected_option = select.first_selected_option
    assert selected_option.text == "Wednesday"


# ---------------------------------------------------------------------------
# A deliberately-failing example test, kept here only to demonstrate the
# screenshot-on-failure hook in conftest.py. Comment out / delete once
# you've confirmed the hook works.
# ---------------------------------------------------------------------------
@pytest.mark.skip(reason="Demo test for the screenshot-on-failure hook; unskip to verify manually")
def test_screenshot_on_failure_demo(driver, base_url):
    driver.get(base_url)
    assert driver.title == "This will not match, triggering a failure screenshot"
