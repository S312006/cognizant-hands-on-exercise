"""
Task 2: WebDriver Navigation and Window Commands
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://www.lambdatest.com/selenium-playground/"


def navigation_and_windows():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)

    # Step 28: navigate to Simple Form Demo, assert URL, go back
    driver.get(URL)
    simple_form_link = driver.find_element("link text", "Simple Form Demo")
    simple_form_link.click()

    assert "simple-form-demo" in driver.current_url, "URL should contain 'simple-form-demo'"
    print("On Simple Form Demo page. Current URL:", driver.current_url)

    driver.back()
    print("Navigated back. Current URL:", driver.current_url)

    # Step 29: open a new tab, switch to it, print its title
    driver.execute_script('window.open("https://www.google.com");')
    print("Open window handles:", driver.window_handles)

    driver.switch_to.window(driver.window_handles[1])
    print("Switched to new tab. Title:", driver.title)

    # Step 30: switch back to original tab, take a screenshot
    driver.switch_to.window(driver.window_handles[0])
    print("Switched back to original tab. Title:", driver.title)

    driver.save_screenshot("playground_screenshot.png")
    print("Screenshot saved as playground_screenshot.png")

    # Step 31: window size
    # Consistent window size matters for responsive UI automation because
    # many pages change their layout (menus collapse into hamburger icons,
    # elements reflow) at different screen widths. If the window size is
    # not fixed, the same locator might find a different element - or no
    # element at all - depending on which layout loaded, making tests
    # unreliable across different machines or CI environments.
    size = driver.get_window_size()
    print("Current window size:", size)

    driver.set_window_size(1280, 800)
    new_size = driver.get_window_size()
    print("Window size after resize:", new_size)

    driver.quit()


if __name__ == "__main__":
    navigation_and_windows()