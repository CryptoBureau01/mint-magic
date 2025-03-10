from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

MINT_URL_FILE = "magic/data_url"

def get_mint_time():
    driver = None  # Initialize driver variable to avoid UnboundLocalError
    try:
        with open(MINT_URL_FILE, "r") as file:
            MINT_URL = file.read().strip()

        if not MINT_URL:
            print("❌ No mint URL found in magic/data!")
            return

        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")  # Debug ke liye headless mode hata diya
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        print(f"🔄 Fetching mint time from: {MINT_URL}")
        driver.get(MINT_URL)
        time.sleep(5)  # JavaScript elements load hone ka wait

        # Debugging ke liye full page source print karo
        print("🔎 Page Source:\n", driver.page_source)

        # Check if countdown timer elements exist
        timer_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'tw-size-8')]/span")
        print("🔍 Found elements:", len(timer_elements))

        if timer_elements:
            countdown = " : ".join([el.text for el in timer_elements])
            print(f"✅ Mint starts in: {countdown}")
        else:
            print("❌ Could not retrieve mint time. Element not found.")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        if driver is not None:
            driver.quit()

get_mint_time()
