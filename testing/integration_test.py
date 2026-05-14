
import os
import socket
import sys
import tempfile
import threading
import time
import unittest

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from werkzeug.serving import make_server

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
	sys.path.insert(0, PROJECT_ROOT)

from app import create_app, db


def get_free_port():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
		sock.bind(("127.0.0.1", 0))
		return sock.getsockname()[1]


class ServerThread(threading.Thread):
	def __init__(self, app, host, port):
		super().__init__(daemon=True)
		self.server = make_server(host, port, app)
		self.ctx = app.app_context()
		self.ctx.push()

	def run(self):
		self.server.serve_forever()

	def shutdown(self):
		self.server.shutdown()
		self.ctx.pop()


class BaseSeleniumIntegrationTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		fd, cls.db_path = tempfile.mkstemp(suffix=".sqlite3")
		os.close(fd)
		os.environ["DATABASE_URL"] = f"sqlite:///{cls.db_path}"

		cls.app = create_app()
		cls.app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)

		with cls.app.app_context():
			db.drop_all()
			db.create_all()

		cls.host = "127.0.0.1"
		cls.port = get_free_port()
		cls.base_url = f"http://{cls.host}:{cls.port}"
		cls.server_thread = ServerThread(cls.app, cls.host, cls.port)
		cls.server_thread.start()

		options = webdriver.ChromeOptions()
		options.add_argument("--headless=new")
		options.add_argument("--window-size=1440,1000")
		options.add_argument("--disable-gpu")
		options.add_argument("--no-sandbox")

		cls.driver = webdriver.Chrome(
			service=Service(ChromeDriverManager().install()),
			options=options,
		)
		cls.wait = WebDriverWait(cls.driver, 12)
		time.sleep(0.2)

	@classmethod
	def tearDownClass(cls):
		cls.driver.quit()
		cls.server_thread.shutdown()

		with cls.app.app_context():
			db.session.remove()
			db.drop_all()

		if os.path.exists(cls.db_path):
			os.remove(cls.db_path)

		os.environ.pop("DATABASE_URL", None)


	def setUp(self):
		# Ensure each test starts from a clean database and anonymous browser session.
		with self.app.app_context():
			db.session.remove()
			db.drop_all()
			db.create_all()

		self.driver.delete_all_cookies()
		self._go_home()
		self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

	def _safe_click(self, element):
		self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
		try:
			self.wait.until(lambda d: element.is_displayed() and element.is_enabled())
			element.click()
		except Exception:
			self.driver.execute_script("arguments[0].click();", element)

	def _go_home(self):
		self.driver.get(f"{self.base_url}/")

	def _get_body_text(self, retries=4):
		last_error = None
		for _ in range(retries):
			try:
				body = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
				return body.text
			except StaleElementReferenceException as exc:
				last_error = exc
				time.sleep(0.2)
		if last_error:
			raise last_error
		return ""

	def _open_login_tab(self):
		self.wait.until(EC.presence_of_element_located((By.ID, "tabli")))
		self._safe_click(self.driver.find_element(By.ID, "tabli"))
		# In headless mode the tab click can be flaky; force visible login form if needed.
		try:
			self.wait.until(EC.visibility_of_element_located((By.ID, "formli")))
		except Exception:
			self.driver.execute_script(
				"const li=document.getElementById('formli');"
				"const su=document.getElementById('formsu');"
				"if(li){li.classList.remove('d-none');}"
				"if(su){su.classList.add('d-none');}"
			)
			self.wait.until(EC.visibility_of_element_located((By.ID, "formli")))

	def _signup(self, first_name, last_name, email, password="password123"):
		self._go_home()
		# If the previous flow left us authenticated, log out once and retry.
		if self.driver.find_elements(By.ID, "create-box"):
			self._logout()
			self._go_home()
		self.wait.until(EC.presence_of_element_located((By.ID, "formsu")))
		self.driver.find_element(By.CSS_SELECTOR, "#formsu input[name='first_name']").send_keys(first_name)
		self.driver.find_element(By.CSS_SELECTOR, "#formsu input[name='last_name']").send_keys(last_name)
		self.driver.find_element(By.CSS_SELECTOR, "#formsu input[name='email']").send_keys(email)
		self.driver.find_element(By.CSS_SELECTOR, "#formsu input[name='password']").send_keys(password)
		self._safe_click(self.driver.find_element(By.CSS_SELECTOR, "#formsu button[type='submit']"))
		self.wait.until(EC.url_contains("/profile"))

	def _complete_profile(self, postcode, gender, sports):
		postcode_input = self.driver.find_element(By.NAME, "postcode")
		postcode_input.clear()
		postcode_input.send_keys(postcode)

		gender_select = Select(self.driver.find_element(By.NAME, "gender"))
		gender_select.select_by_visible_text(gender)

		for sport in sports:
			chip = self.driver.find_element(By.CSS_SELECTOR, f"button.sport-chip[data-sport='{sport}']")
			self._safe_click(chip)

		self._safe_click(self.driver.find_element(By.CSS_SELECTOR, "#user-profile-form button[type='submit']"))
		self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success")))

	def _logout(self):
		self.driver.get(f"{self.base_url}/logout")
		self.wait.until(EC.url_contains("/"))

	def _login(self, email, password="password123"):
		self._go_home()
		self._open_login_tab()
		email_input = self.driver.find_element(By.CSS_SELECTOR, "#formli input[name='email']")
		pass_input = self.driver.find_element(By.CSS_SELECTOR, "#formli input[name='password']")
		email_input.clear()
		pass_input.clear()
		email_input.send_keys(email)
		pass_input.send_keys(password)
		self._safe_click(self.driver.find_element(By.CSS_SELECTOR, "#formli button[type='submit']"))
		self.wait.until(EC.url_to_be(f"{self.base_url}/"))
		# Confirm authenticated session by checking that the logout link is present.
		self.wait.until(EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='Log Out']")))


