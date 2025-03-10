from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# Magic Eden Mint URL file path
MINT_URL_FILE = "magic/data_url"

def get_mint_time():
    driver = None  # Initialize driver variable

    try:
        # Load the URL from the file
        with open(MINT_URL_FILE, "r") as file:
            MINT_URL = file.read().strip()

        if not MINT_URL:
            print("❌ No mint URL found in magic/data!")
            return

        # Chrome WebDriver setup (headless mode)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Background mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        print(f"🔄 Fetching mint time from: {MINT_URL}")
        driver.get(MINT_URL)
        time.sleep(5)  # Wait for JavaScript to load

        # Find the countdown timer (check the exact class name in the webpage)
        try:
            countdown = driver.find_element(By.CLASS_NAME, "countdown-timer").text
            print(f"✅ Mint starts in: {countdown}")
        except:
            print("❌ Could not retrieve mint time. Please check the URL or class name.")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        if driver:  # Only quit if driver was initialized successfully
            driver.quit()

get_mint_time()
