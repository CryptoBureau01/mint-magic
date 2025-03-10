from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# Mint URL jo check karni hai
MINT_URL = "https://magiceden.io/mint-terminal/monad-testnet/0xf92197613fbafd582132c8fe13d9b427b1b02b1b"

def get_mint_time():
    # Chrome WebDriver setup (headless mode)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Background mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        print(f"🔄 Fetching mint time from: {MINT_URL}")
        driver.get(MINT_URL)
        time.sleep(5)  # Wait for JavaScript to load

        # Find the countdown timer (Iska class name check karna padega)
        countdown = driver.find_element(By.CLASS_NAME, "countdown-timer").text

        if countdown:
            print(f"✅ Mint starts in: {countdown}")
        else:
            print("❌ Could not retrieve mint time. Please check the URL.")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        driver.quit()

get_mint_time()
