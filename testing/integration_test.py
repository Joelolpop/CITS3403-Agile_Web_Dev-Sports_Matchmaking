
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

