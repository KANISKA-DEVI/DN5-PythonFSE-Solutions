# ============================================================
# conftest.py — Shared pytest Fixtures
# File: conftest.py
# Location: automation_scripts/conftest.py
# ============================================================

import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the LambdaTest Selenium Playground."""
    return "https://www.lambdatest.com/selenium-playground/"


@pytest.fixture(scope="function")
def driver():
    """
    Provide a fresh Chrome WebDriver for every test.
    Teardown (quit) happens automatically after each test.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1280,800")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    chrome_driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    chrome_driver.implicitly_wait(10)

    yield chrome_driver  # test runs here

    chrome_driver.quit()


# ── Screenshot on failure ──────────────────────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture a screenshot when a test fails and save it to screenshots/."""
    outcome = yield
    report  = outcome.get_result()

    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv:
            os.makedirs("screenshots", exist_ok=True)
            safe_name = item.name.replace(" ", "_").replace("/", "_").replace("[", "_").replace("]", "_")
            path = f"screenshots/{safe_name}_failure.png"
            drv.save_screenshot(path)
            print(f"\n📸 Screenshot saved: {path}")