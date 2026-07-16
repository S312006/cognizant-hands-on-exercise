"""
Hands-On 5, Task 1: Locator Strategies - From Simple to Robust
Name: Sharmi | Register No: 2117230020206 | Program: Digital Nurture 5.0

Steps 32-35: practice all locator strategies against the LambdaTest
Selenium Playground, then rank them by maintainability.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://www.lambdatest.com/selenium-playground/"


def locator_strategies_simple_form():
    """
    Step 32-33: locate the message input on the Simple Form Demo page
    using every locator strategy, then 3 different CSS selectors for
    the same element.
    """
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)

    driver.get(URL)

    # A sticky nav header overlaps the link at some scroll positions,
    # which blocks a normal mouse click. Clicking via JavaScript
    # bypasses that overlap check entirely.
    simple_form_link = driver.find_element(By.LINK_TEXT, "Simple Form Demo")
    driver.execute_script("arguments[0].click();", simple_form_link)

    # --- Step 32: six locator strategies on the same element ---
    # (the message input's real id on the LambdaTest page is "user-message")

    by_id = driver.find_element(By.ID, "user-message")
    print("By.ID found:", by_id.tag_name)

    by_name = driver.find_element(By.NAME, "message")
    print("By.NAME found:", by_name.tag_name)

    by_class = driver.find_element(By.CLASS_NAME, "form-control")
    print("By.CLASS_NAME found:", by_class.tag_name)

    by_tag = driver.find_element(By.TAG_NAME, "input")
    print("By.TAG_NAME found:", by_tag.tag_name)

    # Absolute XPath - brittle, breaks if ANY ancestor element changes.
    # Instead of guessing the path by hand, compute it dynamically with
    # JavaScript so it always matches the real page structure.
    compute_xpath_script = """
    function getAbsoluteXPath(element) {
        if (element === document.body) { return '/html/' + element.tagName.toLowerCase(); }
        var ix = 0;
        var siblings = element.parentNode.childNodes;
        for (var i = 0; i < siblings.length; i++) {
            var sibling = siblings[i];
            if (sibling === element) {
                return getAbsoluteXPath(element.parentNode) + '/' + element.tagName.toLowerCase() + '[' + (ix + 1) + ']';
            }
            if (sibling.nodeType === 1 && sibling.tagName === element.tagName) { ix++; }
        }
    }
    return getAbsoluteXPath(arguments[0]);
    """
    absolute_xpath = driver.execute_script(compute_xpath_script, by_id)
    print("Computed absolute XPath:", absolute_xpath)

    by_xpath_absolute = driver.find_element(By.XPATH, absolute_xpath)
    print("By.XPATH (absolute) found:", by_xpath_absolute.tag_name)

    # Relative XPath using attributes - much more robust
    by_xpath_relative = driver.find_element(By.XPATH, "//input[@id='user-message']")
    print("By.XPATH (relative) found:", by_xpath_relative.tag_name)

    # --- Step 33: three CSS selectors for the same element ---
    css_by_id = driver.find_element(By.CSS_SELECTOR, "#user-message")
    css_by_attribute = driver.find_element(By.CSS_SELECTOR, "[name='message']")
    css_by_parent_child = driver.find_element(By.CSS_SELECTOR, "div > input#user-message")

    print("CSS by ID:", css_by_id.tag_name)
    print("CSS by attribute:", css_by_attribute.tag_name)
    print("CSS by parent > child:", css_by_parent_child.tag_name)

    driver.quit()


def locator_strategies_checkbox():
    """
    Step 34: Checkbox Demo page - XPath text() and contains() to find
    checkbox labels.
    """
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)

    driver.get(URL)

    checkbox_link = driver.find_element(By.LINK_TEXT, "Checkbox Demo")
    driver.execute_script("arguments[0].click();", checkbox_link)

    # exact text() match - fails if the label text changes even slightly
    option_1_label = driver.find_element(By.XPATH, "//label[text()='Option 1']")
    print("Exact text() match:", option_1_label.text)

    # contains() - matches any label containing the word "Option"
    all_option_labels = driver.find_elements(By.XPATH, "//label[contains(text(),'Option')]")
    print(f"contains() matched {len(all_option_labels)} labels:")
    for label in all_option_labels:
        print(" -", label.text)

    driver.quit()


# Step 35: Locator ranking, most to least preferred for maintainable automation
#
# 1. ID           - unique per page, fastest lookup, completely immune
#                    to layout/structure changes elsewhere on the page.
#                    Best choice whenever the element has one.
# 2. CSS_SELECTOR  - fast, readable, and flexible (id, attribute,
#                    parent > child). Nearly as good as ID; the default
#                    fallback whenever there's no usable id.
# 3. NAME          - usually stable on well-built forms, but not
#                    guaranteed unique (several inputs can share a name).
# 4. XPATH         - most powerful (text(), contains(), parent-axis
#                    traversal) but slower and more verbose than CSS.
#                      - Relative XPath (//input[@id='...']) is fine,
#                        reserve it for cases CSS can't express (e.g.
#                        matching by visible text).
#                      - Absolute XPath (/html/body/div[2]/...) is the
#                        WORST option of all: any structural change
#                        anywhere above the element breaks it instantly.
#                        Avoid in real automation.
# 5. CLASS_NAME    - classes are frequently shared for styling purposes,
#                    so this is rarely unique on its own - brittle if
#                    the class is reused or renamed.
# 6. TAG_NAME      - least precise: matches every element of that type
#                    on the whole page. Only useful with find_elements()
#                    to grab a whole group, never to pinpoint one element.


if __name__ == "__main__":
    print("--- Locator strategies: Simple Form Demo ---")
    locator_strategies_simple_form()

    print("\n--- Locator strategies: Checkbox Demo ---")
    locator_strategies_checkbox()