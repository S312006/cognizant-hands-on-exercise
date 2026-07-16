"""
Hands-On 5, Task 2: WebDriverWait and Expected Conditions
Name: Sharmi | Register No: 2117230020206 | Program: Digital Nurture 5.0

Steps 36-39: replace time.sleep() with explicit waits, compare timing,
wait for clickability, and demonstrate FluentWait polling.
"""

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://www.lambdatest.com/selenium-playground/"


def bootstrap_alert_explicit_wait():
    """Step 36: click 'Success Message' button, wait for the alert with
    WebDriverWait + visibility_of_element_located, assert its text."""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)

    driver.get(URL)
    driver.find_element(By.LINK_TEXT, "Bootstrap Alerts").click()

    driver.find_element(By.ID, "success-alert").click()

    success_alert = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
    )
    assert "successfully" in success_alert.text, "Alert should mention 'successfully'"
    print("Alert text:", success_alert.text)

    driver.quit()


def compare_sleep_vs_explicit_wait():
    """
    Step 37: same test written two ways, timed.

    time.sleep(3) ALWAYS blocks for the full 3 seconds no matter how
    fast the element actually appears - wasted time on a fast machine,
    and still not long enough if a slow machine needs more (the test
    just fails outright instead of adapting). WebDriverWait polls
    repeatedly and returns the instant the condition is met, so it's
    typically faster here, and would also be the more reliable choice
    if the page ever took longer than 3 seconds to respond.
    """
    # --- version with time.sleep(3) ---
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(URL)
    driver.find_element(By.LINK_TEXT, "Bootstrap Alerts").click()

    start_sleep = time.time()
    driver.find_element(By.ID, "success-alert").click()
    time.sleep(3)
    alert = driver.find_element(By.CSS_SELECTOR, ".alert-success")
    assert alert.is_displayed()
    sleep_duration = time.time() - start_sleep
    print(f"time.sleep(3) version took: {sleep_duration:.2f}s")
    driver.quit()

    # --- version with WebDriverWait ---
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(URL)
    driver.find_element(By.LINK_TEXT, "Bootstrap Alerts").click()

    start_wait = time.time()
    driver.find_element(By.ID, "success-alert").click()
    alert = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
    )
    wait_duration = time.time() - start_wait
    print(f"WebDriverWait version took: {wait_duration:.2f}s")
    driver.quit()

    print(
        f"\nDifference: sleep version was {sleep_duration - wait_duration:.2f}s slower "
        f"(it waited the full 3s regardless of when the alert actually appeared)."
    )


def element_to_be_clickable_demo():
    """
    Step 38: wait for the button to be clickable before clicking.

    - visibility_of_element_located: element exists in the DOM AND has
      a height/width > 0 (it's visible on screen). It could still be
      disabled, or covered by another element (e.g. a loading spinner
      on top of it), and this condition would still pass.
    - element_to_be_clickable: everything visibility_of_element_located
      checks, PLUS the element is enabled AND not obscured by anything
      else - i.e. a real click would actually land on it. This is the
      right condition to wait for immediately before any .click() call.
    """
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(URL)
    driver.find_element(By.LINK_TEXT, "Bootstrap Alerts").click()

    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "success-alert"))
    )
    button.click()
    print("Clicked button once it was confirmed clickable.")

    driver.quit()


def fluent_wait_demo():
    """
    Step 39: FluentWait - poll every 500ms, timeout after 10s, ignore
    NoSuchElementException while polling. Applied to a dynamically
    loaded table row on the Dynamic Data Loading page.
    """
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(URL)
    driver.find_element(By.LINK_TEXT, "Dynamic Data Loading").click()

    fluent_wait = WebDriverWait(
        driver,
        timeout=10,
        poll_frequency=0.5,
        ignored_exceptions=[NoSuchElementException],
    )

    driver.find_element(By.ID, "populate").click()

    row = fluent_wait.until(
        lambda d: d.find_element(By.CSS_SELECTOR, "#tableDynamic tbody tr")
    )
    print("Dynamically loaded row found:", row.text)

    driver.quit()


if __name__ == "__main__":
    print("--- Bootstrap Alert: explicit wait ---")
    bootstrap_alert_explicit_wait()

    print("\n--- sleep() vs WebDriverWait timing comparison ---")
    compare_sleep_vs_explicit_wait()

    print("\n--- element_to_be_clickable demo ---")
    element_to_be_clickable_demo()

    print("\n--- FluentWait demo ---")
    fluent_wait_demo()
