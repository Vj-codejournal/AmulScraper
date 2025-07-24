from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/run", methods=["POST", "GET"])
def run_scraper():
    results = []
import time
import pywhatkit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# === CONFIG FROM ENVIRONMENT ===
PINCODE = os.getenv("PINCODE", "462003")
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "+918504835404")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
ENABLE_WHATSAPP = os.getenv("ENABLE_WHATSAPP", "false").lower() == "true"

# Validate required environment variables
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is required in .env file")
if not TELEGRAM_CHAT_ID:
    raise ValueError("TELEGRAM_CHAT_ID is required in .env file")
PRODUCT_URLS = {
    "Amul Whey Protein": "https://shop.amul.com/en/product/amul-chocolate-whey-protein-34-g-or-pack-of-60-sachets",
    "Amul High Protein Milk": "https://shop.amul.com/en/product/amul-high-protein-milk-250-ml-or-pack-of-32"
    #"Amul Pro": "https://shop.amul.com/en/product/amul-lactose-free-milk-250-ml-or-pack-of-32",
}

CART_URL = "https://shop.amul.com/en/cart"

# === WhatsApp Notification ===
def notify_whatsapp(product_name):
    if ENABLE_WHATSAPP and WHATSAPP_NUMBER:
        print("[*] Sending WhatsApp notification...")
        msg = f"🟢 {product_name} is back in stock!\n\nAdd to cart completed.\nView your cart here:\n{CART_URL}"
        try:
            pywhatkit.sendwhatmsg_instantly(WHATSAPP_NUMBER, msg, wait_time=20, tab_close=True)
            print("[+] WhatsApp notification sent!")
        except Exception as e:
            print(f"[!] WhatsApp notification failed: {e}")
    else:
        print("[i] WhatsApp notifications disabled or number not configured")

def notify_telegram(product_name):
    cart_link = "https://shop.amul.com/en/cart"
    message = f"🟢 *{product_name}* is in stock!\n\n✅ Added to cart\n🛒 [View Cart]({cart_link})"
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }

    response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        data=payload
    )

    if response.status_code == 200:
        print("[+] Telegram notification sent.")
    else:
        print(f"[!] Telegram send failed: {response.text}")

# === Selenium Task ===
def check_and_add_to_cart(product_name, url):
    print(f"[*] Checking: {product_name}")

    # Configure Chrome/Brave (you can also reuse session via user-data-dir)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # Uncomment this to reuse session (optional):
    # options.add_argument("--user-data-dir=C:/Users/YourUsername/AppData/Local/BraveSoftware/Brave-Browser/User Data")
    # options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        time.sleep(3)

        # Check if pincode prompt is there (only once per session)
        try:
            pincode_input = driver.find_element(By.ID, "search")
            print("[*] Entering pincode...")
            pincode_input.send_keys(PINCODE)
            time.sleep(1.5)
            # submit_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
            # submit_btn.click()
            #pincode_input.send_keys(Keys.ENTER)  # Submit via Enter key
            suggestion = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'searchitem-name')]//p[text()='462003']"))
            )
            suggestion.click()
            print("[+] Pincode submitted via Enter key.")
            time.sleep(3)
        except:
            print("[i] Pincode prompt not shown. Maybe already saved.")

        # Wait for product page to fully load
        time.sleep(5)

        #Look for Add to Cart
        

        try:
            print("[*] Waiting for Add to Cart button...")

            # Wait for presence first
            add_to_cart_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'add-to-cart') and text()='Add to Cart']"))
            )

            # Check if disabled attribute exists and is true
            disabled_attr = add_to_cart_btn.get_attribute("disabled")
            if disabled_attr is not None and disabled_attr != "0":
                print(f"[-] Add to Cart is disabled for {product_name}.")
            else:
                try:
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'add-to-cart') and text()='Add to Cart']")))
                    add_to_cart_btn.click()
                    print(f"[+] {product_name} is in stock. Added to cart via normal click.")
                except ElementClickInterceptedException:
                    # Try JavaScript click if blocked
                    driver.execute_script("arguments[0].click();", add_to_cart_btn)
                    print(f"[+] {product_name} added to cart via JS click workaround.")

                # Notifications
                notify_telegram(product_name)
                if ENABLE_WHATSAPP:
                    notify_whatsapp(product_name)
                return True

        except TimeoutException:
            print(f"[-] Add to Cart button not found in time for {product_name}.")
        except Exception as e:
            print(f"[!] Unexpected error while clicking Add to Cart for {product_name}: {e}")


    except Exception as e:
        print(f"[X] Error with {product_name}: {e}")
    finally:
        driver.quit()

    return False

# === APScheduler for background scraping ===
from apscheduler.schedulers.background import BackgroundScheduler

def scheduled_scrape():
    print("[⏰] Scheduled scrape triggered.")
    for name, url in PRODUCT_URLS.items():
        try:
            found = check_and_add_to_cart(name, url)
            if found:
                print(f"[✓] {name} found, stopping further checks this round.")
                break
        except Exception as e:
            print(f"[!] Error in scheduled scrape for {name}: {e}")

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_scrape, 'interval', minutes=10)
    scheduler.start()
    print("[🚀] Flask app starting with background scheduler.")
    app.run(host='0.0.0.0', port=10000)
