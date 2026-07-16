"""
Task 1: Selenium Architecture and Environment Setup
-----------------------------------------------------
SELENIUM ARCHITECTURE - 3 main components:

1. WebDriver:
   The core component that directly communicates with the browser.
   Each browser (Chrome, Firefox, Edge) has its own driver executable
   (e.g. chromedriver.exe) that WebDriver talks to using the W3C
   WebDriver protocol (HTTP requests under the hood). Selenium sends
   commands like "click this element" or "navigate to this URL", and
   the driver translates them into real browser actions.

2. Selenium Grid:
   Solves the problem of running tests in PARALLEL across multiple
   machines and multiple browser/OS combinations at the same time.
   Instead of running 50 tests one after another on one machine
   (slow), Grid distributes them across several "node" machines,
   drastically cutting down total execution time. Useful for large
   regression suites that need to run on Chrome, Firefox, and Edge
   simultaneously.

3. Selenium IDE:
   A browser extension used for RECORD AND PLAYBACK. You literally
   click around the web page, and it records your actions as a
   script. It also supports exporting the recorded actions as code
   (e.g. Python + Selenium WebDriver code). Useful for quickly
   prototyping a test flow before writing/refining it as a proper
   script.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://www.lambdatest.com/selenium-playground/"


def basic_launch():
    """Task 1, Step 25: minimal script - open, print title, close."""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get(URL)
    print("Page title:", driver.title)

    driver.quit()


def launch_with_implicit_wait():
    """
    Task 1, Step 26: implicit wait.

    driver.implicitly_wait(10) tells WebDriver to poll the DOM for up
    to 10 seconds EVERY TIME it looks for ANY element, before throwing
    NoSuchElementException.

    WHY THIS IS CONSIDERED BAD PRACTICE vs explicit waits:
    - It applies globally to every find_element call for the entire
      driver session, even when you don't need to wait at all -
      this can silently slow down every single locator call.
    - It waits for the element to simply EXIST in the DOM, not for it
      to be visible, clickable, or otherwise actually usable - so
      tests can still fail right after the implicit wait succeeds.
    - Mixing implicit wait with explicit WebDriverWait causes
      unpredictable, inconsistent total wait times (they can stack).
    - Explicit waits (Hands-On 5) let you wait for a SPECIFIC
      condition (visible, clickable, text present) on a SPECIFIC
      element only when needed - more precise and less wasteful.
    """
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)

    driver.get(URL)
    print("Page title (with implicit wait):", driver.title)

    driver.quit()


def launch_headless():
    """Task 1, Step 27: run Chrome headless (no visible window)."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(URL)
    print("Page title (headless mode):", driver.title)
    assert driver.title != "", "Title should not be empty in headless mode"

    driver.quit()


if __name__ == "__main__":
    print("--- Basic launch ---")
    basic_launch()

    print("\n--- Launch with implicit wait ---")
    launch_with_implicit_wait()

    print("\n--- Headless launch ---")
    launch_headless()