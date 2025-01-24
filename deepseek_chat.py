import sys
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException



class DeepSeek:
    def __init__(self, email, password):
        """Initialize DeepSeek chatbot interface with credentials"""
        self.email = email
        self.password = password
        self.last_text_length = 0
        self.driver = self.initialize_driver_options()
        self.login(email=self.email, password=self.password)  # Auto-login on instantiation

    def initialize_driver_options(self):
        """Configure headless Firefox browser options"""
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')  # Run without GUI for server environments
        options.add_argument('--no-sandbox')  # Essential for containerized environments
        options.add_argument('--disable-dev-shm-usage')  # Prevent resource issues
        return webdriver.Firefox(options=options)

    def login_verification(self):
        """Check if user is logged in by verifying current URL"""
        # Returns True if NOT on login page (valid session), False otherwise
        if self.driver.current_url != "https://chat.deepseek.com/sign_in":
            return True
        else:
            print("You have signed out of your account, please log in again.\nTo log in again you can use login function enter email and password.")
            return False
    
    def quit(self):
        """Clean shutdown procedure"""
        self.logout()  # Explicit logout first
        self.driver.quit()  # Close browser
        sys.exit("Session terminated successfully.")

    def verify_url(self, expected_url, timeout=20):
        """Wait for specific URL to verify navigation success"""
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_to_be(expected_url))
            return True
        except:
            return False  # Timeout reached without matching URL

    def login(self, email, password):
        """Complete login workflow with credentials"""
        url = "https://chat.deepseek.com/sign_in"
        self.driver.get(url)

        # Email input - long timeout for initial page load
        WebDriverWait(self.driver, 999).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div[3]/div[1]/div/input"))
        ).send_keys(email)

        # Password input
        self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div[4]/div[1]/div/input").send_keys(password)
        
        # Checkbox and login button
        self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div[5]/div[1]/div/div[1]/div").click()
        self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div[6]").click()

        # Post-login verification
        if self.verify_url(expected_url="https://chat.deepseek.com/"):
            print("Authentication successful!")
        else:
            print("Critical authentication failure!")
            self.driver.quit()
            sys.exit()

    def logout(self):
        """Logout sequence through UI elements"""
        # Profile dropdown activation
        profile_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.c6ab9234"))
        )
        profile_button.click()

        # Logout selection
        logout_option = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='ds-dropdown-menu-option__label' and text()='Log out']"))
        )
        logout_option.click()

        # Logout confirmation
        if self.verify_url("https://chat.deepseek.com/sign_in"):
            print("Session closed properly")
        else:
            print("Warning: Logout may not have completed fully")

    def create_new_chat(self):
        """Start fresh conversation thread"""
        if self.login_verification():
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#root > div > div.c3ecdb44 > div.f2eea526 > div > div.b83ee326 > div > div > div.e886deb9 > div"))
            ).click()
            print("New chat session started")
        else:
            pass  # Fail silently when not logged in

    def deepthink(self):
        """Activate advanced processing mode"""
        if self.login_verification():
            WebDriverWait(self.driver, 999).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.ds-button.ds-button--primary.ds-button--filled.ds-button--rect.ds-button--m.d9f56c96'))
            ).click()
            print("Deep analysis mode activated")
        else:
            pass

    def send_text(self, text):
        """Complete message sending workflow"""
        try:
            if not self._verify_ready_state():
                return None
            
            self._clear_input()
            self._send_chunks(text)
            
            if not self._final_validation(text):
                print("not self._final_validation(text)")
                return None
                
            return self._send_and_capture_response()
            
        except Exception as e:
            print(f"Critical failure: {str(e)}")
            return None

    def _verify_ready_state(self):
        """Ensure system is ready for new input"""
        return self.driver.execute_script("""
            return document.readyState === 'complete' && 
                   !document.querySelector('.loading-indicator')
        """)

    def _clear_input(self):
        """Nuclear input clearing"""
        self.driver.execute_script("""
            const input = document.querySelector('#chat-input');
            input.value = '';
            input.dispatchEvent(new Event('input', { bubbles: true }));
            setTimeout(() => input.focus(), 100);
        """)
        time.sleep(1)

    def _send_chunks(self, text):
        """Chunked injection with atomic validation"""
        CHUNK_SIZE = 500
        for i in range(0, len(text), CHUNK_SIZE):
            chunk = text[i:i+CHUNK_SIZE]
            self._inject_chunk(chunk)
            self._verify_chunk_injection(chunk)
            self.last_text_length += len(chunk)

    def _inject_chunk(self, chunk):
        """Robust chunk insertion"""
        self.driver.execute_script("""
            const chunk = arguments[0];
            const input = document.querySelector('#chat-input');
            
            // Framework-aware insertion
            const nativeSetter = Object.getOwnPropertyDescriptor(
                HTMLTextAreaElement.prototype, 'value'
            ).set;
            
            nativeSetter.call(input, input.value + chunk);
            
            // Event simulation
            ['keydown', 'input', 'change'].forEach(event => {
                input.dispatchEvent(new Event(event, { bubbles: true }));
            });
        """, chunk)
        time.sleep(0.3)

    def _verify_chunk_injection(self, chunk):
        """Real-time chunk verification"""
        current_value = self.driver.execute_script(
            "return document.querySelector('#chat-input').value"
        )
        if not current_value.endswith(chunk):
            raise RuntimeError("Chunk injection failed")

    def _final_validation(self, text):
        """Comprehensive text validation"""
        current_value = self.driver.execute_script(
            "return document.querySelector('#chat-input').value"
        )
        return current_value == text

    def _send_and_capture_response(self):
        """Guaranteed send mechanism"""
        try:
            # Primary click strategy
            self._click_send_button()

            # Return response
            return self._get_response()            
        except Exception as e:
            print(f"Send failed: {str(e)}")
            return None

    def _click_send_button(self):
        """Advanced click handling"""
        button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "f6d670")
            )
        )
        
        # Realistic click simulation
        ActionChains(self.driver)\
            .move_to_element(button)\
            .pause(0.2)\
            .click()\
            .pause(0.5)\
            .perform()
    
    def _get_response(self):
        """More robust version with visibility checks"""
        try:            
            # Wait for the button to be in the desired state: disabled (true) AND no loading spinner
            WebDriverWait(self.driver, timeout=999).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//div[@role='button' and @aria-disabled='true' and not(.//*[contains(@class, 'ds-loading')])]"
                ))
            )
            
            # Directly target last response using DOM order
            last_response = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "(//div[contains(@class, 'ds-markdown--block')])[last()]"
                ))
            )
            return last_response.text 
        
        except TimeoutException:
            return None
