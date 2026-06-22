# Hands-On 3: Test Automation Strategy

---

## TASK 1: Automation Decision and Test Case Selection

### 5 Criteria for Deciding Whether to Automate

**Applied to: "Test that POST /api/courses/ returns 201 with correct data when valid input is provided"**

| # | Criterion | Explanation | Applied to Our Test Case |
|---|-----------|-------------|--------------------------|
| 1 | 🔁 **Repetitive Execution** | If the test must be run many times (every build, every deployment), automation saves time. | ✅ AUTOMATE — this regression test runs on every code push. |
| 2 | 📌 **Stable Requirements** | If the API contract is unlikely to change frequently, the automation investment pays off. | ✅ AUTOMATE — the POST /api/courses/ contract is stable. |
| 3 | ⚠️ **High Risk / Critical Path** | Tests covering core business functionality should be automated for safety. | ✅ AUTOMATE — course creation is a critical feature. |
| 4 | 📊 **Data-Driven Possibility** | If the test needs to run with many data combinations, automation handles this efficiently. | ✅ AUTOMATE — can test with many course data combinations via parameterisation. |
| 5 | 💰 **Feasibility / ROI** | If automating takes less time than manual execution over the test's lifetime, automate it. | ✅ AUTOMATE — 4 hours to automate, 5 minutes per manual run, pays off after ~8 runs. |

**Conclusion: AUTOMATE this test case.** All 5 criteria are met.

---

### Manual or Automate Decision for 6 Test Cases

| # | Test Case | Decision | Justification |
|---|-----------|----------|---------------|
| a | Regression test for all CRUD endpoints after every code change | ✅ **AUTOMATE** | Repetitive, runs on every commit, stable endpoints, very high ROI. |
| b | Exploratory testing of a new search feature | 🖐️ **MANUAL** | Exploratory testing requires human curiosity and creativity. Automation cannot "explore" — it only checks what you have already defined. |
| c | Performance test: 100 concurrent users calling GET /api/courses/ | ✅ **AUTOMATE** | Impossible to manually simulate 100 concurrent users. Tools like Locust or JMeter are required. |
| d | UI test for the login form | ✅ **AUTOMATE** | Repetitive, stable UI, excellent candidate for Selenium automation. |
| e | Verify the API documentation (Swagger) is accurate | 🖐️ **MANUAL** | Checking documentation quality requires human judgment and reading comprehension. |
| f | Smoke test: verify the API is reachable after deployment | ✅ **AUTOMATE** | Quick automated health-check after every deployment — critical safety net, low effort to automate. |

---

### Automation ROI Calculation

| Item | Value |
|------|-------|
| Time to automate (one-time) | 4 hours |
| Time per manual run | 30 minutes (0.5 hours) |
| Breakeven point | 4 ÷ 0.5 = **8 runs** |
| Maintenance overhead (after run 10) | 20% of 0.5 hours = 0.1 hours per run |
| Net saving per run (after run 10) | 0.5 − 0.1 = **0.4 hours saved per run** |

**Summary:**

| Runs | Status |
|------|--------|
| Runs 1–8 | Paying back the 4-hour investment |
| Run 8 | ✅ Breakeven reached |
| Runs 9–10 | Pure savings (0.5 hours per run) |
| Run 11+ | Net savings of 0.4 hours per run after maintenance |
| At 50 runs | Manual = 25 hours total. Automation = 4 + (40 × 0.1) = 8 hours. **Saving: 17 hours** |

---

### Flaky Tests

**What is a flaky test?**

A flaky test is a test that **sometimes passes and sometimes fails** without any change to the code being tested. It is non-deterministic.

**Example:**

> A Selenium test clicks the Submit button and immediately checks for a success message. On a fast machine it passes; on a slow CI server the success message has not appeared yet, so the test fails. The `time.sleep(2)` "fix" makes it pass on slow machines but wastes 2 seconds on every fast run.

**3 Strategies to Prevent/Fix Flaky Tests:**

