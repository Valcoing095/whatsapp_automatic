import time
import urllib.parse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WhatsAppSender:
    def __init__(self, headless=False):
        self.options = Options()
        if headless:
            self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.driver = None

    def start(self):
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get("https://web.whatsapp.com")
        print("Escanea el QR code con tu WhatsApp...")

    def wait_for_qr_disappear(self):
        try:
            WebDriverWait(self.driver, 60).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "_1OW Glenn"))
            )
            print("Sesión iniciada!")
            return True
        except:
            print("Tiempo agotado.")
            return False

    def send_message(self, phone, message):
        try:
            phone = self._format_phone(phone)
            encoded_msg = urllib.parse.quote(message)
            self.driver.get(f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}")
            time.sleep(3)

            send_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='send']"))
            )
            send_btn.click()
            time.sleep(1)
            return True
        except Exception as e:
            print(f"Error al enviar a {phone}: {e}")
            return False

    def _format_phone(self, phone):
        phone = "".join(c for c in str(phone).strip() if c.isdigit())
        if not phone.startswith("57") and len(phone) == 10:
            phone = "57" + phone
        elif not phone.startswith("57") and len(phone) == 9:
            phone = "5" + phone
        return phone

    def close(self):
        if self.driver:
            self.driver.quit()