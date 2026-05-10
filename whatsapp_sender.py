import time
import urllib.parse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
            WebDriverWait(self.driver, 120).until(
                EC.any_of(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "[data-testid='chat-list']")
                    ),
                    EC.presence_of_element_located((By.ID, "pane-side")),
                )
            )
            print("Sesión iniciada!")
            return True
        except Exception:
            print("Tiempo agotado.")
            return False

    def send_message(self, phone, message):
        try:
            phone = self._format_phone(phone)
            encoded_msg = urllib.parse.quote(message)
            self.driver.get(f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}")
            time.sleep(2)

            WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.ID, "main"))
            )
            time.sleep(1.5)

            clicked = self.driver.execute_script(
                """
                const main = document.getElementById('main');
                if (!main) return false;
                const icons = ['send', 'wds-ic-send-filled', 'wds-ic-send'];
                for (const name of icons) {
                    const el = main.querySelector(`span[data-icon="${name}"], [data-icon="${name}"]`);
                    if (!el) continue;
                    const btn = el.closest('button') || el.closest('div[role="button"]');
                    (btn || el).click();
                    return true;
                }
                return false;
                """
            )
            if clicked:
                time.sleep(1.2)
                return True

            footer = self.driver.find_element(By.CSS_SELECTOR, "#main footer")
            for box in reversed(
                footer.find_elements(By.CSS_SELECTOR, "div[contenteditable='true']")
            ):
                try:
                    if not box.is_displayed():
                        continue
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'});", box
                    )
                    box.click()
                    time.sleep(0.2)
                    box.send_keys(Keys.ENTER)
                    time.sleep(1.2)
                    return True
                except Exception:
                    continue

            return False
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