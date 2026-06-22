# ============================================================
# conftest.py — Shared pytest Fixtures
# File: conftest.py
# Location: C:\DigitalNurture5\Module4_SeleniumBasics\automation_scripts\
# ============================================================
import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Session-scoped fixture — base URL available to all tests
@pytest.fixture(scope="session")
def base_url():
    """Base URL for the LambdaTest Selenium Playground."""
    return "https://www.lambdatest.com/selenium-playground/"


# Function-scoped fixture — fresh browser for every single test
@pytest.fixture(scope="function")
def driver():
    """
    Set up Chrome WebDriver before each test.
    Yield the driver to the test.
    Quit the driver after the test (teardown).
    The yield splits the fixture into setup (before) and teardown (after).
    """
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--window-size=1280,800")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    chrome_driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    chrome_driver.implicitly_wait(10)

    yield chrome_driver  # test runs here

    chrome_driver.quit()  # teardown — always runs after test


# Screenshot on failure hook
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Only take screenshot on test CALL phase failure (not setup/teardown)
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver is None:
            return

        # Check if driver session is still alive before screenshotting
        try:
            _ = driver.current_url  # will raise if session is dead
        except Exception:
            return

        # Create screenshots folder if it doesn't exist
        screenshots_dir = os.path.join(os.path.dirname(__file__), "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)

        # Sanitize test name for filename
        safe_name = item.name.replace("/", "_").replace("\\", "_").replace(" ", "_")
        screenshot_path = os.path.join(screenshots_dir, f"{safe_name}_failure.png")

        try:
            driver.save_screenshot(screenshot_path)
            print(f"\n📸 Screenshot saved: screenshots/{safe_name}_failure.png")
        except Exception as e:
            print(f"\n⚠️  Screenshot failed: {e}")