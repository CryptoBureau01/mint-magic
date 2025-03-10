from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# Magic Eden Mint URL file path
MINT_URL_FILE = "magic/data_url"

def get_mint_time():
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

        # **Find the timer numbers using XPath**
        try:
            timer_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'tw-size-8')]/span")

            if len(timer_elements) == 4:
                mint_time = f"{timer_elements[0].text}:{timer_elements[1].text}:{timer_elements[2].text}:{timer_elements[3].text}"
                print(f"✅ Mint starts in: {mint_time}")
            else:
                print("❌ Could not retrieve mint time. Timer format issue.")

        except Exception as e:
            print(f"❌ Error finding timer: {e}")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        driver.quit()

get_mint_time()
