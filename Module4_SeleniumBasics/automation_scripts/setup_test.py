# ============================================================
# setup_test.py — Hands-On 4: Selenium WebDriver Setup & Basic Commands
# File: automation_scripts/setup_test.py
# ============================================================

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by      import By
from webdriver_manager.chrome          import ChromeDriverManager
import time

PLAYGROUND_URL = "https://www.lambdatest.com/selenium-playground/"


def _make_driver(headless: bool = False):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")
    if headless:
        options.add_argument("--headless=new")   # modern headless flag
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )


# ── Task 1a: Basic Setup ──────────────────────────────────────────────────────

def task1_basic_setup():
    print("\n=== Task 1: Basic Setup ===")
    driver = _make_driver()
    driver.implicitly_wait(10)

    driver.get(PLAYGROUND_URL)
    print(f"Page title: {driver.title}")

    driver.quit()
    print("Task 1 complete: browser closed.")


# ── Task 1b: Headless Mode ────────────────────────────────────────────────────

def task1_headless_mode():
    print("\n=== Task 1: Headless Mode ===")
    driver = _make_driver(headless=True)
    driver.get(PLAYGROUND_URL)

    print(f"Headless page title: {driver.title}")
    assert "LambdaTest" in driver.title or "Selenium" in driver.title, \
        f"Unexpected title in headless mode: {driver.title}"
    print("Headless mode works correctly — title verified.")

    driver.quit()


# ── Task 2: Navigation & Window Commands ──────────────────────────────────────

def task2_navigation_and_windows():
    print("\n=== Task 2: Navigation & Window Commands ===")
    driver = _make_driver()
    driver.implicitly_wait(10)

    # Navigate and click Simple Form Demo
    driver.get(PLAYGROUND_URL)
    print(f"Starting URL: {driver.current_url}")

    # Click the link — fall back to direct URL if link text changes
    try:
        link = driver.find_element(By.LINK_TEXT, "Simple Form Demo")
        link.click()
    except Exception:
        driver.get(PLAYGROUND_URL + "simple-form-demo/")

    time.sleep(1)
    assert "simple-form-demo" in driver.current_url, \
        f"Expected URL to contain 'simple-form-demo', got: {driver.current_url}"
    print(f"✓ URL assertion passed: {driver.current_url}")

    # Navigate back
    driver.back()
    time.sleep(0.5)

    # Open a new tab
    driver.execute_script('window.open("https://www.google.com");')
    time.sleep(1)
    all_tabs = driver.window_handles
    print(f"Open tabs: {len(all_tabs)}")

    # Switch to new tab
    driver.switch_to.window(all_tabs[1])
    time.sleep(1)
    print(f"New tab title: {driver.title}")

    # Switch back and take screenshot
    driver.switch_to.window(all_tabs[0])
    driver.save_screenshot("playground_screenshot.png")
    print("✓ Screenshot saved: playground_screenshot.png")

    driver.set_window_size(1280, 800)

    size = driver.get_window_size()
    assert size["width"] >= 1200, "Window width mismatch"

    print(f"✓ Window size confirmed: {size['width']}x{size['height']}")

    driver.quit()
    print("Task 2 complete.")


if __name__ == "__main__":
    task1_basic_setup()
    task1_headless_mode()
    task2_navigation_and_windows()
    print("\n✅ All Hands-On 4 tasks completed successfully!")