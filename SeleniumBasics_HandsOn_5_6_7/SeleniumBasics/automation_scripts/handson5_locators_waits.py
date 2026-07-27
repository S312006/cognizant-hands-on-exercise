"""
Hands-On 5 [Intermediate]
Locators - ID, Name, XPath, CSS Selectors & Explicit Waits
Target: https://www.lambdatest.com/selenium-playground/

Task 1: Locator Strategies - From Simple to Robust
Task 2: WebDriverWait and Expected Conditions
"""

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.lambdatest.com/selenium-playground/"


def get_driver(headless: bool = False):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


# ---------------------------------------------------------------------------
# Task 1: Locator Strategies - From Simple to Robust
# ---------------------------------------------------------------------------
def task1_locator_strategies():
    """
    Steps 32-35: locate the message input on the Simple Form Demo page using
    every major locator strategy, then locate checkbox labels with XPath
    text()/contains().
    """
    driver = get_driver()
    try:
        driver.get(BASE_URL)

        # Navigate to the Simple Form Demo page
        driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "user-message")))

        # --- Step 32: locate the same element 6 different ways -------------
        by_id = driver.find_element(By.ID, "user-message")
        by_name = driver.find_element(By.NAME, "message")
        by_class = driver.find_element(By.CLASS_NAME, "form-control")
        by_tag = driver.find_element(By.TAG_NAME, "textarea")
        # Absolute XPath - fragile, breaks if any ancestor tag changes
        by_xpath_absolute = driver.find_element(
            By.XPATH,
            "/html/body/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/textarea",
        )
        # Relative XPath using attributes - much more robust
        by_xpath_relative = driver.find_element(By.XPATH, "//textarea[@id='user-message']")

        for label, el in [
            ("By.ID", by_id),
            ("By.NAME", by_name),
            ("By.CLASS_NAME", by_class),
            ("By.TAG_NAME", by_tag),
            ("By.XPATH (absolute)", by_xpath_absolute),
            ("By.XPATH (relative)", by_xpath_relative),
        ]:
            print(f"{label:25s} -> found tag <{el.tag_name}>")

        # --- Step 33: three CSS selectors for the same element -------------
        css_by_id = driver.find_element(By.CSS_SELECTOR, "#user-message")
        css_by_attr = driver.find_element(By.CSS_SELECTOR, "[name='message']")
        css_by_parent_child = driver.find_element(By.CSS_SELECTOR, "div.form-group > textarea")
        assert css_by_id == css_by_attr == css_by_parent_child, "CSS selectors point to different elements!"
        print("All 3 CSS selectors resolved to the same <textarea> element.")

        # --- Step 34: Checkbox Demo, XPath text() and contains() -----------
        driver.get(BASE_URL)
        driver.find_element(By.LINK_TEXT, "Checkbox Demo").click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Option 1']")))

        first_option = driver.find_element(By.XPATH, "//label[text()='Option 1']")
        print("Exact text() match:", first_option.text)

        all_options = driver.find_elements(By.XPATH, "//label[contains(text(),'Option')]")
        print(f"contains() found {len(all_options)} labels:")
        for opt in all_options:
            print("  -", opt.text)

        # --- Step 35: ranking (documented as comments, see below) ----------

    finally:
        driver.quit()


# Step 35 ranking - most to least preferred for maintainable automation:
#
# 1. By.ID            - unique per page, fastest lookup, immune to layout
#                        changes. Use whenever the app assigns stable IDs.
# 2. By.NAME           - almost as reliable as ID; common on form inputs.
# 3. By.CSS_SELECTOR   - flexible, fast, readable; can target attributes,
#                        classes, and structure without walking the DOM tree
#                        like XPath does.
# 4. By.XPATH (relative, attribute-based) - needed when CSS can't express
#                        the condition, e.g. matching visible text or
#                        walking up to a parent/ancestor.
# 5. By.CLASS_NAME / By.TAG_NAME - rarely unique on their own (many elements
#                        share a class or tag), so they're brittle unless
#                        combined with other conditions.
# 6. By.XPATH (absolute path) - LEAST preferred. Tied to exact DOM
#                        structure; any inserted <div> anywhere upstream
#                        breaks every absolute XPath in the suite.