class TestSeleniumTutorialStyleSuite(BaseSeleniumIntegrationTest):
	def test_01_homepage_smoke(self):
		self._go_home()
		self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
		self.assertIn("MatchUp", self.driver.title)
		self.assertTrue(self.driver.find_element(By.ID, "formsu").is_displayed())
		
    def test_02_signup_and_profile_update(self):
		unique = int(time.time() * 1000)
		email = f"tutorial_user_{unique}@example.com"

		self._signup("Selenium", "Learner", email)
		self._complete_profile("6009", "MALE", ["Soccer", "Tennis"])

		body_text = self._get_body_text()
		self.assertIn("Profile updated successfully", body_text)
		
    def test_03_login_and_create_event(self):
		unique = int(time.time() * 1000)
		email = f"event_owner_{unique}@example.com"

		self._signup("Event", "Owner", email)
		self._complete_profile("6009", "MALE", ["Tennis"])
		self._logout()

		self._login(email)
		self.wait.until(EC.presence_of_element_located((By.ID, "create-box")))

		self.driver.find_element(By.CSS_SELECTOR, "#create-box input[name='event_name']").send_keys("Tutorial Tennis Match")
		Select(self.driver.find_element(By.CSS_SELECTOR, "#create-box select[name='sport']")).select_by_visible_text("Tennis")
		self.driver.find_element(By.CSS_SELECTOR, "#create-box input[name='spots_total']").send_keys("12")
		self.driver.find_element(By.CSS_SELECTOR, "#create-box input[name='date']").send_keys("05162026")
		self.driver.find_element(By.CSS_SELECTOR, "#create-box input[name='time']").send_keys("1830")
		self.driver.find_element(By.CSS_SELECTOR, "#create-box input[name='location']").send_keys("Nedlands")
		self.driver.find_element(By.CSS_SELECTOR, "#create-box input[name='postcode']").send_keys("6009")
		self.driver.find_element(By.CSS_SELECTOR, "#create-box textarea[name='description']").send_keys("Tutorial-driven event")
		self._safe_click(self.driver.find_element(By.CSS_SELECTOR, "#create-box button[type='submit']"))

		self.wait.until(EC.url_contains("/events/"))
		self.assertIn("Tutorial Tennis Match", self._get_body_text())