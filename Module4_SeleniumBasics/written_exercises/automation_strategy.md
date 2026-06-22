# Hands-On 3: Test Automation Strategy

---

## TASK 1: Automation Decision and Test Case Selection

### 5 Criteria for Deciding Whether to Automate

**Applied to: "Test that POST /api/courses/ returns 201 with correct data when valid input is provided"**

| Criterion | Explanation | Applied to our test case |
|---|---|---|
| **1. Repetitive execution** | If the test must be run many times (every build, every deployment), automation saves time. | ✅ AUTOMATE — this regression test runs on every code push. |
| **2. Stable requirements** | If the API contract is unlikely to change frequently, the automation investment pays off. | ✅ AUTOMATE — the POST /api/courses/ contract is stable. |
| **3. High risk / critical path** | Tests covering core business functionality should be automated for safety. | ✅ AUTOMATE — course creation is a critical feature. |
| **4. Data-driven possibility** | If the test needs to run with many data combinations, automation handles this efficiently. | ✅ AUTOMATE — can test with many course data combinations via parameterisation. |
| **5. Feasibility / ROI** | If automating takes less time than manual execution over the test's lifetime, automate it. | ✅ AUTOMATE — 4 hours to automate, 5 minutes per manual run, pays off after ~50 runs. |

**Conclusion: AUTOMATE this test case.** All 5 criteria are met.

---

### Manual or Automate Decision for 6 Test Cases