| # | Strategy | Description |
|---|----------|-------------|
| 1 | ⏱️ **Use Explicit Waits** | Replace `time.sleep(3)` with `WebDriverWait(driver, 10).until(EC.visibility_of_element_located(...))`. The test waits exactly as long as needed — no longer, no shorter. |
| 2 | 🔒 **Isolate Tests — No Shared State** | Each test sets up its own data and cleans up after itself. Tests must never depend on the order of execution or data left by another test. |
| 3 | 🔄 **Retry Mechanism** | Use `pytest-rerunfailures` to automatically retry a failed test once before marking it as a failure. Handles true intermittent network issues while still catching real regressions. |

---

## TASK 2: Compare Automation Framework Types

### Framework Comparison

| Framework | Description | Advantage | Disadvantage | When to Use for Course Management |
|-----------|-------------|-----------|--------------|-----------------------------------|
| 📝 **Linear** | Each test is a standalone script with no reusable components. All steps recorded in one file. | Simple to understand and quick to create for small projects. | No reusability — if login steps change, every script must be updated. | Only for a quick one-off demo or proof of concept. |
| 🧩 **Modular** | Common actions (login, create course, logout) extracted into reusable modules/functions. Tests call these modules. | Changes to a module only need to be updated in one place. | Requires more upfront design effort than linear. | When 10+ test cases all start with the same login step — extract login into a shared module. |
| 📊 **Data-Driven** | Test logic written once; test data stored externally in CSV/Excel/JSON. Same test runs with each row of data. | Testing 50 different combinations requires only adding rows to a data file — no new test code. | Harder to debug when a specific data row fails. | Testing POST /api/courses/ with 50 different valid and invalid input combinations. |
| 🔑 **Keyword-Driven** | Test cases written using keywords (CLICK, ENTER_TEXT, VERIFY) in spreadsheets. Non-technical members can write tests. | Business analysts and manual testers can write automated tests without knowing Python. | Complex to build and maintain the keyword library. | When non-technical stakeholders need to write and maintain acceptance tests. |
| 🔀 **Hybrid** | Combines Modular + Data-Driven + optionally Keyword-Driven. Most real-world frameworks are hybrid. | Best of all worlds — reusability, parameterisation, and flexibility. | Most complex to design initially. | Recommended for a mature, growing test suite. |

---

### Recommended Framework for the Scenario

**Scenario:** Test login with 50 user/password combinations, reuse login steps across 20 test cases, support both technical and non-technical team members.

**Recommendation: ✅ Hybrid Framework (Data-Driven + Modular)**

| Requirement | Solution |
|-------------|----------|
| Test login with 50 combinations | **Data-Driven:** Store combinations in a CSV file. Use `@pytest.mark.parametrize` to run with each row automatically. |
| Reuse login steps across 20 tests | **Modular (POM):** Extract login into a `LoginPage` class. All 20 tests call `login_page.login(username, password)` — one line. |
| Support non-technical members | Provide a simple CSV template where they add test data rows without touching Python code. |

---

### Hybrid Framework Folder Structure

| Folder / File | Purpose |
|---|---|
| 📁 `config/config.ini` | Base URL, browser, timeout settings |
| 📁 `test_data/login_data.csv` | 50 username/password combinations |
| 📁 `test_data/course_data.json` | Course creation test data |
| 📁 `test_data/invalid_data.csv` | Invalid input test cases |
| 📁 `pages/base_page.py` | Common methods (navigate, wait, screenshot) |
| 📁 `pages/login_page.py` | Login page interactions |
| 📁 `pages/courses_page.py` | Course listing/creation interactions |
| 📁 `pages/enrollment_page.py` | Enrollment form interactions |
| 📁 `utils/driver_factory.py` | Creates Chrome/Firefox WebDriver |
| 📁 `utils/data_reader.py` | Reads CSV/JSON test data files |
| 📁 `utils/screenshot.py` | Captures screenshots on failure |
| 📁 `tests/test_login.py` | Login tests (parameterised with CSV data) |
| 📁 `tests/test_courses.py` | Course CRUD tests |
| 📁 `tests/test_enrollment.py` | Enrollment tests |
| 📁 `reports/` | Generated HTML test reports |
| 📄 `conftest.py` | Shared pytest fixtures (driver, base_url) |
| 📄 `requirements.txt` | selenium, pytest, webdriver-manager, pytest-html |