# ---------------------------------------------------------------------------
# Task 2: WebDriverWait and Expected Conditions
# ---------------------------------------------------------------------------
def task2_explicit_wait_success_alert():
    """Step 36: wait for the Bootstrap success alert instead of sleeping."""
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        driver.find_element(By.LINK_TEXT, "Bootstrap Alerts").click()

        driver.find_element(By.ID, "success-alert").click()

        wait = WebDriverWait(driver, 10)
        alert = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#successAlert.alert-success")))
        assert "successfully" in alert.text.lower(), f"Unexpected alert text: {alert.text}"
        print("Success alert text:", alert.text)
    finally:
        driver.quit()


def task2_sleep_vs_explicit_wait_timing():
    """
    Step 37: compare time.sleep(3) vs WebDriverWait for the same interaction.
    Explicit waits return as soon as the condition is true (often faster),
    and they retry instead of failing outright on slow page loads (more
    reliable) - a fixed sleep is neither adaptive nor a guarantee.
    """
    # --- version A: hard-coded sleep ---
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        driver.find_element(By.LINK_TEXT, "Bootstrap Alerts").click()
        start = time.time()
        driver.find_element(By.ID, "success-alert").click()
        time.sleep(3)  # BAD: always waits the full 3s, even if alert appears in 200ms
        alert = driver.find_element(By.CSS_SELECTOR, "#successAlert.alert-success")
        assert alert.is_displayed()
        sleep_duration = time.time() - start
        print(f"time.sleep(3) version took {sleep_duration:.2f}s")
    finally:
        driver.quit()

    # --- version B: explicit wait ---
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        driver.find_element(By.LINK_TEXT, "Bootstrap Alerts").click()
        start = time.time()
        driver.find_element(By.ID, "success-alert").click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#successAlert.alert-success"))
        )
        wait_duration = time.time() - start
        print(f"WebDriverWait version took {wait_duration:.2f}s")
    finally:
        driver.quit()

    # On a fast machine the explicit-wait version finishes as soon as the
    # alert renders (often under a second), while the sleep() version always
    # burns the full 3 seconds. On a slow/loaded machine, a fixed sleep(3)
    # might not even be long enough, causing a flaky failure, whereas
    # WebDriverWait keeps polling up to its timeout.


def task2_wait_for_clickable():
    """
    Step 38: wait for a button to be clickable before clicking.

    visibility_of_element_located only checks that the element is present
    in the DOM and has non-zero size/display - it says nothing about
    whether it's enabled or covered by another element.

    element_to_be_clickable additionally checks the element is enabled and
    not obscured, so a click sent immediately after won't raise
    ElementClickInterceptedException or ElementNotInteractableException.
    """
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        driver.find_element(By.LINK_TEXT, "Bootstrap Alerts").click()

        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "success-alert"))
        )
        button.click()
        print("Clicked success-alert button safely after element_to_be_clickable.")
    finally:
        driver.quit()


def task2_fluent_wait_dynamic_table():
    """
    Step 39: FluentWait equivalent - poll every 500ms, timeout after 10s,
    and ignore NoSuchElementException while polling for a dynamically
    loaded table row.
    """
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        driver.find_element(By.LINK_TEXT, "Table Sort").click()

        fluent_wait = WebDriverWait(
            driver,
            timeout=10,
            poll_frequency=0.5,
            ignored_exceptions=[NoSuchElementException],
        )
        first_row = fluent_wait.until(
            lambda d: d.find_element(By.CSS_SELECTOR, "table#product-list-sorting tbody tr")
        )
        print("First table row loaded:", first_row.text[:60])
    finally:
        driver.quit()


if __name__ == "__main__":
    task1_locator_strategies()
    task2_explicit_wait_success_alert()
    task2_sleep_vs_explicit_wait_timing()
    task2_wait_for_clickable()
    task2_fluent_wait_dynamic_table()
