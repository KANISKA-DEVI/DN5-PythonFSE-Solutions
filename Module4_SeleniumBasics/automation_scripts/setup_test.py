# ============================================================
# Hands-On 4: Selenium WebDriver Setup, Browser Drivers & Basic Commands
# File: setup_test.py
# Location: C:\DigitalNurture5\Module4_SeleniumBasics\automation_scripts\
#
# SELENIUM ARCHITECTURE:
# ─────────────────────
# 1. WEBDRIVER:
#    The core Selenium component. It is a browser automation API.
#    Your Python script sends commands (click, type, navigate) to WebDriver.
#    WebDriver translates these commands to browser-native instructions
#    using the W3C WebDriver protocol (HTTP JSON Wire Protocol).
#    ChromeDriver acts as the bridge between Selenium and Chrome.
#
# 2. SELENIUM GRID:
#    Solves the problem of parallel execution across multiple machines/browsers.
#    A Grid Hub receives tests and distributes them to Node machines
#    that have different browsers (Chrome on Windows, Safari on Mac, etc).
#    Enables running 100 tests simultaneously instead of sequentially.
#
# 3. SELENIUM IDE:
#    A browser extension (Chrome/Firefox) for recording and playing back
#    user interactions. Good for generating initial test code quickly.
#    The generated code is a starting point — not production quality.
# ============================================================

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

PLAYGROUND_URL = "https://www.lambdatest.com/selenium-playground/"


# ============================================================
# TASK 1: Basic Setup and Navigation
# ============================================================

def task1_basic_setup():
    """
    Task 1: Set up WebDriver, navigate to the playground, print title.
    webdriver-manager auto-downloads the correct ChromeDriver version —
    no manual driver management needed.
    """
    print("\n=== Task 1: Basic Setup ===")

    # Set up Chrome options
    options = webdriver.ChromeOptions()
    # Suppress "Chrome is being controlled by automated test software" bar
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Initialize Chrome WebDriver (webdriver_manager downloads ChromeDriver automatically)
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    # WHY implicit wait is considered BAD practice:
    # driver.implicitly_wait(10) sets a global timeout for finding elements.
    # PROBLEM 1: It applies to EVERY find_element call — slows down tests when
    #            an element is intentionally absent (e.g., checking an error message
    #            is NOT shown — it waits 10 seconds before confirming absence).
    # PROBLEM 2: It mixes with explicit waits unpredictably.
    # BETTER: Use explicit WebDriverWait with specific ExpectedConditions per element.
    # We demonstrate explicit waits properly in Hands-On 5.
    driver.implicitly_wait(10)  # Used here for simplicity; explicit waits are better

    # Navigate to the Selenium Playground
    driver.get(PLAYGROUND_URL)

    # Print the page title
    print(f"Page title: {driver.title}")

    driver.quit()
    print("Task 1 complete: browser closed.")


def task1_headless_mode():
    """
    Task 1, Step 27: Run Chrome in headless mode (no visible browser window).
    Useful for CI/CD pipelines where there is no display.
    """
    print("\n=== Task 1: Headless Mode ===")

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')           # No visible window
    options.add_argument('--no-sandbox')         # Required in some CI environments
    options.add_argument('--disable-dev-shm-usage')  # Prevents memory issues in Docker

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(PLAYGROUND_URL)
    print(f"Headless page title: {driver.title}")
    assert len(driver.title) > 0, f"Title check failed in headless mode. Got: {driver.title}"
    print("Headless mode works correctly — title verified without visible window.")

    driver.quit()


# ============================================================
# TASK 2: Navigation and Window Commands
# ============================================================

def task2_navigation_and_windows():
    """
    Task 2: Navigate, assert URL, open new tab, switch windows, take screenshot.
    """
    print("\n=== Task 2: Navigation & Window Commands ===")

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver  = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(10)

    # Step 28: Navigate to playground, click Simple Form Demo, assert URL
    driver.get(PLAYGROUND_URL)
    print(f"Starting URL: {driver.current_url}")

    # Click the Simple Form Demo link
    simple_form_link = driver.find_element(By.LINK_TEXT, "Simple Form Demo")
    simple_form_link.click()
    time.sleep(1)

    # Assert URL contains 'simple-form-demo'
    assert 'simple-form-demo' in driver.current_url, \
        f"Expected URL to contain 'simple-form-demo', got: {driver.current_url}"
    print(f"✓ URL assertion passed: {driver.current_url}")

    # Navigate back to playground
    driver.back()
    print(f"Navigated back to: {driver.current_url}")

    # Step 29: Open a new browser tab
    driver.execute_script('window.open("https://www.google.com");')
    time.sleep(1)

    all_tabs = driver.window_handles
    print(f"Open tabs: {len(all_tabs)}")

    # Switch to the new tab (index 1)
    driver.switch_to.window(all_tabs[1])
    time.sleep(1)
    print(f"Google tab title: {driver.title}")

    # Step 30: Switch back to original tab and take screenshot
    driver.switch_to.window(all_tabs[0])
    driver.save_screenshot('playground_screenshot.png')
    print("✓ Screenshot saved: playground_screenshot.png")

    # Step 31: Window size management
    # WHY consistent window size matters:
    # Responsive websites change layout at different screen widths.
    # A button visible at 1280px wide may be hidden (inside a hamburger menu)
    # at 375px. Inconsistent window sizes cause tests to fail randomly
    # depending on the tester's monitor resolution.
    current_size = driver.get_window_size()
    print(f"Current window size: {current_size['width']}x{current_size['height']}")

    driver.set_window_size(1280, 800)
    new_size = driver.get_window_size()
    print(f"Set window size to: {new_size['width']}x{new_size['height']}")
    assert new_size['width'] >= 1280, f"Window width not set correctly. Got: {new_size['width']}"
    print("✓ Window size set and verified")

    driver.quit()
    print("Task 2 complete.")


# ============================================================
# Run all tasks
# ============================================================
if __name__ == "__main__":
    task1_basic_setup()
    task1_headless_mode()
    task2_navigation_and_windows()
    print("\n✅ All Hands-On 4 tasks completed successfully!")