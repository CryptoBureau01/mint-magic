from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

MINT_URL_FILE = "/root/magic/data_url"

def get_mint_time():
    driver = None  # Initialize driver to prevent UnboundLocalError
    try:
        with open(MINT_URL_FILE, "r") as file:
            MINT_URL = file.read().strip()

        if not MINT_URL:
            print("❌ No mint URL found in magic/data!")
            return

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"), options=options)

        print(f"🔄 Fetching mint time from: {MINT_URL}")
        driver.get(MINT_URL)
        time.sleep(5)  # Wait for JavaScript elements to load

        # Debugging: Print full page source
        print("🔎 Page Source:\n", driver.page_source)

        # Extract countdown elements
        timer_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'tw-size-8')]/span")

        if timer_elements:
            countdown = " : ".join([el.text for el in timer_elements])
            print(f"✅ Mint starts in: {countdown}")
        else:
            print("❌ Could not retrieve mint time. Element not found.")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        if driver is not None:  # Ensure driver exists before quitting
            driver.quit()

get_mint_time()
