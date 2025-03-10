from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

MINT_URL_FILE = "magic/data_url"

def get_mint_time():
    try:
        with open(MINT_URL_FILE, "r") as file:
            MINT_URL = file.read().strip()

        if not MINT_URL:
            print("❌ No mint URL found in magic/data!")
            return

        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")  # COMMENT THIS LINE FOR DEBUGGING
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        print(f"🔄 Fetching mint time from: {MINT_URL}")
        driver.get(MINT_URL)
        time.sleep(5)  # Wait for JavaScript to load

        # PRINT FULL PAGE SOURCE FOR DEBUGGING
        print("🔎 Page Source:\n", driver.page_source)

        # Check if elements are found
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
        driver.quit()

get_mint_time()
