@'
# Hands-On 3: Test Automation Process, Lifecycle & Framework Types
**Name:** Sharmi | **Register No:** 2117230020206 | **Program:** Digital Nurture 5.0 - Python Full Stack Engineer Track

---

## Task 1: Automation Decision and Test Case Selection

### 17. Five criteria for deciding whether to automate

Applied to: "Test that POST /api/courses/ returns 201 with correct course data when valid input is provided."

1. **Repeatability** - Will this test run many times (every build/regression)? Yes - this endpoint will be hit on every regression run, making it a strong automation candidate.
2. **Stability of the feature** - Is the feature's behavior unlikely to change frequently? Course creation is a core, stable feature, not something in constant flux - good for automation.
3. **High business risk if broken** - Is this a critical path? Yes - course creation failing blocks the entire admin workflow, so automated coverage protects against regressions.
4. **Time savings vs manual effort** - Manual testing takes ~2 minutes each run; automated takes ~2 seconds after setup. Over hundreds of runs, automation clearly pays off.
5. **Objective, verifiable pass/fail criteria** - The expected result (201 status + specific JSON fields) is exact and machine-checkable, unlike subjective UI polish checks - ideal for automation.

### 18. Automate or Manual?

| Test Case | Decision | Justification |
|---|---|---|
| (a) Regression test for all CRUD endpoints after every code change | **Automate** | Repetitive, runs on every change, objective pass/fail - textbook automation candidate |
| (b) Exploratory testing of a new search feature | **Manual** | Requires human intuition and creativity to find unexpected issues; no fixed script to follow |
| (c) Performance test: 100 concurrent users on GET /api/courses/ | **Automate** | Needs a load-testing tool (e.g. Locust/JMeter) - impossible to simulate 100 concurrent users manually |
| (d) UI test for the login form | **Automate** | Stable, repetitive, well-defined pass/fail via Selenium |
| (e) Verify API documentation (Swagger) is accurate | **Manual** | Requires human judgment to compare docs against actual intended behavior/wording |
| (f) Smoke test: verify API is reachable after deployment | **Automate** | Simple, fast, run on every deployment - ideal for a CI pipeline check |

### 19. Automation ROI calculation

- Automating the test: **4 hours** one-time cost
- Manual execution: **30 minutes (0.5 hr)** per run
- Breakeven (ignoring maintenance): 4 hrs / 0.5 hr = **8 runs**
- **With 20% maintenance overhead per run after the 10th run:**
  - Runs 1-10: no extra overhead, cost = 4 hrs (setup) only
  - From run 11 onward, each run costs an extra 20% of the manual time saved per run = 0.2 x 0.5 hr = 0.1 hr maintenance overhead per run
  - Since breakeven already occurs at run 8 (before overhead kicks in at run 11), automation still pays for itself by **run 8**, and remains net-positive even after overhead starts, because 0.1 hr overhead per run is still far less than the 0.5 hr manual cost it replaces.

**Conclusion:** Automation pays for itself after 8 runs, and stays profitable long-term despite the 20% maintenance overhead after run 10.

### 20. Flaky Tests

A **flaky test** is a test that sometimes passes and sometimes fails without any change to the code being tested - its result is inconsistent/non-deterministic.

**Example:** A Selenium test that clicks "Submit" and immediately checks for a success message using time.sleep(1) - on a slow CI machine the message hasn't rendered yet, so the test fails intermittently even though the app works correctly.

**3 strategies to prevent/fix flaky tests:**
1. Replace hard-coded sleep() calls with explicit WebDriverWait + ExpectedConditions, so the test waits exactly as long as needed instead of a fixed guess.
2. Ensure test isolation - each test creates its own data and cleans up after itself, so tests don't fail due to leftover state from a previous run.
3. Avoid brittle locators (like absolute XPath) that break with minor UI changes; use stable, unique locators like id or data-testid attributes.

---

## Task 2: Compare Automation Framework Types

### 21. The Five Framework Types

| Framework | Description | Advantage | Disadvantage | Use Case for Course Management |
|---|---|---|---|---|
| **Linear** | Tests are recorded/written as straight-line scripts, one action after another, no reuse or structure | Fastest to write for a one-off check | Massive duplication - any UI change requires editing every script that touches that element | Quick throwaway script to sanity-check the login page during a demo |
| **Modular** | Common actions (e.g. "login") are broken into reusable functions/modules called by multiple tests | Reduces duplication; a UI change means updating one function | Still requires programming skill to write and maintain modules | Reusing a login() module across 20 different Course Management test cases |
| **Data-Driven** | Test logic is separated from test data; the same script runs repeatedly with different data sets (usually from CSV/Excel/DB) | Easily test many input combinations without duplicating scripts | Test logic can be harder to trace when a specific data row fails | Testing course creation with 50 different course code/name combinations |
| **Keyword-Driven** | Test steps are represented as keywords (e.g. "Click", "EnterText") in a spreadsheet, interpreted by a driver engine | Non-technical team members can write tests using keywords | Significant upfront effort to build the keyword-interpreting engine | Allowing a non-technical QA lead to define new test flows for the admin panel without writing Python |
| **Hybrid** | Combines Modular reusability + Data-Driven parameterization + optionally Keyword-Driven abstraction | Most flexible and closest to real-world project needs | Most complex to design and set up initially | The full Course Management automation suite - reusable page objects, data-driven test data, clear structure |

### 22. Recommendation for the described scenario

**Scenario:** login with 50 user/password combinations, reuse login steps across 20 test cases, support both technical and non-technical team members.

**Recommendation: Hybrid framework** (Modular + Data-Driven, with light Keyword-Driven elements).
- **Modular** gives a single reusable login() page-object method used by all 20 test cases.
- **Data-Driven** feeds the 50 username/password combinations from a CSV/JSON file into that one login test via parametrization.
- A lightweight **Keyword-Driven** layer (e.g. a simple mapping of readable action names to page-object methods) lets non-technical members define new test scenarios without touching raw Selenium code.

This combination gives both engineering efficiency (no duplicated code) and team accessibility (non-programmers can still contribute test scenarios).

### 23. Hybrid Folder Structure

CourseManagement_Tests/
|-- data/
|   |-- login_credentials.csv          # 50 username/password pairs
|   `-- course_test_data.json
|-- pages/
|   |-- base_page.py                   # common driver actions
|   |-- login_page.py
|   `-- course_page.py
|-- utils/
|   |-- driver_factory.py              # browser setup/teardown helper
|   `-- data_reader.py                 # reads CSV/JSON test data
|-- tests/
|   |-- test_login.py
|   `-- test_course_creation.py
|-- config/
|   `-- config.yaml                    # base_url, timeouts, browser choice
|-- conftest.py
|-- requirements.txt
`-- pytest.ini
'@ | Set-Content -Path written_exercises\automation_strategy.md -Encoding UTF8