| Test Case | Decision | Justification |
|---|---|---|
| **(a) Regression test for all CRUD endpoints after every code change** | **AUTOMATE** | Repetitive, runs on every commit, stable endpoints, high ROI. |
| **(b) Exploratory testing of a new search feature** | **MANUAL** | Exploratory testing requires human curiosity and creativity. Automation cannot "explore" — it only checks what you've already defined. |
| **(c) Performance test: 100 concurrent users calling GET /api/courses/** | **AUTOMATE** | It is impossible to manually simulate 100 concurrent users. Tools like Locust or JMeter are required. |
| **(d) UI test for the login form** | **AUTOMATE** | Repetitive, stable UI, good candidate for Selenium automation. |
| **(e) Verify the API documentation (Swagger) is accurate** | **MANUAL** | Checking documentation quality requires human judgment and reading comprehension. |
| **(f) Smoke test: verify the API is reachable after deployment** | **AUTOMATE** | A quick automated health-check after every deployment — critical safety net, low effort. |

---

### Automation ROI Calculation

- **Time to automate:** 4 hours (one-time investment)
- **Time per manual run:** 30 minutes = 0.5 hours
- **Breakeven without maintenance:** 4 hours ÷ 0.5 hours = **8 runs** to pay for itself

**With 20% maintenance overhead after the 10th run:**
- After run 10, each run costs an additional 20% of 0.5 hours = 0.1 hours maintenance
- Effective cost per run after run 10: 0.5 hours saved − 0.1 hours maintenance = **0.4 hours net saving per run**

**Summary:**
- Runs 1–8: Automation is paying back the investment
- Run 8: Breakeven reached
- Run 9 onwards: Pure savings (0.5 hours per run)
- Run 11 onwards: Net savings of 0.4 hours per run (after maintenance overhead)
- At 50 runs: Total manual time = 25 hours. Automation cost = 4 hours + (40 × 0.1) = 8 hours. **Saving: 17 hours.**

---

### Flaky Tests

**What is a flaky test?**
A flaky test is a test that sometimes passes and sometimes fails without any change to the code being tested. It is non-deterministic.

**Example:**
A Selenium test clicks the Submit button and immediately checks for a success message. On a fast machine it passes; on a slow CI server the success message hasn't appeared yet, so the test fails. The `time.sleep(2)` "fix" makes it pass on slow machines but wastes 2 seconds on every fast run.

**3 Strategies to Prevent/Fix Flaky Tests:**

1. **Use explicit waits instead of time.sleep():** Replace `time.sleep(3)` with `WebDriverWait(driver, 10).until(EC.visibility_of_element_located(...))`. The test waits exactly as long as needed — no longer, no shorter.

2. **Isolate tests — no shared state:** Each test should set up its own data and clean up after itself. If Test A creates a course and Test B expects no courses to exist, they will conflict when run in parallel. Use database fixtures that reset state between tests.

3. **Retry mechanism for known intermittent issues:** Use `pytest-rerunfailures` to automatically retry a failed test once before marking it as a failure. This handles true intermittent network issues while still catching real regressions.

---

## TASK 2: Compare Automation Framework Types

### Framework Comparison

**1. Linear Framework**
Each test is a standalone script with no reusable components. The script records all steps from login to assertion in one file.
- **Advantage:** Simple to understand and quick to create for small projects.
- **Disadvantage:** No reusability — if the login steps change, you update every single test script.
- **When to use for Course Management:** Only for a quick one-off demo or proof of concept. Not suitable for a growing test suite.

**2. Modular Framework**
Common actions (login, create course, logout) are extracted into reusable modules/functions. Tests call these modules.
- **Advantage:** Changes to a module (e.g., login) only need to be updated in one place.
- **Disadvantage:** Requires more upfront design effort than linear.
- **When to use for Course Management:** When you have 10+ test cases that all start with a login step — extract login into a shared module.

**3. Data-Driven Framework**
Test logic is written once; test data (inputs and expected outputs) is stored externally in CSV, Excel, or JSON files. The same test runs with each row of data.
- **Advantage:** Testing 50 different course name/code combinations requires only adding rows to a data file — no new test code.
- **Disadvantage:** Harder to debug when a specific data row fails.
- **When to use for Course Management:** Testing POST /api/courses/ with 50 different valid and invalid input combinations.

**4. Keyword-Driven Framework**
Test cases are written using keywords (e.g., `CLICK`, `ENTER_TEXT`, `VERIFY`) in spreadsheets. Non-technical team members can write tests without knowing Python.
- **Advantage:** Business analysts and manual testers can write automated tests.
- **Disadvantage:** Complex to build and maintain the keyword library. Can become rigid.
- **When to use for Course Management:** When non-technical stakeholders need to write and maintain acceptance tests.

**5. Hybrid Framework**
Combines Modular (reusable page/action modules) + Data-Driven (external test data) + optionally Keyword-Driven. Most real-world frameworks are hybrid.
- **Advantage:** Best of all worlds — reusability, parameterisation, and flexibility.
- **Disadvantage:** Most complex to design initially.
- **When to use for Course Management:** The recommended approach for a mature test suite.

---

### Recommended Framework for the Scenario

**Scenario:** Test login with 50 user/password combinations, reuse login steps across 20 test cases, support both technical and non-technical team members.

**Recommendation: Hybrid Framework (Data-Driven + Modular)**

- **Data-Driven component:** Store 50 username/password combinations in a CSV file. Use `@pytest.mark.parametrize` to run the login test with each row. No new test code per combination.
- **Modular component:** Extract the login action into a `LoginPage` class (Page Object Model). All 20 test cases that need login just call `login_page.login(username, password)` — one line.
- **For non-technical members:** Provide a simple CSV template where they can add test data rows without touching Python code.

---

### Hybrid Framework Folder Structure
course_management_tests/
│
├── config/
│   └── config.ini          ← Base URL, browser, timeout settings
│
├── test_data/
│   ├── login_data.csv      ← 50 username/password combinations
│   ├── course_data.json    ← Course creation test data
│   └── invalid_data.csv    ← Invalid input test cases
│
├── pages/                  ← Page Object Model classes
│   ├── base_page.py        ← Common methods (navigate, wait, screenshot)
│   ├── login_page.py       ← Login page interactions
│   ├── courses_page.py     ← Course listing/creation interactions
│   └── enrollment_page.py  ← Enrollment form interactions
│
├── utils/
│   ├── driver_factory.py   ← Creates Chrome/Firefox WebDriver
│   ├── data_reader.py      ← Reads CSV/JSON test data files
│   └── screenshot.py       ← Captures screenshots on failure
│
├── tests/
│   ├── test_login.py       ← Login tests (parameterised with CSV data)
│   ├── test_courses.py     ← Course CRUD tests
│   └── test_enrollment.py  ← Enrollment tests
│
├── reports/                ← Generated HTML test reports
│
├── conftest.py             ← Shared pytest fixtures (driver, base_url)
└── requirements.txt        ← selenium, pytest, webdriver-manager, pytest-html


---