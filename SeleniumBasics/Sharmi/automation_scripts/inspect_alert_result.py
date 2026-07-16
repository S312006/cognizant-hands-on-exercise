"""
Inspector - click 'Get Random User' on Dynamic Data Loading and print
every element that appears afterward, so we know the real structure
for FluentWait to poll against.
"""

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://www.lambdatest.com/selenium-playground/"


def inspect_dynamic_loading_result():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(URL)

    link = driver.find_element(By.LINK_TEXT, "Dynamic Data Loading")
    driver.execute_script("arguments[0].click();", link)

    button = driver.find_element(By.ID, "save")
    driver.execute_script("arguments[0].click();", button)

    time.sleep(3)  # one-off inspection only, real script will use FluentWait

    # print the container the button lives in, and anything that looks
    # like a result (paragraph, div, span with actual text)
    candidates = driver.find_elements(By.XPATH, "//p | //div[string-length(text()) > 0] | //span[string-length(text()) > 0]")
    print(f"\n--- {len(candidates)} candidate result elements found ---")
    for el in candidates[:30]:  # cap output
        text = el.text.strip()
        if text:
            print(f"tag='{el.tag_name}' | id='{el.get_attribute('id')}' | class='{el.get_attribute('class')}' | text='{text}'")

    driver.quit()


if __name__ == "__main__":
    inspect_dynamic_loading_result()