"""
Hands-On 6 [Advanced]
conftest.py - shared fixtures for the pytest Selenium suite.
"""

import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "failure_screenshots")


# Step 48: session-scoped base_url constant, reused by every test instead of
# hardcoding the URL in each test function.
@pytest.fixture(scope="session")
def base_url():
    return "https://www.lambdatest.com/selenium-playground/"


# Step 41: function-scoped driver fixture.
# scope='function' -> a brand-new browser instance per test, so tests are
# fully isolated from one another. scope='session' would reuse a single
# browser for the whole run (faster, but state can leak between tests).
@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless=new")  # uncomment for CI runs
    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    drv.implicitly_wait(5)

    yield drv  # -------- setup happens above, teardown happens below --------

    drv.quit()


# Step 46: capture a screenshot whenever a test fails.
# pytest_runtest_makereport is a hook that runs after each test phase
# (setup/call/teardown); we only care about the "call" phase failing.
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver_fixture = item.funcargs.get("driver")
        if driver_fixture is not None:
            os.makedirs(SCREENSHOT_DIR, exist_ok=True)
            test_name = item.name.replace(os.sep, "_")
            screenshot_path = os.path.join(SCREENSHOT_DIR, f"{test_name}_failure.png")
            driver_fixture.save_screenshot(screenshot_path)
            print(f"\nScreenshot saved on failure: {screenshot_path}")
